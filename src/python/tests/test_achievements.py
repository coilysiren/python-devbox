import json
import sys

import pytest

from ..server import SnippetModel
from .helper import json_body
from .test_fixtures import app, db, session, test_app


def test_get_achievements_none(test_app, session):
    # function under test
    response = test_app.get(
        '/achievements',
        json={'text': 'example', 'shared': True},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 200
    assert int(json_body(response)['created']) == 0
    assert int(json_body(response)['liked']) == 0
    assert int(json_body(response)['shared']) == 0


def test_get_achievements_created(test_app, session):
    # setup
    snips = 20
    for i in range(snips):
        test_app.post(
            '/snippets',
            json={'text': 'example', 'shared': True},
            headers={'Authorization': 'lynncyrin@gmail.com'}
        )
    # function under test
    response = test_app.get(
        '/achievements',
        json={'text': 'example', 'shared': True},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    # assertion
    body = json_body(response)
    assert response.status_code == 200
    assert body
    assert int(body['created']) == snips / 10


def test_get_achievements_liked(test_app, session):
    # setup
    snips = 20
    responses = [
        test_app.post(
            '/snippets',
            json={'text': 'example', 'shared': True},
            headers={'Authorization': 'lynncyrin@gmail.com'}
        )
        for i in range(snips)
    ]
    for response in responses:
        snippet_id = json_body(response)['id']
        test_app.put(
            f'/snippets/{snippet_id}',
            json={'liked': True},
            headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
        )
    # function under test
    response = test_app.get(
        '/achievements',
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    # assertion
    body = json_body(response)
    assert response.status_code == 200
    assert body
    assert int(body['liked']) == snips / 10


def test_get_achievements_shared(test_app, session):
    # setup
    snips = 20
    responses = [
        test_app.post(
            '/snippets',
            json={'text': 'example', 'shared': True},
            headers={'Authorization': 'lynncyrin@gmail.com'}
        )
        for i in range(snips)
    ]
    for response in responses:
        snippet_id = json_body(response)['id']
        test_app.put(
            f'/snippets/{snippet_id}',
            json={'shared': True},
            headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
        )
    # function under test
    response = test_app.get(
        '/achievements',
        headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
    )
    # assertion
    body = json_body(response)
    assert response.status_code == 200
    assert body
    assert int(body['shared']) == snips / 10


def test_get_achievements_like_and_unlike_still_grants_achievements(test_app, session):
    # setup
    snips = 20
    responses = [
        test_app.post(
            '/snippets',
            json={'text': 'example', 'shared': True},
            headers={'Authorization': 'lynncyrin@gmail.com'}
        )
        for i in range(snips)
    ]
    for response in responses:
        snippet_id = json_body(response)['id']
        test_app.put(
            f'/snippets/{snippet_id}',
            json={'liked': True},
            headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
        )
        test_app.put(
            f'/snippets/{snippet_id}',
            json={'liked': False},
            headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
        )
    # function under test
    response = test_app.get(
        '/achievements',
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    # assertion
    body = json_body(response)
    assert response.status_code == 200
    assert body
    assert int(body['liked']) == snips / 10


def test_get_achievements_share_and_unshare_still_grants_achievements(test_app, session):
    # setup
    snips = 20
    responses = [
        test_app.post(
            '/snippets',
            json={'text': 'example', 'shared': True},
            headers={'Authorization': 'lynncyrin@gmail.com'}
        )
        for i in range(snips)
    ]
    for response in responses:
        snippet_id = json_body(response)['id']
        test_app.put(
            f'/snippets/{snippet_id}',
            json={'shared': True},
            headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
        )
        test_app.put(
            f'/snippets/{snippet_id}',
            json={'shared': True},
            headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
        )
    # function under test
    response = test_app.get(
        '/achievements',
        headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
    )
    # assertion
    body = json_body(response)
    assert response.status_code == 200
    assert body
    assert int(body['shared']) == snips / 10


def test_get_achievements_share_and_unshare_reshare_grants_double_achievements(test_app, session):
    # setup
    snips = 20
    responses = [
        test_app.post(
            '/snippets',
            json={'text': 'example', 'shared': True},
            headers={'Authorization': 'lynncyrin@gmail.com'}
        )
        for i in range(snips)
    ]
    for response in responses:
        snippet_id = json_body(response)['id']
        test_app.put(
            f'/snippets/{snippet_id}',
            json={'shared': True},
            headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
        )
        test_app.put(
            f'/snippets/{snippet_id}',
            json={'shared': False},
            headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
        )
        test_app.put(
            f'/snippets/{snippet_id}',
            json={'shared': True},
            headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
        )
    # function under test
    response = test_app.get(
        '/achievements',
        headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
    )
    # assertion
    body = json_body(response)
    assert response.status_code == 200
    assert body
    assert int(body['shared']) == 2 * snips / 10
