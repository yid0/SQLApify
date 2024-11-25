from enum import Enum
from .env_value_mixin import EnvMixin


class ApplicationUserConfig(EnvMixin, Enum):
    APP_BUILD_TARGET = ("BUILD_TARGET", "build_target")
    SQLAPIFY_DB_SCHEMA = ("SQLAPIFY_DB_SCHEMA", "schema")
    SQLAPIFY_DB_USER = ("SQLAPIFY_DB_USER", "username")
    SQLAPIFY_DB_PASSWORD = ("SQLAPIFY_DB_PASSWORD", "password")
    SQLAPIFY_DB_NAME = ("SQLAPIFY_DB_NAME", "database")
    env_dict: dict

    def load():
        from os import getenv

        env_dict = {
            ApplicationUserConfig.DB_SCHEMA[1]: getenv(
                str(ApplicationUserConfig.SQLAPIFY_DB_SCHEMA.env_name)
            ),
            ApplicationUserConfig.DB_USERNAME[1]: getenv(
                str(ApplicationUserConfig.SQLAPIFY_DB_USER.env_name)
            ),
            ApplicationUserConfig.DB_PASSWORD[1]: getenv(
                str(ApplicationUserConfig.SQLAPIFY_DB_PASSWORD.env_name)
            ),
            ApplicationUserConfig.DB_NAME[1]: getenv(
                str(ApplicationUserConfig.SQLAPIFY_DB_NAME.env_name)
            ),
        }

        ApplicationUserConfig.validate(env_dict)

        return env_dict

    def validate(env_values):
        from config.app_user_validator import AppUserEnvValidator

        print("Validator: ", env_values)
        return AppUserEnvValidator(**env_values)
