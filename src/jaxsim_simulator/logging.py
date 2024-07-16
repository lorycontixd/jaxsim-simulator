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

# Logging formatter supporting colorized output
class LogFormatter(logging.Formatter):

    COLOR_CODES = {
        logging.CRITICAL: "\033[1;35m", # bright/bold magenta
        logging.ERROR:    "\033[1;31m", # bright/bold red
        logging.WARNING:  "\033[1;33m", # bright/bold yellow
        logging.INFO:     "\033[0;37m", # white / light gray
        logging.DEBUG:    "\033[1;30m"  # bright/bold black / dark gray
    }

    RESET_CODE = "\033[0m"

    def __init__(self, color, *args, **kwargs):
        super(LogFormatter, self).__init__(*args, **kwargs)
        self.color = color

    def format(self, record, *args, **kwargs):
        if (self.color == True and record.levelno in self.COLOR_CODES):
            record.color_on  = self.COLOR_CODES[record.levelno]
            record.color_off = self.RESET_CODE
        else:
            record.color_on  = ""
            record.color_off = ""
        return super(LogFormatter, self).format(record, *args, **kwargs)

def _logger() -> logging.Logger:
    logger = logging.getLogger(name=LOGGER_NAME)

    # Check if logger already has a stream handler
    has_ch: bool = False
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            return logger

    ch = logging.StreamHandler()
    ch.setLevel(logger.level)
    ch.setFormatter(fmt=coloredlogs.ColoredFormatter(fmt=FMT))
    logger.addHandler(ch)
    return logger
    
def add_file_handler(file_path: str) -> None:
    for handler in _logger().handlers:
        if isinstance(handler, logging.FileHandler) and handler.baseFilename == file_path:
            warning("File handler with such file path already exists. Ignoring call...")
            return

    handler = logging.FileHandler(file_path, mode="w", encoding="utf-8")
    log_line_template = "%(color_on)s[%(created)d] [%(threadName)s] [%(levelname)-8s] %(message)s%(color_off)s"
    logfile_log_color = True
    logfile_formatter = LogFormatter(fmt=log_line_template, color=logfile_log_color)
    handler.setFormatter(logfile_formatter)
    handler.setLevel(_logger().level)
    _logger().addHandler(handler)

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