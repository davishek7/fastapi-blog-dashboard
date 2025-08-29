from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime, timezone
from .auth_schema import UserResponse


class BlogUpdateSchema(BaseModel):
    title: str
    subtitle: str
    content: str
    is_active: bool = Field(default=True)


class BlogCreateSchema(BlogUpdateSchema):
    deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BlogResponse(BaseModel):
    id: str
    title: str
    subtitle: str
    slug: str
    content: str
    created_at: str
    is_active: bool
    author: UserResponse
    deleted: bool
    deleted_at: Optional[datetime] = None


class PaginatedResponse(BaseModel):
    posts: List[BlogResponse]
    limit: int
    offset: int
    total: int
