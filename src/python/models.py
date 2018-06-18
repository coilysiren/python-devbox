from pprint import pprint

from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import InstrumentedAttribute


load_dotenv(find_dotenv())
db = SQLAlchemy()


class ApiModelMixin(object):

    def get_dict_attr(self, column):
        '''
        turns sql columns into dictionary attributes, given:
         - foreign keys
         - normal attributes (strings, bools, etc)
        '''
        # if this column is a set of foreign keys
        if column.foreign_keys:
            # get all those foreign keys
            for foreign_key in column.foreign_keys:
                short_name = foreign_key.parent.name.strip('_id')
                foreign_model = getattr(self, short_name)
                # and return their "short_name" with their attrs as a dict
                if foreign_model:
                    return {short_name: foreign_model.as_dict}
                # or nothing, if theres no valid foreign model
                else:
                    return {}
        # otherwise its a regular attr, so we return that
        else:
            return {column.name: getattr(self, column.name)}

    @property
    def as_dict(self):
        '''
        turns the current model into a dictionary, so we can turn it into a json response

        recurses down foreign keyed models so they're all turned into dicts too
        '''
        attrs = {}
        for column in self.__table__.columns:
            attrs.update(self.get_dict_attr(column))
        attrs['object'] = self.__class__.__tablename__
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
    snippets = db.relationship('SnippetModel', backref='user')


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
    likes = db.relationship("LikeModel", back_populates="snippet")
    shares = db.relationship("ShareModel", back_populates="snippet")

    @property
    def as_dict(self):
        '''
        add alias attributes, and simplified attributes to snippet json
        '''
        attrs = super().as_dict
        # alias attributes
        attrs['snippetId'] = self.id
        attrs['owner'] = attrs.get('user', {}).get('email_address')
        # simplified attributes
        attrs['shares'] = len(self.shares)
        attrs['likes'] = len(self.likes)
        return attrs


class LikeModel(
        db.Model,
        ApiModelMixin,
):
    # universal attrs
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True)
    # relationships
    snippet_id = db.Column(db.Integer, db.ForeignKey('snippet.id'))
    snippet = db.relationship("SnippetModel", back_populates="likes")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class ShareModel(
        db.Model,
        ApiModelMixin,
):
    # universal attrs
    __tablename__ = 'share'
    id = db.Column(db.Integer, primary_key=True)
    # relationships
    snippet_id = db.Column(db.Integer, db.ForeignKey('snippet.id'))
    snippet = db.relationship("SnippetModel", back_populates="shares")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class AcheievementModel(
        db.Model,
        ApiModelMixin,
):
    # universal attrs
    __tablename__ = 'achievement'
    id = db.Column(db.Integer, primary_key=True)
