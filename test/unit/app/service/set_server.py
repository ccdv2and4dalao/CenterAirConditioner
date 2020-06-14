import unittest
from abstract.service.admin import AdminSetUpdateDelayService, AdminSetMetricDelayService
from abstract.component.air import MasterAirCond
from proto.admin.set_update_delay import AdminSetUpdateDelayRequest
from proto.admin.set_metric_delay import AdminSetMetricDelayRequest
from app.server_builder import ServerBuilder

class SetServerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.builder = ServerBuilder(use_test_database=True)
        self.builder.build_base()
        self.builder.build_model()
        self.builder.build_service()
        self.inj = self.builder.injector

    def test(self):
        up = self.inj.require(AdminSetUpdateDelayService)
        me = self.inj.require(AdminSetMetricDelayService)
        ac = self.inj.require(MasterAirCond)
        

        r = AdminSetUpdateDelayRequest()
        r.delay = 50
        up.serve(r)

        r = AdminSetMetricDelayRequest()
        r.delay = 25
        me.serve(r)

        self.assertEqual(50, ac.update_delay)
        self.assertEqual(25, ac.metric_delay)


if __name__ == '__main__':
    t = SetServerTest()
    t.setUp()
    t.test()