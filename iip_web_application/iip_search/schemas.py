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
    dimensions: Optional[dict]
    display_status: DisplayStatus
    editions: List[Edition]
    filename: str
    images: List[Image]
    location_coordinates: Optional[List[float]]
    location_metadata: Optional[dict]
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


class IIPMaterial(IIPBase):
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


class Location(IIPBase):
    id: int
    description: Optional[str]
    label: Optional[str]
    placename: str
    pleiades_ref: Optional[str]


class InscriptionMapResponse(IIPBase):
    id: int
    city: Optional[City]
    description: Optional[str]
    dimensions: Optional[dict]
    filename: str
    images: Optional[List[Image]]
    location_coordinates: Optional[List[float]]
    location_metadata: Optional[dict]
    not_after: Optional[str]
    not_before: Optional[str]
    short_description: Optional[str]
    title: Optional[str]


class InscriptionListResponse(IIPBase):
    id: int
    city: Optional[City]
    description: Optional[str]
    dimensions: Optional[dict]
    editions: List[Edition]
    filename: str
    images: Optional[List[Image]]
    languages: List[Language]
    location_coordinates: Optional[List[float]]
    location_metadata: Optional[dict]
    not_after: Optional[str]
    not_before: Optional[str]
    short_description: Optional[str]
    title: Optional[str]


class FacetsResponse(IIPBase):
    cities: list[City]
    genres: list[IIPGenre]
    languages: list[Language]
    materials: list[IIPMaterial]
    physical_types: list[IIPForm]
    provenances: list[Provenance]
    regions: list[Region]
    religions: list[IIPReligion]
