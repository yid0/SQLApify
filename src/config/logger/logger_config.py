from enum import Enum
from config.env_value_mixin import EnvMixin


class LoggerConfig(EnvMixin, Enum):
    APP_LOG_LEVEL = ("LOG_LEVEL", "log_level")
    APP_LOG_FORMAT = ("LOG_FORMAT", "log_format")

    def load():
        from os import getenv

        env_dict = {
            LoggerConfig.APP_LOG_FORMAT.alias: getenv(
                str(LoggerConfig.APP_LOG_FORMAT.env_name), "standard"
            ),
            LoggerConfig.APP_LOG_LEVEL.alias: getenv(
                str(LoggerConfig.APP_LOG_LEVEL.env_name), "INFO"
            ),
        }

        LoggerConfig.validate(env_dict)

        return env_dict

    def validate(env_values):
        print(env_values)
        from .logger_config_validator import LoggerConfigValidator

        return LoggerConfigValidator(**env_values)
