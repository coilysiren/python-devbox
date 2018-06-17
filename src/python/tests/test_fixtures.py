import pytest

from ..server import app as _app
from ..server import db as _db


# ref: http://alexmic.net/flask-sqlalchemy-pytest/


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    return _app.test_client()


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""

    def teardown():
        _db.drop_all()

    _db.create_all()

    request.addfinalizer(teardown)

    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""

    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
