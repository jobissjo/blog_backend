import asyncio
from datetime import datetime, timedelta , timezone
from typing import Any, Dict, Optional
from functools import partial
import bcrypt
import jwt
from litestar.exceptions import NotAuthorizedException


class PasswordHasher:
    """Utility class for password hashing and verification using bcrypt with async support."""
    
    @staticmethod
    async def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt with salt asynchronously.
        
        Args:
            password: Plain text password to hash
            
        Returns:
            Hashed password as string
        """
        def _hash_password_sync(password: str) -> str:
            salt = bcrypt.gensalt()
            password_bytes = password.encode('utf-8')
            hashed = bcrypt.hashpw(password_bytes, salt)
            return hashed.decode('utf-8')
        
        # Run the CPU-intensive hashing in a thread pool
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _hash_password_sync, password)
    
    @staticmethod
    async def verify_password(password: str, hashed: str) -> bool:
        """
        Verify a password against its hash asynchronously.
        
        Args:
            password: Plain text password to verify
            hashed: Stored password hash
            
        Returns:
            True if password matches hash, False otherwise
        """
        def _verify_password_sync(password: str, hashed: str) -> bool:
            password_bytes = password.encode('utf-8')
            hashed_bytes = hashed.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        
        # Run the CPU-intensive verification in a thread pool
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _verify_password_sync, password, hashed)


class JWTHandler:
    """Utility class for JWT token creation and validation with async support."""
    
    def __init__(self, secret: str, algorithm: str = "HS256", expiration_hours: int = 24):
        """
        Initialize JWT handler with configuration.
        
        Args:
            secret: JWT secret key
            algorithm: JWT algorithm (default: HS256)
            expiration_hours: Token expiration time in hours (default: 24)
        """
        self.secret = secret
        self.algorithm = algorithm
        self.expiration_hours = expiration_hours
    
    async def create_access_token(self, user_id: str, email: str, extra_data: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a JWT access token asynchronously.
        
        Args:
            user_id: User's unique identifier
            email: User's email address
            extra_data: Additional data to include in token payload
            
        Returns:
            JWT token as string
        """
        def _create_token_sync() -> str:
            expire = datetime.now(timezone.utc) + timedelta(hours=self.expiration_hours)
            payload = {
                "sub": user_id,
                "email": email,
                "exp": expire,
                "iat": datetime.now(timezone.utc),
                "type": "access"
            }
            
            # Add extra data if provided
            if extra_data:
                payload.update(extra_data)
                
            return jwt.encode(payload, self.secret, algorithm=self.algorithm)
        
        # Run token creation in thread pool for consistency
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _create_token_sync)
    
    async def create_refresh_token(self, user_id: str) -> str:
        """
        Create a JWT refresh token with longer expiration asynchronously.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            JWT refresh token as string
        """
        def _create_refresh_token_sync() -> str:
            expire = datetime.now(timezone.utc) + timedelta(days=30)  # 30 days for refresh token
            payload = {
                "sub": user_id,
                "exp": expire,
                "iat": datetime.now(timezone.utc),
                "type": "refresh"
            }
            return jwt.encode(payload, self.secret, algorithm=self.algorithm)
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _create_refresh_token_sync)
    
    async def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Decode and validate a JWT token asynchronously.
        
        Args:
            token: JWT token to decode
            
        Returns:
            Token payload as dictionary
            
        Raises:
            NotAuthorizedException: If token is invalid or expired
        """
        def _decode_token_sync(token: str) -> Dict[str, Any]:
            try:
                payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
                return payload
            except jwt.ExpiredSignatureError:
                raise NotAuthorizedException("Token has expired")
            except jwt.InvalidTokenError:
                raise NotAuthorizedException("Invalid token")
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _decode_token_sync, token)
    
    async def get_user_id_from_token(self, token: str) -> str:
        """
        Extract user ID from JWT token asynchronously.
        
        Args:
            token: JWT token
            
        Returns:
            User ID as string
        """
        payload = await self.decode_token(token)
        return payload.get("user_id")
    
    async def is_token_valid(self, token: str) -> bool:
        """
        Check if token is valid without raising exceptions asynchronously.
        
        Args:
            token: JWT token to validate
            
        Returns:
            True if token is valid, False otherwise
        """
        try:
            await self.decode_token(token)
            return True
        except NotAuthorizedException:
            return False