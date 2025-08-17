from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.response import Response
from .exceptions import AppException


def app_exception_handler(exc: AppException) -> Response:
    return Response(
        {"error": exc.message},
        status_code=exc.status_code,
    )


def http_exception_handler(exc: HTTPException) -> Response:
    return Response(
        {"error": exc.detail},
        status_code=exc.status_code,
    )


def generic_exception_handler(_exc: Exception) -> Response:
    return Response(
        {"error": "Internal Server Error"},
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )
