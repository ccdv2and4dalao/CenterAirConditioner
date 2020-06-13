from abc import abstractmethod


class MetricsController(object):

    @abstractmethod
    def update_metrics(self, *args, **kwargs):
        pass
