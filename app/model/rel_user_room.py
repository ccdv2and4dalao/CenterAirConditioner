from abstract.model import UserInRoomRelationshipModel, UserInRoomRelationship
from app.model.model import SQLModel


class UserInRoomRelationshipModelImpl(SQLModel, UserInRoomRelationshipModel):
    def create(self) -> bool:
        return self.db.create(f"""
        create table if not exists {UserInRoomRelationship.table_name} (
            {UserInRoomRelationship.user_id_key} integer,
            {UserInRoomRelationship.room_id_key} integer,
            primary key ({UserInRoomRelationship.user_id_key}, {UserInRoomRelationship.room_id_key})
        )
        """)

    def insert(self, user_id: int, room_id: int):
        return self.db.insert(f'''
        insert into {UserInRoomRelationship.table_name} (
        {UserInRoomRelationship.user_id_key},
        {UserInRoomRelationship.room_id_key})
        values
        (%s, %s)
        ''', user_id, room_id)

    def query(self, user_id: int, room_id: int) -> bool:
        return self.db.select(f'''
        select * from {UserInRoomRelationship.table_name} where
            {UserInRoomRelationship.user_id_key} = %s and {UserInRoomRelationship.room_id_key} = %s
        ''', user_id, room_id) is not None

    def query_by_room_id(self, room_id: int):
        data = self.db.select(f'''
        select {UserInRoomRelationship.user_id_key} from {UserInRoomRelationship.table_name} where
            {UserInRoomRelationship.room_id_key} = %s
        ''', room_id)
        if data is None:
            return

        return list(map(lambda tup: tup[0], data))

    def query_by_user_id(self, user_id: int):
        data = self.db.select(f'''
        select {UserInRoomRelationship.room_id_key} from {UserInRoomRelationship.table_name} where
            {UserInRoomRelationship.user_id_key} = %s
        ''', user_id)
        if data is None:
            return

        return list(map(lambda tup: tup[0], data))

    def delete(self, user_id: int, room_id: int) -> bool:
        return self.db.delete(f'''
        delete from {UserInRoomRelationship.table_name} where
            {UserInRoomRelationship.user_id_key} = %s and {UserInRoomRelationship.room_id_key} = %s
        ''', user_id, room_id)
