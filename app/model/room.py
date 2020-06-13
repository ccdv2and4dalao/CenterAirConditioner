from abstract.model import RoomModel, Room
from app.model.model import SQLModel


class RoomModelImpl(SQLModel, RoomModel):

    def create(self) -> bool:
        return self.db.create(f"""
        create table if not exists {Room.table_name} (
            {Room.id_key} integer primary key autoincrement,
            {Room.room_id_key} VARCHAR(19),
            {Room.app_key_key} VARCHAR(65)
        )""")

    def insert(self, room_id: str, app_key: str):
        return self.db.insert(f'''
        insert into {Room.table_name} (
        {Room.room_id_key}, {Room.app_key_key})
        values
        ({self.db.placeholder}, {self.db.placeholder})''', room_id, app_key)

    def query_page(self, page_size: int = 10, page_number: int = 1):
        # assuming MySQL Impl
        data = self.db.select(f'''
        select * from {Room.table_name} limit {self.db.placeholder}, {self.db.placeholder}
        ''', page_size * (page_number - 1), page_size * page_number)
        if data is None:
            return None

        return list(map(lambda d: Room(*d), data))

    def query_by_room_id(self, room_id: str):
        data = self.select_1(Room.table_name, Room.room_id_key, room_id)
        return data and Room(inc_id=data[0][0], room_id=data[0][1], app_key=data[0][2])

    def delete_by_room_id(self, room_id: str):
        return self.db.delete(f'''
        delete from {Room.table_name} where {Room.room_id_key} = {self.db.placeholder}
        ''', room_id)
