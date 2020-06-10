from abc import abstractmethod

from abstract.service import Service


class Middleware(object):

    @abstractmethod
    def __call__(self, service: Service) -> Service:
        pass
