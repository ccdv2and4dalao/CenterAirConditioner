from abc import abstractmethod

from abstract.model.model import Model


class UserInRoomRelationship:
    table_name = "user_in_room"
    # 用户id
    user_id_key = "user_id"
    # 房间id
    room_id_key = "room_id"

    def __init__(self):
        self.user_id = 0  # type: int
        self.room_id = 0  # type: int


class UserInRoomRelationshipModel(Model):
    """
    操作user_in_room表
    """

    @abstractmethod
    def create(self) -> bool:
        pass

    @abstractmethod
    def insert(self, user_id: int, room_id: int) -> bool:
        """
        :param user_id: 用户id
        :param room_id: 房间id
        :return: 插入是否成功
        """
        pass

    @abstractmethod
    def authenticate(self, user_id: str, room_id: str) -> bool:
        """
        :param user_id: 用户id
        :param room_id: 房间id
        :return: 关系是否存在
        """
        pass

    # @abstractmethod
    # def query(self, user_id: int, room_id: int) -> bool:
    #     """
    #     :param user_id: 用户id
    #     :param room_id: 房间id
    #     :return: 关系是否存在
    #     """
    #     pass

    # @abstractmethod
    # def query_by_room_id(self, room_id: int) -> List[int]:
    #     """
    #     :param room_id: 房间id
    #     :return: user.id[]或返回None
    #     """
    #     pass

    # @abstractmethod
    # def query_by_user_id(self, user_id: int) -> List[int]:
    #     """
    #     :param user_id: 用户id
    #     :return: room.id[]或返回None
    #     """
    #     pass

    @abstractmethod
    def delete(self, user_id: int, room_id: int) -> bool:
        """
        :param user_id: 用户id
        :param room_id: 房间id
        :return: 删除是否成功
        """
        pass
