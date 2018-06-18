from ..models import JobModel
from .helper import json_body
from .test_fixtures import app, db, session, test_app


def test_job_answer_post_control(test_app, session):
    # function under test
    response = test_app.post('/jobs/1/answer')
    # assertion
    assert response.status_code == 200
