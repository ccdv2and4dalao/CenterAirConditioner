import unittest

from lib.serializer import JSONSerializer
from proto import Response
from proto.connection import ConnectionResponse


class JSONSerializerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.s = JSONSerializer()

    def tearDown(self) -> None:
        pass

    def test_serialize_basic_response(self):
        resp = Response()
        self.assertEqual(self.s.serialize(resp), '{"code": 0}')

    def test_serialize_inherited_response(self):
        resp = ConnectionResponse()
        self.assertEqual(self.s.serialize(resp),
                         '{"code": 0, "default_temperature": 0.0, "metric_delay": 0, "update_delay": 0, "mode": ""}')
