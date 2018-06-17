import sys
import traceback
from functools import wraps

from flask import request
from flask_restful import Resource

from .models import db, UserModel


def errorLog(log):
    print(f'[LOG] {log}', file=sys.stderr)


class ApiUnauthorizedException(BaseException):
    pass


def with_authorization(optional=False):
    def decorator(request_function):
        @wraps(request_function)
        def decorated_function(*args, **kwargs):

            email_address = request.headers.get('Authorization')

            # invalid authorization case
            if not email_address and not optional:
                raise ApiUnauthorizedException

            # valid authorization case
            else:
                # get or create user
                user = UserModel.query.filter_by(
                    email_address=email_address).first()
                if not user:
                    user = UserModel(email_address=email_address)
                    db.session.add(user)
                    db.session.commit()
                # continue executing reponse with user set on the request
                request.user = user
                return request_function(*args, **kwargs)

        return decorated_function
    return decorator


class ResourceWithErrorHandling(Resource):

    def dispatch_request(self, *args, **kwargs):
        try:
            super().dispatch_request(self, *args, **kwargs)
        except ApiUnauthorizedException as e:
            errorLog(f'request headers: {request.headers}')
            return 'unauthorized api request', 401
        except BaseException as e:
            traceback.print_exc()
            errorLog(e)
            return 'server error', 500
