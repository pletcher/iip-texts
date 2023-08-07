# -*- coding: utf-8 -*-
import os
import unicodedata

from fastapi import Depends
from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse

from sqlalchemy import select
from sqlalchemy.orm import Session

from iip_search import models
from iip_search import schemas

from iip_search.db import SessionLocal
from iip_search.db import engine

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request: Request, exc: ResponseValidationError):
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


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


@app.get("/", response_model=list[schemas.InscriptionResponse])
def search(search: str | None = None, db: Session = Depends(get_db)):
    normalized_string = remove_accents(search)
    stmt = (
        select(models.Inscription)
        .distinct(models.Inscription.id)
        .join(
            models.Inscription.editions.and_(
                models.Edition.searchable_text.match(normalized_string)
            ),
        )
    )

    results = db.execute(stmt).scalars()

    return results


# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db_session.remove()


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])
