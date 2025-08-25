# app/domain/series/models.py
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.domain.posts.models import Post



class Series(Base):
    __tablename__ = "series"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    thumbnail: Mapped[Optional[str]] = mapped_column(String)

    # Relationship: one series → many posts
    posts: Mapped[List["Post"]] = relationship(
        "Post", back_populates="series", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Series(id={self.id!r}, name={self.name!r})"
