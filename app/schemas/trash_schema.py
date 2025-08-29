from pydantic import BaseModel
from typing import List


class TrashedBlog(BaseModel):
    id: str
    title: str
    slug: str
    deleted_at: str


class PaginatedTrashedBlog(BaseModel):
    total: int
    limit: int
    offset: int
    blogs: List[TrashedBlog]


class TrashedContact(BaseModel):
    id: str
    full_name: str
    email: str
    deleted_at: str


class PaginatedTrashedContact(BaseModel):
    total: int
    limit: int
    offset: int
    contacts: List[TrashedContact]
