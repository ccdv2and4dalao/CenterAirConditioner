from abc import abstractmethod

from abstract.consensus import AirMode

Millisecond = int


class Configuration(object):
    admin_config_key = 'admin'
    database_config_key = 'database'
    master_default_config_key = 'master-default'
    slave_default_config_key = 'slave-default'

    class Admin:
        app_key_key = 'app-key'
        admin_password_key = 'admin-password'

        def __init__(self,
                     app_key=None,
                     admin_password=None):
            self.app_key = app_key or ''  # type: str
            self.admin_password = admin_password or ''  # type: str

    class MasterDefault:
        default_temperature_key = 'default-temperature'
        mode_key = 'mode'

        def __init__(self,
                     default_temperature=None,
                     mode=None):
            self.default_temperature = default_temperature or 22.0  # type: float
            self.mode = mode or AirMode.Cool.value  # type: str

    class SlaveDefault:
        metric_delay_key = 'metric-delay'
        update_delay_key = 'update-delay'

        def __init__(self,
                     metric_delay=None,
                     update_delay=None):
            self.metric_delay = metric_delay or 100  # type: Millisecond
            self.update_delay = update_delay or 100  # type: Millisecond

    class Database:
        connection_type_key = 'connection-type'
        user_key = 'user-name'
        password_key = 'password'
        host_key = 'host'
        database_name_key = 'database-name'
        charset_key = 'charset'
        max_idle_key = 'max-idle'
        max_active_key = 'max-active'
        escape_key = 'escape'
        location_key = 'location'

        def __init__(self,
                     connection_type=None,
                     user=None,
                     password=None,
                     host=None,
                     database_name=None,
                     charset=None,
                     max_idle=None,
                     max_active=None,
                     escape=None,
                     location=None):
            self.connection_type = connection_type or 'mysql'  # type: str
            self.user = user or 'admin'  # type: str
            self.password = password or '12345678'  # type: str
            self.host = host or 'localhost:3306'  # type: str
            self.database_name = database_name or 'backend'  # type: str
            self.charset = charset or 'utf8mb4'  # type: str
            self.max_idle = max_idle or 100  # type: int
            self.max_active = max_active or 100  # type: int
            self.escape = escape or '`'  # type: str
            self.location = location or 'Local'  # type: str

    def __init__(self, admin_config=None, database_config=None, master_default=None, slave_default=None):
        self.admin_config = admin_config or Configuration.Admin()  # type: Configuration.Admin
        self.database_config = database_config or Configuration.Database()  # type: Configuration.Database
        self.master_default = master_default or Configuration.MasterDefault()  # type: Configuration.MasterDefault
        self.slave_default = slave_default or Configuration.SlaveDefault()  # type: Configuration.SlaveDefault


class ConfigurationProvider(object):

    @abstractmethod
    def get(self) -> Configuration:
        """
        :return: 返回一个Configuration结构体，该结构体原则上是不可变的（例如文件变化时，该结构体对应字段不会被更新）
        """
        pass
