from ..schemas.blog_schema import BlogResponse
from ..schemas.contact_schema import Contact
from ..schemas.auth_schema import UserResponse
from ..schemas.trash_schema import TrashedBlog, TrashedContact
from zoneinfo import ZoneInfo
from ..configs.settings import settings
from .response_sanitizer import strip_html
from .datetime_formatter import format_datetime


def serialize_blog(blog: dict) -> BlogResponse:
    blog["id"] = str(blog["_id"])
    del blog["_id"]
    blog["created_at"] = format_datetime(blog["created_at"])
    blog["author"] = serialize_user(blog["author"])
    blog["content"] = strip_html(blog["content"])
    return BlogResponse(**blog)


def serialize_contact(contact: dict) -> Contact:
    contact["id"] = str(contact["_id"])
    del contact["_id"]
    contact["created_at"] = format_datetime(contact["created_at"])
    return Contact(**contact)


def serialize_user(user: dict) -> UserResponse:
    user["id"] = str(user["_id"])
    del user["_id"]
    user["created_at"] = user["created_at"].astimezone(ZoneInfo(settings.TIMEZONE))
    return UserResponse(**user)


def serialize_trashed_blog(blog: dict) -> TrashedBlog:
    blog["id"] = str(blog["_id"])
    del blog["_id"]
    blog["deleted_at"] = format_datetime(blog["deleted_at"])
    return TrashedBlog(**blog)


def serialize_trashed_contact(contact: dict) -> TrashedContact:
    contact["id"] = str(contact["_id"])
    del contact["_id"]
    contact["deleted_at"] = format_datetime(contact["deleted_at"])
    return TrashedContact(**contact)
