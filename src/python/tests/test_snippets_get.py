import json
import sys

from ..server import SnippetModel
from .test_helper import json_body
from .test_fixtures import app, db, session


def test_get_snippets_requires_snippets(app, session):
    # function under test
    response = app.get('/snippets')
    # assertion
    assert len(json_body(response)) == 0
    assert response.status_code == 404


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
    assert response.status_code == 404


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


def test_get_snippets_also_shows_current_users_unshared_snippets(app, session):
    # TODO, need authorization pattern first
    pass


def test_get_snippets_default_to_TODO(app, session):
    # TODO, sync with product manager RE default share state
    # setup
    session.add(SnippetModel())
    session.commit()
    # function under test
    response = app.get('/snippets')
    # assertion
    assert len(json_body(response)) == 1
    assert response.status_code == 200
