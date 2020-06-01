from abc import abstractmethod


class ConnectController(object):

    @abstractmethod
    def connect(self, *args, **kwargs):
        pass
