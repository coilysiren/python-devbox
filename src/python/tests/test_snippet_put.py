import json
import sys

import pytest

from ..server import SnippetModel
from .helper import json_body
from .test_fixtures import app, db, session, test_app


def test_put_snippet_requires_data(test_app, session):
    # setup
    response = test_app.post(
        '/snippets',
        json={'text': 'example', 'shared': False},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    snippet_id = json_body(response)['id']
    # function under test
    response = test_app.put(
        f'/snippets/{snippet_id}',
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 400


def test_put_snippet_can_update_shared_status(test_app, session):
    # setup
    response = test_app.post(
        '/snippets',
        json={'text': 'example', 'shared': False},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    snippet_id = json_body(response)['id']
    # control assertion
    assert SnippetModel.query.filter_by(id=snippet_id).first().shared == False
    # function under test
    response = test_app.put(
        f'/snippets/{snippet_id}',
        json={'allow_sharing': True},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    # assertion
    assert SnippetModel.query.filter_by(id=snippet_id).first().shared == True


def test_put_snippet_updates_shares(test_app, session):
    # setup
    response = test_app.post(
        '/snippets',
        json={'text': 'example', 'shared': True},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    snippet_id = json_body(response)['id']
    # control assertion
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['shares'] == 0
    # function under test
    response = test_app.put(
        f'/snippets/{snippet_id}',
        json={'shared': True},
        headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 200
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['shares'] == 1


def test_put_snippet_can_only_update_share_status_on_own_snippet(test_app, session):
    # setup
    response = test_app.post(
        '/snippets',
        json={'text': 'example', 'shared': False},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    snippet_id = json_body(response)['id']
    # control assertion
    assert SnippetModel.query.filter_by(id=snippet_id).first().shared == False
    # function under test
    response = test_app.put(
        f'/snippets/{snippet_id}',
        json={'allow_sharing': True},
        headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 404
    assert SnippetModel.query.filter_by(id=snippet_id).first().shared == False


def test_put_snippet_cannot_share_unshareable_snippet(test_app, session):
    # setup
    response = test_app.post(
        '/snippets',
        json={'text': 'example', 'shared': False},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    snippet_id = json_body(response)['id']
    # control assertion
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['shares'] == 0
    # function under test
    response = test_app.put(
        f'/snippets/{snippet_id}',
        json={'shared': True},
        headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code != 200
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['shares'] == 0


def test_put_snippet_updates_likes(test_app, session):
    # setup
    response = test_app.post(
        '/snippets',
        json={'text': 'example', 'shared': True},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    snippet_id = json_body(response)['id']
    # control assertion
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['likes'] == 0
    # function under test
    response = test_app.put(
        f'/snippets/{snippet_id}',
        json={'liked': True},
        headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 200
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['likes'] == 1


def test_put_snippet_updated_data_returned_in_response(test_app, session):
    # setup
    response = test_app.post(
        '/snippets',
        json={'text': 'example', 'shared': True},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    snippet_id = json_body(response)['id']
    # control assertion
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['likes'] == 0
    # function under test
    response = test_app.put(
        f'/snippets/{snippet_id}',
        json={'liked': True},
        headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 200
    assert json_body(response)['likes'] == 1
    assert json_body(response)['likes_data']


def test_put_snippet_actions_return_their_performer(test_app, session):
    # setup
    response = test_app.post(
        '/snippets',
        json={'text': 'example', 'shared': True},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    snippet_id = json_body(response)['id']
    # control assertion
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['likes'] == 0
    # function under test
    response = test_app.put(
        f'/snippets/{snippet_id}',
        json={'liked': True},
        headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 200
    assert json_body(response)[
        'likes_data'][0]['performer']['email_address'] == 'totallynotlynncyrin@gmail.com'


def test_put_snippet_cannot_share_own_snippet(test_app, session):
    # setup
    response = test_app.post(
        '/snippets',
        json={'text': 'example', 'shared': True},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    snippet_id = json_body(response)['id']
    # control assertion
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['shares'] == 0
    # function under test
    response = test_app.put(
        f'/snippets/{snippet_id}',
        json={'shared': True},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 401
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['shares'] == 0


def test_put_snippet_cannot_like_own_snippet(test_app, session):
    # setup
    response = test_app.post(
        '/snippets',
        json={'text': 'example', 'shared': True},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    snippet_id = json_body(response)['id']
    # control assertion
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['likes'] == 0
    # function under test
    response = test_app.put(
        f'/snippets/{snippet_id}',
        json={'liked': True},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 401
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['likes'] == 0


def test_put_snippet_cannot_like_multiple_times(test_app, session):
    # setup
    response = test_app.post(
        '/snippets',
        json={'text': 'example', 'shared': True},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    snippet_id = json_body(response)['id']
    # control assertion
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['likes'] == 0
    # function under test
    test_app.put(
        f'/snippets/{snippet_id}',
        json={'liked': True},
        headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
    )
    response = test_app.put(
        f'/snippets/{snippet_id}',
        json={'liked': True},
        headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 200
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['likes'] == 1


def test_put_snippet_cannot_share_multiple_times(test_app, session):
    # setup
    response = test_app.post(
        '/snippets',
        json={'text': 'example', 'shared': True},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    snippet_id = json_body(response)['id']
    # control assertion
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['shares'] == 0
    # function under test
    test_app.put(
        f'/snippets/{snippet_id}',
        json={'shared': True},
        headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
    )
    response = test_app.put(
        f'/snippets/{snippet_id}',
        json={'shared': True},
        headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 200
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['shares'] == 1


def test_put_snippet_can_like_and_share_at_the_same_time(test_app, session):
    # setup
    response = test_app.post(
        '/snippets',
        json={'text': 'example', 'shared': True},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    snippet_id = json_body(response)['id']
    # control assertion
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['shares'] == 0
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['likes'] == 0
    # function under test
    test_app.put(
        f'/snippets/{snippet_id}',
        json={'shared': True, 'liked': True},
        headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
    )
    # assertion
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['shares'] == 1
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['likes'] == 1


def test_put_snippet_can_unlike(test_app, session):
    # setup
    response = test_app.post(
        '/snippets',
        json={'text': 'example', 'shared': True},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    snippet_id = json_body(response)['id']
    test_app.put(
        f'/snippets/{snippet_id}',
        json={'liked': True},
        headers={'Authorization': 'lynnbot2000@gmail.com'}
    )
    test_app.put(
        f'/snippets/{snippet_id}',
        json={'liked': True},
        headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
    )
    # control assertion
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['likes'] == 2
    # function under test
    response = test_app.put(
        f'/snippets/{snippet_id}',
        json={'liked': False},
        headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 200
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['likes'] == 1


def test_put_snippet_can_unshare(test_app, session):
    # setup
    response = test_app.post(
        '/snippets',
        json={'text': 'example', 'shared': True},
        headers={'Authorization': 'lynncyrin@gmail.com'}
    )
    snippet_id = json_body(response)['id']
    test_app.put(
        f'/snippets/{snippet_id}',
        json={'shared': True},
        headers={'Authorization': 'lynnbot2000@gmail.com'}
    )
    test_app.put(
        f'/snippets/{snippet_id}',
        json={'shared': True},
        headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
    )
    # control assertion
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['shares'] == 2
    # function under test
    response = test_app.put(
        f'/snippets/{snippet_id}',
        json={'shared': False},
        headers={'Authorization': 'totallynotlynncyrin@gmail.com'}
    )
    # assertion
    assert response.status_code == 200
    assert SnippetModel.query.filter_by(
        id=snippet_id).first().as_dict['shares'] == 1
