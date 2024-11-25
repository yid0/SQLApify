from enum import Enum


class DbType(str, Enum):
    POSTGRES = "postgres"
    SQLITE = "sqlite"
