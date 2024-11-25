from abc import ABC, abstractmethod
from .connection import Connection
from .engine import Engine


class BaseDatabase(ABC):
    def __init__(self, connection: Connection, engine: Engine):
        self.engine = engine

    """
    Abstract class for database
    """

    @abstractmethod
    def connect(self):
        """
        Abstract method to ensure connection to the database.
        Will be overridden by each database type implementation.
        """
        pass

    @abstractmethod
    def get_connection_url(self) -> str:
        """
        Abstract method to get the database connection URL.
        Will be overridden by each database type implementation.
        """
        pass

    @abstractmethod
    def get_sql_adapter(self):
        """
        Abstract method to return the appropriate SQLStatementAdapter
        for the current database.
        Will be overridden by each database type implementation.
        """
        pass

    @abstractmethod
    def dispose(self):
        pass
