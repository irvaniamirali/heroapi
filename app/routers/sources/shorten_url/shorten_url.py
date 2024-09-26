from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session

from app.database.shorten_url import models, crud, database

router = APIRouter(prefix="/api/shorten-url", tags=["Shorten URL"])

models.base.metadata.create_all(bind=database.engine)


@router.post("/urls/", status_code=status.HTTP_200_OK)
async def create_url(url: models.URLCreate, db: Session = Depends(database.get_db)):
    return crud.create_url(db=db, target_url=url.target_url)


@router.get("/{short_url}", status_code=status.HTTP_200_OK)
async def forward_to_target(short_url: str, response: Response, db: Session = Depends(database.get_db)):
    db_url = crud.get_url_by_short(db, short_url)
    if db_url is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "URL not found."}
    return RedirectResponse(db_url.target_url)
