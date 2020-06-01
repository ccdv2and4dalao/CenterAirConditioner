
class Request(object):
    def __init__(self):
        pass


class Response(object):
    def __init__(self):
        self.code = 0  # type: int


class FailedResponse(object):
    def __init__(self):
        self.data = None  # type: dict or None
