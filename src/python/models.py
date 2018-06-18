from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy


load_dotenv(find_dotenv())
db = SQLAlchemy()


class ApiModelMixin(object):

    def get_dict_attr(self, column):
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
        # the following doesnt work perfectly as a dict comprehension
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
