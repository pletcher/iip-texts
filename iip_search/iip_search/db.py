import datetime
import enum
import os

from dataclasses import dataclass

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy import Column, Computed
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import TSVECTOR

from sqlalchemy.ext.mutable import MutableDict

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

"""
IIP{Form,Material,Genre,Preservation,Writing,Religion} should 
be validated against those listed
in include_taxonomies.xml (./classDecl/taxonomy[@xml:id="IIP-{form,material,genre,preservation,writing,religion}"]).

`xml_id` corresponds to the @xml:id attribute in the taxonomy, e.g.,
for
```xml
<category xml:id="funerary">
    <catDesc>Funerary</catDesc>
</category>
```
`xml_id` == "funerary"

`description` corresponds to the textValue of `catDesc`, e.g.,
for 
```xml
<category xml:id="funerary">
    <catDesc>Funerary</catDesc>
</category>
```
`description` == "Funerary"
"""
class IIPForm(db.Model):
    __tablename__ = "iip_forms"
    __table_args__ = (
        UniqueConstraint("xml_id"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    inscriptions: Mapped[Set["Inscription"]] = relationship(back_populates="iip_form")
    xml_id: Mapped[str] = mapped_column(unique=True, nullable=False)

class IIPGenre(db.Model):
    __tablename__ = "iip_genres"
    __table_args__ = (
        UniqueConstraint("xml_id"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    inscriptions: Mapped[Set["Inscription"]] = relationship(back_populates="iip_genre")
    xml_id: Mapped[str] = mapped_column(unique=True, nullable=False)

class IIPMaterial(db.Model):
    __tablename__ = "iip_materials"
    __table_args__ = (
        UniqueConstraint("xml_id"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    inscriptions: Mapped[Set["Inscription"]] = relationship(back_populates="iip_material")
    xml_id: Mapped[str] = mapped_column(unique=True, nullable=False)

class IIPPreservation(db.Model):
    __tablename__ = "iip_preservations"
    __table_args__ = (
        UniqueConstraint("xml_id"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    inscriptions: Mapped[Set["Inscription"]] = relationship(back_populates="iip_preservation")
    xml_id: Mapped[str] = mapped_column(unique=True, nullable=False)

class IIPReligion(db.Model):
    __tablename__ = "iip_religions"
    __table_args__ = (
        UniqueConstraint("xml_id"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    inscriptions: Mapped[Set["Inscription"]] = relationship(back_populates="iip_religion")
    xml_id: Mapped[str] = mapped_column(unique=True, nullable=False)

class IIPWriting(db.Model):
    __tablename__ = "iip_writings"
    __table_args__ = (
        UniqueConstraint("xml_id"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    inscriptions: Mapped[Set["Inscription"]] = relationship(back_populates="iip_writing")
    xml_id: Mapped[str] = mapped_column(unique=True, nullable=False)

class Language(db.Model):
    __tablename__ = "languages"
    __table_args__ = (
        UniqueConstraint("label"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    inscriptions: Mapped[Set["Inscription"]] = relationship(back_populates="language")
    label: Mapped[str] = mapped_column(nullable=False, unique=True)
    short_form: Mapped[str] = mapped_column(nullable=False, unique=True)

class Region(db.Model):
    __tablename__ = "regions"
    __table_args__ = (
        UniqueConstraint("label"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    inscriptions: Mapped[Set["Inscription"]] = relationship(back_populates="region")
    label: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False, unique=True)

class Religion(db.Model):
    __tablename__ = "religions"
    __table_args__ = (
        UniqueConstraint("label"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(nullable=False, unique=True)
    inscriptions: Mapped[Set["Inscription"]] = relationship(back_populates="religion")
    short_form: Mapped[str] = mapped_column(nullable=False, unique=True)

class DisplayStatus(enum.Enum):
    APPROVED = "approved"
    TO_CORRECT = "to correct"
    TO_APPROVE = "to approve"

@dataclass
class Inscription(db.Model):
    __tablename__ = "inscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    dimensions: Mapped[dict] = mapped_column(MutableDict.as_mutable(JSONB))
    display_status: Mapped[DisplayStatus] = mapped_column(nullable=False, default=DisplayStatus.APPROVED)
    editions: Mapped[Set["Edition"]] = relationship(back_populates="inscription")
    filename: Mapped[str]
    # FIXME: iip_form (`physical_type` in the solr schema) can be many-to-many
    iip_form_id = mapped_column(ForeignKey("iip_forms.id"))
    iip_form: Mapped[IIPForm] = relationship(back_populates="inscriptions")
    # FIXME: iip_genre (`type` in the solr schema) can be many-to-many
    iip_genre_id = mapped_column(ForeignKey("iip_genres.id"))
    iip_genre: Mapped[IIPGenre] = relationship(back_populates="inscriptions")
    # FIXME: iip_material (`material` in the solr schema) can be many-to-many
    iip_material_id = mapped_column(ForeignKey("iip_materials.id"))
    iip_material: Mapped[IIPMaterial] = relationship(back_populates="inscriptions")
    iip_preservation_id = mapped_column(ForeignKey("iip_preservations.id"))
    iip_preservation: Mapped[IIPPreservation] = relationship(back_populates="inscriptions")
    # FIXME: religions is many-to-many
    iip_religion_id = mapped_column(ForeignKey("iip_religions.id"))
    iip_religion: Mapped[IIPReligion] = relationship(back_populates="inscriptions")
    iip_writing_id = mapped_column(ForeignKey("iip_writings.id"))
    iip_writing: Mapped[IIPWriting] = relationship(back_populates="inscriptions")
    images: Mapped[Set["Image"]] = relationship(back_populates="inscription")
    # FIXME: language is many-to-many
    language_id = mapped_column(ForeignKey("languages.id"))
    language: Mapped[Language] = relationship(back_populates="inscription")
    parsed_at: Mapped[datetime.datetime]
    short_description: Mapped[str]
    title: Mapped[str]


"""
<facsimile xmlns:xi="http://www.w3.org/2001/XInclude">
    <surface>
        <desc>Gary Todd - Flickr (public domain)</desc>
        <graphic url="cape0002.jpg"/>
        <note>https://www.flickr.com/photos/101561334@N08/43293429452/in/album-72157668660233597/</note>
    </surface>
</facsimile>
"""
class Image(db.Model):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    graphic_url: Mapped[str]
    inscription_id = mapped_column(ForeignKey("inscriptions.id"))
    inscription: Mapped[Inscription] = relationship(back_populates="images")
    source: Mapped[str]

class BibliographicEntry(db.Model):
    __tablename__ = "bibliographic_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    # many-to-many with editions

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