from .database import get_db
from ..services.blog_service import BlogService
from ..services.contact_service import ContactService
from pymongo import DESCENDING


async def get_blog_service():
    db = get_db()
    await db["blog"].create_index([("created_at", DESCENDING)])
    return BlogService(db["blog"])


async def get_contact_service():
    db = get_db()
    await db["contact"].create_index([("created_at", DESCENDING)])
    return ContactService(db["contact"])