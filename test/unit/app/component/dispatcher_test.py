import unittest
from random import randint
from time import sleep

from app.component import QueueDispatcher, QueueDispatcherWithThreadPool


def dispatcher_schedule_successfully(_, tag):
    sleep(randint(3, 6) / 10)
    print(f'{tag} bye')


def dispatcher_schedule_failed(_, tag):
    print(f'{tag} poped')


class DispatcherFunctionTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def basic_main(self, target_dispatcher):
        qd = target_dispatcher(fallback_threshold=30)
        qd.on_pop(dispatcher_schedule_successfully)
        qd.on_fallback(dispatcher_schedule_failed)
        qd.boot_up()
        for i in range(10):
            sleep(0.1)
            qd.push(None, str(i))
            print(f'push {i}')
        # qd.shut_down(0)
        # sleep(1)
        # qd.boot_up()
        # sleep(2)
        # qd.shut_down()
        sleep(1.5)
        qd.shut_down()
        self.assertTrue(qd.waiting_queue.qsize() == 0)

    def test_basic_QueueDispatcher(self):
        self.basic_main(QueueDispatcher)

    def test_basic_QueueDispatcherWithThreadPool(self):
        self.basic_main(QueueDispatcherWithThreadPool)
