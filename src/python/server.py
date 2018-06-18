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
        # add all shared snippets
        snippets = [
            snippet.as_dict
            for snippet in SnippetModel.query.filter_by(shared=True)
        ]
        # add unshared snippets for authorized user
        if request.user:
            snippets += [
                snippet.as_dict
                for snippet in SnippetModel.query.filter_by(
                    shared=False, user=request.user)
            ]
        ### response step ###
        if snippets:
            return snippets, 200
        else:
            return [], 404

    @with_authorization()
    def post(self):
        ### request data parsing step ###
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

    def _snippet_resource_response(self, snippet_id):
        ### snippet retrieval step ###
        # look for shared for a shared snippet with this id
        snippet = SnippetModel.query.filter_by(
            id=snippet_id, shared=True).first()
        # otherwise, look for an unshared snippet with this id
        # if there is an authorized user on this request
        if not snippet and request.user:
            snippet = SnippetModel.query.filter_by(
                id=snippet_id, shared=False, user=request.user,
            ).first()

        ### response step ###
        if snippet:
            # `put` needs request.snippet, `get` doesnt
            request.snippet = snippet
            return snippet.as_dict, 200
        else:
            return 'not found', 404

    @with_authorization(optional=True)
    def get(self, snippet_id):
        return self._snippet_resource_response(snippet_id)

    @with_authorization()
    def put(self, snippet_id):
        # use _snippet_resource_response to set request.snippet
        # and do the update action before you return the response
        response = self._snippet_resource_response(snippet_id)

        ACTIONS = [
            'allow_sharing',
            'like',
            'share'
        ]

        ### request data parsing step ###
        data = request.get_json()
        if not data:
            return 'PUT data required', 400
        elif not any([
            data.get(action)
            for action in ACTIONS
        ]):
            return f'PUT requires one of {ACTIONS}', 400

        ### update actions step ###
        # note! these are purposefully not elifs
        if data.get('allow_sharing'):
            request.snippet.shared = data.get('allow_sharing')
        if data.get('like'):
            pass
        if data.get('share'):
            pass
        db.session.commit()

        return response


@app.route('/')
def index():
    return 'hello world!!'


@app.route('/api/ping')
def ping():
    return jsonify({'data': 'pong'})
