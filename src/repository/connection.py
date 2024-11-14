from abc import ABC, abstractmethod

class Connection(ABC):
    """
    Abstract class defining a database conncetion 
    """

    @abstractmethod
    def url(self) -> str:
        """
        Get url conncetion
        """
        pass






