import json

import pytest

from .helper import json_body
from .test_fixtures import app, db, session, test_app


def test_post_snipped_requires_authorization(test_app, session):
    # function under test
    response = test_app.post(
        '/snippets',
    )
    # assertion
    assert response.status_code == 401


def test_post_snipped_requires_data(test_app, session):
    # function under test
    response = test_app.post(
        '/snippets',
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 400


def test_post_snipped_requires_data_text(test_app, session):
    # function under test
    response = test_app.post(
        '/snippets',
        data={},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 400


def test_post_snipped_requires_json(test_app, session):
    # function under test
    response = test_app.post(
        '/snippets',
        data={'text': 'rawr'},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 400


def test_post_snipped_requires_content_type(test_app, session):
    # function under test
    response = test_app.post(
        '/snippets',
        data=json.dumps({'text': 'rawr'}),
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 400


def test_post_control_example_returns_snippet(test_app, session):
    # function under test
    response = test_app.post(
        '/snippets',
        data=json.dumps({'text': 'rawr'}),
        content_type='application/json',
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 201
    assert json_body(response)['object'] == 'Snippet'


def test_post_returns_snippet(test_app, session):
    # function under test
    response = test_app.post(
        '/snippets',
        json={'text': 'rawr'},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 201
    assert json_body(response)['object'] == 'Snippet'


def test_post_respects_text_input(test_app, session):
    # function under test
    response = test_app.post(
        '/snippets',
        json={'text': 'rawr'},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 201
    assert json_body(response)['text'] == 'rawr'


def test_post_requires_text_input(test_app, session):
    # function under test
    response = test_app.post(
        '/snippets',
        json={'text': ''},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 400


def test_post_respects_share_input_false(test_app, session):
    # function under test
    response = test_app.post(
        '/snippets',
        json={'text': 'rawr', 'shared': False},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 201
    assert json_body(response)['shared'] == False


def test_post_respects_share_input_true(test_app, session):
    # function under test
    response = test_app.post(
        '/snippets',
        json={'text': 'rawr', 'shared': True},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 201
    assert json_body(response)['shared'] == True


def test_post_returns_authorized_user_object(test_app, session):
    # function under test
    response = test_app.post(
        '/snippets',
        json={'text': 'rawr', 'shared': True},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 201
    assert json_body(response)[
        'user']['email_address'] == 'lynncyrin@gmail.com'


def test_post_returns_data_with_owner_attribute(test_app, session):
    # function under test
    response = test_app.post(
        '/snippets',
        json={'text': 'rawr', 'shared': True},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 201
    assert json_body(response)['owner'] == 'lynncyrin@gmail.com'
