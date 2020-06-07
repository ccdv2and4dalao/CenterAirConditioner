from functools import *


def compose2(f, g):
    return lambda *a, **kw: f(g(*a, **kw))


def compose(*fs):
    return reduce(compose2, fs)


def compose_(*fs):
    return reduce(compose2, reversed(fs))
