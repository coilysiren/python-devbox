from . import app
import json
import sys


def json_body(response):
    return json.loads(response.get_data().decode(sys.getdefaultencoding()))


def test_index():
    test_app = app.test_client()
    response = test_app.get('/')
    assert response.get_data(as_text=True) == 'hello world!!'


def test_ping():
    test_app = app.test_client()
    response = test_app.get('/api/ping')
    assert json_body(response) == {'data': 'pong'}
