from abc import abstractmethod


class Bootable(object):

    @abstractmethod
    def boot_up(self):
        """
        拥有该属性的类都将能够启动
        boot_up要求是无阻塞的
        """
        pass

    # @abstractmethod
    # def pause(self, timeout: float = None):
    #     """
    #     暂停boot_up拉起的服务
    #     """
    #     pass

    @abstractmethod
    def shut_down(self, timeout: float = None):
        """
        停止boot_up拉起的服务
        :param timeout: 如果传入，则要求在timeout秒内停止，否则强制停止；如果该参数小于零则服务会直接强制停止
        """
        pass
