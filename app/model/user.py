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
            {User.id_key} integer autoincrement primary key,
            {User.id_card_number_key} VARCHAR(19),
        )
        """)

    def insert(self, id_card_number: str) -> int:
        return self.db.insert(f'''
        INSERT INTO {User.table_name} (
        {User.id_card_number_key})
        VALUES
        (%s)
        ''', id_card_number)

    def query_by_id_card_number(self, id_card_number: str):
        data = self.db.select(f'''
        SELECT * FROM {User.table_name} WHERE {User.id_card_number_key} = %s
        ''', id_card_number)
        if data is None:
            return None

        assert (len(data) == 1)
        return User(user_id=data[0], id_card_number=data[1])

    def delete_by_id_card_number(self, id_card_number: str) -> bool:
        return self.db.delete(f'''
        DELETE FROM {User.table_name} WHERE {User.id_card_number_key} = %s
        ''', id_card_number)
