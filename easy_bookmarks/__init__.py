import logging


logging.getLogger(__name__).addHandler(logging.NullHandler())


def add_stderr_logger(level: int = logging.DEBUG) -> logging.StreamHandler:
    "For debug purposes, add a stderr logger to the root logger."
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.debug("Added a stderr logging handler to logger: %s", __name__)
    return handler
