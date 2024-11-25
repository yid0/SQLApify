from repository import DbType, Connection
from repository.provider import PostgresConnection
from repository.provider import SQLiteConnection
from config.logger import AppLogger


class ConnectionFactory:
    logger = AppLogger(__name__).get_logger()

    @classmethod
    def create_connection(self, db_type: DbType, scope=None, **kwargs) -> Connection:
        match db_type:
            case DbType.POSTGRES:
                return self.__create(self, scope=scope)
            case DbType.SQLITE:
                return SQLiteConnection(db_name=kwargs["db_name"])
            case _:
                raise ValueError(f"Unsupported database type: {db_type}")

    def __create(self, scope: str):
        connection: None
        match scope:
            case "super_user":
                connection = PostgresConnection.super_user()
            case "app_user":
                connection = PostgresConnection.app_user()
            case "management_user":
                connection = PostgresConnection.management_user()
            case _:
                raise ValueError(f"Unsupported database type: {scope}")

        self.logger.debug(f"DATA CONNECTION {connection}")
        return connection
