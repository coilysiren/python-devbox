import sys
import traceback
from functools import wraps

from flask import request
from flask_restful import Resource

from .models import db, UserModel


def error_log(log):
    '''
    use so you can visually scan for [LOG] in your output

    writes to stderr to avoid buffering / capturing / etc
    '''
    print(f'[LOG] {log}', file=sys.stderr)


def with_authorization(optional=False):
    '''
    adds authorization to a given route

    uses ApiUnauthorizedException to communicate errors to ResourceWithErrorHandling
    '''

    def decorator(request_function):
        @wraps(request_function)
        def decorated_function(*args, **kwargs):

            request.user = None
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


class ApiUnauthorizedException(BaseException):
    '''custom exception so we can catch authorization errors on any resource route'''
    pass


class ResourceWithErrorHandling(Resource):
    '''
    Adds 401 and 500 handling to all resource routes

    catches ApiUnauthorizedException from with_authorization

    and catches BaseException for all other issues
    '''

    def dispatch_request(self, *args, **kwargs):
        try:
            return super().dispatch_request(*args, **kwargs)
        except ApiUnauthorizedException as error:
            error_log(f'request headers: {request.headers}')
            return 'unauthorized api request', 401
        except BaseException as error:
            traceback.print_exc()
            error_log(error)
            return 'server error', 500
