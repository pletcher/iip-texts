from sqlalchemy.orm import Session
from iip_search import models


def search_inscriptions(db: Session, input_str: str):
    normalized_string = remove_accents(search)
    stmt = (
        select(models.Inscription)
        .distinct(models.Inscription.id)
        .join(
            models.Inscription.editions.and_(
                models.Edition.searchable_text.match(normalized_string)
            ),
        )
    )

    return db.execute(stmt).scalars()


def list_inscriptions(db: Session):
    return db.query(models.Inscription).all()


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])
