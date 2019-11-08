import functools
import logging

# Get an instance of a logger
from django.http import Http404
from django.shortcuts import render

logger = logging.getLogger(__name__)


def view_status_logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ex_args = ""
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            logging.exception('Errors happened')
            ex_args = e.args
        else:
            return res
        kwargs['context'] = {'msg': ex_args}
        kwargs['template_name'] = 'access_restrictions/internal_server_error.html'
        print(args, kwargs)
        return render(*args, **kwargs)

    return wrapper


def class_status_logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            logging.error(e.args)
            ex_args = e.args
            raise Http404("Query error occurred.", e.args)
        return res

    return wrapper
