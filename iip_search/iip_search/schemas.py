from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy.dialects.postgresql.types import TSVECTOR

from iip_search import models


class BibliographicEntrySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.BibliographicEntry
        exclude = ("searchable_text",)
        include_relationships = True
        load_instance = True


class CitySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.City
        exclude = ("searchable_text",)


class EditionSchema(SQLAlchemyAutoSchema):
    id = auto_field()
    inscription = Nested(lambda: InscriptionSchema(only=("id", "title")))

    class Meta:
        model = models.Edition
        exclude = ("searchable_text",)
        include_fk = True
        load_instance = True

    edition_type = fields.Enum(models.EditionType)


class InscriptionSchema(SQLAlchemyAutoSchema):
    id = auto_field()
    editions = fields.List(Nested(EditionSchema(exclude=("inscription",))))
    city = Nested(CitySchema)

    class Meta:
        model = models.Inscription
        exclude = (
            "display_status",
            "searchable_text",
        )
        include_relationships = True
        load_instance = True
