from ..schemas.blog_schema import Blog
from ..schemas.contact_schema import Contact
from zoneinfo import ZoneInfo
from ..configs.settings import settings
from ..schemas.auth_schema import AccessToken


def serialize_access_token(token: str) -> AccessToken:
    return AccessToken(access_token=token, token_type="bearer")


def serialize_blog(blog: dict) -> Blog:
    blog["id"] = str(blog["_id"])
    del blog["_id"]
    blog["created_at"] = blog["created_at"].astimezone(ZoneInfo(settings.TIMEZONE))
    return Blog(**blog)


def serialize_contact(contact: dict) -> Contact:
    contact["id"] = str(contact["_id"])
    del contact["_id"]
    contact["created_at"] = contact["created_at"].astimezone(
        ZoneInfo(settings.TIMEZONE)
    )
    return Contact(**contact)
