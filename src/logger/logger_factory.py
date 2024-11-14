import os
from .providers import OpenSearchLoggerFactory, ElasticsLoggerFactory, StandardLoggerFactory

class LoggerFactory:
    """Factory class to select and create the appropriate logger based on environment configuration."""
    
    @classmethod
    def get_logger_factory(cls, name):
        log_format = os.getenv("LOG_FORMAT", "standard").lower()
        match log_format:
            case "standard":
                return StandardLoggerFactory(name)
            case "ecs":
                return ElasticsLoggerFactory(name)
            case "opensearch":
                return OpenSearchLoggerFactory(name)
            case _:
                raise ValueError(f"Unknown log format: {log_format}")
