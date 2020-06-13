from abc import abstractmethod


class StatisticsController(object):

    @abstractmethod
    def generate_statistics(self, *args, **kwargs):
        pass
