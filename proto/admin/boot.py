from proto import Request, Response


class AdminBootMasterRequest(Request):
    def __init__(self):
        super().__init__()
        self.jwt_token = ''  # type: str


class AdminBootMasterResponse(Response):
    def __init__(self):
        super().__init__()
