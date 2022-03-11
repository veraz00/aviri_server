import sys
import traceback
import linecache
import functools

from flask import make_response, jsonify

class HttpError(Exception):
    status_code = 400
    message = ""

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

def print_exception():
    '''
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    '''
    traceback.print_stack()

def exception_handler(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HttpError as e:
            return make_response(jsonify({ "code": e.status_code, "errorMsg": e.message }), e.status_code)
        except Exception as e:
            #print_exception()
            print(traceback.format_exc())
            return make_response(jsonify({ "code": 400, "errorMsg": str(e) }), 400)
    return inner_func
