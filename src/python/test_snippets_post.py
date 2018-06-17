import json
import sys

from .server import SnippetModel
from .test_helper import json_body, app, db, session


def test_post_snipped_requires_data(app, session):
    # TODO, sync with product manager RE empty snippets
    # function under test
    response = app.post(
        '/snippets',
    )
    # assertion
    assert len(json_body(response)) == 0
    assert response.status_code == 400


def test_post_snipped_requires_data_text(app, session):
    # TODO, sync with product manager RE empty snippets
    # function under test
    response = app.post(
        '/snippets',
        data={},
    )
    # assertion
    assert len(json_body(response)) == 0
    assert response.status_code == 400


def test_post_returns_snippet(app, session):
    # TODO, sync with product manager RE empty snippets
    # function under test
    response = app.post(
        '/snippets',
        data={'text': 'rawr'},
    )
    # assertion
    assert len(json_body(response)) == 1
    assert response.status_code == 201


def test_post_respects_text_input(app, session):
    # TODO, sync with product manager RE empty snippets
    # function under test
    response = app.post(
        '/snippets',
        data={'text': 'rawr'},
    )
    # assertion
    assert json_body(response)['text'] == 'rawr'
    assert response.status_code == 201


def test_post_respects_share_input_false(app, session):
    # function under test
    response = app.post(
        '/snippets',
        data={'text': 'rawr', 'shared': False},
    )
    # assertion
    assert json_body(response)['shared'] == False
    assert response.status_code == 201


def test_post_respects_share_input_true(app, session):
    # function under test
    response = app.post(
        '/snippets',
        data={'text': 'rawr', 'shared': True},
    )
    # assertion
    assert json_body(response)['shared'] == True
    assert response.status_code == 201
