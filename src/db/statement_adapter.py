from abc import ABC, abstractmethod

class SQLStatementAdapter(ABC):
    @abstractmethod
    def create_schema_statement(self, schema_name: str) -> str:
        pass

    @abstractmethod
    def create_user_statement(self, username: str, password: str) -> str:
        pass

    @abstractmethod
    def create_role_statement(self, role_name: str) -> str:
        pass
    
    @abstractmethod
    def grant(self, role_name: str) -> str:
        pass
