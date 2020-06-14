from proto import Request, Response

class AdminSetUpdateDelayRequest(Request):
    def __init__(self):
        super().__init__()
        self.delay = 0 # type: int
        self.jwt_token = '' # type: str

    def bind_header(self, h):
        self.jwt_token = h['Authorization']


class AdminSetUpdateDelayResponse(Response):
    def __init__(self):
        super().__init__()
