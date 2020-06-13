from abc import abstractmethod


class SlaveStateControlController(object):

    @abstractmethod
    def start_state_control(self, *args, **kwargs):
        pass

    @abstractmethod
    def stop_state_control(self, *args, **kwargs):
        pass
