from lxml import etree
from pathlib import Path

import os

EPIDOC_DIR = Path("epidoc-files")
NAMESPACES = {
    "tei": "http://www.tei-c.org/ns/1.0"
}

class EpidocParser():
    transcription_xpath = "//tei:text/tei:body/tei:div[@type = 'edition' and @subtype = 'transcription']/tei:p/*"
    transcription_segmented_xpath = "//tei:text/tei:body/tei:div[@type = 'edition' and @subtype = 'transcription_segmented']/tei:p/*"
    translation_xpath = "//tei:text/tei:body/tei:div[@type = 'edition' and @subtype = 'translation']/tei:p/*"

    def __init__(self, dir = EPIDOC_DIR):
        self._dir = dir

    def list_directory_contents(self):
        return os.listdir(self._dir)

    def get_text_elements(self, filename, xpath = self.transcription_xpath):
        root = etree.parse(Path(self._dir / filename)).getroot()
        xml = root.xpath(xpath, namespaces=NAMESPACES)
        
        return [(el, etree.tostring(el, encoding="unicode", method="text").strip()) for el in xml]

if __name__ == "__main__":
    parser = EpidocParser()
    print(EpidocParser.get_text_elements("abur0001.xml"))