from fastapi import APIRouter, Query, Depends
from ..schemas.blog_schema import BlogCreateSchema
from ..configs.dependency import get_blog_service


router = APIRouter()


@router.get("/")
async def post_list(
    limit: int = Query(10, gt=0),
    offset: int = Query(0, ge=0),
    blog_service=Depends(get_blog_service),
):
    return await blog_service.get_all(limit, offset)


@router.get("/{slug}")
async def get_post(slug: str, blog_service=Depends(get_blog_service)):
    return await blog_service.get(slug)


@router.post("/")
async def post_create(
    blog_create_schema: BlogCreateSchema, blog_service=Depends(get_blog_service)
):
    return await blog_service.create(blog_create_schema)
