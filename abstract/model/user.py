from abc import abstractmethod

from abstract.model.model import Model


class User:
    table_name = "user"
    # 主键
    id_key = "id"
    # 身份证号
    id_card_number_key = "id_card_number"

    def __init__(self):
        self.id = 0  # type: int
        self.id_card_number = ''  # type: str


class UserModel(Model):
    """
    操作user表
    """

    @abstractmethod
    def create(self) -> bool:
        pass

    @abstractmethod
    def insert(self, id_card_number: str) -> int:
        """
        :param id_card_number: 用户身份证号码
        :return: user.id或返回None
        """
        pass

    # @abstractmethod
    # def query(self, user_id: int):
    #     pass

    @abstractmethod
    def query_by_id_card_number(self, id_card_number: str) -> User:
        """
        :param id_card_number: 用户身份证号码
        :return: user或返回None
        """
        pass

    # @abstractmethod
    # def delete(self, user_id: int):
    #     pass

    @abstractmethod
    def delete_by_id_card_number(self, id_card_number: str) -> bool:
        """
        :param id_card_number: 用户身份证号码
        :return: 删除是否成功
        """
        pass
