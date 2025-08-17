# app/domain/posts/models.py
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.domain.comments.models import Comment
    from app.domain.series.models import Series


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    excerpt: Mapped[Optional[str]] = mapped_column(String(500))
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    series_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("series.id"))
    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
    image_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationship to comments
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )
    series: Mapped[Optional["Series"]] = relationship("Series", back_populates="posts")

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r}, author={self.author!r})"
