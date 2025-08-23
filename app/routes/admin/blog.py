from fastapi import APIRouter, Query, Depends, Security
from ...schemas.blog_schema import BlogCreateSchema, BlogUpdateSchema
from ...configs.dependency import get_blog_service
from fastapi_jwt import JwtAuthorizationCredentials
from ...utils.auth import access_security


router = APIRouter()


@router.get("/")
async def post_list(
    limit: int = Query(10, gt=0),
    offset: int = Query(0, ge=0),
    blog_service=Depends(get_blog_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await blog_service.get_all(limit, offset, include_inactive=True)


@router.get("/{slug}")
async def get_post(
    slug: str,
    blog_service=Depends(get_blog_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    user_id = credentials["user_id"]
    return await blog_service.get(slug, user_id)


@router.post("/")
async def post_create(
    blog_create_schema: BlogCreateSchema,
    blog_service=Depends(get_blog_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    user_id = credentials["user_id"]
    return await blog_service.create(blog_create_schema, user_id)


@router.put("/{blog_id}")
async def post_update(
    blog_id: str,
    blog_update_schema: BlogUpdateSchema,
    blog_service=Depends(get_blog_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    user_id = credentials["user_id"]
    return await blog_service.update(blog_id, blog_update_schema)


@router.patch("/{blog_id}")
async def post_status_update(
    blog_id: str,
    blog_service=Depends(get_blog_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await blog_service.update_status(blog_id)


@router.delete("/{blog_id}")
async def post_delete(
    blog_id: str,
    blog_service=Depends(get_blog_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    user_id = credentials["user_id"]
    return await blog_service.delete(blog_id)
