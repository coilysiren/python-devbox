import json

from .server import SnippetModel
from .test_helper import json_body, app, db, session


def test_post_snipped_requires_data(app, session):
    # TODO, sync with product manager RE empty snippets
    # function under test
    response = app.post(
        '/snippets',
    )
    # assertion
    assert response.status_code == 400


def test_post_snipped_requires_data_text(app, session):
    # TODO, sync with product manager RE empty snippets
    # function under test
    response = app.post(
        '/snippets',
        data={},
    )
    # assertion
    assert response.status_code == 400


def test_post_snipped_requires_json(app, session):
    # TODO, sync with product manager RE empty snippets
    # function under test
    response = app.post(
        '/snippets',
        data={'text': 'rawr'},
    )
    # assertion
    assert response.status_code == 400


def test_post_snipped_requires_content_type(app, session):
    # TODO, sync with product manager RE empty snippets
    # function under test
    response = app.post(
        '/snippets',
        data=json.dumps({'text': 'rawr'}),
    )
    # assertion
    assert response.status_code == 400


def test_post_returns_snippet(app, session):
    # TODO, sync with product manager RE empty snippets
    # function under test
    response = app.post(
        '/snippets',
        data=json.dumps({'text': 'rawr'}),
        content_type='application/json',
    )
    # assertion
    assert len(json_body(response)) == 1
    assert json_body(response)['object'] == 'Snippet'
    assert response.status_code == 201


def test_post_respects_text_input(app, session):
    # TODO, sync with product manager RE empty snippets
    # function under test
    response = app.post(
        '/snippets',
        data=json.dumps({'text': 'rawr'}),
        content_type='application/json',
    )
    # assertion
    assert json_body(response)['text'] == 'rawr'
    assert response.status_code == 201


def test_post_respects_share_input_false(app, session):
    # function under test
    response = app.post(
        '/snippets',
        data=json.dumps({'text': 'rawr', 'shared': False}),
        content_type='application/json',
    )
    # assertion
    assert json_body(response)['shared'] == False
    assert response.status_code == 201


def test_post_respects_share_input_true(app, session):
    # function under test
    response = app.post(
        '/snippets',
        data=json.dumps({'text': 'rawr', 'shared': True}),
        content_type='application/json',
    )
    # assertion
    assert json_body(response)['shared'] == True
    assert response.status_code == 201
