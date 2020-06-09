﻿from abstract.component.dispatcher import Dispatcher
from app.component.bootable import BootableImpl
from threading import Thread, Lock

class QueueDispatcher(Dispatcher, BootableImpl):
    def __init__(self, active_size=3, fallback_threshold=30):
        super().__init__(self._schedule, daemonic=True)
        self.on_pop_func = None
        self.on_fallback_func = None
        self.waiting_queue = []
        self.active_size = active_size
        self.active_count = 0
        self.count_lock = Lock()
        self.fallback_threshold = fallback_threshold

    def push(self, opaque, tag):
        self.waiting_queue.append({'opaque': opaque, 'tag': tag}) # append is atomic

    def _schedule(self):
        if len(self.waiting_queue) > 0:
            while len(self.waiting_queue) > self.fallback_threshold:
                last = self.waiting_queue.pop()
                self.on_fallback_func(last['opaque'], last['tag'])

            if self.active_count < self.active_size:
                self.__dispatch_one()

          
    def __dispatch_one(self):
        with self.count_lock:
            self.active_count += 1
        first = self.waiting_queue.pop(0)
        def guard():
            self.on_pop_func(first['opaque'], first['tag'])
            with self.count_lock:
                self.active_count -= 1
        Thread(target=guard, daemon=False).start()

    def on_pop(self, pop_callback=lambda opaque,tag: None):
        self.on_pop_func = pop_callback

    def on_fallback(self, fallback_callback=lambda opaque,tag: None):
        self.on_fallback_func = fallback_callback


if __name__ == '__main__':
    from time import sleep
    from random import randint
    import itertools

    def foo(opaque, tag):
        sleep(randint(5, 10))
        print(f'{tag} bye')

    def foo2(opaque, tag):
        print(f'{tag} poped')

    qd = QueueDispatcher(fallback_threshold=30)
    qd.on_pop(foo)
    qd.on_fallback(foo2)
    qd.boot_up()
    for i in range(10):
        sleep(1)
        qd.push(None, str(i))
        print(f'push {i}')
    qd.shut_down(0)
    sleep(20)
    qd.boot_up()
    sleep(20)
    qd.shut_down()

