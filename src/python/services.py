import sys
import traceback
import distutils.util
from functools import wraps

from flask import request
from flask_restful import Resource

from .models import db, JobModel


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


class NotFoundException(BaseException):
    pass


class NotFoundNoJobsAvailableException(NotFoundException):
    pass


class NotFoundJobDoesNotExistException(NotFoundException):
    pass


class BadRequestException(BaseException):
    pass


class BadRequestNoDataException(BadRequestException):
    pass


class BadRequestMissingAttributeException(BadRequestException):
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
        except NotFoundException as error:
            return error.__class__.__name__, 404
        except BaseException as error:
            traceback.print_exc()
            error_log(error)
            return error, 500


class JobsService(object):

    @classmethod
    def get_all_jobs(cls, request):
        return '', 200

    @classmethod
    def post_job_answer(cls, request, job_id):
        return '', 200

    @classmethod
    def get_job_info(cls, request, job_id):
        return '', 200
