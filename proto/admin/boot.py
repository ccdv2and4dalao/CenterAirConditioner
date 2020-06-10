from proto import Request, Response


class AdminBootMasterRequest(Request):
    def __init__(self):
        super().__init__()
        self.jwt_token = ''  # type: str

    def bind_header(self, h):
        self.jwt_token = h['Authorization']


class AdminBootMasterResponse(Response):
    def __init__(self):
        super().__init__()
