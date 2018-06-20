from ..models import JobModel
from .helper import json_body
from .test_fixtures import app, db, session, test_app, TOTAL_SEED_JOBS


def test_jobs_get_control(test_app, session):
    # function under test
    response = test_app.get('/jobs')
    # assertion
    assert response.status_code == 200
    assert len(json_body(response)) == TOTAL_SEED_JOBS


def test_jobs_none_present(test_app, session):
    # setup
    JobModel.query.delete()
    session.commit()
    # function under test
    response = test_app.get('/jobs')
    # assertion
    assert response.status_code == 404
    assert json_body(response) == 'NotFoundNoJobsAvailableException'
