from proto import Request, Response


class AdminSetModeRequest(Request):
    def __init__(self):
        super().__init__()
        self.jwt_token = ''  # type: str
        self.mode = ''  # type: str

    def bind_dict(self, d: dict):
        if d is None:
            return
        self.mode = d['mode']

    def bind_header(self, h):
        self.jwt_token = h['Authorization']


class AdminSetModeResponse(Response):
    def __init__(self):
        super().__init__()
