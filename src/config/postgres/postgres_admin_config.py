from enum import Enum
from config.env_value_mixin import EnvMixin


class PostgresAdminConfig(EnvMixin, Enum):
    POSTGRES_PROTOCOL = ("POSTGRES_PROTOCOL", "protocol")
    POSTGRES_HOST = ("POSTGRES_HOST", "host")
    POSTGRES_PORT = ("POSTGRES_PORT", "port")
    POSTGRES_DATABASE = ("POSTGRES_DATABASE", "database")
    POSTGRES_ADMIN_USERNAME = ("POSTGRES_ADMIN_USERNAME", "username")
    POSTGRES_ADMIN_PASSWORD = ("POSTGRES_ADMIN_PASSWORD", "password")

    def load() -> dict:
        from os import getenv

        env_dict = {
            PostgresAdminConfig.DB_HOST[1]: getenv(
                str(PostgresAdminConfig.POSTGRES_HOST.env_name)
            ),
            PostgresAdminConfig.DB_PORT[1]: getenv(
                str(PostgresAdminConfig.POSTGRES_PORT.env_name)
            ),
            PostgresAdminConfig.DB_PROTOCOL[1]: getenv(
                str(PostgresAdminConfig.POSTGRES_PROTOCOL.env_name)
                or "postgresql+asyncpg"
            ),
            PostgresAdminConfig.DB_USERNAME[1]: getenv(
                str(PostgresAdminConfig.POSTGRES_ADMIN_USERNAME.env_name)
            ),
            PostgresAdminConfig.DB_PASSWORD[1]: getenv(
                str(PostgresAdminConfig.POSTGRES_ADMIN_PASSWORD.env_name)
            ),
            PostgresAdminConfig.DB_NAME[1]: getenv(
                str(PostgresAdminConfig.POSTGRES_DATABASE.env_name)
            ),
        }

        PostgresAdminConfig.validate(env_dict)

        return env_dict

    def validate(env_values):
        from config.postgres import PostgresConfigValidator

        return PostgresConfigValidator(**env_values)
