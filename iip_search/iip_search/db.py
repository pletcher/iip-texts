import datetime
import enum
import os

from dataclasses import dataclass

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy import Column, Computed
from sqlalchemy import ForeignKey

from sqlalchemy.dialects.postgresql import TSVECTOR

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session, sessionmaker

from sqlalchemy.types import TypeDecorator

from typing import Set

DB_URL = os.getenv("DB_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/iip_search_dev")
engine = create_engine(DB_URL)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

db = SQLAlchemy()

# Models

class TSVector(TypeDecorator):
    impl = TSVECTOR

@dataclass
class Inscription(db.Model):
    __tablename__ = "inscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str]
    editions: Mapped[Set["Edition"]] = relationship(back_populates="inscription")
    parsed_at: Mapped[datetime.datetime]

class EditionType(enum.Enum):
    DIPLOMATIC = "diplomatic"
    TRANSCRIPTION = "transcription"
    TRANSCRIPTION_SEGMENTED = "transcription_segmented"
    TRANSLATION = "translation"

class Edition(db.Model):
    __tablename__ = "editions"

    id: Mapped[int] = mapped_column(primary_key=True)
    edition_type: Mapped[EditionType]
    inscription_id = mapped_column(ForeignKey("inscriptions.id"))
    inscription: Mapped["Inscription"] = relationship(back_populates="editions")
    # NOTE: (charles) Since we're using Postgres, we *could* use the built-in
    # XML type. But there's really no advantage in doing so unless
    # we plan to query against this column. As it stands now, this column
    # is mainly a sanity check to make sure that the derived `text` field
    # looks correct.
    raw_xml: Mapped[str]
    text: Mapped[str]
    searchable_text: Mapped[TSVector] = db.Column(Computed(
        """
        to_tsvector('english', regexp_replace(normalize(text, NFKD), '[\u0300-\u036f]', '', 'g'))
        """, 
        persisted=True
    ))