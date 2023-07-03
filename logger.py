import sys
from loguru import logger

logger.remove(0)
logger.add(
    sys.stderr,
    format="<red>[{level}]</red> <green>{message}</green> @ {time:HH:mm:ss}",
    colorize=True,
    backtrace=True,
    diagnose=True,
    level="INFO",
)
