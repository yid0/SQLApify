from .base_configuration import BaseConfiguration
from .postgres import PostgresAdminConfig
from .app_user_config import ApplicationUserConfig
from .logger import LoggerConfig


class Configuration(BaseConfiguration):
    _instances = {}
    config_dict: None

    def __init__(self, key: str):
        if key in self._instances:
            return self

        self.config_type = key
        self.config_dict = None

    def create(self):
        match self.config_type:
            case "postgres":
                self.config_dict = PostgresAdminConfig.load()
            case "application":
                self.config_dict = ApplicationUserConfig.load()
            case "logger":
                self.config_dict = LoggerConfig.load()
            case _:
                raise ValueError(
                    f"Unsupported DB Configuration type: {self.config_type}"
                )

    @classmethod
    def get_instance(cls, key: str):
        if key not in cls._instances:
            cls._instances[key] = cls(key)
        print(cls._instances[key])
        return cls._instances[key]

    def load(self):
        if self.config_dict is None:
            self.create()
        return self.config_dict
