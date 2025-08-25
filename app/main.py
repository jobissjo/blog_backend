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
from app.core.security import jwt_auth, openapi_config
from litestar.config.cors import CORSConfig

cors_config = CORSConfig(
    # Allow specific origins (recommended for production)
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:3000",
        "https://yourdomain.com",  # Your production domain
        "http://192.168.1.6:5173"
    ],
    
    # Or allow all origins (only for development)
    # allow_origins=["*"],
    
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "User-Agent",
        "DNT",
        "Cache-Control",
        "X-Mx-ReqToken",
        "Keep-Alive",
        "X-Requested-With",
        "If-Modified-Since",
    ],
    allow_credentials=True,  # Allow cookies/auth headers
    expose_headers=["*"],
    max_age=600,  # Preflight cache time in seconds
)


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
        cors_config=cors_config,
        openapi_config=openapi_config,
    )


app = create_app()
