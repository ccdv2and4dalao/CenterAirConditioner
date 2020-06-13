from abc import abstractmethod


class Connection(object):

    @property
    def room_id(self) -> int:
        return 0

    @property
    def user_id(self) -> int:
        return 0

    @property
    def current_temperature(self) -> float:
        return 0.0

    @property
    def need_fan(self) -> bool:
        return False

    @property
    def fan_speed(self) -> str:
        return ''


class ConnectionPool(object):

    @abstractmethod
    def put(self, room_id: int, user_id: int, need_fan: bool):
        pass

    @abstractmethod
    def put_need_fan(self, room_id: int, need_fan: bool):
        pass

    @abstractmethod
    def delete(self, room_id: int):
        pass

    @abstractmethod
    def get(self, room_id: int) -> Connection:
        pass
