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

    @abstractmethod
    def super_user(self) -> str:
        """
        Get url conncetion
        """
        pass

    @abstractmethod
    def management_user(self) -> str:
        """
        Get url conncetion
        """
        pass

    @abstractmethod
    def app_user(self) -> str:
        """
        Get url conncetion
        """
        pass
