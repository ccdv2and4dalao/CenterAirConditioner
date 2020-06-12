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

