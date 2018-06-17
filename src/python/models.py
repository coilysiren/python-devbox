from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy


load_dotenv(find_dotenv())
db = SQLAlchemy()


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
    # universal attrs
    id = db.Column(db.Integer, primary_key=True)
    # local attrs
    email_address = db.Column(db.Boolean, default=True)
    # relationships
    snippets = db.relationship('SnippetModel', backref='user', lazy=True)


class SnippetModel(
        db.Model,
        ApiModelMixin,
):
    # universal attrs
    id = db.Column(db.Integer, primary_key=True)
    # local attrs
    shared = db.Column(db.Boolean, default=True)
    text = db.Column(db.String)
    # relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))


class ActionModel(
        db.Model,
        ApiModelMixin,
):
    # universal attrs
    id = db.Column(db.Integer, primary_key=True)


class AcheievementModel(
        db.Model,
        ApiModelMixin,
):
    # universal attrs
    id = db.Column(db.Integer, primary_key=True)
