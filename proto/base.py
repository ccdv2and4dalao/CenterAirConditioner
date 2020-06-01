class Request(object):
    def __init__(self):
        pass

    def bind_dict(self, d: dict):
        pass


class Response(object):
    def __init__(self, code: int = 0):
        self.code = code  # type: int

    def to_json(self, serialize):
        return serialize(self)


class FailedResponse(Response):
    def __init__(self, code: int = 0, data=None):
        super().__init__(code)
        self.data = data  # type: dict or None


class NotFound(FailedResponse):
    def __init__(self, data: str):
        super().__init__(1, data)
