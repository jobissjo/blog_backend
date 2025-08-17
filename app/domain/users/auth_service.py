from typing import Optional
from uuid import uuid4
from app.domain.users.repository import UserRepository
from app.domain.users.schemas import LoginSchema, UserCreate, TokenResponse
from app.utils import JWTHandler, PasswordHasher
from app.domain.users.models import User
from app.core.config import settings
from app.core.exceptions import AppException


class AuthService:
    """Service for handling user authentication operations."""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository,
        self.password_hasher = PasswordHasher()
        self.jwt_handler = JWTHandler(
            secret=settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
            expiration_hours=settings.JWT_EXPIRATION_HOURS
        )
    
    async def register_user(self, user_data: UserCreate) -> User:
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
        if await self._user_exists_by_email(user_data.email):
            raise AppException("User with this email already exists", status_code=400)
        
        # Hash password
        password_hash = self.password_hasher.hash_password(user_data.password)
        
        # Create user (implement your DB logic here)
        user = User(
            id=str(uuid4()),
            email=user_data.email,
            password_hash=password_hash
        )
        
        # Save to database
        await self._save_user(user)
        
        return user
    
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
        user = await self._get_user_by_email(login_data.email)
        if not user:
            raise AppException("Invalid credentials", status_code=401)
        
        # Verify password
        if not self.password_hasher.verify_password(login_data.password, user.password_hash):
            raise AppException("Invalid credentials", status_code=400)
        
        if not user.is_active:
            raise AppException("Account is deactivated", status_code=400)
        
        # Create tokens
        access_token = self.jwt_handler.create_access_token(
            user_id=str(user.id),
            email=user.email
        )
        refresh_token = self.jwt_handler.create_refresh_token(str(user.id))
        
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
    
    # Private helper methods (implement based on your DB)
    async def _user_exists_by_email(self, email: str) -> bool:
        """Check if user exists by email."""
        # Implement your database logic
        pass
    
    async def _get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        # Implement your database logic
        pass
    
    async def _get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        # Implement your database logic
        pass
    
    async def _save_user(self, user: User) -> None:
        """Save user to database."""
        # Implement your database logic
        pass