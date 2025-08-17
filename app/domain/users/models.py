# app/domain/users/models.py
from typing import Optional, List
from sqlalchemy import String, ForeignKey, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="user")  # "admin" or "user"
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    profile: Mapped["Profile"] = relationship(
        "Profile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), unique=True)
    profile_image: Mapped[Optional[str]] = mapped_column(String)
    bio: Mapped[Optional[str]] = mapped_column(Text)
    profession: Mapped[Optional[str]] = mapped_column(String(100))

    user: Mapped["User"] = relationship("User", back_populates="profile")
    social_links: Mapped[List["ProfileSocialLink"]] = relationship(
        "ProfileSocialLink", back_populates="profile", cascade="all, delete-orphan"
    )


class SocialMedia(Base):
    """
    Admin-defined social media platforms
    Example: Twitter, GitHub, LinkedIn
    """
    __tablename__ = "social_media"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    icon: Mapped[str] = mapped_column(String, nullable=True)  # maybe a URL or icon name
    base_url: Mapped[Optional[str]] = mapped_column(String)


class ProfileSocialLink(Base):
    """
    User-specific link for a social media platform.
    Links a profile with a SocialMedia type.
    """
    __tablename__ = "profile_social_links"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    profile_id: Mapped[str] = mapped_column(ForeignKey("profiles.id"))
    social_media_id: Mapped[str] = mapped_column(ForeignKey("social_media.id"))
    url: Mapped[str] = mapped_column(String, nullable=False)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="social_links")
    social_media: Mapped["SocialMedia"] = relationship("SocialMedia")
