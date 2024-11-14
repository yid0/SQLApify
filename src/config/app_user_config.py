from enum import Enum
from .env_value_mixin import EnvMixin

class ApplicationUserConfig(EnvMixin, Enum):
    APP_BUILD_TARGET= ("BUILD_TARGET", "build_target")
    SQLAPIFY_DB_SCHEMA= ("SQLAPIFY_DB_SCHEMA", "schema")    
    SQLAPIFY_DB_USER= ("SQLAPIFY_DB_USER", "username")
    SQLAPIFY_DB_PASSWORD=("SQLAPIFY_DB_PASSWORD", "password")
    SQLAPIFY_DB_NAME=("SQLAPIFY_DB_NAME", "database")

    def load(self):
        from os import getenv

        self.env_dict = {
            super().DB_SCHEMA[1] : getenv(str(ApplicationUserConfig.SQLAPIFY_DB_SCHEMA.env_name)),
            super().DB_USERNAME[1] : getenv(str(ApplicationUserConfig.SQLAPIFY_DB_USER.env_name)),
            super().DB_PASSWORD[1] : getenv(str(ApplicationUserConfig.SQLAPIFY_DB_PASSWORD.env_name)),
            super().DB_NAME[1] : getenv(str(ApplicationUserConfig.SQLAPIFY_DB_NAME.env_name))
        }
        
        self.validate(self, self.env_dict)  

        return self.env_dict
    
    
    def validate(self, env_values):
        from config.app_user_validator import AppUserEnvValidator
        print("Validator: ", env_values)
        return bool(AppUserEnvValidator(**env_values))

 