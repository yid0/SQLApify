from unittest.mock import patch
from src.config.logger import AppLogger


logger_mock = logger_mock = {
    "info" :"logging.Logger.info",
    "debug": "logging.Logger.debug",
    "error": "logging.Logger.error",
    "trace":"logging.Logger.trace"
}

log_message = "SQLApify log message"

def test_logging_info_output():
    with patch('logging.Logger.info') as mock_info:
        logger = AppLogger(logger_mock["info"]).get_logger()
        logger.info("Test log message")

        mock_info.assert_called_once_with("Test log message")

def test_logging_debug_output():
    with patch(logger_mock["debug"]) as mock_info:
        logger = AppLogger("test_logger").get_logger()
        logger.debug("Test log message")

        mock_info.assert_called_once_with("Test log message")