"""
flask server, and optional helper code
"""

import os
import sys
import collections

from flask import Flask, jsonify, request
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api


load_dotenv(find_dotenv())
app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/pythondevbox_v4.db'
db = SQLAlchemy(app)
api = Api(app)


def errorLog(log):
    print(f'[LOG] {log}', file=sys.stderr)


class ApiModelMixin(object):

    @property
    def as_dict(self):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }


class UserModel(
        db.Model,
        ApiModelMixin,
):
    id = db.Column(db.Integer, primary_key=True)


class SnippetModel(
        db.Model,
        ApiModelMixin,
):
    id = db.Column(db.Integer, primary_key=True)


class ActionModel(
        db.Model,
        ApiModelMixin,
):
    id = db.Column(db.Integer, primary_key=True)


class AcheievementModel(
        db.Model,
        ApiModelMixin,
):
    id = db.Column(db.Integer, primary_key=True)


@api.resource('/api/todos/<todo_id>')
class TodoResource(Resource):

    def delete(self, todo_id):
        # TodoModel.query.filter_by(id=todo_id).delete()
        # db.session.commit()
        return '', 204


@api.resource('/api/todos')
class TodoListResource(Resource):

    def get(self):
        try:
            # results = [
            #     todo.as_dict
            #     for todo in TodoModel.query.all()
            # ]
            # priorities = [
            #     result['priority']
            #     for result in results
            # ]
            # repeats = [item for item, count in collections.Counter(
            #     priorities).items() if count > 1]
            return '', 201
            # return [results, repeats]
        except BaseException as e:
            errorLog(e)
            return '', 500

    def post(self):
        try:
            # data = request.get_json()
            # todo = TodoModel(**data)
            # db.session.add(todo)
            # db.session.commit()
            return '', 201
        except BaseException as e:
            errorLog(e)
            return '', 500


@app.route('/')
def index():
    return 'hello world!!'


@app.route('/api/ping')
def ping():
    return jsonify({'data': 'pong'})


db.create_all()
