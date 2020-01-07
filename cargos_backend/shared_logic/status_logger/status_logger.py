import functools
import logging

# Get an instance of a logger
from django.http import Http404
from django.shortcuts import render

# logger = logging.getLogger("status_logger")
# print(logger)

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s %(message)s',
    filename='logs/logs.log', )


def view_status_logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ex_args = ""
        try:
            res = func(*args, **kwargs)
        # except forms.ValidationError as ve:
        #     raise forms.ValidationError(ve)
        except Exception as e:
            # logging.exception('~' * 30 + 'Errors happened' + 30 * '~')
            logger.exception('~' * 30 + 'Errors happened' + 30 * '~')
            ex_args = e
        else:
            return res
        kwargs['context'] = {'msg': ex_args}
        kwargs['template_name'] = 'access_restrictions/internal_server_error.html'
        return render(*args, **kwargs)

    return wrapper


def class_status_logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        # except ValidationError as ve:
        #     raise ValidationError(ve)
        except Exception as e:
            logging.error(e.args)
            ex_args = e.args
            raise Http404("Query error occurred.", e.args)
        return res

    return wrapper
