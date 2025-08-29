from .database import get_db
from ..services.blog_service import BlogService
from ..services.contact_service import ContactService
from ..services.auth_service import AuthService
from ..services.token_service import TokenService
from ..services.trash_service import TrashService
from pymongo import DESCENDING


async def get_blog_service() -> BlogService:
    db = get_db()
    await db["blog"].create_index([("created_at", DESCENDING)])
    await db["blog"].create_index("slug", unique=True)
    return BlogService(db["blog"])


async def get_contact_service() -> ContactService:
    db = get_db()
    await db["contact"].create_index([("created_at", DESCENDING)])
    return ContactService(db["contact"])


async def get_auth_service() -> AuthService:
    db = get_db()
    await db["auth"].create_index("email", unique=True)
    await db["auth"].create_index("username", unique=True)
    return AuthService(db["auth"])


async def get_email_verification_token_service() -> TokenService:
    db = get_db()
    return TokenService(db["email_verification_token"])


async def get_password_reset_token_service() -> TokenService:
    db = get_db()
    await db["password_reset_token"].create_index("expires_at", expireAfterSeconds=0)
    return TokenService(db["password_reset_token"])


async def get_trashed_blog_service() -> TrashService:
    db = get_db()
    await db["blog"].create_index([("deleted_at", DESCENDING)])
    return TrashService(db["blog"], lookup_field="slug")


async def get_trashed_contact_service() -> TrashService:
    db = get_db()
    await db["contact"].create_index([("deleted_at", DESCENDING)])
    return TrashService(db["contact"], lookup_field="_id")
