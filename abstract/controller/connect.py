from abc import abstractmethod


class ConnectController(object):

    @abstractmethod
    def connect(self, *args, **kwargs):
        pass

    @abstractmethod
    def disconnect(self, *args, **kwargs):
        pass