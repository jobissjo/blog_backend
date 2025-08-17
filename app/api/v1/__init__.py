from app.api.v1.posts import PostController
from app.api.v1.series import SeriesController
from app.api.v1.comments import CommentController
from app.api.v1.users import UserController
from app.api.v1.auth import AuthController

__all__ = [
    "PostController",
    "SeriesController",
    "CommentController",
    "UserController",
    "AuthController",
]
