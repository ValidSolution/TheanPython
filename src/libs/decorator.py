import time
import threading


def print_run_time(func):
    def wrapper(*args, **kw):
        start = time.time()
        res = func(*args, **kw)
        end = time.time()
        print('[%s]: %.2fms' % (func.__name__, (end - start) * 1000))
        return res
    return wrapper


def synchronized(func):
    func.__lock__ = threading.Lock()

    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return lock_func
