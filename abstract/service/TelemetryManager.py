from abc import abstractmethod

class TelemetryManager(object):
    @abstractmethod
    def receive_config(self, cfgReq): 
        pass

    @abstractmethod
    def update_config(self, cfgReq):
        pass

    @abstractmethod
    def save_config(self, cfgReq):
        pass

    @abstractmethod
    def set_update_timer(self, duration: int):
        pass