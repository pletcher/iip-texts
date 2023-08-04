import os

from sqlalchemy import create_engine

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

DB_URL = os.getenv(
    "DB_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/iip_search_dev"
)
engine = create_engine(DB_URL)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import iip_search.models

    Base.metadata.create_all(bind=engine)
