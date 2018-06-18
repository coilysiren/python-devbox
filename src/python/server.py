"""
flask server, and optional helper code
"""

import os

from flask import Flask, jsonify, request
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from .view_helpers import ResourceWithErrorHandling, with_authorization
from .models import db, SnippetModel


load_dotenv(find_dotenv())
app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/pythondevbox_v4.db'
api = Api(app)
db.init_app(app)


@api.resource('/snippets')
class ResourceSnippets(ResourceWithErrorHandling):

    @with_authorization(optional=True)
    def get(self):
        snippets = [
            snippet.as_dict
            for snippet in SnippetModel.query.filter_by(shared=True)
        ]
        if request.user:
            snippets += [
                snippet.as_dict
                for snippet in SnippetModel.query.filter_by(
                    shared=False, user=request.user)
            ]
        if snippets:
            return snippets, 200
        else:
            return [], 404

    @with_authorization()
    def post(self):

        data = request.get_json()
        if not data:
            return 'POST data required', 400
        elif not data.get('text'):
            return 'POST data.text required', 400
        data['user'] = request.user

        snippet = SnippetModel(**data)
        db.session.add(snippet)
        db.session.commit()
        return snippet.as_dict, 201


@api.resource('/snippets/<snippet_id>')
class ResourceSnippet(ResourceWithErrorHandling):

    @with_authorization(optional=True)
    def get(self, snippet_id):
        snippet = SnippetModel.query.filter_by(id=snippet_id).first()
        return snippet.as_dict, 200

    @with_authorization()
    def put(self, snippet_id):
        snippet = SnippetModel.query.filter_by(id=snippet_id).first()
        return snippet.as_dict, 200


@app.route('/')
def index():
    return 'hello world!!'


@app.route('/api/ping')
def ping():
    return jsonify({'data': 'pong'})
