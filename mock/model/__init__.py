from typing import List

from abstract.model import UserInRoomRelationshipModel, UserModel, User, RoomModel, Room


class MockUserInRoomRelationshipModel(UserInRoomRelationshipModel):
    def authenticate(self, user_id: str, room_id: str) -> bool:

        if room_id == '101' and user_id == '111111202002023333':
            return True
        return False

    def why(self):
        pass

    def create(self) -> bool:
        pass

    def insert(self, user_id: int, room_id: int) -> bool:
        pass

    def query(self, user_id: int, room_id: int) -> bool:
        if user_id == 1 and room_id == 2:
            return True
        return False

    def query_by_room_id(self, room_id: int) -> List[int]:
        pass

    def query_by_user_id(self, user_id: int) -> List[int]:
        pass

    def delete(self, user_id: int, room_id: int) -> bool:
        pass

    def __init__(self):
        pass


class MockUserModel(UserModel):
    def create(self) -> bool:
        pass

    def insert(self, id_card_number: str) -> int:
        pass

    def query_by_id_card_number(self, id_card_number: str):
        if id_card_number == '111111202002023333':
            user = User()
            user.id = 1
            user.id_card_number = id_card_number
            return user
        return

    def delete_by_id_card_number(self, id_card_number: str) -> bool:
        pass

    def why(self):
        pass


class MockRoomModel(RoomModel):
    def create(self) -> bool:
        pass

    def insert(self, room_id: str) -> int:
        pass

    def query_by_room_id(self, room_id: str):
        if room_id == '101':
            room = Room()
            room.id = 2
            room.room_id = room_id
            return room
        return

    def delete_by_room_id(self, room_id: str) -> bool:
        pass

    def why(self):
        pass
