from litestar.security.jwt import JWTAuth
from app.core.config import settings
from app.core.middlewares import retrieve_user_handler

jwt_auth = JWTAuth(
    retrieve_user_handler=retrieve_user_handler,
    token_secret=settings.SECRET_KEY,
    exclude=["/api/v1/auth/register", "/api/v1/auth/login", "/schema/swagger", "/schema"]
)