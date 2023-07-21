#!/usr/bin/env python3

import os

from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from iip_search import db
from iip_search import models
from iip_search.epidoc_parser import EpidocParser


def main(session):
    files = list_directory_xml("../epidoc-files")

    for file in files:
        parser = EpidocParser(f"../epidoc-files/{file}")
        bibliographic_entries = parser.get_bibliography()
        city = parser.get_city()
        description = parser.get_description()
        dimensions = parser.get_dimensions()
        iip_form = parser.get_iip_form()
        iip_genres = parser.get_iip_genres()
        iip_materials = parser.get_iip_materials()
        iip_preservation = parser.get_iip_preservation()
        iip_religions = parser.get_iip_religions()
        iip_writings = parser.get_iip_writings()
        images = parser.get_images()
        languages = parser.get_languages()
        not_after = parser.get_not_after()
        not_before = parser.get_not_before()
        provenance = parser.get_provenance()
        region = parser.get_region()
        short_description = parser.get_short_description()
        title = parser.get_title()

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

        session.add(inscription)


def list_directory_xml(directory):
    return [f for f in os.listdir(directory) if f[-4:] == ".xml"]


if __name__ == "__main__":
    with Session(db.engine) as session:
        main(session)

        session.commit()
