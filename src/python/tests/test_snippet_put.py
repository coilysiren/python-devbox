import json
import sys

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
    response = test_app.put(f'/snippets/{snippet_id}')
    # assertion
    assert response.status_code == 400


def test_put_snippet_updates_share_status(test_app, session):
    pass


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
