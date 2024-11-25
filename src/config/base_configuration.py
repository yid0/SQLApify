from abc import ABC, abstractmethod


class BaseConfiguration(ABC):
    @abstractmethod
    def load(self):
        """
        Load the needed configuration class
        """
