import enum
import logging
from typing import Union

import coloredlogs

LOGGER_NAME = "jaxsim-simulator"
FMT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class LoggingLevel(enum.IntEnum):
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


def _logger() -> logging.Logger:
    logger = logging.getLogger(name=LOGGER_NAME)

    ch = logging.StreamHandler()
    ch.setLevel(logger.level)
    ch.setFormatter(fmt=coloredlogs.ColoredFormatter(fmt=FMT))
    logger.addHandler(ch)

    fh = logging.FileHandler("jaxsim-simulator.log")
    fh.setLevel(logger.level)
    fh.setFormatter(fmt=fmt)
    logger.addHandler(fh)

    return logger
    
def add_file_handler(file_path: str) -> None:
    fh = logging.FileHandler(file_path)
    fh.setFormatter(fmt=FMT)
    fh.setLevel(_logger().level)
    _logger().addHandler(fh)

def remove_file_handler() -> None:
    for handler in _logger().handlers:
        if isinstance(handler, logging.FileHandler):
            _logger().removeHandler(handler)
            break

def set_logging_level(level: Union[int, LoggingLevel] = LoggingLevel.WARNING):
    if isinstance(level, int):
        level = LoggingLevel(level)

    _logger().setLevel(level=level.value)


def get_logging_level() -> LoggingLevel:
    level = _logger().getEffectiveLevel()
    return LoggingLevel(level)


def configure(level: LoggingLevel = LoggingLevel.WARNING) -> None:
    info("Configuring the 'jaxsim' logger")

    handler = logging.StreamHandler()
    handler.setFormatter(fmt=FMT)
    _logger().addHandler(hdlr=handler)

    # Do not propagate the messages to handlers of parent loggers
    # (preventing duplicate logging)
    _logger().propagate = False

    set_logging_level(level=level)


def debug(msg: str = "") -> None:
    _logger().debug(msg=msg)


def info(msg: str = "") -> None:
    _logger().info(msg=msg)


def warning(msg: str = "") -> None:
    _logger().warning(msg=msg)


def error(msg: str = "") -> None:
    _logger().error(msg=msg)


def critical(msg: str = "") -> None:
    _logger().critical(msg=msg)


def exception(msg: str = "") -> None:
    _logger().exception(msg=msg)