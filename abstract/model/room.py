from abc import abstractmethod
from typing import List, Optional

from abstract.model.model import Model


class Room:
    table_name = "room"
    # 主键
    id_key = "id"
    # 房间号
    room_id_key = "room_id"
    # 房间的app key
    app_key_key = "app_key"
    # 房间的特权级
    room_privilege_key = "room_privilege"

    def __init__(self, inc_id=0, room_id='', app_key='', privilege=0):
        self.id = inc_id  # type: int
        self.room_id = room_id  # type: str
        self.app_key = app_key  # type: str
        self.room_privilege = privilege  # type: int


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

    @abstractmethod
    def query_page(self, page_size: int = None, page_number: int = None) -> List[Room]:
        """
        :param page_size: 页大小
        :param page_number: 页偏移
        :return: List[Room]或返回None
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

    @abstractmethod
    def query_by_id(self, _id: int) -> Optional[Room]:
        pass
