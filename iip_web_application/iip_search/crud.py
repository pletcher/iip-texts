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


def list_inscriptions(db: Session):
    return (
        db.query(models.Inscription)
        .filter(models.Inscription.display_status == models.DisplayStatus.APPROVED)
        .all()
    )


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])
