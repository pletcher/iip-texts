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

        city = None
        if city_raw is not None:
            city = get_or_create_city(
                session, city_raw["placename"], city_raw["pleiades_ref"]
            )

        iip_preservation = None
        if iip_preservation_raw is not None:
            iip_preservation = get_or_create(
                session, models.IIPPreservation, **iip_preservation_raw
            )
        else:
            logging.warning(f"No iip_preservation for {file}!")

        provenance = None
        if provenance_raw.get("placename") is not None:
            provenance = get_or_create(session, models.Provenance, **provenance_raw)
        else:
            logging.warning(f"No provenance for {file}!")

        region = None
        if region_raw is not None:
            region = get_or_create(session, models.Region, **region_raw)
        else:
            logging.warning(f"No region for {file}!")

        bibliographic_entries = [
            get_or_create(session, models.BibliographicEntry, **raw)
            for raw in bibliographic_entries_raw
        ]

        iip_forms = []
        if iip_forms_raw is not None:
            iip_forms = [
                get_or_create(session, models.IIPForm, **raw) for raw in iip_forms_raw
            ]

        iip_genres = []
        if iip_genres_raw is not None:
            iip_genres = [
                get_or_create(session, models.IIPGenre, **raw) for raw in iip_genres_raw
            ]

        iip_materials = [
            get_or_create(session, models.IIPMaterial, **raw)
            for raw in iip_materials_raw
        ]

        iip_religions = []
        if iip_religions_raw is not None:
            iip_religions = [
                get_or_create(session, models.IIPReligion, **raw)
                for raw in iip_religions_raw
            ]

        iip_writings = []
        if iip_writings_raw is not None:
            iip_writings = [
                get_or_create_iip_writing(session, **raw) for raw in iip_writings_raw
            ]

        languages = [
            get_or_create(session, models.Language, **raw) for raw in languages_raw
        ]

        inscription = get_or_create_inscription(
            session,
            file,
            **dict(
                city_id=city.id if city else None,
                description=description_raw,
                dimensions={"dimensions": dimensions_raw},
                iip_preservation_id=iip_preservation.id if iip_preservation else None,
                not_after=not_after_raw,
                not_before=not_before_raw,
                parsed_at=datetime.now(),
                provenance_id=provenance.id if provenance else None,
                region_id=region.id if region else None,
                short_description=short_description_raw,
                title=title_raw,
            ),
        )

        (transcription_xml, s_transcription) = parser.get_transcription()
        (
            transcription_segmented_xml,
            s_transcription_segmented,
        ) = parser.get_transcription_segmented()
        (translation_xml, s_translation) = parser.get_translation()

        if transcription_xml is not None:
            inscription.editions.add(
                models.Edition(
                    edition_type=models.EditionType.TRANSCRIPTION,
                    raw_xml=transcription_xml,
                    text=s_transcription,
                )
            )

        if transcription_segmented_xml is not None:
            inscription.editions.add(
                models.Edition(
                    edition_type=models.EditionType.TRANSCRIPTION_SEGMENTED,
                    raw_xml=transcription_segmented_xml,
                    text=s_transcription_segmented,
                )
            )

        if translation_xml is not None:
            inscription.editions.add(
                models.Edition(
                    edition_type=models.EditionType.TRANSLATION,
                    raw_xml=translation_xml,
                    text=s_translation,
                )
            )

        session.add(inscription)
        session.commit()
        session.flush()


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()

    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def get_or_create_city(session, placename, pleiades_ref):
    instance = session.query(models.City).filter_by(placename=placename).one_or_none()

    if instance:
        return instance
    else:
        instance = models.City(placename=placename, pleiades_ref=pleiades_ref)
        session.add(instance)
        session.commit()
        return instance


def get_or_create_iip_writing(session, **kwargs):
    xml_id = kwargs.pop("xml_id")

    instance = session.query(models.IIPWriting).filter_by(xml_id=xml_id).one_or_none()

    if instance:
        return instance
    else:
        instance = models.IIPWriting(xml_id=xml_id, **kwargs)
        session.add(instance)
        session.commit()
        return instance


def get_or_create_inscription(session, filename, **kwargs):
    instance = (
        session.query(models.Inscription).filter_by(filename=filename).one_or_none()
    )

    if instance:
        return instance
    else:
        instance = models.Inscription(filename=filename, **kwargs)
        session.add(instance)
        session.commit()
        return instance


def list_directory_xml(directory):
    return [f for f in os.listdir(directory) if f[-4:] == ".xml"]


if __name__ == "__main__":
    with Session(db.engine) as session:
        main(session)

        session.commit()
