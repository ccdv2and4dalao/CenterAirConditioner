from abc import abstractmethod

class StatisticService(object):
	@abstractmethod
	def generate_statistic(self, *args, **kwargs):
		pass