import sys
import traceback
import distutils.util
from functools import wraps

from flask import request
from flask_restful import Resource

from .models import db, UserModel


def boolean_parser(boolean):
    if isinstance(boolean, bool):
        return boolean
    if isinstance(boolean, str):
        return distutils.util.strtobool(boolean)


def error_log(log):
    '''
    use so you can visually scan for [LOG] in your output

    writes to stderr to avoid buffering / capturing / etc
    '''
    print(f'[LOG] {log}', file=sys.stderr)


def with_authorization(optional=False):
    '''
    adds authorization to a given route

    uses UnauthorizedInvalidHeaderException to communicate errors to ResourceWithErrorHandling
    '''

    def decorator(request_function):
        @wraps(request_function)
        def decorated_function(*args, **kwargs):

            request.user = None
            email_address = request.headers.get('Authorization')

            # invalid authorization case
            if not email_address and not optional:
                raise UnauthorizedInvalidHeaderException

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


class NotFoundException(BaseException):
    pass


class UnauthorizedException(BaseException):
    pass


class UnauthorizedInvalidHeaderException(UnauthorizedException):
    pass


class UnauthorizedNotShareableException(UnauthorizedException):
    pass


class UnauthorizedCannotPerformOnOwnException(UnauthorizedException):
    pass


class BadRequestException(BaseException):
    pass


class BadRequestNoDataException(BadRequestException):
    pass


class BadRequestMissingAttributeException(BadRequestException):
    pass


class BadRequestNoActionFoundException(BadRequestException):
    pass


class ResourceWithErrorHandling(Resource):
    '''
    Adds 400* and 500 handling to all resource routes
    '''

    def dispatch_request(self, *args, **kwargs):
        try:
            return super().dispatch_request(*args, **kwargs)
        except BadRequestException as error:
            return error.__class__.__name__, 400
        except UnauthorizedException as error:
            return error.__class__.__name__, 401
        except NotFoundException as error:
            return error.__class__.__name__, 404
        except BaseException as error:
            traceback.print_exc()
            error_log(error)
            return error, 500
