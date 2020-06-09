from abstract.service import Service, abstractmethod


class Middleware(object):

    @abstractmethod
    def __call__(self, service: Service) -> Service:
        pass
