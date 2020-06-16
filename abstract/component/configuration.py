from abc import abstractmethod

from abstract.consensus import AirMode

Millisecond = int


# 2.中央空调是冷暖两用，根据季节进行工作模式调整。
#     a)当设置为供暖时，供暖温度控制在25°C～30°C之间；
#     b)当设置为制冷时，制冷温度控制在18°C～25°C之间。
# 3.中央空调具备开关按钮，只可人工开启和关闭，中央空调正常开启后处于待机状态。
#     a)中央空调开机后，默认处于制冷模式，缺省工作温度为22°C，当切换到供暖模式时，缺省工作温度为28°C；
# 8.中央空调能够实时监测各房间的温度和状态，并要求实时刷新的频率能够进行配置；

class Configuration(object):
    admin_config_key = 'admin'
    server_config_key = 'server'
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
        cool_min_key = 'cool_min'
        cool_max_key = 'cool_max'
        heat_min_key = 'heat_min'
        heat_max_key = 'heat_max'
        def __init__(self,
                     default_temperature=None,
                     mode=None, cool_min=None, cool_max=None,
                     heat_min=None, heat_max=None):
            self.default_temperature = default_temperature or 22.0  # type: float
            self.mode = mode or AirMode.Cool.value  # type: str
            self.cool_min = cool_min or 18.0 # type: float
            self.cool_max = cool_max or 25.0 # type: float
            self.heat_min = heat_min or 25.0 # type: float
            self.heat_max = heat_max or 30.0 # type: float

    class SlaveDefault:
        metric_delay_key = 'metric-delay'
        update_delay_key = 'update-delay'

        def __init__(self,
                     metric_delay=None,
                     update_delay=None):
            self.metric_delay = metric_delay or 100  # type: Millisecond
            self.update_delay = update_delay or 100  # type: Millisecond

    class Server:
        bcrypt_salt_key = 'bcrypt-salt'

        def __init__(self, bcrypt_salt=None):
            self.bcrypt_salt = (bcrypt_salt or '$2b$12$LJh77o2qdckmSf0kZNjude').encode()  # type: bytes

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

    def __init__(self, admin_config=None, server_config=None, database_config=None, master_default=None,
                 slave_default=None):
        self.admin_config = admin_config or Configuration.Admin()  # type: Configuration.Admin
        self.server_config = server_config or Configuration.Server()  # type: Configuration.Server
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
