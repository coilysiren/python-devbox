"""
flask server, and optional helper code
"""

import os

from flask import Flask, jsonify, request
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api


load_dotenv(find_dotenv())
app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/pythondevbox.db'
db = SQLAlchemy(app)
api = Api(app)


class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)

    @property
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class TodoResource(Resource):

    def delete(self, todo_id):
        TodoModel.query.filter_by(id=todo_id).delete()
        db.session.commit()
        return '', 204


class TodoListResource(Resource):

    def get(self):
        return [
            todo.as_dict
            for todo in TodoModel.query.all()
        ]

    def post(self):
        data = request.get_json()
        todo = TodoModel(content=data['data'])
        db.session.add(todo)
        db.session.commit()
        return '', 201


@app.route('/')
def index():
    return 'hello world!!'


@app.route('/api/ping')
def ping():
    return jsonify({'data': 'pong'})


db.create_all()
api.add_resource(TodoListResource,  '/api/todos')
api.add_resource(TodoResource,      '/api/todos/<todo_id>')
