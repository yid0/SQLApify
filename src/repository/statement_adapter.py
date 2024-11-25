from abc import ABC, abstractmethod


class SQLStatementAdapter(ABC):
    @abstractmethod
    def check_role_exists(self, role_name: str):
        pass

    @abstractmethod
    def check_db_exists(self, db_name: str):
        pass

    @abstractmethod
    def create_db_statement(self, db_name: str, owner: str) -> str:
        pass

    @abstractmethod
    def create_schema_statement(self, schema_name: str) -> str:
        pass

    @abstractmethod
    def create_role_statement(self, role_name: str) -> str:
        pass

    @abstractmethod
    def grant_role(self, role_name: str, schema: str = None) -> str:
        pass

    @abstractmethod
    def revoke(self, role_name: str, db_name: str, schema: str = "public") -> str:
        pass

    @abstractmethod
    def grant_role_tmp_permissions_statement(self, role_name):
        pass

    @abstractmethod
    def revoke_permissions(self, role_name):
        pass

    @abstractmethod
    def grant_role_connection(self, role_name: str, db_name: str):
        pass
