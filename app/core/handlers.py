from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.response import Response
from litestar.connection import Request
from .exceptions import AppException
import logging

logger = logging.getLogger(__name__)


def app_exception_handler(_request: Request, exc: AppException) -> Response:
    logger.error(exc.message)
    return Response(
        {"error": exc.message},
        status_code=exc.status_code,
    )


def http_exception_handler(_request: Request,exc: HTTPException) -> Response:
    logger.error(exc.detail)
    return Response(
        {"error": exc.detail},
        status_code=exc.status_code,
    )


def generic_exception_handler(_request: Request,exc: Exception) -> Response:
    logger.error(f"{exc}")
    return Response(
        {"error": "Internal Server Error"},
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )
