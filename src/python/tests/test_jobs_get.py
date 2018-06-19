from ..models import JobModel
from ..server import TOTAL_SEED_JOBS
from .helper import json_body
from .test_fixtures import app, db, session, test_app


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


def test_jobs_responding_to_job_makes_it_unavailable(test_app, session):
    # setup
    job = JobModel.query.all()[0]
    job.response_text = 'Cats'
    session.add(job)
    session.commit()
    # function under test
    response = test_app.get('/jobs')
    # assertion
    assert response.status_code == 200
    assert len(json_body(response)) == TOTAL_SEED_JOBS - 1
