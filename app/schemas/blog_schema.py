from pydantic import BaseModel, Field, EmailStr
from typing import List
from datetime import datetime, timezone
from .auth_schema import UserResponse


class BlogUpdateSchema(BaseModel):
    title: str
    subtitle: str
    content: str
    is_active: bool = Field(default=True)


class BlogCreateSchema(BlogUpdateSchema):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BlogResponse(BaseModel):
    id: str
    title: str
    subtitle: str
    slug: str
    content: str
    created_at: datetime
    is_active: bool
    author: UserResponse


class PaginatedResponse(BaseModel):
    posts: List[BlogResponse]
    limit: int
    offset: int
    total: int
