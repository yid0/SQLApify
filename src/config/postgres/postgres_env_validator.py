from pydantic import Field
from common.validator import BaseValidator


class PostgresConfigValidator(BaseValidator):
    protocol: str = Field(min_length=3, max_length=20)
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8)
    host: str = Field(min_length=3, max_length=255)
    port: int = Field(ge=5432, le=65535)
    database: str = Field(min_length=3, max_length=50)
