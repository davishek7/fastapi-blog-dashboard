from fastapi import status
from ..schemas.blog_schema import BlogCreateSchema
from ..utils.blog import serialize_blog
from slugify import slugify  # type: ignore
from ..utils.response import success_response
from ..exceptions.custom_exception import AppException
from pymongo import DESCENDING
import asyncio


class BlogService:
    def __init__(self, collection):
        self.collection = collection

    async def create(self, blog_create_schema: BlogCreateSchema):
        blog = blog_create_schema.model_dump()
        result = await self.collection.insert_one(blog)

        blog_id = str(result.inserted_id)
        slug = f"{slugify(blog_create_schema.title)}-{blog_id}"

        await self.collection.update_one(
            {"_id": result.inserted_id}, {"$set": {"slug": slug}}
        )
        return success_response(
            "Post created successfully", status.HTTP_201_CREATED, {"blog_id": blog_id}
        )

    async def get_all(self, limit: int, offset: int):
        await asyncio.sleep(3)
        total = await self.collection.count_documents({})
        cursor = (
            self.collection.find()
            .sort("created_at", DESCENDING)
            .skip(offset)
            .limit(limit)
        )
        blogs = []
        async for blog in cursor:
            blogs.append(serialize_blog(blog))
        if not blogs:
            return success_response(
                "No posts found",
                status.HTTP_200_OK,
                {"posts": [], "limit": limit, "offset": offset, "total": total},
            )
        return success_response(
            "Posts fetched successfully",
            status.HTTP_200_OK,
            {"posts": blogs, "limit": limit, "offset": offset, "total": total},
        )

    async def get(self, slug: str):
        blog = await self.collection.find_one({"slug": slug})
        if not blog:
            raise AppException("Post not found", status.HTTP_404_NOT_FOUND)
        return success_response(
            "Post fetched successfully", status.HTTP_200_OK, data=serialize_blog(blog)
        )
