from functools import partial, wraps
from itertools import ifilter, imap
from operator import not_


def identity(x):
    return x


def caller(method_name, *args, **kwargs):
    def call_obj(obj):
        return getattr(obj, method_name)(*args, **kwargs)
    return call_obj


def compose(*functions):
    if not functions:
        raise ValueError("Must specify functions to compose")
    def composed(*args, **kwargs):
        fs = list(functions)
        y = fs.pop()(*args, **kwargs)
        while fs:
            f = fs.pop()
            y = f(y)
        return y
    return composed


def wrap_result(wrapper):
    return lambda f: wraps(f)(compose(wrapper, f))


negate = wrap_result(not_)


def on_items(f, d):
    return compose(dict, f, caller('items'))(d)


def map_dict(f, d):
    return on_items(partial(imap, f), d)


def filter_dict(p, d):
    return on_items(partial(ifilter, p), d)


def map_keys(f, d):
    return map_dict(lambda (k, v): (f(k), v), d)


def dichotomy(p, xs):
    return ifilter(negate(p), xs), ifilter(p, xs)
