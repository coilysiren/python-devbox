"""
flask server, and optional helper code
"""

import os

from flask import Flask, jsonify, request
from dotenv import load_dotenv, find_dotenv
from flask_restful import Api, Resource

from .services import JobsService
from .models import db, JobModel


load_dotenv(find_dotenv())
app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/pythondevbox_v5.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db.init_app(app)
TOTAL_SEED_JOBS = 20


@api.resource('/jobs')
class JobsResource(Resource):

    def get(self):
        return JobsService().get_all_jobs(request)


@api.resource('/jobs/<job_id>/answer')
class JobAnswerResouce(Resource):

    def post(self, job_id):
        return JobsService().post_job_answer(request, job_id)


@api.resource('/jobs/<job_id>')
class JobResource(Resource):

    def get(self, job_id):
        return JobsService().get_job_info(request, job_id)


@app.route('/')
def index():
    return 'hello world!!'


@app.route('/api/seed')
def lazy_girls_seed_data_route():
    for i in range(TOTAL_SEED_JOBS):
        db.session.add(JobModel())
    db.session.commit()
    return 'data seeded!'


@app.route('/api/ping')
def ping():
    return jsonify({'data': 'pong'})
