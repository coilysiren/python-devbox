import json
import sys

from ..server import SnippetModel
from .helper import json_body
from .test_fixtures import app, db, session, test_app


def test_get_snippets_requires_snippets(test_app, session):
    # function under test
    response = test_app.get('/snippets')
    # assertion
    assert response.status_code == 404
    assert len(json_body(response)) == 0


def test_get_snippets_shows_shared_snippets(test_app, session):
    # setup
    snippet = SnippetModel(shared=True)
    session.add(snippet)
    session.commit()
    # function under test
    response = test_app.get('/snippets')
    # assertion
    assert response.status_code == 200
    assert len(json_body(response)) == 1


def test_get_snippets_does_not_show_unshared_snippets(test_app, session):
    # setup
    snippet = SnippetModel(shared=False)
    session.add(snippet)
    session.commit()
    # function under test
    response = test_app.get('/snippets')
    # assertion
    assert response.status_code == 404
    assert len(json_body(response)) == 0


def test_get_snippets_shows_proper_count_when_mixed_types(test_app, session):
    # setup
    session.add(SnippetModel(shared=True))
    session.add(SnippetModel(shared=True))
    session.add(SnippetModel(shared=False))
    session.commit()
    # function under test
    response = test_app.get('/snippets')
    # assertion
    assert response.status_code == 200
    assert len(json_body(response)) == 2


def test_get_snippets_also_shows_current_users_unshared_snippets(test_app, session):
    # TODO, need authorization pattern first
    pass


def test_get_snippets_default_to_TODO(test_app, session):
    # setup
    session.add(SnippetModel())
    session.commit()
    # function under test
    response = test_app.get('/snippets')
    # assertion
    assert response.status_code == 200
    assert len(json_body(response)) == 1
