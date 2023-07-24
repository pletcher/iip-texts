from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy import fields as masqla_fields
from sqlalchemy.dialects.postgresql.types import TSVECTOR

from iip_search import models
from iip_search import db


class BibliographicEntrySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.BibliographicEntry
        exclude = ("searchable_text",)
        include_relationships = True
        load_instance = True
        sqla_session = db.db_session


class CitySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.City
        exclude = ("searchable_text",)
        sqla_session = db.db_session


class EditionSchema(SQLAlchemyAutoSchema):
    id = auto_field()
    inscription = masqla_fields.Nested(lambda: InscriptionSchema(only=("id", "title")))

    class Meta:
        model = models.Edition
        exclude = ("searchable_text",)
        include_fk = True
        load_instance = True
        sqla_session = db.db_session

    edition_type = fields.Enum(models.EditionType)


class IIPFormSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.IIPForm
        exclude = ("searchable_text",)
        sqla_session = db.db_session


class IIPGenreSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.IIPGenre
        exclude = ("searchable_text",)
        sqla_session = db.db_session


class IIPMaterialSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.IIPMaterial
        exclude = ("searchable_text",)
        sqla_session = db.db_session


class IIPPreservationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.IIPPreservation
        exclude = ("searchable_text",)
        sqla_session = db.db_session


class IIPReligionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.IIPReligion
        exclude = ("searchable_text",)
        sqla_session = db.db_session


class IIPWritingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.IIPWriting
        exclude = ("searchable_text",)
        sqla_session = db.db_session


class ImageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.Image
        sqla_session = db.db_session


class LanguageSchema(SQLAlchemyAutoSchema):
    label = auto_field()

    class Meta:
        model = models.Language
        exclude = ("searchable_text",)
        sqla_session = db.db_session


class ProvenanceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.Provenance
        exclude = ("searchable_text",)
        sqla_session = db.db_session


class RegionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.Region
        exclude = ("searchable_text",)
        sqla_session = db.db_session


class InscriptionSchema(SQLAlchemyAutoSchema):
    id = auto_field()
    editions = fields.List(
        masqla_fields.Nested(EditionSchema(exclude=("inscription",)))
    )
    city = masqla_fields.Nested(CitySchema)
    iip_forms = masqla_fields.Nested(IIPFormSchema, many=True)
    iip_genres = masqla_fields.Nested(IIPGenreSchema, many=True)
    iip_materials = masqla_fields.Nested(IIPMaterialSchema, many=True)
    iip_preservation = masqla_fields.Nested(IIPPreservationSchema)
    iip_religions = masqla_fields.Nested(IIPReligionSchema, many=True)
    iip_writings = masqla_fields.Nested(IIPWritingSchema, many=True)
    images = masqla_fields.Nested(ImageSchema, many=True)
    languages = fields.List(masqla_fields.Nested(LanguageSchema))
    provenance = masqla_fields.Nested(ProvenanceSchema)
    region = masqla_fields.Nested(RegionSchema)

    class Meta:
        model = models.Inscription
        exclude = (
            "display_status",
            "searchable_text",
        )
        include_relationships = True
        load_instance = True
        sqla_session = db.db_session
