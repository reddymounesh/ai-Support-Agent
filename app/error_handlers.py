import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("app")


def register_exception_handlers(app: FastAPI) -> None:
    """
    Ensures every error response (whether raised by us via HTTPException,
    or by FastAPI's own request validation) has the SAME JSON shape:
        {"error": {"message": "...", "status_code": ...}}
    A frontend can rely on this shape everywhere, instead of handling
    different error formats per endpoint.
    """

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        request_id = getattr(request.state, "request_id", None)
        logger.warning(
            "http_exception",
            extra={"request_id": request_id, "status_code": exc.status_code, "detail": exc.detail},
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "message": exc.detail,
                    "status_code": exc.status_code,
                    "request_id": request_id,
                }
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        request_id = getattr(request.state, "request_id", None)
        logger.warning(
            "validation_error",
            extra={"request_id": request_id, "errors": exc.errors()},
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "message": "Request validation failed",
                    "status_code": 422,
                    "request_id": request_id,
                    "details": exc.errors(),
                }
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        request_id = getattr(request.state, "request_id", None)
        # Log the FULL exception internally — never expose internals to the client.
        logger.error(
            "unhandled_exception", extra={"request_id": request_id}, exc_info=exc
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "message": "An unexpected error occurred.",
                    "status_code": 500,
                    "request_id": request_id,
                }
            },
        )