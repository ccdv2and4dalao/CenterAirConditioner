from abc import abstractmethod

from abstract.model.model import Model


class Room:
    table_name = "room"
    # 主键
    id_key = "id"
    # 房间号
    room_id_key = "room_id"
    # 房间的app key
    app_key_key = "app_key"

    def __init__(self):
        self.id = 0  # type: int
        self.room_id = ''  # type: str
        self.app_key = ''  # type: str


class RoomModel(Model):
    """
    操作room表
    """

    @abstractmethod
    def create(self) -> bool:
        pass

    @abstractmethod
    def insert(self, room_id: str, app_key: str) -> int:
        """
        :param room_id: 房间号（墙上的名字）
        :param app_key: 房间的app key
        :return: room.id或返回None
        """
        pass

    # @abstractmethod
    # def query(self, room_id: int):
    #     pass

    @abstractmethod
    def query_by_room_id(self, room_id: str) -> Room:
        """
        :param room_id: 房间号（墙上的名字）
        :return: room或返回None
        """
        pass

    # @abstractmethod
    # def delete(self, room_id: int):
    #     pass

    @abstractmethod
    def delete_by_room_id(self, room_id: str) -> bool:
        """
        :param room_id: 房间号（墙上的名字）
        :return: 删除是否成功
        """
        pass
