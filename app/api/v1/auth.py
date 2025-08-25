from litestar import Controller,  post
from app.domain.users.auth_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.users.repository import UserRepository
from app.domain.users.schemas import LoginSchema, TokenResponse, UserCreate, UserRead,ChangePasswordSchema, ForgotEmailPwdSchema, VerifyEmailOtpSchema


class AuthController(Controller):
    path = "/api/v1/auth"
    tags = ["Auth"]

    @post("/login")
    async def login(self, data: LoginSchema, session: AsyncSession)->TokenResponse:
        auth_service = AuthService(UserRepository(session))
        return await auth_service.authenticate_user(data)
    
    @post("/register")
    async def register(self, data: UserCreate, session: AsyncSession)->UserRead:
        auth_service = AuthService(UserRepository(session))
        return await auth_service.register_user(data)
    
    @post("/change-password")
    async def change_password(self, data: ChangePasswordSchema, session: AsyncSession)->UserRead:
        auth_service = AuthService(UserRepository(session))
        return await auth_service.change_password(data)

    @post('/forgot-password')
    async def forgot_password(self, data: ForgotEmailPwdSchema, session: AsyncSession)->dict[str, str]:
        auth_service = AuthService(UserRepository(session))
        await auth_service.generate_forgot_otp(data.email)
        return {"message": "OTP sent to your email"}
    
    @post('/verify-otp')
    async def verify_otp(self, data: VerifyEmailOtpSchema, session: AsyncSession)->UserRead:
        auth_service = AuthService(UserRepository(session))
        await auth_service.verify_otp(data.email, data.otp)
        return {"message": "OTP verified"}
    

    @post('/reset-password')
    async def reset_password(self, data: ChangePasswordSchema, session: AsyncSession)->UserRead:
        auth_service = AuthService(UserRepository(session))
        return await auth_service.reset_password(data)
    


