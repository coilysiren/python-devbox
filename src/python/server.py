"""
flask server, and optional helper code
"""

import os

from flask import Flask, jsonify, request
from dotenv import load_dotenv, find_dotenv
from flask_restful import Api

from .view_helpers import (
    ResourceWithErrorHandling, with_authorization, UnauthorizedNotShareableException,
    UnauthorizedCannotPerformOnOwnException, NotFoundException, BadRequestException,
    BadRequestNoActionFoundException
)
from .models import db, SnippetModel, LikeModel, ShareModel


load_dotenv(find_dotenv())
app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/pythondevbox_v5.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
            raise NotFoundException

    @with_authorization()
    def post(self):
        ### request data parsing step ###
        data = request.get_json()
        if not data:
            raise BadRequestException
        elif not data.get('text'):
            raise BadRequestException
        data['user'] = request.user

        snippet = SnippetModel(**data)
        snippet.user.snippets_created_count += 1
        db.session.add(snippet)
        db.session.commit()
        return snippet.as_dict, 201


@api.resource('/snippets/<snippet_id>')
class ResourceSnippet(ResourceWithErrorHandling):

    def _process_snippet_request(self, snippet_id):
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
            raise NotFoundException

    @with_authorization(optional=True)
    def get(self, snippet_id):
        # _process_snippet_request is basically `get`
        # but moved into its own function so that `put` can use it also
        return self._process_snippet_request(snippet_id)

    @with_authorization()
    def put(self, snippet_id):
        # use _process_snippet_request to set request.snippet
        # it will also exit early with errors as needed
        self._process_snippet_request(snippet_id)

        ### request data parsing step ###
        data = request.get_json()
        if not data:
            raise BadRequestException
        elif not any([
            data.get(action) in [True, False]
            for action in [
                'allow_sharing',
                'liked',
                'shared'
            ]
        ]):
            raise BadRequestNoActionFoundException

        ### update actions step ###
        if data.get('allow_sharing'):
            request.snippet.shared = data.get('allow_sharing')
        if data.get('shared') in [True, False] or data.get('liked') in [True, False]:
            if not request.snippet.shared:
                raise UnauthorizedNotShareableException
            if request.snippet.user.id == request.user.id:
                raise UnauthorizedCannotPerformOnOwnException

        ### update action liked ###
        if data.get('liked') == True:
            like = LikeModel.query.filter_by(
                snippet_id=request.snippet.id,
                user_id=request.user.id,
            ).first()
            if not like:
                request.snippet.user.likes_recieved_count += 1
                db.session.add(LikeModel(
                    snippet_id=request.snippet.id,
                    user_id=request.user.id,
                ))
        elif data.get('liked') == False:
            LikeModel.query.filter_by(
                snippet_id=request.snippet.id,
                user_id=request.user.id,
            ).delete()

        ### update action shared ###
        if data.get('shared') == True:
            share = ShareModel.query.filter_by(
                snippet_id=request.snippet.id,
                user_id=request.user.id,
            ).first()
            if not share:
                request.user.snippets_shared_count += 1
                db.session.add(ShareModel(
                    snippet_id=request.snippet.id,
                    user_id=request.user.id,
                ))
        elif data.get('shared') == False:
            ShareModel.query.filter_by(
                snippet_id=request.snippet.id,
                user_id=request.user.id,
            ).delete()

        ### final steps ###
        db.session.commit()
        return request.snippet.as_dict, 200


@api.resource('/achievements')
class ResourceAchievements(ResourceWithErrorHandling):

    @with_authorization()
    def get(self):
        return request.user.achievements, 200


@app.route('/')
def index():
    return 'hello world!!'


@app.route('/api/ping')
def ping():
    return jsonify({'data': 'pong'})
