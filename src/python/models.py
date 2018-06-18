from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy


load_dotenv(find_dotenv())
db = SQLAlchemy()


class ApiModelMixin(object):

    def get_dict_attr(self, column):
        from pprint import pprint
        if column.foreign_keys:
            for foreign_key in column.foreign_keys:
                short_name = foreign_key.parent.name.strip('_id')
                foreign_model = getattr(self, short_name)
                try:
                    return {short_name: foreign_model.as_dict()}
                except BaseException:
                    return {short_name: foreign_model}
        return {column.name: getattr(self, column.name)}

    def as_dict(self):
        # the following is a tad to complicated to be a dict comprehension
        attrs = {}
        for column in self.__table__.columns:
            attrs.update(self.get_dict_attr(column))
        attrs['object'] = self.__class__.__name__.strip('Model')
        return attrs


class UserModel(
        db.Model,
        ApiModelMixin,
):
    # universal attrs
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # local attrs
    email_address = db.Column(db.String, default=True)
    # relationships
    snippets = db.relationship('SnippetModel', backref='user', lazy=True)


class SnippetModel(
        db.Model,
        ApiModelMixin,
):
    # universal attrs
    __tablename__ = 'snippet'
    id = db.Column(db.Integer, primary_key=True)
    # local attrs
    shared = db.Column(db.Boolean, default=True)
    text = db.Column(db.String)
    # relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class ActionModel(
        db.Model,
        ApiModelMixin,
):
    # universal attrs
    __tablename__ = 'action'
    id = db.Column(db.Integer, primary_key=True)


class AcheievementModel(
        db.Model,
        ApiModelMixin,
):
    # universal attrs
    __tablename__ = 'achievement'
    id = db.Column(db.Integer, primary_key=True)
