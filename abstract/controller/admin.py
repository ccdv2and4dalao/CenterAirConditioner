from abc import abstractmethod


class AdminController(object):

    @abstractmethod
    def login(self, *args, **kwargs):
        """
        /v1/admin/login POST

        request:
        {"admin-token": "0123456789"}
        response:
        {"code": 0, "jwt-token": "9876543210"}
        """
        pass

    @abstractmethod
    def boot(self, *args, **kwargs):
        """
        /v1/admin/boot POST

        request:
        with header: "Authorization" : "Bearer " + jwt-token
        response:
        {"code": 0}
        """
        pass

    @abstractmethod
    def shutdown(self, *args, **kwargs):
        """
        /v1/admin/shutdown POST

        request:
        with header: "Authorization" : "Bearer " + jwt-token
        response:
        {"code": 0}
        """
        pass

    @abstractmethod
    def set_mode(self, *args, **kwargs):
        """
        /v1/admin/mode POST

        request:
        {mode:"cool"|"heat"}
        with header: "Authorization" : "Bearer " + jwt-token
        response:
        {"code": 0}
        """
        pass

    @abstractmethod
    def set_heat_mode(self, *args, **kwargs):
        # self.set_mode(*args, **kwargs)
        pass

    @abstractmethod
    def set_cool_mode(self, *args, **kwargs):
        # self.set_mode(*args, **kwargs)
        pass

    @abstractmethod
    def set_current_temperature(self, *args, **kwargs):
        """
        /v1/admin/current-temp POST

        request:
        {"target": 22.0}
        with header: "Authorization" : "Bearer " + jwt-token
        response:
        {"code": 0}
        """
        pass

    @abstractmethod
    def temp_increase(self, *args, **kwargs):
        # req.target = current_temperature + 1
        # self.set_current_temperature(*args, **kwargs)
        pass

    @abstractmethod
    def temp_decrease(self, *args, **kwargs):
        # req.target = current_temperature - 1
        # self.set_current_temperature(*args, **kwargs)
        pass

    @abstractmethod
    def get_server_status(self, *args, **kwargs):
        """
        /v1/admin/status POST

        request:
        {"target": 22.0}
        with header: "Authorization" : "Bearer " + jwt-token
        response:
        {"code": 0, "server_state": "on" | "off" | "idle", "mode": "heat"|"cool"}
        """
        pass
