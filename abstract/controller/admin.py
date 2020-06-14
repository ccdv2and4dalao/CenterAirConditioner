from abc import abstractmethod


class DaemonAdminController(object):

    @abstractmethod
    def login(self, *args, **kwargs):
        """
        /v1/admin/login POST

        request:
        {"admin_token": "0123456789"}
        response:
        {"code": 0, "jwt_token": "9876543210"}
        """
        pass

    @abstractmethod
    def boot(self, *args, **kwargs):
        """
        /v1/admin/boot POST

        request:
        with header: "Authorization" : "Bearer " + jwt_token
        response:
        {"code": 0}
        """
        pass

    @abstractmethod
    def shutdown(self, *args, **kwargs):
        """
        /v1/admin/shutdown POST

        request:
        with header: "Authorization" : "Bearer " + jwt_token
        response:
        {"code": 0}
        """
        pass


class AdminController(object):
    @abstractmethod
    def set_mode(self, *args, **kwargs):
        """
        /v1/admin/mode POST

        request:
        {mode:"cool"|"heat"}
        with header: "Authorization" : "Bearer " + jwt_token
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
        with header: "Authorization" : "Bearer " + jwt_token
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
        /v1/admin/status GET

        request:
        with header: "Authorization" : "Bearer " + jwt_token
        response:
        {"code": 0, "server_state": "on" | "off" | "idle", "mode": "heat"|"cool"}
        """
        pass

    @abstractmethod
    def get_slave_statistics(self, *args, **kwargs):
        """
        /v1/admin/slave/statistics GET

        request:
        {"room_id": 1, "start_time": timestamp, "stop_time": timestamp}
        with header: "Authorization" : "Bearer " + jwt_token
        response:
        {"code": 0, to be done}
        """
        pass

    @abstractmethod
    def get_report(self, *args, **kwargs):
        """
        /v1/admin/report GET

        request:
        {"type": "day" | "week" | "month", "stop_time": time}
        with header: "Authorization" : "Bearer " + jwt_token
        response:
        {"code": 0, to be done}
        """
        pass

    @abstractmethod
    def get_connected_slaves(self, *args, **kwargs):
        """
        /v1/admin/pool-list GET

        request:-
        page_number=1&page_size=1
        with header: "Authorization" : "Bearer " + jwt_token
        response:
        self.id = inc_id  # type: int
        self.room_id = room_id  # type: str
        self.connected = connected  # type: bool
        self.current_temperature = current_temperature  # type: float
        self.need_fan = need_fan  # type: bool
        self.fan_speed = fan_speed  # type: str
        {"code": 0, "data": [{
                "id": 1, ""room_id: "A-101", "connected": true, "current_temperature": 22.0,
                "need_fan": true, "fan_speed": "high"}]}
        """
        pass

    @abstractmethod
    def get_connected_slave(self, *args, **kwargs):
        """
        /v1/admin/pool GET

        request:
        id=1
        with header: "Authorization" : "Bearer " + jwt_token
        response:
        {"code": 0, "data": {
                "id": 1, ""room_id: "A-101", "connected": true, "current_temperature": 22.0,
                "need_fan": true, "fan_speed": "high"}}
        """
        pass
