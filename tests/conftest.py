import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from database import Base, get_db
from main import app

db_host = os.getenv("TEST_DB_HOST")
db_port = os.getenv("TEST_DB_PORT")
db_name = os.getenv("TEST_DB_NAME")
db_psw = os.getenv("TEST_DB_PASS")
db_user = os.getenv("TEST_DB_USER")

PG_CONN_URL = f"postgresql://{db_user}:{db_psw}@{db_host}:{db_port}/{db_name}"


@pytest.fixture()
def engine_root():
    """Returns DB engine with root privileges."""
    return create_engine(PG_CONN_URL)


@pytest.fixture(scope="function", autouse=True)
def clean_db(engine_root) -> Generator:
    """Cleans & creates DB schema"""
    Base.metadata.create_all(bind=engine_root, checkfirst=True)
    yield
    Base.metadata.drop_all(bind=engine_root)


def get_engine():
    return create_engine(PG_CONN_URL)


@pytest.fixture()
def db_session(engine_root):
    connection = engine_root.connect()
    Session = scoped_session(sessionmaker(autoflush=False))
    session = Session(bind=connection)
    yield session
    session.close()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db_new():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db_new
    yield TestClient(app)
    del app.dependency_overrides[get_db]
