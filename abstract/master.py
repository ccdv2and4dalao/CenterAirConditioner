from abc import abstractmethod


class Master(object):

    @abstractmethod
    def boot(self):
        """
        开启中央主空调
        :return: None
        """
        pass

    @abstractmethod
    def shutdown(self):
        """
        关闭中央主空调
        :return: None
        """
        pass

    @abstractmethod
    def set_cooling_mode(self):
        """
        设置中央主空调制冷模式
        :return: None
        """
        pass


    @abstractmethod
    def set_heat_mode(self):
        """
        设置中央主空调制热模式
        :return: None
        """
        pass

    @abstractmethod
    def temp_increase(self):
        """
        设置中央主空调温度加一
        :return: None
        """
        pass

    @abstractmethod
    def temp_decrease(self):
        """
        设置中央主空调温度减一
        :return: None
        """
        pass
