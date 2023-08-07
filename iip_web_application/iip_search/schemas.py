from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict

from .models import DisplayStatus, EditionType


class IIPBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Edition(IIPBase):
    id: int
    edition_type: EditionType
    raw_xml: str
    text: str


class Image(IIPBase):
    id: int
    description: Optional[str]
    graphic_url: str


class Inscription(IIPBase):
    id: int
    description: Optional[str]
    dimensions: dict = None
    display_status: DisplayStatus
    editions: List[Edition]
    filename: str
    images: List[Image]
    not_after: Optional[str]
    not_before: Optional[str]
    short_description: Optional[str]
    title: Optional[str]


class City(IIPBase):
    id: int
    placename: str
    pleiades_ref: Optional[str]


class IIPPreservation(IIPBase):
    id: int
    description: Optional[str]
    xml_id: str


class Provenance(IIPBase):
    id: int
    placename: str


class Region(IIPBase):
    id: int
    label: str
    description: str


class BibliographicEntry(IIPBase):
    id: int
    bibl_scope: Optional[str]
    bibl_scope_unit: Optional[str]
    ptr_target: Optional[str]
    ptr_type: Optional[str]
    raw_xml: str
    xml_id: str


class IIPForm(IIPBase):
    id: int
    ana: Optional[str]
    description: Optional[str]
    xml_id: str


class IIPGenre(IIPBase):
    id: int
    description: Optional[str]
    xml_id: str


class IIPReligion(IIPBase):
    id: int
    description: Optional[str]
    xml_id: str


class Language(IIPBase):
    id: int
    label: str
    short_form: str


class InscriptionResponse(Inscription):
    city: Optional[City]
    iip_preservation: Optional[IIPPreservation]
    provenance: Optional[Provenance]
    region: Optional[Region]
    bibliographic_entries: List[BibliographicEntry]
    iip_forms: List[IIPForm]
    iip_genres: List[IIPGenre]
    iip_religions: List[IIPReligion]
    languages: List[Language]
