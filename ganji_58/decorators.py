import time
import functools


def log(text=None):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            result = '{} {} {}'.format(text, f(*args, **kwargs), text)
            return result
        return wrapper
    return decorator


def time_elapse(text=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            t0 = time.time()
            result = 'call: {} {} time elapse: {} {}'.format(func.__name__, func(*args, **kwargs), time.time() - t0,
                                                             text)
            return result
        return wrapper
    return decorator


@log('****')
@time_elapse('....')
def function(x, y):
    return x * y


if __name__ == '__main__':
    print(function(4, 20))
