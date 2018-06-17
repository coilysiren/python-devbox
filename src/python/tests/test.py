import json
import sys

from ..server import SnippetModel
from .test_helper import json_body
from .test_fixtures import app, db, session, test_app


def test_index(test_app):
    response = app.get('/')
    assert response.get_data(as_text=True) == 'hello world!!'


def test_ping(test_app):
    response = app.get('/api/ping')
    assert json_body(response) == {'data': 'pong'}
