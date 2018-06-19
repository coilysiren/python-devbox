from ..models import JobModel
from ..server import TOTAL_SEED_JOBS
from .helper import json_body
from .test_fixtures import app, db, session, test_app


def test_job_answer_post_control(test_app, session):
    # function under test
    response = test_app.post('/jobs/1/answer')
    # assertion
    assert response.status_code == 200


def test_job_answer_returns_updated_job_info(test_app, session):
    pass


def test_job_answer_cannot_answer_others(test_app, session):
    pass


def test_job_answer_returns_duplicate_status(test_app, session):
    pass
