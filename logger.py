import sys
from loguru import logger


logging_format = "<green>{time:YY:MM:DD HH:mm:ss}</green>|<level>{level: <8}</level>|<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

logger_handler = 0
logger.remove(logger_handler)
logger_handler = logger.add(
    sys.stderr,
    format=logging_format,
    level="DEBUG"
    # colorize=True,
    # backtrace=True,
    # diagnose=True,
)

# logger.add(
#     sys.stderr,
#     format="<red>[{level}]</red> <green>{message}</green> @ {time:HH:mm:ss}",
#     colorize=True,
#     backtrace=True,
#     diagnose=True,
#     level="INFO",
# )


def log_trace():
    global logger_handler
    logger.remove(logger_handler)
    logger_handler = logger.add(
        sys.stderr,
        format=logging_format,
        level="TRACE"
        # colorize=True,
        # backtrace=True,
        # diagnose=True,
    )


def log_info():
    global logger_handler
    logger.remove(logger_handler)
    logger_handler = logger.add(
        sys.stderr,
        format=logging_format,
        level="INFO"
        # colorize=True,
        # backtrace=True,
        # diagnose=True,
    )


def log_debug():
    global logger_handler
    logger.remove(logger_handler)
    logger_handler = logger.add(
        sys.stderr,
        format=logging_format,
        level="DEBUG"
        # colorize=True,
        # backtrace=True,
        # diagnose=True,
    )


import functools


def logger_wraps(*, entry=True, exit=True, level="TRACE"):
    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1)
            if entry:
                logger_.log(
                    level, "Entering '{}' (args={}, kwargs={})", name, args, kwargs
                )
            result = func(*args, **kwargs)
            if exit:
                logger_.log(level, "Exiting '{}' (result={})", name, result)
            return result

        return wrapped

    return wrapper
