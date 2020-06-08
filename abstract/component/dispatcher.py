from abc import abstractmethod, ABC

from abstract.component.bootable import Bootable


class Dispatcher(Bootable, ABC):

    @abstractmethod
    def push(self, opaque, tag: str):
        pass

    @abstractmethod
    def on_pop(self, pop_callback=lambda opaque, tag: None):
        pass

    @abstractmethod
    def on_fallback(self, fallback_callback=lambda opaque, tag: None):
        pass
