import logging
import os
import re

from lxml import etree
from pathlib import Path

from iip_search import models

EPIDOC_DIR = Path("../epidoc-files")
NAMESPACES = {
    "tei": "http://www.tei-c.org/ns/1.0",
    "xml": "http://www.w3.org/XML/1998/namespace",
}
TAXONOMY_FILE = Path("../include_taxonomies.xml")
XML_ID_ATTRIB = "{http://www.w3.org/XML/1998/namespace}id"
XML_LANG_ATTRIB = "{http://www.w3.org/XML/1998/namespace}lang"

logging.basicConfig(format="%(levelname)s: %(asctime)s %(message)s", level=logging.INFO)

whitespace_regex = re.compile(r"\s+")

LANGUAGES = {
    "arc": {
        "label": "Aramaic",
    },
    "geo": {
        "label": "Georgian",
    },
    "grc": {
        "label": "Greek",
    },
    "he": {
        "label": "Hebrew",
        "short_form": "heb",
    },
    "heb": {
        "label": "Hebrew",
    },
    "la": {
        "label": "Latin",
        "short_form": "lat",
    },
    "lat": {"label": "Latin"},
    "Other": {
        "label": "Other",
    },
    "phn": {
        "label": "Phoenician",
    },
    "syc": {
        "label": "Syriac",
    },
    "x-unknown": {
        "label": "Unknown",
    },
    "xcl": {"label": "Armenian"},
}


class EpidocParser:
    bibliography_xpath = (
        "//tei:text/tei:back/tei:div[@type = 'bibliography']/tei:listBibl/tei:bibl"
    )
    dimensions_xpath = "//tei:dimensions"
    iip_form_description_xpath = (
        "//tei:sourceDesc/tei:msDesc/tei:physDesc/tei:objectDesc"
    )
    transcription_xpath = (
        "//tei:text/tei:body/tei:div[@type = 'edition' and @subtype = 'transcription']"
    )
    transcription_segmented_xpath = "//tei:text/tei:body/tei:div[@type = 'edition' and @subtype = 'transcription_segmented']"
    translation_xpath = "//tei:text/tei:body/tei:div[@type = 'translation']"

    def __init__(self, filename):
        self.filename = filename
        self.taxonomies = self._get_taxonomies()
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
        settlement = self.tree.find(
            "//tei:placeName/tei:settlement", namespaces=NAMESPACES
        )

        return models.City(
            placename=settlement.text, pleaides_ref=settlement.get("ref")
        )

    def get_description(self):
        commentary = self.tree.xpath(
            "//tei:div[@type = 'commentary']/tei:p/text()", namespaces=NAMESPACES
        )[0]

        return whitespace_regex.sub(" ", commentary)

    def get_dimensions(self):
        dimensions = []
        for dimension_entry in self.tree.iterfind(
            self.dimensions_xpath, namespaces=NAMESPACES
        ):
            attributes = dict(dimension_entry.attrib)

            depth = dimension_entry.xpath("./tei:depth/text()", namespaces=NAMESPACES)
            height = dimension_entry.xpath("./tei:height/text()", namespaces=NAMESPACES)
            width = dimension_entry.xpath("./tei:width/text()", namespaces=NAMESPACES)

            depth = depth[0] if len(depth) > 0 else None
            height = height[0] if len(height) > 0 else None
            width = width[0] if len(width) > 0 else None
            entry = {"depth": depth, "height": height, "width": width}
            entry.update(attributes)
            dimensions.append(entry)

        return dimensions

    def get_iip_form(self):
        object_description = self.tree.find(
            self.iip_form_description_xpath, namespaces=NAMESPACES
        )

        forms = []
        for form in object_description.get("ana").replace("#", "").split(" "):
            ana = self.taxonomies[form]["ana"]
            description = self.taxonomies[form]["description"]

            forms.append(models.IIPForm(xml_id=form, ana=ana, description=description))

        return forms

    def get_iip_genres(self):
        ms_item = self.tree.find("//tei:msItem", namespaces=NAMESPACES)

        return [
            models.IIPGenre(
                xml_id=genre, description=self.taxonomies[genre].get("description")
            )
            for genre in ms_item.get("class").replace("#", "").split(" ")
        ]

    def get_iip_materials(self):
        support_desc = self.tree.find("//tei:supportDesc", namespaces=NAMESPACES)

        return [
            models.IIPMaterial(
                xml_id=materials,
                description=self.taxonomies[materials].get("description"),
            )
            for materials in support_desc.get("ana").replace("#", "").split(" ")
        ]

    def get_iip_preservation(self):
        preservation = self.tree.find("//tei:condition", namespaces=NAMESPACES)

        return models.IIPPreservation(
            xml_id=preservation,
            description=self.taxonomies[preservation]["description"],
        )

    def get_iip_religions(self):
        ms_item = self.tree.find("//tei:msItem", namespaces=NAMESPACES)

        return [
            models.IIPReligion(
                xml_id=religion,
                description=self.taxonomies[religion].get("description"),
            )
            for religion in ms_item.get("ana").replace("#", "").split(" ")
        ]

    def get_iip_writings(self):
        hand_note = self.tree.find("//tei:handNote", namespaces=NAMESPACES)
        ana = hand_note.get("ana").replace("#", "")
        note = hand_note.find("./tei:p", namespaces=NAMESPACES)

        if note is not None:
            note = note.text

        return [
            models.IIPWriting(
                xml_id=ana,
                note=note,
                description=self.taxonomies[ana].get("description"),
            )
        ]

    def get_images(self):
        images = []

        main_image = self.tree.find(
            "//tei:facsimile/tei:graphic", namespaces=NAMESPACES
        )

        if main_image is not None:
            images.append(models.Image(graphic_url=main_image.get("url")))

        for image in self.tree.iterfind(
            "//tei:facsimile/tei:surface", namespaces=NAMESPACES
        ):
            desc_tag = image.find("./tei:desc", namespaces=NAMESPACES)
            graphic_tag = image.find("./tei:graphic", namespaces=NAMESPACES)
            graphic_url = graphic_tag.get("url", "")

            if len(graphic_url) > 0:
                images.append(
                    models.Image(description=desc_tag.text, graphic_url=graphic_url)
                )

        return images

    def get_languages(self):
        lang_codes = set()
        for tag in self.tree.iterfind(
            f"//*[@{XML_LANG_ATTRIB}]", namespaces=NAMESPACES
        ):
            lang = tag.get(XML_LANG_ATTRIB)
            short_form = LANGUAGES.get(lang).get("short_form", lang)

            lang_codes.add(short_form)

        languages = []
        for short_form in list(lang_codes):
            label = LANGUAGES.get(short_form).get("label")

            # TODO: This check is most likely unnecessary, but it's worth
            # keeping an eye on.
            if label is not None:
                languages.append(models.Language(label=label, short_form=short_form))
            else:
                logging.warn(
                    f"No language label found for short (ISO 639-3) form {short_form}."
                )

        return languages

    def get_not_before(self):
        date = self.tree.find("//tei:origin/tei:date", namespaces=NAMESPACES)

        return date.get("notBefore")

    def get_not_after(self):
        date = self.tree.find("//tei:origin/tei:date", namespaces=NAMESPACES)

        return date.get("notAfter")

    def get_provenance(self):
        provance_tag = self.tree.find(
            "//tei:history/tei:provenance", namespaces=NAMESPACES
        )

        if provenance_tag is not None:
            placename = provenance_tag.find("./tei:placeName", namespaces=NAMESPACES)

            if placename is not None:
                return models.Provenance(placename=placename.text)

        return None

    def get_region(self):
        region_tag = self.tree.find(
            "//tei:history/tei:origin/tei:region", namespaces=NAMESPACES
        )

        if region_tag is not None:
            return models.Region(label=region_tag.text)

        return None

    def get_short_description(self):
        pass

    def get_title(self):
        ms_item_text = self.tree.xpath(
            "//tei:msDesc/tei:msContents/tei:msItem/*/text()", namespaces=NAMESPACES
        )

        return ms_item_text[0].strip()

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

    def _get_taxonomies(self):
        tree = etree.parse(TAXONOMY_FILE)

        forms = self._get_taxonomy(tree, "form")
        genres = self._get_taxonomy(tree, "genre")
        materials = self._get_taxonomy(tree, "materials")
        preservations = self._get_taxonomy(tree, "preservation")
        religions = self._get_taxonomy(tree, "religion")
        writings = self._get_taxonomy(tree, "writing")

        return {
            "forms": forms,
            "genres": genres,
            "materials": materials,
            "preservations": preservations,
            "religions": religions,
            "writings": writings,
        }

    def _get_taxonomy(self, tree, taxonomy_name):
        logging.info(f"Getting {taxonomy_name} taxonomy...")
        taxonomy = {}
        for item in tree.find(
            f"//tei:taxonomy[@xml:id = 'IIP-{taxonomy_name}']", namespaces=NAMESPACES
        ):
            xml_id = item.get(XML_ID_ATTRIB)
            taxonomy[xml_id] = {}

            # only forms appear to have an @ana attribute
            if taxonomy_name == "form":
                taxonomy[xml_id]["ana"] = item.get("ana")

            description = item.find("./tei:catDesc", namespaces=NAMESPACES)
            taxonomy[xml_id]["description"] = (
                description.text if description is not None else description
            )

        return taxonomy

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
