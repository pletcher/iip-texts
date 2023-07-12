import datetime
import enum
import os

from sqlalchemy import create_engine
from sqlalchemy import ForeignKey

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from typing import List

DB_URL = os.getenv("DB_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/iip_search_dev")
engine = create_engine(DB_URL)

# Models

class Base(DeclarativeBase):
    pass

class Inscription(Base):
    __tablename__ = "inscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str]
    editions: Mapped[List["Edition"]] = relationship(back_populates="edition")
    parsed_at: Mapped[datetime.datetime]

class EditionType(enum.Enum):
    DIPLOMATIC = "diplomatic"
    TRANSCRIPTION = "transcription"
    TRANSCRIPTION_SEGMENTED = "transcription_segmented"
    TRANSLATION = "translation"

class Edition(Base):
    __tablename__ = "editions"

    id: Mapped[int] = mapped_column(primary_key=True)
    edition_type: Mapped[EditionType]
    inscription_id = mapped_column(ForeignKey("inscriptions.id"))
    inscription: Mapped["Inscription"] = relationship(back_populates="inscriptions")
    # NOTE: (charles) Since we're using Postgres, we *could* use the built-in
    # XML type. But there's really no advantage in doing so unless
    # we plan to query against this column. As it stands now, this column
    # is mainly a sanity check to make sure that the derived `text` field
    # looks correct.
    raw_xml: Mapped[str]
    text: Mapped[str]