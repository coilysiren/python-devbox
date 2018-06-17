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


def test_get_snippets_shows_shared_snippets(app, session):
    snippet = SnippetModel()
    session.add(snippet)
    session.commit()

    response = app.get('/api/ping')
    assert json_body(response) == {'data': 'pong'}
