from proto import Request, Response


class AdminGetConnectedSlavesRequest(Request):
    def __init__(self):
        super().__init__()
        self.jwt_token = ''  # type: str
        self.page_number = 0  # type: int
        self.page_size = 0  # type: int

    def bind_dict(self, d: dict):
        if d is None:
            return
        self.page_number = d['page_number']
        self.page_size = d['page_size']

    def bind_header(self, h):
        self.jwt_token = h['Authorization']


class AdminGetConnectedSlavesResponse(Response):
    def __init__(self):
        super().__init__()
