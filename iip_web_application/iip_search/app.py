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

from iip_search import crud
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
    return crud.search_inscriptions(db, search)


@app.get("/facets", response_model=schemas.FacetsResponse)
def facets(db: Session = Depends(get_db)):
    return crud.list_facets(db)


@app.get("/inscriptions", response_model=list[schemas.InscriptionResponse])
def list_inscriptions(db: Session = Depends(get_db)):
    return crud.list_inscriptions(db)


@app.get("/languages", response_model=list[schemas.Language])
def list_languages(db: Session = Depends(get_db)):
    return crud.list_languages(db)


@app.get("/locations", response_model=list[schemas.Location])
def list_locations(db: Session = Depends(get_db)):
    return crud.list_locations(db)
