from pprint import pprint

from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import InstrumentedAttribute


load_dotenv(find_dotenv())
db = SQLAlchemy()


class ApiModelMixin(object):

    @property
    def as_dict(self):
        '''
        turns the current model into a dictionary, so we can turn it into a json response

        recurses down foreign keyed models so they're all turned into dicts too
        '''
        attrs = {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
        attrs['object'] = self.__class__.__tablename__
        return attrs


class UserModel(
        ApiModelMixin,
        db.Model,
):
    # universal attrs
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # local attrs
    email_address = db.Column(db.String, default=True)
    snippets_created_count = db.Column(db.Integer, default=True)
    likes_recieved_count = db.Column(db.Integer, default=True)
    snippets_shared_count = db.Column(db.Integer, default=True)
    # relationships
    snippets = db.relationship('SnippetModel', backref='user')

    @property
    def achievements(self):
        return {
            'created': self.snippets_created_count / 10,
            'liked': self.likes_recieved_count / 10,
            'shared': self.snippets_shared_count / 10,
        }

    @property
    def as_dict(self):
        attrs = super().as_dict
        attrs['achievements'] = self.achievements
        return attrs


class SnippetModel(
        ApiModelMixin,
        db.Model,
):
    # universal attrs
    __tablename__ = 'snippet'
    id = db.Column(db.Integer, primary_key=True)
    # local attrs
    shared = db.Column(db.Boolean, default=True)
    text = db.Column(db.String)
    # relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes = db.relationship("LikeModel", back_populates="snippet")
    shares = db.relationship("ShareModel", back_populates="snippet")

    @property
    def as_dict(self):
        '''
        add alias attributes, and simplified attributes to snippet json
        '''
        attrs = super().as_dict
        # relationships
        attrs['user'] = self.user.as_dict if self.user else {}
        attrs['shares'] = len(self.shares)
        attrs['likes'] = len(self.likes)
        attrs['shares_data'] = [share.as_dict for share in self.shares]
        attrs['likes_data'] = [like.as_dict for like in self.likes]
        # alias attributes
        attrs['snippetId'] = self.id
        attrs['owner'] = attrs.get('user', {}).get('email_address')
        return attrs


class ActionPerformerMixin(object):

    @property
    def as_dict(self):
        attrs = super().as_dict
        attrs['performer'] = self.user.as_dict if self.user else {}
        return attrs


class LikeModel(
        ActionPerformerMixin,
        ApiModelMixin,
        db.Model,
):
    # universal attrs
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True)
    # relationships
    snippet_id = db.Column(db.Integer, db.ForeignKey('snippet.id'))
    snippet = db.relationship("SnippetModel", back_populates="likes")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("UserModel")


class ShareModel(
        ActionPerformerMixin,
        ApiModelMixin,
        db.Model,
):
    # universal attrs
    __tablename__ = 'share'
    id = db.Column(db.Integer, primary_key=True)
    # relationships
    snippet_id = db.Column(db.Integer, db.ForeignKey('snippet.id'))
    snippet = db.relationship("SnippetModel", back_populates="shares")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("UserModel")
