from . import app


def test_index():
    test_app = app.test_client()
    response = test_app.get('/')
    assert response.body == 'hello world!!'
