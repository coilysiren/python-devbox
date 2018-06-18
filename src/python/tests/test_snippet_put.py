import json
import sys

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
    pass


def test_put_snippet_cannot_share_unshareable_snippet(test_app, session):
    pass


def test_put_snippet_updates_likes(test_app, session):
    pass


def test_put_snippet_can_share_own_snippet(test_app, session):
    pass


def test_put_snippet_can_like_own_snippet(test_app, session):
    pass


def test_put_snippet_cannot_share_unauthorized_snippet(test_app, session):
    pass


def test_put_snippet_cannot_like_unauthorized_snippet(test_app, session):
    pass


def test_put_snippet_can_like_share_multiple_times(test_app, session):
    pass


def test_put_snippet_can_like_snippet_multiple_times(test_app, session):
    pass


def test_put_snippet_snippet_can_be_shared_after_updating_share_status(test_app, session):
    pass
