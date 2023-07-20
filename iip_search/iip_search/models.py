import datetime
import enum

from dataclasses import dataclass

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Computed
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy import UniqueConstraint

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import TSVECTOR

from sqlalchemy.ext.mutable import MutableDict

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from sqlalchemy.types import TypeDecorator

from typing import Set

from iip_search.db import Base


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


class IIPForm(Base):
    __tablename__ = "iip_forms"
    __table_args__ = (UniqueConstraint("xml_id", name="iip_form_xml_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    inscriptions: Mapped[Set["Inscription"]] = relationship(back_populates="iip_form")
    xml_id: Mapped[str] = mapped_column(nullable=False, unique=True)


class IIPPreservation(Base):
    __tablename__ = "iip_preservations"
    __table_args__ = (UniqueConstraint("xml_id", name="iip_preservation_xml_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    inscriptions: Mapped[Set["Inscription"]] = relationship(
        back_populates="iip_preservation"
    )
    xml_id: Mapped[str] = mapped_column(nullable=False, unique=True)


class Provenance(Base):
    __tablename__ = "provenances"
    __table_args__ = (UniqueConstraint("placename", name="provenance_placename"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    inscriptions: Mapped[Set["Inscription"]] = relationship(back_populates="provenance")
    placename: Mapped[str]


class City(Base):
    __tablename__ = "cities"
    __table_args__ = (UniqueConstraint("placename", name="city_placename"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    inscriptions: Mapped[Set["Inscription"]] = relationship(back_populates="city")
    placename: Mapped[str]


class Region(Base):
    __tablename__ = "regions"
    __table_args__ = (UniqueConstraint("label", name="region_label"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    inscriptions: Mapped[Set["Inscription"]] = relationship(back_populates="region")
    label: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False, unique=True)


iip_genre_inscription = Table(
    "iip_genre_inscription",
    Base.metadata,
    Column("iip_genre_id", ForeignKey("iip_genres.id"), primary_key=True),
    Column("inscription_id", ForeignKey("inscriptions.id"), primary_key=True),
)

iip_material_inscription = Table(
    "iip_material_inscription",
    Base.metadata,
    Column("iip_material_id", ForeignKey("iip_materials.id"), primary_key=True),
    Column("inscription_id", ForeignKey("inscriptions.id"), primary_key=True),
)

iip_writing_inscription = Table(
    "iip_writing_inscription",
    Base.metadata,
    Column("iip_writing_id", ForeignKey("iip_writings.id"), primary_key=True),
    Column("inscription_id", ForeignKey("inscriptions.id"), primary_key=True),
)

iip_religion_inscription = Table(
    "iip_religion_inscription",
    Base.metadata,
    Column("iip_religion_id", ForeignKey("iip_religions.id"), primary_key=True),
    Column("inscription_id", ForeignKey("inscriptions.id"), primary_key=True),
)

language_inscription = Table(
    "language_inscription",
    Base.metadata,
    Column("language_id", ForeignKey("languages.id"), primary_key=True),
    Column("inscription_id", ForeignKey("inscriptions.id"), primary_key=True),
)


class IIPGenre(Base):
    __tablename__ = "iip_genres"
    __table_args__ = (UniqueConstraint("xml_id", name="iip_genre_xml_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    inscriptions: Mapped[Set["Inscription"]] = relationship(
        secondary=iip_genre_inscription, back_populates="iip_genres"
    )
    xml_id: Mapped[str] = mapped_column(nullable=False, unique=True)


class IIPMaterial(Base):
    __tablename__ = "iip_materials"
    __table_args__ = (UniqueConstraint("xml_id", name="iip_material_xml_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    inscriptions: Mapped[Set["Inscription"]] = relationship(
        secondary=iip_material_inscription, back_populates="iip_material"
    )
    xml_id: Mapped[str] = mapped_column(nullable=False, unique=True)


class IIPReligion(Base):
    __tablename__ = "iip_religions"
    __table_args__ = (UniqueConstraint("xml_id", name="iip_religion_xml_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    inscriptions: Mapped[Set["Inscription"]] = relationship(
        secondary=iip_religion_inscription, back_populates="religion"
    )
    xml_id: Mapped[str] = mapped_column(nullable=False, unique=True)


class IIPWriting(Base):
    __tablename__ = "iip_writings"
    __table_args__ = (UniqueConstraint("xml_id", name="iip_writing_xml_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    inscriptions: Mapped[Set["Inscription"]] = relationship(
        secondary=iip_writing_inscription, back_populates="iip_writing"
    )
    xml_id: Mapped[str] = mapped_column(nullable=False, unique=True)


class Language(Base):
    __tablename__ = "languages"
    __table_args__ = (UniqueConstraint("label", name="language_label"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    inscriptions: Mapped[Set["Inscription"]] = relationship(back_populates="language")
    label: Mapped[str] = mapped_column(nullable=False, unique=True)
    short_form: Mapped[str] = mapped_column(nullable=False, unique=True)


class DisplayStatus(enum.Enum):
    APPROVED = "approved"
    TO_CORRECT = "to correct"
    TO_APPROVE = "to approve"


@dataclass
class Inscription(Base):
    __tablename__ = "inscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id = mapped_column(ForeignKey("cities.id"))
    city: Mapped[City] = relationship(back_populates="inscriptions")
    description: Mapped[str]
    dimensions: Mapped[dict] = mapped_column(MutableDict.as_mutable(JSONB))
    display_status: Mapped[DisplayStatus] = mapped_column(
        nullable=False, default=DisplayStatus.APPROVED
    )
    editions: Mapped[Set["Edition"]] = relationship(back_populates="inscription")
    filename: Mapped[str] = mapped_column(nullable=False, unique=True)
    iip_form_id = mapped_column(ForeignKey("iip_forms.id"))
    iip_form: Mapped[IIPForm] = relationship(back_populates="inscriptions")
    iip_genres: Mapped[Set[IIPGenre]] = relationship(
        secondary=iip_genre_inscription, back_populates="inscriptions"
    )
    iip_materials: Mapped[Set[IIPMaterial]] = relationship(
        secondary=iip_material_inscription, back_populates="inscriptions"
    )
    iip_preservation_id = mapped_column(ForeignKey("iip_preservations.id"))
    iip_preservation: Mapped[IIPPreservation] = relationship(
        back_populates="inscriptions"
    )
    iip_religions: Mapped[Set[IIPReligion]] = relationship(
        secondary=iip_religion_inscription, back_populates="inscriptions"
    )
    iip_writings: Mapped[IIPWriting] = relationship(
        secondary=iip_writing_inscription, back_populates="inscriptions"
    )
    images: Mapped[Set["Image"]] = relationship(back_populates="inscription")
    language: Mapped[Set[Language]] = relationship(
        secondary=language_inscription, back_populates="inscriptions"
    )
    not_after: Mapped[str]
    not_before: Mapped[str]
    parsed_at: Mapped[datetime.datetime]
    provenance_id = mapped_column(ForeignKey("provenances.id"))
    provenance: Mapped[Provenance] = relationship(back_populates="inscriptions")
    region_id = mapped_column(ForeignKey("regions.id"))
    region: Mapped[Region] = relationship(back_populates="inscriptions")
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


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    graphic_url: Mapped[str]
    inscription_id = mapped_column(ForeignKey("inscriptions.id"))
    inscription: Mapped[Inscription] = relationship(back_populates="images")
    source: Mapped[str]


edition_bibliographic_entry = Table(
    "edition_bibliographic_entry",
    Base.metadata,
    Column("edition_id", ForeignKey("editions.id"), primary_key=True),
    Column(
        "bibliographic_entry_id",
        ForeignKey("bibliographic_entries.id"),
        primary_key=True,
    ),
)


"""
Example bibliography:
<div type="bibliography">
    <listBibl>
        <bibl xml:id="b1">
            <ptr type="biblItem" target="IIP-475.xml"/>
            <biblScope unit="page">52</biblScope>
        </bibl>
        <bibl xml:id="b2">
            <ptr type="biblItem" target="IIP-053.xml"/>
            <biblScope unit="page">57</biblScope>
        </bibl>
    </listBibl>
</div>
"""


class BibliographicEntry(Base):
    __tablename__ = "bibliographic_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    bibl_scope: Mapped[str]
    bibl_scope_unit: Mapped[str]
    editions: Mapped[Set["Edition"]] = relationship(
        secondary=edition_bibliographic_entry, back_populates="bibliographic_entries"
    )
    ptr_target: Mapped[str]
    ptr_type: Mapped[str]
    raw_xml: Mapped[str] = mapped_column(nullable=False)
    xml_id: Mapped[str] = mapped_column(nullable=False)


class EditionType(enum.Enum):
    DIPLOMATIC = "diplomatic"
    TRANSCRIPTION = "transcription"
    TRANSCRIPTION_SEGMENTED = "transcription_segmented"
    TRANSLATION = "translation"


class Edition(Base):
    __tablename__ = "editions"

    id: Mapped[int] = mapped_column(primary_key=True)
    bibliographic_entries: Mapped[Set[BibliographicEntry]] = relationship(
        secondary=edition_bibliographic_entry, back_populates="editions"
    )
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
    searchable_text = mapped_column(
        TSVector,
        Computed(
            """
        to_tsvector('english', regexp_replace(normalize(text, NFKD), '[\u0300-\u036f]', '', 'g'))
        """,
            persisted=True,
        ),
    )
