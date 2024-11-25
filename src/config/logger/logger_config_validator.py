from pydantic import Field,field_validator
from common.validator import BaseValidator
from typing import List
from enum import Enum


class LogLevel(str, Enum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    TRACE = "TRACE"
    NONE = ""  # Option to specify no level


class LogFormat(str, Enum):
    STANDARD = "standard"
    ECS = "ecs"


class LoggerConfigValidator(BaseValidator):
    authorized_values: List[str] = ["standard", "ecs", "opensearch"]

    log_level: LogLevel = Field(
        min_length=3, max_length=10, description="Defines the logging level"
    )
    log_format: LogFormat = Field(
        min_length=3, max_length=20, description="Specifies the log output format"
    )

    @classmethod
    @field_validator("log_format")
    def validate_log_format(cls, value):
        if value not in cls.authorized_values:
            raise ValueError(f"Invalid log format '{value}'")
        return value
