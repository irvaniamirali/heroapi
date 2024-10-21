from sqlalchemy.orm import Session

from . import models
from app.api.sources.shorten_url.shorten_url import generate_short_url


def create_url(db: Session, target_url: str):
    db_url = db.query(models.URL).filter(models.URL.target_url == target_url).first()
    if db_url:
        return db_url

    short_url = generate_short_url()

    db_url = models.URL(target_url=target_url, short_url=short_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_url_by_short(db: Session, short_url: str):
    return db.query(models.URL).filter(models.URL.short_url == short_url).first()
