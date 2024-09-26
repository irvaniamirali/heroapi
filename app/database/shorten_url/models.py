from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel
from .database import base


class URLCreate(BaseModel):
    target_url: str


class URL(base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    target_url = Column(String, index=True, unique=True)
    short_url = Column(String, index=True, unique=True)
    is_active = Column(Boolean, default=True)
