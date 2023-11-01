from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import get_settings

# sqlalchemy is an orm

# You can think of engine as the entry point to your database.
# The first argument is the database URL, which you receive from db_url of the settings
# You set check_same_thread to False because you’re working with an SQLite database. With this
# connection argument, SQLite allows more than one request at a time to communicate with the database.
engine = create_engine(
    get_settings().db_url, connect_args={"check_same_thread": False}
)
# You’ll create a working
# database session when you instantiate SessionLocal later.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# declarative_base function returns a class that connects the
# database engine to the SQLAlchemy functionality of the models.
# Base will be the class that the database model inherits from in your models.py file.
Base = declarative_base()
