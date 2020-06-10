from abc import abstractmethod


class Connection(object):

    @property
    def room_id(self) -> int:
        return 0

    @property
    def user_id(self) -> int:
        return 0

    @property
    def need_fan(self) -> bool:
        return False


class ConnectionPool(object):

    @abstractmethod
    def put(self, token: str, room_id: int, user_id: int, need_fan: bool):
        pass

    @abstractmethod
    def put_need_fan(self, token: str, need_fan: bool):
        pass

    @abstractmethod
    def delete(self, token: str):
        pass

    @abstractmethod
    def get(self, token: str) -> Connection:
        pass
