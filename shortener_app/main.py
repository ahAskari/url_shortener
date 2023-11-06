import validators
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse

from .utility import generate_random_key
from .import schema, models
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

    key = generate_random_key(5)
    secret_key = generate_random_key(8)
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key

    return db_url


@app.get('/{url_key}')
def forward_to_target_url(url_key: str, request: Request, db: Session = Depends(get_db)):
    db_url = (
        db.query(models.URL).filter(models.URL.key == url_key, models.URL.is_active).first()
    )

    if db_url:
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request):
    message = f'URL \'{request.url}\' doesn\'t exist'
    raise HTTPException(status_code=400, detail=message)
