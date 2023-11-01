import validators
import secrets
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse

from . import models, schemas
from .database import SessionLocal, engine

app = FastAPI()

# binds your database engine with models.Base.metadata.create_all().
# If the database that you defined in engine doesn't exist yet,
# then it’ll be created with all modeled tables once you run your app the first time.
models.Base.metadata.create_all(bind=engine)


# define the get_db() function, which will create and yield new database
# sessions with each request. Once the request is finished, you close the
# session with db.close().
# You use the try … finally block to close the database connection
# in any case, even when an error occurs during the request.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def read_root():
    return "Welcome to the URL shortener API :)"


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)


# Line 25 defines create_url(), which requires a URLBase schema
# as an argument and depends on the database session.
# By passing get_db into Depends(),
# you establish a database session for the request
# and close the session when the request is finished.
@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")

    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key

    return db_url


# RedirectResponse returns an HTTP redirect that forwards the request of the client.
@app.get("/{url_key}")
def forward_to_target_url(
        url_key: str, request: Request, db: Session = Depends(get_db)
):
    db_url = (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )
    if db_url:
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)
