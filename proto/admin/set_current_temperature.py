from proto import Request, Response


class AdminSetCurrentTemperatureRequest(Request):
    def __init__(self):
        super().__init__()
        self.jwt_token = ''  # type: str
        self.target = 0.0  # type: float

    def bind_dict(self, d: dict):
        if d is None:
            return
        self.target = d['target']

    def bind_header(self, h):
        self.jwt_token = h['Authorization']


class AdminSetCurrentTemperatureResponse(Response):
    def __init__(self):
        super().__init__()
