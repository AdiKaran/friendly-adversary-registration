import pytest
from app import create_app

from database.db import db
from database.models import *


@pytest.fixture(scope="session")
def client():
    """Test client with application context"""
    app = create_app("config.testing")
    context = app.app_context()
    context.push()
    with app.test_client() as client:
        yield client
    context.pop()


@pytest.fixture(scope="session")
def database(client):
    """Session wide database"""
    db.app = client
    db.create_all()
    yield db
    db.drop_all()


@pytest.fixture
def session(database):
    """Database session for individual tests"""
    connection = database.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = database.create_scoped_session(options=options)

    database.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()
