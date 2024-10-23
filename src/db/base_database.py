from abc import ABC, abstractmethod

class BaseDatabase(ABC):
    """
    Abstract class for database
    """
    
    @abstractmethod
    def connect(self):
        """
        Abstract method to ensure connction to the databas.
        Will be overridden by each database type implemention
        """
        pass
    
    @abstractmethod
    def get_connection_url(self) -> str:
        """
        Abstract method to get database url connection
        Will be owerride by each database type implemention

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