from abstract.model import UserModel, User

# 主键
from app.model.model import SQLModel

id_key = "id"
# 身份证号
id_card_number_key = "id_card_number"


class UserModelImpl(SQLModel, UserModel):
    def __init__(self, inj):
        super().__init__(inj)

    def create(self) -> bool:
        return self.db.create(f"""
        create table if not exists {User.table_name} (
            {User.id_key} integer primary key autoincrement,
            {User.id_card_number_key} VARCHAR(19)
        )
        """)

    def insert(self, id_card_number: str) -> int:
        return self.db.insert(f'''
        insert into {User.table_name} (
        {User.id_card_number_key})
        values
        ({self.db.placeholder})
        ''', id_card_number)

    def query_by_id_card_number(self, id_card_number: str):
        data = self.select_1(User.table_name, User.id_card_number_key, id_card_number)
        return data and User(user_id=data[0][0], id_card_number=data[0][1])

    def delete_by_id_card_number(self, id_card_number: str) -> bool:
        return self.db.delete(f'''
        delete from {User.table_name} where {User.id_card_number_key} = {self.db.placeholder}
        ''', id_card_number)
