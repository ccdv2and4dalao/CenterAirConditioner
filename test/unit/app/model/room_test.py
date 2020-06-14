import unittest
from lib.injector import Injector
from app.model import RoomModelImpl, UserModelImpl, UserInRoomRelationshipModelImpl
from abstract.model import Room, User
from app.database import BaseSQLDatabaseImpl
from abstract.database import SQLDatabase
from sys import argv
from lib.bcrypt_password_verifier import BCryptPasswordVerifier
from app.server_builder import ServerBuilder

class RoomModelTest(unittest.TestCase):
    def setUp(self):
        self.builder = ServerBuilder()
        self.builder.build()
        self.inj = self.builder.injector
        self.db = self.inj.require(SQLDatabase)
        self.db.connect()

    def insert_data(self):
        rm = RoomModelImpl(self.inj)
        um = UserModelImpl(self.inj)
        uirm = UserInRoomRelationshipModelImpl(self.inj)

        r1 = Room(room_id='room_test_1')
        u1 = User(id_card_number='user_test_1')
        r1id = rm.insert(r1.room_id, r1.app_key)
        u1id = um.insert(u1.id_card_number)
        uirm.insert(u1id, r1id)

        r2 = Room(room_id='room_test_2', app_key='room_test_2')
        u2 = User(id_card_number='user_test_2')
        r2id = rm.insert(r2.room_id, r2.app_key)
        u2id = um.insert(u2.id_card_number)
        uirm.insert(u2id, r2id)

    def insert_data2(self):
        rm = RoomModelImpl(self.inj)
        um = UserModelImpl(self.inj)
        uirm = UserInRoomRelationshipModelImpl(self.inj)
        pw = BCryptPasswordVerifier(self.inj)

        r3 = Room(room_id='room_test_3')
        u3 = User(id_card_number='user_test_3')
        r3id = rm.insert(r3.room_id, pw.create(r3.room_id))
        u3id = um.insert(u3.id_card_number)
        uirm.insert(u3id, r3id)

        r4 = Room(room_id='room_test_4', app_key='room_test_4')
        u4 = User(id_card_number='user_test_4')
        r4id = rm.insert(r4.room_id, pw.create('room_test_4'))
        u4id = um.insert(u4.id_card_number)
        uirm.insert(u4id, r4id)

if __name__ == '__main__':
    rmt = RoomModelTest()
    rmt.setUp()
    rmt.insert_data2()