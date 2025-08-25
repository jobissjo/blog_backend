# app/domain/users/schemas.py
import msgspec
from typing import Optional, List


class SocialMediaBase(msgspec.Struct):
    name: str
    icon: Optional[str] = None
    base_url: Optional[str] = None


class SocialMediaRead(msgspec.Struct):
    id: str
    name: str
    icon: Optional[str] = None
    base_url: Optional[str] = None


class ProfileSocialLinkBase(msgspec.Struct):
    social_media_id: str
    url: str


class ProfileSocialLinkRead(ProfileSocialLinkBase):
    id: str
    social_media: SocialMediaRead


class ProfileBase(msgspec.Struct):
    profile_image: Optional[str] = None
    bio: Optional[str] = None
    profession: Optional[str] = None


class ProfileRead(msgspec.Struct):
    id: str
    social_links: List[ProfileSocialLinkRead]
    profile_image: Optional[str] = None
    bio: Optional[str] = None
    profession: Optional[str] = None


class UserBase(msgspec.Struct):
    username: str
    email: str


class UserCreate(UserBase):
    password: str
    first_name: str = msgspec.field(name="firstName")
    last_name: str = msgspec.field(name="lastName")

class LoginSchema(msgspec.Struct):
    email: str
    password: str

class TokenResponse(msgspec.Struct):
    access_token: str
    refresh_token: str
    token_type: str
    role: str


class UserRead(msgspec.Struct):
    id: str
    username: str
    email: str
    role: str
    profile: Optional[ProfileRead] = None


class ChangePasswordSchema(msgspec.Struct):
    old_password: str = msgspec.field(name="oldPassword")
    new_password: str = msgspec.field(name="newPassword")

class ForgotEmailPwdSchema(msgspec.Struct):
    email: str

class VerifyEmailOtpSchema(msgspec.Struct):
    email: str
    otp: str