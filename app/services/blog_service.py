from fastapi import status
from ..schemas.blog_schema import BlogCreateSchema, BlogUpdateSchema
from ..utils.serializers import serialize_blog
from slugify import slugify  # type: ignore
from ..utils.responses import success_response
from ..utils.shortcuts import get_object_or_404
from pymongo import DESCENDING
from bson import ObjectId
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
        blog = await get_object_or_404(self.collection, "slug", slug, "Post")
        return success_response(
            "Post fetched successfully", status.HTTP_200_OK, data=serialize_blog(blog)
        )

    async def update(self, blog_id: str, blog_update_schema: BlogUpdateSchema):
        await get_object_or_404(self.collection, "_id", ObjectId(blog_id), "Post")
        await self.collection.update_one(
            {"_id": ObjectId(blog_id)}, {"$set": blog_update_schema.model_dump()}
        )
        return success_response("Post updated successfully", status.HTTP_200_OK)

    async def delete(self, blog_id: str):
        await get_object_or_404(self.collection, "_id", ObjectId(blog_id), "Post")
        await self.collection.delete_one({"_id": ObjectId(blog_id)})
        return success_response("Post deleted successfully", status.HTTP_200_OK)
