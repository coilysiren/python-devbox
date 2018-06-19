from ..models import JobModel
from ..server import TOTAL_SEED_JOBS
from .helper import json_body
from .test_fixtures import app, db, session, test_app


def test_job_answer_post_control(test_app, session):
    # function under test
    response = test_app.post(
        '/jobs/1/answer',
        data={'response': 'Cats'},
    )
    # assertion
    assert response.status_code == 200


def test_job_answer_bad_data_case_one(test_app, session):
    # function under test
    response = test_app.post('/jobs/1/answer')
    # assertion
    assert response.status_code == 400
    assert json_body(response) == 'BadRequestNoDataException'


def test_job_answer_bad_data_case_two(test_app, session):
    # function under test
    response = test_app.post(
        '/jobs/1/answer',
        data={'bad key': 'bad value'},
    )
    # assertion
    assert response.status_code == 400
    assert json_body(response) == 'BadRequestMissingAttributeException'


def test_job_answer_returns_updated_job_info(test_app, session):
    # function under test
    response = test_app.post(
        '/jobs/1/answer',
        data={'response': 'Cats'},
    )
    # assertion
    assert response.status_code == 200
    assert type(json_body(response)) == dict
    assert json_body(response)['response'] == 'Cats'


def test_job_answer_cannot_answer_others(test_app, session):
    # setup
    test_app.post(
        '/jobs/1/answer',
        data={'response': 'Dogs'},
    )
    # function under test
    response = test_app.post(
        '/jobs/1/answer',
        data={'response': 'Cats'},
    )
    # assertion
    assert response.status_code == 403
    assert json_body(response) == 'ForbiddenException'


def test_job_answer_returns_duplicate_status(test_app, session):
    # setup
    test_app.post(
        '/jobs/1/answer',
        data={'response': 'Cats'},
    )
    # function under test
    response = test_app.post(
        '/jobs/1/answer',
        data={'response': 'Cats'},
    )
    # assertion
    assert response.status_code == 409
    assert json_body(response) == 'ConflictException'


def test_job_answer_job_does_not_exist(test_app, session):
    # function under test
    response = test_app.post(f'/jobs/{TOTAL_SEED_JOBS + 1}/answer')
    # assertion
    assert response.status_code == 404
    assert json_body(response) == 'NotFoundJobDoesNotExistException'
