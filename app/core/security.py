from litestar.security.jwt import JWTAuth
from app.core.config import settings
from app.core.middlewares import retrieve_user_handler
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Components, SecurityScheme


openapi_config = OpenAPIConfig(
    title="Blog API",
    version="1.0.0",
    description="API with JWT Authentication",
    components=Components(
        security_schemes={
            "BearerAuth": SecurityScheme(
                type="http",
                scheme="bearer",
                bearer_format="JWT",
                description="Enter JWT token"
            )
        }
    ),
    security=[{"BearerAuth": []}],  # Apply globally
    use_handler_docstrings=True,
)

jwt_auth = JWTAuth(
    retrieve_user_handler=retrieve_user_handler,
    token_secret=settings.SECRET_KEY,
    exclude=["/api/v1/auth/register", "/api/v1/auth/login", "/schema/swagger", "/schema",
             "/api/v1/auth/forgot-password", "/api/v1/auth/reset-password", "/api/v1/auth/verify-otp",
             "/media/*"],
)