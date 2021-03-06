﻿import time
from queue import Queue, PriorityQueue
from threading import Thread, Lock

from abstract.component.connection_pool import ConnectionPool
from abstract.consensus import FanSpeed
from app.component.basic_thread_dispatcher import BasicThreadDispatcher


class QueueDispatcher(BasicThreadDispatcher):
    def __init__(self, active_size=3, fallback_threshold=30):
        super().__init__(self._schedule)
        self.waiting_queue = Queue()
        self.active_size = active_size
        self.active_count = 0
        self.count_lock = Lock()
        self.fallback_threshold = fallback_threshold

    def push(self, opaque, tag):
        self.waiting_queue.put({'opaque': opaque, 'tag': tag})  # append is atomic

    def _schedule(self):
        if not self.waiting_queue.empty():
            while self.waiting_queue.qsize() > self.fallback_threshold:
                last = self.waiting_queue.get()
                self.on_fallback_func(last['opaque'], last['tag'])

            if self.active_count < self.active_size:
                self.__dispatch_one()

    def __dispatch_one(self):
        with self.count_lock:
            self.active_count += 1
        first = self.waiting_queue.get()

        def guard():
            self.on_pop_func(first['opaque'], first['tag'])
            with self.count_lock:
                self.active_count -= 1

        Thread(target=guard, daemon=False).start()


class PriQueueDispatcher(BasicThreadDispatcher):
    def __init__(self, inj, active_size=3, fallback_threshold=30):
        super().__init__(self._schedule)
        self.waiting_queue = PriorityQueue()
        self.active_size = active_size
        self.active_count = 0
        self.count_lock = Lock()
        self.fallback_threshold = fallback_threshold
        self.connection_pool = inj.require(ConnectionPool)  # type: ConnectionPool
        self.timestamp = time.time()

    def push(self, opaque, tag):
        self.waiting_queue.put((self.weighing_function(opaque),
                                {'opaque': opaque, 'tag': tag}))  # append is atomic

    def weighing_function(self, opaque) -> float:
        room_id = opaque["room_id"]
        room_info = self.connection_pool.get(room_id)
        room_privilege = room_info.room_privilege
        pri_coe = 100
        speed_coe = {
            FanSpeed.low: 25,
            FanSpeed.mid: 50,
            FanSpeed.high: 75
        }
        weight = pri_coe * room_privilege - (time.time() - self.timestamp) + speed_coe[opaque['speed_fan']]
        return -weight

    def _schedule(self):
        if not self.waiting_queue.empty():
            while self.waiting_queue.qsize() > self.fallback_threshold:
                pri, last = self.waiting_queue.get()
                self.on_fallback_func(last['opaque'], last['tag'])

            if self.active_count < self.active_size:
                self.__dispatch_one()

    def __dispatch_one(self):
        with self.count_lock:
            self.active_count += 1
        first = self.waiting_queue.get()

        def guard():
            self.on_pop_func(first['opaque'], first['tag'])
            with self.count_lock:
                self.active_count -= 1

        Thread(target=guard, daemon=False).start()
