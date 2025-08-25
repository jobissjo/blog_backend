from typing import Optional
from uuid import uuid4
from app.domain.users.repository import UserRepository
from app.domain.users.schemas import LoginSchema, UserCreate, TokenResponse, UserRead
from app.utils import JWTHandler, PasswordHasher
from app.domain.users.models import User
from app.core.config import settings
from app.core.exceptions import AppException
import random


class AuthService:
    """Service for handling user authentication operations."""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
        self.password_hasher = PasswordHasher()
        self.jwt_handler = JWTHandler(
            secret=settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
            expiration_hours=settings.JWT_EXPIRATION_HOURS
        )
    
    async def register_user(self, user_data: UserCreate) -> UserRead:
        """
        Register a new user with hashed password.
        
        Args:
            user_data: User registration data
            
        Returns:
            Created user instance
            
        Raises:
            ValidationException: If user already exists
        """
        # Check if user exists (implement your DB logic here)
        if await self.repository.get_by_email(user_data.email):
            raise AppException("User with this email already exists", status_code=400)
        
        # Hash password
        password_hash = await self.password_hasher.hash_password(user_data.password)
        
        # Create user (implement your DB logic here)
        user = User(
            email=user_data.email,
            password=password_hash,
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name

        )
        
        # Save to database
        user_instance = await self.repository.add_user(user)
        print(user_instance)

        
        
        return UserRead(
        id=user_instance.id,
        username=user_instance.username,
        email=user_instance.email,
        role=user_instance.role,
        profile=None
        )
    
    async def authenticate_user(self, login_data: LoginSchema) -> TokenResponse:
        """
        Authenticate user and return JWT tokens.
        
        Args:
            login_data: User login credentials
            
        Returns:
            Dictionary containing access token and refresh token
            
        Raises:
            NotAuthorizedException: If credentials are invalid
        """
        # Find user by email (implement your DB logic here)
        user = await self.repository.get_by_email(login_data.email)
        if not user:
            raise AppException("User with this email not exists", status_code=401)
        
        # Verify password
        if not self.password_hasher.verify_password(login_data.password, user.password):
            raise AppException("Invalid credentials", status_code=400)
        
        if not user.is_active:
            raise AppException("Account is deactivated", status_code=400)
        
        # Create tokens
        access_token = await self.jwt_handler.create_access_token(
            user_id=str(user.id),
            email=user.email
        )
        refresh_token = await self.jwt_handler.create_refresh_token(str(user.id))
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "role": user.role
        }
    
    async def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        """
        Create new access token using refresh token.
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            New access token
        """
        payload = self.jwt_handler.decode_token(refresh_token)
        
        if payload.get("type") != "refresh":
            raise AppException("Invalid refresh token", status_code=400)
        
        user_id = payload.get("user_id")
        user = await self._get_user_by_id(user_id)
        
        if not user or not user.is_active:
            raise AppException("User not found or inactive", status_code=400)
        
        access_token = self.jwt_handler.create_access_token(
            user_id=str(user.id),
            email=user.email
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": self.jwt_handler.expiration_hours * 3600
        }

    async def generate_forgot_otp(self, email: str) -> str:
        user = await self.repository.get_by_email(email)
        if not user:
            raise AppException("User with this email not exists", status_code=400)
        
        otp = random.randint(100000, 999999)
        self.repository.create_or_update_temp_otp(user, otp)

    async def verify_otp(self, email: str, otp: str) -> User:
        user = await self.repository.get_by_email(email)
        if not user:
            raise AppException("User with this email not exists", status_code=400)
        
        temp_otp = await self.repository.get_email_otp(email)
        print(temp_otp)
        if not temp_otp or temp_otp.otp != otp:
            raise AppException("Invalid OTP", status_code=400)
        

    
    