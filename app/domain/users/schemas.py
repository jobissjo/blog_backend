# app/domain/users/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List


class SocialMediaBase(BaseModel):
    name: str
    icon: Optional[str] = None
    base_url: Optional[str] = None

    class Config:
        from_attributes = True


class SocialMediaRead(SocialMediaBase):
    id: str

    class Config:
        from_attributes = True


class ProfileSocialLinkBase(BaseModel):
    social_media_id: str
    url: str

    class Config:
        from_attributes = True


class ProfileSocialLinkRead(ProfileSocialLinkBase):
    id: str
    social_media: SocialMediaRead

    class Config:
        from_attributes = True


class ProfileBase(BaseModel):
    profile_image: Optional[str] = None
    bio: Optional[str] = None
    profession: Optional[str] = None

    class Config:
        from_attributes = True


class ProfileRead(BaseModel):
    id: str
    social_links: List[ProfileSocialLinkRead]
    profile_image: Optional[str] = None
    bio: Optional[str] = None
    profession: Optional[str] = None

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")


class LoginSchema(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    role: str


class UserRead(BaseModel):
    id: str
    username: str
    email: str
    role: str
    profile: Optional[ProfileRead] = None

    class Config:
        from_attributes = True


class ChangePasswordSchema(BaseModel):
    old_password: str = Field(alias="oldPassword")
    new_password: str = Field(alias="newPassword")


class ForgotEmailPwdSchema(BaseModel):
    email: str


class VerifyEmailOtpSchema(BaseModel):
    email: str
    otp: str