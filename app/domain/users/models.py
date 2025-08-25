# app/domain/users/models.py
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import DateTime, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.domain.comments.models import Comment



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="user")  # "admin" or "user"
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    profile: Mapped["Profile"] = relationship(
        "Profile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="user", cascade="all, delete-orphan")


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    icon: Mapped[str] = mapped_column(String, nullable=True)  # maybe a URL or icon name
    base_url: Mapped[Optional[str]] = mapped_column(String)


class ProfileSocialLink(Base):
    """
    User-specific link for a social media platform.
    Links a profile with a SocialMedia type.
    """
    __tablename__ = "profile_social_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"))
    social_media_id: Mapped[int] = mapped_column(ForeignKey("social_media.id"))
    url: Mapped[str] = mapped_column(String, nullable=False)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="social_links")
    social_media: Mapped["SocialMedia"] = relationship("SocialMedia")
    

class TempOtp(Base):
    __tablename__ = "temp_otp"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    otp: Mapped[str] = mapped_column(String(6), nullable=False)
    generated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))

    def __repr__(self):
        return f"TempOtp(id={self.id}, email={self.email}, otp={self.otp})"