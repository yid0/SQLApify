from abc import ABC, abstractmethod
from repository import DbType

class Query(ABC):
    db_type: DbType
    
    @abstractmethod
    def create(**kwargs) -> bool:
        pass