from ..models import JobModel
from ..server import TOTAL_SEED_JOBS
from .helper import json_body
from .test_fixtures import app, db, session, test_app


def test_job_get_control(test_app, session):
    # function under test
    response = test_app.get('/jobs/1')
    # assertion
    assert response.status_code == 200
    body = json_body(response)
    assert body['status'] == 'open'


def test_job_get_does_not_exist(test_app, session):
    # function under test
    response = test_app.get(f'/jobs/{TOTAL_SEED_JOBS + 1}')
    # assertion
    assert response.status_code == 404
    assert json_body(response) == 'NotFoundJobDoesNotExistException'


def test_job_already_taken_job_returns_closed_status(test_app, session):
    # setup
    test_app.post(
        '/jobs/1/answer',
        data={'response': 'Dogs'},
    )
    # function under test
    response = test_app.get('/jobs/1')
    # assertion
    assert response.status_code == 200
    body = json_body(response)
    assert body['status'] == 'closed'
