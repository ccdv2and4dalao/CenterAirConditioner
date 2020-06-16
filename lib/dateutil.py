import datetime

from dateutil.parser import parse
from dateutil.tz import tzutc, tzlocal

_utc = tzutc()
_local = tzlocal()


def to_utc(dt, format=True):
    if format:
        return dt.astimezone(_utc).strftime('%Y-%m-%d %H:%M:%S')
    else:
        return dt.astimezone(_utc)


def to_local(dt, format=True):
    if format:
        return dt.astimezone(_local).strftime('%Y-%m-%d %H:%M:%S')
    else:
        return dt.astimezone(_local)


def now(format=True):
    if format:
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        return datetime.datetime.now()


def to_rfc3339(dt: datetime.datetime):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def str_to_rfc3339(dt: str):
    return parse(dt).strftime("%Y-%m-%dT%H:%M:%SZ")
