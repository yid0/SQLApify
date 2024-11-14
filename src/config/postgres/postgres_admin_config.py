from enum import Enum
from config.env_value_mixin import EnvMixin

class PostgresAdminConfig(EnvMixin, Enum):
        
    POSTGRES_PROTOCOL= ("POSTGRES_PROTOCOL", "protocol")
    POSTGRES_HOST= ("POSTGRES_HOST" , "host")
    POSTGRES_PORT= ("POSTGRES_PORT", "port")
    POSTGRES_DATABASE= ("POSTGRES_DATABASE", "database")
    POSTGRES_ADMIN_USERNAME= ("POSTGRES_ADMIN_USERNAME", "username")
    POSTGRES_ADMIN_PASSWORD= ("POSTGRES_ADMIN_PASSWORD", "password")
        
    def load(self) -> dict :
        from os import getenv       
               
        self.env_dict = {
            super().DB_HOST[1]: getenv(str(PostgresAdminConfig.POSTGRES_HOST.env_name)),
            super().DB_PORT[1]: getenv(str(PostgresAdminConfig.POSTGRES_PORT.env_name)),
            super().DB_PROTOCOL[1]: getenv(str(PostgresAdminConfig.POSTGRES_PROTOCOL.env_name) or "postgresql+psycopg2"),
            super().DB_USERNAME[1]: getenv(str(PostgresAdminConfig.POSTGRES_ADMIN_USERNAME.env_name)),
            super().DB_PASSWORD[1]: getenv(str(PostgresAdminConfig.POSTGRES_ADMIN_PASSWORD.env_name)),
            super().DB_NAME[1]: getenv(str(PostgresAdminConfig.POSTGRES_DATABASE.env_name))
        }

        self.validate(self, self.env_dict) 

        return self.env_dict
    
    
    def validate(self, env_values):
        from config.postgres import PostgresConfigValidator
        return bool(PostgresConfigValidator(**env_values))
