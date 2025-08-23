from ..schemas.blog_schema import BlogResponse
from ..schemas.contact_schema import Contact
from ..schemas.auth_schema import UserResponse
from zoneinfo import ZoneInfo
from ..configs.settings import settings
from ..schemas.auth_schema import AccessToken


def serialize_access_token(token: str) -> AccessToken:
    return AccessToken(access_token=token, token_type="bearer")


def serialize_blog(blog: dict) -> BlogResponse:
    blog["id"] = str(blog["_id"])
    del blog["_id"]
    blog["created_at"] = blog["created_at"].astimezone(ZoneInfo(settings.TIMEZONE))
    blog["author"] = serialize_user(blog["author"])
    return BlogResponse(**blog)


def serialize_contact(contact: dict) -> Contact:
    contact["id"] = str(contact["_id"])
    del contact["_id"]
    contact["created_at"] = contact["created_at"].astimezone(
        ZoneInfo(settings.TIMEZONE)
    )
    return Contact(**contact)


def serialize_user(user: dict) -> UserResponse:
    user["id"] = str(user["_id"])
    del user["_id"]
    user["created_at"] = user["created_at"].astimezone(ZoneInfo(settings.TIMEZONE))
    return UserResponse(**user)
