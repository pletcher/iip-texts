#!/usr/bin/env python3

from iip_search import db
from iip_search.epidoc_parser import EpidocParser

import os

def main():
    parser = EpidocParser()
    files = parser.list_directory_contents()

    for file in files:
        parser.get_text_elements(file)

if __name__ == "__main__":
    main()