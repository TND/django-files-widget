from functools import partial


def curry(func, *a, **kw):
    return partial(func, *a, **kw)
