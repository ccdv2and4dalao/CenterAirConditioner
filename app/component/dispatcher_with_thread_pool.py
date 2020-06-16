import queue
import time
from threading import Lock, Thread, Event

from abstract.component.connection_pool import ConnectionPool
from abstract.consensus import FanSpeed
from app.component.basic_thread_dispatcher import BasicThreadDispatcher


class AtomicInteger(object):

    def __init__(self, value: int):
        self._value = value
        self.count_lock = Lock()

    @property
    def value(self):
        self.count_lock.acquire()
        value = self._value
        self.count_lock.release()
        return value

    @value.setter
    def value(self, v: int):
        self.count_lock.acquire()
        self._value = v
        self.count_lock.release()

    def inc(self):
        self.count_lock.acquire()
        self._value += 1
        self.count_lock.release()

    def dec(self):
        self.count_lock.acquire()
        self._value -= 1
        self.count_lock.release()


class QueueDispatcherWithThreadPool(BasicThreadDispatcher):

    def __init__(self, active_size=3, fallback_threshold=30):
        super(BasicThreadDispatcher, self).__init__(
            self._schedule, daemonic=True)

        self.active_size = active_size
        self.fallback_threshold = fallback_threshold
        self.control_precision = 0.1

        self.waiting_queue = queue.Queue(maxsize=fallback_threshold)

    def is_idle(self) -> bool:
        return self.waiting_queue.empty()

    def boot_up(self, timeout=0):
        for i in range(self.active_size):
            t = Thread(target=self._pop_guard, daemon=True)
            t.start()

    def push(self, opaque, tag):
        self.waiting_queue.put((opaque, tag))  # append is atomic

    def _schedule(self):
        while self.waiting_queue.qsize() > self.fallback_threshold:
            self.on_fallback_func(*self.waiting_queue.get())
        time.sleep(self.control_precision)

    def _pop_guard(self, *args):
        while True:
            self.on_pop_func(*self.waiting_queue.get())


class PriQueueDispatcherWithThreadPool(BasicThreadDispatcher):

    def __init__(self, active_size=3, fallback_threshold=30):
        super(BasicThreadDispatcher, self).__init__(
            self._schedule, daemonic=True)

        self.active_size = active_size
        self.fallback_threshold = fallback_threshold
        self.control_precision = 0.1

        self.waiting_queue = queue.PriorityQueue()

    def is_idle(self) -> bool:
        return self.waiting_queue.empty()

    def boot_up(self, timeout=0):
        for i in range(self.active_size):
            t = Thread(target=self._pop_guard, daemon=True)
            t.start()

    def weighing_function(self, opaque) -> float:
        #room_id = opaque["room_id"]
        #room_info = self.connection_pool.get(room_id)
        #room_privilege = room_info.room_privilege
        #pri_coe = 100
        speed_coe = {
            FanSpeed.Low: 3,
            FanSpeed.Mid: 2,
            FanSpeed.High: 1,
            FanSpeed.Low.value: 3,
            FanSpeed.Mid.value: 2,
            FanSpeed.High.value: 1
        }
        weight = speed_coe[opaque['speed_fan']]
        return weight

    def push(self, opaque, tag):
        pri = self.weighing_function(opaque)
        self.waiting_queue.put((pri, (opaque, tag)))  # append is atomic

    def _schedule(self):
        while self.waiting_queue.qsize() > self.fallback_threshold:
            pri, tp = self.waiting_queue.get()
            self.on_fallback_func(*tp)
        time.sleep(self.control_precision)

    def _pop_guard(self, *args):
        while True:
            pri, tp = self.waiting_queue.get()
            self.on_pop_func(*tp)


class SuspendableQueueDispatcherWithThreadPool(QueueDispatcherWithThreadPool):

    def __init__(self, active_size=3, fallback_threshold=30):
        super(BasicThreadDispatcher, self).__init__(
            self._schedule, daemonic=True)

        self.active_size = active_size
        self.fallback_threshold = fallback_threshold
        self.control_precision = 0.1

        self.waiting_queue = queue.Queue()
        self.thread_pool = []

    def boot_up(self, timeout=0):
        for i in range(self.active_size - len(self.thread_pool)):
            e = Event()
            t = Thread(target=self._pop_guard, args=(e,), daemon=True)
            t.start()
            self.thread_pool.append((e, t))

    def pause(self, timeout=0):
        """
        暂停线程
        """
        ddl = time.perf_counter() + timeout

        for (e, t) in self.thread_pool:
            e.set()
            t.join(ddl - time.perf_counter())

        self.thread_pool.clear()
        super(BasicThreadDispatcher, self).shut_down(ddl - time.perf_counter())

    def _pop_guard(self, context: Event):
        while True:
            try:
                while True:
                    self.on_pop_func(
                        *self.waiting_queue.get(timeout=self.control_precision))
            except queue.Empty:
                if context.is_set():
                    return
