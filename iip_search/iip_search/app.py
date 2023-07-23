# -*- coding: utf-8 -*-
import os

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
    stmt = select(models.Edition).where(
        models.Edition.searchable_text.match(search_string)
    )
    results = [
        schemas.InscriptionSchema().dumps(r.inscription)
        for r in db_session.execute(stmt).scalars()
    ]

    return {"results": results, "search": search_string}


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
