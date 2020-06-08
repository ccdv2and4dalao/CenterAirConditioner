from abc import abstractmethod


class Bootable(object):

    @abstractmethod
    def boot_up(self):
        pass

    @abstractmethod
    def shut_down(self, timeout: float):
        pass
