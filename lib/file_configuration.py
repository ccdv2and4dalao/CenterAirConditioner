import os

from abstract.component import ConfigurationProvider, Configuration, OptionProvider
from abstract.singleton import option_context, OptionArgument
from lib.injector import Injector

option_context.arguments.append(OptionArgument(
    long_opt='config', help_msg='config file path'))


def load_admin_configuration_from_dict(d: dict):
    return Configuration.Admin(
        app_key=d.get(Configuration.Admin.app_key_key),
        admin_password=d.get(Configuration.Admin.admin_password_key))


def load_server_configuration_from_dict(d: dict):
    if d is None:
        return Configuration.Server()
    return Configuration.Server(
        bcrypt_salt=d.get(Configuration.Server.bcrypt_salt_key))


def load_database_configuration_from_dict(d: dict):
    if d is None:
        return Configuration.Database()
    return Configuration.Database(
        connection_type=d.get(Configuration.Database.connection_type_key),
        user=d.get(Configuration.Database.user_key),
        password=d.get(Configuration.Database.password_key),
        host=d.get(Configuration.Database.host_key),
        database_name=d.get(Configuration.Database.database_name_key),
        charset=d.get(Configuration.Database.charset_key),
        max_idle=d.get(Configuration.Database.max_idle_key),
        max_active=d.get(Configuration.Database.max_active_key),
        escape=d.get(Configuration.Database.escape_key),
        location=d.get(Configuration.Database.location_key))


def load_master_default_configuration_from_dict(d: dict):
    if d is None:
        return Configuration.MasterDefault()
    return Configuration.MasterDefault(
        default_temperature=d.get(Configuration.MasterDefault.default_temperature_key),
        mode=d.get(Configuration.MasterDefault.mode_key))


def load_slave_default_configuration_from_dict(d: dict):
    if d is None:
        return Configuration.SlaveDefault()
    return Configuration.SlaveDefault(
        metric_delay=d.get(Configuration.SlaveDefault.metric_delay_key),
        update_delay=d.get(Configuration.SlaveDefault.update_delay_key))


def load_configuration_from_dict(d: dict):
    if d is None:
        return Configuration()
    return Configuration(
        admin_config=load_admin_configuration_from_dict(d.get(Configuration.admin_config_key)),
        server_config=load_server_configuration_from_dict(d.get(Configuration.server_config_key)),
        database_config=load_database_configuration_from_dict(d.get(Configuration.database_config_key)),
        master_default=load_master_default_configuration_from_dict(d.get(Configuration.master_default_config_key)),
        slave_default=load_slave_default_configuration_from_dict(d.get(Configuration.slave_default_config_key)))


__yaml_loaded = False
__yaml_module = None


def load_yaml_module():
    global __yaml_loaded
    global __yaml_module
    if not __yaml_loaded:
        import yaml
        __yaml_module = yaml
        __yaml_loaded = True
    return __yaml_module


class FileConfigurationProvider(ConfigurationProvider):

    def __init__(self, injector: Injector):

        self.opt = injector.require(OptionProvider)  # type: OptionProvider
        self.file_path = self.opt.find('config')
        if self.file_path:
            with open(self.file_path) as f:
                ext = os.path.splitext(self.file_path)[1]
                if ext == '.yaml' or ext == '.yml' or ext == '':
                    yaml = load_yaml_module()
                    self.config = load_configuration_from_dict(yaml.load(f, yaml.SafeLoader))
                else:
                    raise ValueError(f'configuration file with unknown ext: path {self.file_path}, ext {ext}')
        else:
            self.config = Configuration()

    def get(self) -> Configuration:
        return self.config
