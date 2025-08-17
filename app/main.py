# app/main.py
from litestar import Litestar
from app.api.v1 import (
    PostController,
    SeriesController,
    UserController,
    CommentController,
    AuthController
)
from app.core.di import provide_session
from app.core.handlers import (
    generic_exception_handler,
    http_exception_handler,
    app_exception_handler,
)
from litestar.exceptions import HTTPException
from app.core.exceptions import AppException
from app.core.security import jwt_auth


def create_app() -> Litestar:
    return Litestar(
        route_handlers=[
            PostController,
            SeriesController,
            UserController,
            CommentController,
            AuthController
            
        ],
        dependencies={"session": provide_session},
        exception_handlers={
            AppException: app_exception_handler,
            HTTPException: http_exception_handler,
            Exception: generic_exception_handler,
        },
        middleware=[jwt_auth.middleware],
    )


app = create_app()
