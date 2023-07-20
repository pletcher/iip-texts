#!/usr/bin/env python3

from sqlalchemy.orm import Session

from iip_search import db
from iip_search.epidoc_parser import EpidocParser

from datetime import datetime
import os


def main(session):
    parser = EpidocParser()
    files = parser.list_directory_contents()

    for file in files:
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


if __name__ == "__main__":
    with Session(db.engine) as session:
        main(session)

        session.commit()
