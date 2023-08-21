from typing import Literal

from sqlalchemy.orm import Session
from iip_search import models


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).one()


def get_inscription(db: Session, slug: str):
    return (
        db.query(models.Inscription)
        .filter(models.Inscription.filename == f"{slug}.xml")
        .one()
    )


def get_provenance(db: Session, provenance_id: id):
    return (
        db.query(models.Provenance).filter(models.Provenance.id == provenance_id).one()
    )


def get_region(db: Session, region_id: int):
    return db.query(models.Region).filter(models.Region.id == region_id).one()


def list_cities(db: Session):
    return db.query(models.City).all()


# possibly maps to "physical type" in the interface?
def list_forms(db: Session):
    return db.query(models.IIPForm).all()


def list_genres(db: Session):
    return db.query(models.IIPGenre).all()


def list_languages(db: Session):
    return db.query(models.Language).all()


def list_locations(db: Session):
    cities = list_cities(db)
    provenances = list_provenances(db)
    regions = list_regions(db)

    return cities + provenances + regions


def list_materials(db: Session):
    return db.query(models.IIPMaterial).all()


def list_provenances(db: Session):
    return db.query(models.Provenance).all()


def list_regions(db: Session):
    return db.query(models.Region).all()


def list_religions(db: Session):
    return db.query(models.IIPReligion).all()


def list_facets(db: Session):
    cities = list_cities(db)
    genres = list_genres(db)
    languages = list_languages(db)
    materials = list_materials(db)
    physical_types = list_forms(db)
    provenances = list_provenances(db)
    regions = list_regions(db)
    religions = list_religions(db)

    return dict(
        cities=cities,
        genres=genres,
        languages=languages,
        materials=materials,
        physical_types=physical_types,
        provenances=provenances,
        regions=regions,
        religions=religions,
    )


def search_inscriptions(db: Session, input_str: str):
    normalized_string = remove_accents(search)
    stmt = (
        select(models.Inscription)
        .filter(models.Inscription.display_status == models.DisplayStatus.APPROVED)
        .distinct(models.Inscription.id)
        .join(
            models.Inscription.editions.and_(
                models.Edition.searchable_text.match(normalized_string)
            ),
        )
    )

    return db.execute(stmt).scalars()


def list_inscriptions(
    db: Session,
    text_search: str | None = None,
    description_place_id: str | None = None,
    figures: str | None = None,
    not_before: int | None = None,
    not_before_era: Literal["bce"] | Literal["ce"] | None = None,
    not_after: int | None = None,
    not_after_era: Literal["bce"] | Literal["ce"] | None = None,
    cities: list[int] | None = [],
    provenances: list[int] | None = [],
    genres: list[int] | None = [],
    physical_types: list[int] | None = [],
    languages: list[int] | None = [],
    religions: list[int] | None = [],
    materials: list[int] | None = [],
):
    query = (
        db.query(models.Inscription)
        .filter(models.Inscription.display_status == models.DisplayStatus.APPROVED)
        .distinct(models.Inscription.id)
    )

    if not_before is not None and not_before != "":
        if not_before_era == "bce":
            not_before = -int(not_before)
        query = query.filter(models.Inscription.not_before >= not_before)

    if not_after is not None and not_after != "":
        if not_after_era == "bce":
            not_after = -int(not_after)
        query = query.filter(models.Inscription.not_after <= not_after)

    if cities is not None and len(cities) > 0:
        query = query.filter(models.Inscription.city_id.in_(cities))

    if provenances is not None and len(provenances) > 0:
        query = query.filter(models.Inscription.provenance_id.in_(provenances))

    # if len(genres) > 0:
    #     query = query.filter(models.Inscription.iip_genres)

    # if len(physical_types) > 0:
    #     query = query.filter(models.Inscription.iip_forms)

    return query


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])
