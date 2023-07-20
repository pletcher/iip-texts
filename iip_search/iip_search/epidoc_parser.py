import logging
import os

from lxml import etree
from pathlib import Path

from iip_search import models

EPIDOC_DIR = Path("../epidoc-files")
NAMESPACES = {"tei": "http://www.tei-c.org/ns/1.0"}
XML_ID_ATTRIB = "{http://www.w3.org/XML/1998/namespace}id"

logging.basicConfig(format="%(levelname)s: %(asctime)s %(message)s", level=logging.INFO)


class EpidocParser:
    bibliography_xpath = (
        "//tei:text/tei:back/tei:div[@type = 'bibliography']/tei:listBibl/tei:bibl"
    )
    transcription_xpath = (
        "//tei:text/tei:body/tei:div[@type = 'edition' and @subtype = 'transcription']"
    )
    transcription_segmented_xpath = "//tei:text/tei:body/tei:div[@type = 'edition' and @subtype = 'transcription_segmented']"
    translation_xpath = "//tei:text/tei:body/tei:div[@type = 'translation']"

    def __init__(self, filename):
        self.filename = filename
        self.tree = self._parse_file()

    def list_directory_contents(self):
        return [f for f in os.listdir(self._dir) if f[-4:] == ".xml"]

    # ------- Begin Inscription fields and relations ------- #

    def get_bibliography(self):
        entries = []
        for bibl in self.tree.iterfind(self.bibliography_xpath, namespaces=NAMESPACES):
            xml_id = bibl.attrib.get(XML_ID_ATTRIB)
            bibl_scope = bibl.find("./tei:biblScope", namespaces=NAMESPACES)
            bibl_scope_unit = bibl_scope.attrib.get("unit")
            bibl_scope_text = bibl_scope.text
            ptr = bibl.find("./tei:ptr", namespaces=NAMESPACES)
            ptr_target = ptr.attrib.get("target")
            ptr_type = ptr.attrib.get("type")

            entries.append(
                models.BibliographicEntry(
                    xml_id=xml_id,
                    bibl_scope=bibl_scope_text,
                    bibl_scope_unit=bibl_scope_unit,
                    ptr_target=ptr_target,
                    ptr_type=ptr_type,
                    raw_xml=etree.tostring(bibl),
                )
            )
        return entries

    def get_city(self):
        pass

    def get_description(self):
        pass

    def get_dimensions(self):
        pass

    def get_iip_form(self):
        pass

    def get_iip_genres(self):
        pass

    def get_iip_materials(self):
        pass

    def get_iip_preservation(self):
        pass

    def get_iip_religions(self):
        pass

    def get_iip_writings(self):
        pass

    def get_images(self):
        pass

    def get_languages(self):
        pass

    def get_not_before(self):
        pass

    def get_not_after(self):
        pass

    def get_provenance(self):
        pass

    def get_region(self):
        pass

    def get_short_description(self):
        pass

    def get_title(self):
        pass

    # ------- End Inscription fields and relations ------- #

    def get_edition(self, xpath):
        editions = self.tree.xpath(xpath, namespaces=NAMESPACES)

        if len(editions) > 1:
            logging.warn(
                f"Expected to find a single edition, but found {len(editions)} for {xpath} in {etree.tostring(tree, encoding='unicode')}."
            )

        if len(editions) == 0:
            return None

        return editions[0]

    def get_text_elements(self, xpath):
        return self.tree.xpath(f"{xpath}/tei:p/*", namespaces=NAMESPACES)

    def get_transcription(self):
        return self._stringify_xml_and_text(self.filename, self.transcription_xpath)

    def get_transcription_segmented(self):
        return self._stringify_xml_and_text(
            self.filename, self.transcription_segmented_xpath
        )

    def get_translation(self):
        return self._stringify_xml_and_text(self.filename, self.translation_xpath)

    def _parse_file(self):
        logging.info(f"Attempting to parse {self.filename}.")

        return etree.parse(self.filename)

    def _stringify_xml_and_text(self, xpath):
        edition = self.get_edition(self.tree, xpath)
        elements = self.get_text_elements(self.tree, xpath)

        if edition is not None:
            return (
                etree.tostring(edition, encoding="unicode"),
                " ".join(
                    [
                        etree.tostring(el, encoding="unicode", method="text").strip()
                        for el in elements
                    ]
                ),
            )

        logging.warning(f"No nodes found for {xpath} in {self.filename}.")

        return (None, None)
