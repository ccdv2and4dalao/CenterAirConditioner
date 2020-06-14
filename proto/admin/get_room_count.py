from proto import Request, Response


class AdminGetRoomCountRequest(Request):
    def __init__(self):
        super().__init__()
        self.jwt_token = ''  # type: str

    def bind_header(self, h):
        self.jwt_token = h['Authorization']


class AdminGetRoomCountResponse(Response):
    def __init__(self, data=0):
        super().__init__()
        self.data = data  # type: int
