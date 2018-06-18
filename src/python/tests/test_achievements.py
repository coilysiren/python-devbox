import json
import sys

import pytest

from ..server import SnippetModel
from .helper import json_body
from .test_fixtures import app, db, session, test_app


def test_get_achievements_created(test_app, session):
    # setup
    snips = 40
    for i in range(4 + 1):
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
    assert response.status_code == 200
    assert int(json_body(response)['created']) == snips / 10
