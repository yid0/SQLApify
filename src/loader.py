import os
import importlib
from abc import ABC, abstractmethod
from fastapi import FastAPI

class BaseRouterLoader(ABC):
    
    def __init__(self, app: FastAPI, routes_dir: str):
        self.app = app
        self.routes_dir = routes_dir
        self.load_routes()
    
    @abstractmethod
    def load_routes(self):
        """
        Abstract method for loading and including routers.
        """
        pass


class RouterLoader(BaseRouterLoader):
    
    def load_routes(self):
        """
        Dynamically loads all files in the rest/routes directory and includes them in FastAPI.
        """
        for filename in os.listdir(self.routes_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                module_path = f"src.rest.{module_name}"
                module = importlib.import_module(module_path)
                
                if hasattr(module, 'router'):
                    self.app.include_router(getattr(module, 'router'))
