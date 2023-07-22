#!/usr/bin/env python3

import logging
import os

from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from iip_search import db
from iip_search import models
from iip_search.epidoc_parser import EpidocParser

logging.basicConfig(format="%(levelname)s: %(asctime)s %(message)s", level=logging.INFO)


def main(session):
    files = list_directory_xml("../epidoc-files")

    for file in files:
        parser = EpidocParser(f"../epidoc-files/{file}")

        bibliographic_entries_raw = parser.get_bibliography()
        city_raw = parser.get_city()
        description_raw = parser.get_description()
        dimensions_raw = parser.get_dimensions()
        iip_forms_raw = parser.get_iip_forms()
        iip_genres_raw = parser.get_iip_genres()
        iip_materials_raw = parser.get_iip_materials()
        iip_preservation_raw = parser.get_iip_preservation()
        iip_religions_raw = parser.get_iip_religions()
        iip_writings_raw = parser.get_iip_writings()
        images_raw = parser.get_images()
        languages_raw = parser.get_languages()
        not_after_raw = parser.get_not_after()
        not_before_raw = parser.get_not_before()
        provenance_raw = parser.get_provenance()
        region_raw = parser.get_region()
        short_description_raw = parser.get_short_description()
        title_raw = parser.get_title()

        city = get_or_create(session, models.City, **city_raw)

        if iip_preservation_raw is not None:
            iip_preservation = get_or_create(
                session, models.IIPPreservation, **iip_preservation_raw
            )
        else:
            logging.warning(
                f"No iip_preservation for {file}! Can't continue. Inscription will not be saved."
            )
            continue

        if provenance_raw.get("placename") is not None:
            provenance = get_or_create(session, models.Provenance, **provenance_raw)
        else:
            logging.warning(
                f"No provenance for {file}! Can't continue. Inscription will not be saved."
            )
            continue

        if region_raw is not None:
            region = get_or_create(session, models.Region, **region_raw)
        else:
            logging.warning(
                f"No region for {file}! Can't continue. Inscription will not be saved."
            )
            continue

        bibliographic_entries = [
            get_or_create(session, models.BibliographicEntry, **raw)
            for raw in bibliographic_entries_raw
        ]
        iip_forms = [
            get_or_create(session, models.IIPForm, **raw) for raw in iip_forms_raw
        ]
        iip_genres = [
            get_or_create(session, models.IIPGenre, **raw) for raw in iip_genres_raw
        ]
        iip_materials = [
            get_or_create(session, models.IIPMaterial, **raw)
            for raw in iip_materials_raw
        ]
        iip_religions = [
            get_or_create(session, models.IIPReligion, **raw)
            for raw in iip_religions_raw
        ]
        iip_writings = [
            get_or_create(session, models.IIPWriting, **raw) for raw in iip_writings_raw
        ]
        languages = [
            get_or_create(session, models.Language, **raw) for raw in languages_raw
        ]
        inscription = get_or_create(
            session,
            models.Inscription,
            **dict(
                city_id=city.id,
                description=description_raw,
                dimensions=dimensions_raw,
                filename=file,
                iip_preservation_id=iip_preservation.id,
                not_after=not_after_raw,
                not_before=not_before_raw,
                parsed_at=datetime.now(),
                provenance_id=provenance.id,
                region_id=region.id,
                short_description=short_description_raw,
                title=title_raw,
            ),
        )

        (transcription_xml, s_transcription) = parser.get_transcription(file)
        (
            transcription_segmented_xml,
            s_transcription_segmented,
        ) = parser.get_transcription_segmented(file)
        (translation_xml, s_translation) = parser.get_translation(file)

        inscription = db.Inscription(filename=file, parsed_at=datetime.now())

        if transcription_xml is not None:
            inscription.editions.add(
                db.Edition(
                    edition_type=db.EditionType.TRANSCRIPTION,
                    raw_xml=transcription_xml,
                    text=s_transcription,
                )
            )

        if transcription_segmented_xml is not None:
            inscription.editions.add(
                db.Edition(
                    edition_type=db.EditionType.TRANSCRIPTION_SEGMENTED,
                    raw_xml=transcription_segmented_xml,
                    text=s_transcription_segmented,
                )
            )

        if translation_xml is not None:
            inscription.editions.add(
                db.Edition(
                    edition_type=db.EditionType.TRANSLATION,
                    raw_xml=translation_xml,
                    text=s_translation,
                )
            )

        get_or_create(session, models.Inscription, **inscription)
        session.flush()


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    print(instance)
    print(model)
    print(kwargs)
    if instance:
        return instance
    else:
        try:
            instance = model(**kwargs)
            session.add(instance)
            session.commit()
            return instance
        except:
            logging.error(f"Unable to save {kwargs} on {model}.")


def list_directory_xml(directory):
    return [f for f in os.listdir(directory) if f[-4:] == ".xml"]


if __name__ == "__main__":
    with Session(db.engine) as session:
        main(session)

        session.commit()
