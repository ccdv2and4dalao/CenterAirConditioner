from proto import Request, Response


class AdminLoginRequest(Request):
    def __init__(self):
        super().__init__()
        self.admin_token = ''  # type: str

    def bind_dict(self, d: dict):
        if d is None:
            return
        self.admin_token = d['admin_token']


class AdminLoginResponse(Response):
    def __init__(self, jwt_token=''):
        super().__init__()
        self.jwt_token = jwt_token  # type: str
