# -*- coding: utf-8 -*-
import os
import unicodedata

from flask import Flask
from flask import json
from flask import request

from sqlalchemy import select

from iip_search import models
from iip_search import schemas

from iip_search.db import init_db
from iip_search.db import db_session

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")

json.provider.DefaultJSONProvider.ensure_ascii = False

with app.app_context():
    init_db()


@app.route("/heartbeat")
def heartbeat():
    return "OK"


# Search fields from https://github.com/Brown-University-Library/iip-production/blob/main/iip_smr_web_app/common.py#L146C74-L146C136
# `(
#   'text',
#   'metadata',
#   'figure',
#   'region',
#   'city',
#   'place',
#   'type',
#   'physical_type',
#   'language',
#   'religion',
#   'material',
#   'notBefore',
#   'notAfter',
#   'display_status'
# )`


@app.route("/")
def search():
    search_string = request.args.get("search", "")
    normalized_string = remove_accents(search_string)
    stmt = (
        select(models.Inscription)
        .distinct(models.Inscription.id)
        .join(
            models.Inscription.editions.and_(
                models.Edition.searchable_text.match(normalized_string)
            ),
        )
    )

    results = [
        schemas.InscriptionSchema().dump(r) for r in db_session.execute(stmt).scalars()
    ]

    return {"results": results, "search": search_string}


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])
