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


@api.resource('/jobs')
class JobsResource(Resource):

    def get(self):
        return '', 200


@api.resource('/jobs/<job_id>/answer')
class JobAnswerResouce(Resource):

    def post(self, job_id):
        return '', 200


@api.resource('/jobs/<job_id>')
class JobResource(Resource):

    def get(self, job_id):
        return '', 200


@app.route('/')
def index():
    return 'hello world!!'


@app.route('/api/ping')
def ping():
    return jsonify({'data': 'pong'})
