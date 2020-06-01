from proto import Response


class PingResponse(Response):
    def __init__(self, version=''):
        super().__init__()
        self.version = version  # type: str
