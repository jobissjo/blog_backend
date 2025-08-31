# app/domain/posts/models.py
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Integer, String, Text, DateTime, func, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.domain.comments.models import Comment
    from app.domain.series.models import Series
    from app.domain.users.models import User


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    excerpt: Mapped[Optional[str]] = mapped_column(String(500))
    author_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"))
    series_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("series.id"))
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
    tags: Mapped[List["Tag"]] = relationship(
        "Tag", secondary="post_tags", back_populates="posts"
    )
    author: Mapped[Optional["User"]] = relationship("User", back_populates="posts")


    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r}, author={self.author!r})"


post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationship to posts
    posts: Mapped[List["Post"]] = relationship(
        "Post", secondary=post_tags, back_populates="tags"
    )

    def __repr__(self) -> str:
        return f"Tag(id={self.id!r}, name={self.name!r})"