from ..models import JobModel
from .helper import json_body
from .test_fixtures import app, db, session, test_app


def test_job_get_control(test_app, session):
    # function under test
    response = test_app.get('/jobs/1')
    # assertion
    assert response.status_code == 200
