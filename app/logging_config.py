import logging
import sys
from pythonjsonlogger import jsonlogger


def configure_logging() -> None:
    """
    Configures the root 'app' logger to emit structured JSON lines instead
    of plain text. JSON logs are machine-parseable — you can grep/filter
    them by field (e.g. request_id, status_code) instead of relying on
    fragile string matching against free-text log messages.
    """
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s"
    )
    handler.setFormatter(formatter)

    logger.handlers = [handler]
    logger.propagate = False