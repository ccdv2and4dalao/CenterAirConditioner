from abstract.model import RoomModel, Room
from app.model.model import SQLModel


class RoomModelImpl(SQLModel, RoomModel):

    def create(self) -> bool:
        return self.db.create(f"""
        create table if not exists {Room.table_name} (
            {Room.id_key} integer autoincrement primary key,
            {Room.room_id_key} VARCHAR(19),
            {Room.app_key_key} VARCHAR(65)
        )""")

    def insert(self, room_id: str, app_key: str):
        return self.db.insert(f'''
        insert into {Room.table_name} (
        {Room.room_id_key}, {Room.app_key_key})
        values
        (%s, %s)''', room_id, app_key)

    def query_by_room_id(self, room_id: str):
        data = self.db.select(f'''
        select * from {Room.table_name} where {Room.room_id_key} = %s
        ''', room_id)
        if data is None:
            return None

        assert (len(data) == 1)
        return Room(inc_id=data[0], room_id=data[1], app_key=data[2])

    def delete_by_room_id(self, room_id: str):
        return self.db.delete(f'''
        delete from {Room.table_name} where {Room.room_id_key} = %s
        ''', room_id)
