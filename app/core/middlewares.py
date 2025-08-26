from litestar.security.jwt import Token
from litestar.connection import ASGIConnection
from typing import Optional
from app.core.di import  provide_session_ctx
from app.core.exceptions import AppException
from app.domain.users.models import User
from app.domain.users.repository import UserRepository

async def retrieve_user_handler(token: Token, _connection: ASGIConnection) -> Optional[User]:
    """Retrieve user from token payload."""
    try:
        # Fix: Properly consume the async generator to get the session
        async with provide_session_ctx() as session:
            user_repository = UserRepository(session)
            user_id = token.sub
            user = await user_repository.get_by_id(int(user_id))
            if user and user.is_active:
                return user
    except Exception as e:
        raise AppException(str(e), status_code=500)
    return None
            