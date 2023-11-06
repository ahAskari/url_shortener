import validators
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse

from . import schema, models, crud
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def read_root():
    return 'Welcome to url shortener'


@app.post('/url', response_model=schema.URLInfo)
def create_url(url: schema.UrlBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        return raise_bad_request('Your provided URL is not valid')

    db_url = crud.create_db_url(db=db, url=url)
    db_url.url = db_url.key
    db_url.admin_url = db_url.secret_key

    return db_url


@app.get('/{url_key}')
def forward_to_target_url(url_key: str, request: Request, db: Session = Depends(get_db)):
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request):
    message = f'URL \'{request.url}\' doesn\'t exist'
    raise HTTPException(status_code=400, detail=message)
