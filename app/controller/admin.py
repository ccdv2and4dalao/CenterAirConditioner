from abstract.controller import AdminController, DaemonAdminController
from lib.injector import Injector


class FlaskDaemonAdminControllerImpl(DaemonAdminController):

    def __init__(self, _: Injector):
        pass

    def login(self, *args, **kwargs):
        return

    def boot(self, *args, **kwargs):
        pass

    def shutdown(self, *args, **kwargs):
        pass


class FlaskAdminControllerImpl(AdminController):

    def __init__(self, _: Injector):
        pass

    def set_mode(self, *args, **kwargs):
        pass

    def set_heat_mode(self, *args, **kwargs):
        # self.set_mode(*args, **kwargs)
        pass

    def set_cool_mode(self, *args, **kwargs):
        # self.set_mode(*args, **kwargs)
        pass

    def set_current_temperature(self, *args, **kwargs):
        pass

    def temp_increase(self, *args, **kwargs):
        # req.target = current_temperature + 1
        # self.set_current_temperature(*args, **kwargs)
        pass

    def temp_decrease(self, *args, **kwargs):
        # req.target = current_temperature - 1
        # self.set_current_temperature(*args, **kwargs)
        pass

    def get_server_status(self, *args, **kwargs):
        pass
