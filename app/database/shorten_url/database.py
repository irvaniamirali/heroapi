from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./shorten_url.db"

engine = create_engine(DATABASE_URL)
base = declarative_base()
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
