from pydantic import BaseModel, Field
from typing import List
from datetime import datetime, timezone 


class BlogCreateSchema(BaseModel):
    title: str
    subtitle: str
    author: str
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Blog(BlogCreateSchema):
    id: str
    slug: str


class PaginatedResponse(BaseModel):
    posts: List[Blog]
    limit: int
    offset: int
    total: int
