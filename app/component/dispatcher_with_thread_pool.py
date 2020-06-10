import queue
import time
from threading import Lock
from threading import Thread
from typing import List

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
        super().__init__(self._schedule, daemonic=True)

        self.active_size = active_size
        self.fallback_threshold = fallback_threshold
        self.control_precision = 0.1
        # self.block_timeout = 0.2

        self.waiting_queue = queue.Queue()

        # self.thread_pool = ThreadPoolExecutor(max_workers=active_size)
        self.thread_pool = []  # type: List[Thread]

    def shut_down(self, timeout=0):
        '''
        暂停线程
        '''
        # self.thread_pool.shutdown(wait=False)
        ddl = time.perf_counter() + timeout
        for t in self.thread_pool:
            t.join(ddl - time.perf_counter())
        super().shut_down(ddl - time.perf_counter())

    def push(self, opaque, tag):
        self.waiting_queue.put((opaque, tag))  # append is atomic

    def _schedule(self):
        for i in range(self.active_size):
            t = Thread(target=self._pop_guard, daemon=True)
            t.start()
            self.thread_pool.append(t)

        while True:
            if self.waiting_queue.qsize() > self.fallback_threshold:
                self.on_fallback_func(*self.waiting_queue.get())
            else:
                time.sleep(self.control_precision)
            # try:
            #     while True:
            #         if self.active_count.value >= self.active_size:
            #             time.sleep(self.control_precision)
            #         else:
            #             self.thread_pool.submit(self._pop_guard, self.waiting_queue.get(timeout=self.block_timeout))
            # except queue.Empty:
            #     while self.waiting_queue.qsize() > self.fallback_threshold:
            #         self.on_fallback_func(*self.waiting_queue.get())

    def _pop_guard(self):
        while True:
            self.on_pop_func(*self.waiting_queue.get())
