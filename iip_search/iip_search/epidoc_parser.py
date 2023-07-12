from lxml import etree
from pathlib import Path

import logging
import os

EPIDOC_DIR = Path("../epidoc-files")
NAMESPACES = {
    "tei": "http://www.tei-c.org/ns/1.0"
}

logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s', level=logging.INFO)

class EpidocParser:
    transcription_xpath = "//tei:text/tei:body/tei:div[@type = 'edition' and @subtype = 'transcription']"
    transcription_segmented_xpath = "//tei:text/tei:body/tei:div[@type = 'edition' and @subtype = 'transcription_segmented']"
    translation_xpath = "//tei:text/tei:body/tei:div[@type = 'translation']"

    def __init__(self, dir = EPIDOC_DIR):
        self._dir = dir

    def list_directory_contents(self):
        return [f for f in os.listdir(self._dir) if f[-4:] == ".xml"]

    def get_edition(self, tree, xpath = transcription_xpath):
        editions = tree.xpath(xpath, namespaces=NAMESPACES)

        if len(editions) > 1:
            logging.warn(f"Expected to find a single edition, but found {len(editions)} for {xpath} in {etree.tostring(tree, encoding='unicode')}.")
        
        if len(editions) == 0:
            return None

        return editions[0]

    def get_text_elements(self, tree, xpath = transcription_xpath):
        xml = tree.xpath(f'{xpath}/tei:p/*', namespaces=NAMESPACES)
        
        return xml
    
    def get_transcription(self, filename):
        return self._stringify_xml_and_text(filename, self.transcription_xpath)

    def get_transcription_segmented(self, filename):
        return self._stringify_xml_and_text(filename, self.transcription_segmented_xpath)

    def get_translation(self, filename):
        return self._stringify_xml_and_text(filename, self.translation_xpath)

    def _parse_file(self, filename):
        file = Path(self._dir / filename)

        logging.info(f"Attempting to parse {file}.")

        return etree.parse(file).getroot()
    
    def _stringify_xml_and_text(self, filename, xpath):
        tree = self._parse_file(filename)
        edition = self.get_edition(tree, xpath)
        elements = self.get_text_elements(tree, xpath)

        if edition is not None:
            return (
                etree.tostring(edition, encoding="unicode"), 
                " ".join([etree.tostring(el, encoding="unicode", method="text").strip() for el in elements])
            )

        logging.warning(f"No nodes found for {xpath} in {filename}.")

        return (None, None)