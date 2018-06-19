from ..models import JobModel
from ..server import TOTAL_SEED_JOBS
from .helper import json_body
from .test_fixtures import app, db, session, test_app


def test_job_answer_post_control(test_app, session):
    # setup
    # test_app.get('/api/seed')
    # function under test
    response = test_app.post('/jobs/1/answer')
    # assertion
    assert response.status_code == 200
