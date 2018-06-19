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


class ConflictException(BaseException):
    pass


class ForbiddenException(BaseException):
    pass


def service_error_handler(service_func):

    def wrapper(*args, **kwargs):

        try:
            return service_func(*args, **kwargs)
        except BadRequestException as error:
            return error.__class__.__name__, 400
        except ForbiddenException as error:
            return error.__class__.__name__, 403
        except NotFoundException as error:
            return error.__class__.__name__, 404
        except ConflictException as error:
            return error.__class__.__name__, 409
        except BaseException as error:
            traceback.print_exc()
            error_log(error)
            return error, 500

    return wrapper


class JobsService(object):

    @service_error_handler
    def get_all_jobs(self, request):
        jobs = self._get_jobs()
        return jobs, 200

    @service_error_handler
    def post_job_answer(self, request, job_id):
        job = self._get_job(job_id)
        return job.as_dict, 200

    @service_error_handler
    def get_job_info(self, request, job_id):
        job = self._get_job(job_id)
        data = self._get_post_answer_data(request)
        job = self._set_response(job, data['response'])
        db.session.add(job)
        db.session.commit()

        job_data = job.as_dict
        job_data['status'] = 'ok'
        return job_data, 200

    def _get_jobs(self):
        jobs = [
            job.as_dict
            for job in JobModel.query.filter_by(response=None)
        ]
        if not jobs:
            raise NotFoundNoJobsAvailableException
        return jobs

    def _get_job(self, job_id):
        job = JobModel.query.filter_by(id=job_id).first()
        if not job:
            raise NotFoundJobDoesNotExistException
        return job

    def _get_post_answer_data(self, request):
        data = request.form or request.get_json()
        if not data:
            raise BadRequestNoDataException
        if not data.get('response'):
            raise BadRequestNoDataException
        return data

    def _set_response(self, job, response):
        if job.response == response:
            raise ConflictException
        if job.response:
            raise ForbiddenException
        job.response = response
        return job
