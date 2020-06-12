from dateutil.tz import tzutc, tzlocal

_utc = tzutc()
_local = tzlocal()


def to_utc(dt):
    return dt.astimezone(_utc)


def to_local(dt):
    return dt.astimezone(_local)
