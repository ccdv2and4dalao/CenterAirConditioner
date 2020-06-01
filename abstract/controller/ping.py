from abc import abstractmethod


class PingController(object):

    @abstractmethod
    def ping(self, *args, **kwargs):
        pass
