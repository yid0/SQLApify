from pydantic import Field
from common.validator.base_validator import BaseValidator

class AppUserEnvValidator(BaseValidator): 
    
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8)
    schema: str = Field(min_length=3, max_length=20)
    database: str = Field(min_length=3, max_length=50)
 