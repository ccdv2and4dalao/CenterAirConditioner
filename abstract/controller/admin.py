from abc import abstractmethod


class AdminController(object):

    @abstractmethod
    def boot(self, *args, **kwargs):
        pass

    @abstractmethod
    def shutdown(self, *args, **kwargs):
        pass

    @abstractmethod
    def set_cooling_mode(self, *args, **kwargs):
        pass

    @abstractmethod
    def set_heat_mode(self, *args, **kwargs):
        pass

    @abstractmethod
    def temp_increase(self, *args, **kwargs):
        pass

    @abstractmethod
    def temp_decrease(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_server_status(self, *args, **kwargs):
        pass

    @abstractmethod
    def login(self, *args, **kwargs):
        pass
