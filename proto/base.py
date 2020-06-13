import enum


class Request(object):
    def __init__(self):
        self.label = 0  # type: int
        self.room_id = '' # type: str
        self.timestamp = 0 # type: int

    def bind_dict(self, d: dict):
        if d is None:
            return
        self.label = d.get('label', 0)
        self.room_id = d.get('room_id', '')
        self.timestamp = d.get('timestamp', 0)

    def bind_header(self, h):
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


class ServiceCode(enum.Enum):
    NotFound = 1
    ConflictMode = 2
    InvalidModeValue = 3
    InvalidFanSpeedValue = 4
    WrongPassword = 5
    AuthJWTFailed = 6
    DatabaseError = 7
    InvalidTargetTemperature = 8

class DatabaseError(FailedResponse):
    def __init__(self, data: str):
        super().__init__(ServiceCode.DatabaseError.value, data)


class NotFound(FailedResponse):
    def __init__(self, data: str):
        super().__init__(ServiceCode.NotFound.value, data)


class ConflictMode(FailedResponse):
    def __init__(self, data: str):
        super().__init__(ServiceCode.ConflictMode.value, data)


class InvalidModeValue(FailedResponse):
    def __init__(self, data: str):
        super().__init__(ServiceCode.InvalidModeValue.value, data)


class InvalidFanSpeedValue(FailedResponse):
    def __init__(self, data: str):
        super().__init__(ServiceCode.InvalidFanSpeedValue.value, data)


class WrongPassword(FailedResponse):
    def __init__(self):
        super().__init__(ServiceCode.WrongPassword.value)


class AuthJWTFailed(FailedResponse):
    def __init__(self, data: str):
        super().__init__(ServiceCode.AuthJWTFailed.value, data)

class InvalidTargetTemperature(FailedResponse):
    def __init__(self, data: str):
        super().__init__(ServiceCode.InvalidTargetTemperature.value, data)
