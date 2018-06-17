import json
import sys

from .server import SnippetModel
from .test_helper import app, db, session


def json_body(response):
    return json.loads(response.get_data().decode(sys.getdefaultencoding()))


def test_index(app):
    response = app.get('/')
    assert response.get_data(as_text=True) == 'hello world!!'


def test_ping(app):
    response = app.get('/api/ping')
    assert json_body(response) == {'data': 'pong'}


def test_get_snippets_requires_snippets(app, session):
    # function under test
    response = app.get('/snippets')
    # assertion
    assert len(json_body(response)) == 0
    # assert response.status_code == 404


def test_get_snippets_shows_shared_snippets(app, session):
    # setup
    snippet = SnippetModel(shared=True)
    session.add(snippet)
    session.commit()
    # function under test
    response = app.get('/snippets')
    # assertion
    assert len(json_body(response)) == 1
    assert response.status_code == 200


def test_get_snippets_does_not_show_unshared_snippets(app, session):
    # setup
    snippet = SnippetModel(shared=False)
    session.add(snippet)
    session.commit()
    # function under test
    response = app.get('/snippets')
    # assertion
    assert len(json_body(response)) == 0
    # assert response.status_code == 404


def test_get_snippets_shows_proper_count_when_mixed_types(app, session):
    # setup
    session.add(SnippetModel(shared=True))
    session.add(SnippetModel(shared=True))
    session.add(SnippetModel(shared=False))
    session.commit()
    # function under test
    response = app.get('/snippets')
    # assertion
    assert len(json_body(response)) == 2
    assert response.status_code == 200
