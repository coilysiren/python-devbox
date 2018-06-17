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
        attrs = {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
        attrs['object'] = self.__class__.__name__.strip('Model')
        return attrs


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
    shared = db.Column(db.Boolean, default=True)
    text = db.Column(db.String)


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


@api.resource('/snippets')
class ResourceSnippets(Resource):

    def get(self):
        try:
            snippets = [
                snippet.as_dict
                for snippet in SnippetModel.query.filter_by(shared=True)
            ]
            if snippets:
                return snippets, 200
            else:
                return [], 404
        except BaseException as e:
            errorLog(e)
            return 'server error', 500

    def post(self):
        try:
            data = request.get_json()

            if not data:
                errorLog(data)
                return 'POST data required', 400
            elif not data.get('text'):
                errorLog(data)
                return 'POST data.text required', 400

            snippet = SnippetModel(**data)
            db.session.add(snippet)
            db.session.commit()
            return snippet.as_dict, 201
        except BaseException as e:
            errorLog(e)
            return 'server error', 500


@app.route('/')
def index():
    return 'hello world!!'


@app.route('/api/ping')
def ping():
    return jsonify({'data': 'pong'})


db.create_all()
