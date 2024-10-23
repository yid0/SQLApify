from abc import ABC, abstractmethod

class GrantStrategy(ABC):
    
    @abstractmethod
    def create_role(self, role_name: str) -> str:
        pass

    @abstractmethod
    def grant_permissions(self, role_name: str, schema: str, database: str) -> str:
        pass
