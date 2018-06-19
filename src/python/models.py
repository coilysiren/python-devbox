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
        '''
        attrs = {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
        attrs['object'] = self.__class__.__tablename__
        return attrs


class JobModel(
        ApiModelMixin,
        db.Model,
):
    # universal attrs
    __tablename__ = 'job'
    id = db.Column(db.Integer, primary_key=True)
    # local attrs
    question = db.Column(db.String, default='What is your name?')
    response = db.Column(db.String)

    @property
    def as_dict(self):
        data = super().as_dict
        if self.response:
            data['status'] = 'closed'
        else:
            data['status'] = 'open'
        return data
