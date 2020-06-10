from abc import ABC

from abstract.component import Dispatcher
from app.component.bootable import BootableImpl


class BasicThreadDispatcher(Dispatcher, BootableImpl, ABC):

    def __init__(self, schedule_fn, daemonic=True):
        super().__init__(schedule_fn, daemonic=daemonic)
        self.on_pop_func = None
        self.on_fallback_func = None

    def on_pop(self, pop_callback=lambda opaque, tag: None):
        self.on_pop_func = pop_callback

    def on_fallback(self, fallback_callback=lambda opaque, tag: None):
        self.on_fallback_func = fallback_callback
