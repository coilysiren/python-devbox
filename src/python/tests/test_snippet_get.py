import json
import sys

from .helper import json_body
from .test_fixtures import app, db, session, test_app


def test_get_snippet_requires_snippets(test_app, session):
    # function under test
    response = test_app.get('/snippets/0/')
    # assertion
    assert response.status_code == 404


def test_get_snippet_unshared_snippets_require_authorization(test_app, session):
    # setup
    response = test_app.post(
        '/snippets',
        json={'text': 'example', 'shared': False},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    snippet_id = json_body(response)['id']
    # function under test
    response = test_app.get(f'/snippets/{snippet_id}')
    # assertion
    assert response.status_code == 404


def test_get_snippet_unshared_snippets_require_authorization_as_owner(test_app, session):
    # setup
    response = test_app.post(
        '/snippets',
        json={'text': 'example', 'shared': False},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    snippet_id = json_body(response)['id']
    # function under test
    response = test_app.get(
        f'/snippets/{snippet_id}',
        json={'text': 'example', 'shared': False},
        headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 404


def test_get_snippet_unshared_snippets_visible_to_current_user(test_app, session):
    # setup
    response = test_app.post(
        '/snippets',
        json={'text': 'example', 'shared': False},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    snippet_id = json_body(response)['id']
    # function under test
    response = test_app.get(
        f'/snippets/{snippet_id}',
        json={'text': 'example', 'shared': False},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 200
    assert json_body(response).get('id') == snippet_id
