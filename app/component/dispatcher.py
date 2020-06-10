from queue import Queue
from threading import Thread, Lock

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
