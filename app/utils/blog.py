from ..schemas.blog_schema import Blog
from zoneinfo import ZoneInfo
from ..configs.settings import settings


def serialize_blog(blog: dict) -> Blog:
    blog["id"] = str(blog["_id"])
    del blog["_id"]
    blog["created_at"] = blog["created_at"].astimezone(ZoneInfo(settings.TIMEZONE))
    return Blog(**blog)