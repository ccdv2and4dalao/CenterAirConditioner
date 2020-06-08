

from abc import abstractmethod


class Configuration(object):
    database_config_key = 'database'

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

    def __init__(self, database_config=None):
        self.database_config = database_config or Configuration.Database()  # type: Configuration.Database


class ConfigurationProvider(object):

    @abstractmethod
    def get(self) -> Configuration:
        """
        :return: 返回一个Configuration结构体，该结构体原则上是不可变的（例如文件变化时，该结构体对应字段不会被更新）
        """
        pass
