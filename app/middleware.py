import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("app")


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Generates a unique request_id for every incoming request, stores it on
    request.state (so route handlers and exception handlers can read it),
    adds it to the response headers (so a frontend/caller can report it
    back if something goes wrong), and logs request start/end with timing.
    """

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        start_time = time.monotonic()

        logger.info(
            "request_started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
            },
        )

        response = await call_next(request)

        duration_ms = round((time.monotonic() - start_time) * 1000, 2)
        response.headers["X-Request-ID"] = request_id

        logger.info(
            "request_completed",
            extra={
                "request_id": request_id,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            },
        )

        return response