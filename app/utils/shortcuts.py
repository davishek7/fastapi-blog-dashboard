from fastapi import status
from pymongo.collection import Collection
from bson import ObjectId
from ..exceptions.custom_exception import AppException


async def get_object_or_404(
    collection: Collection, key: str, value: str | ObjectId, object_name: str
):
    doc = await collection.find_one({key: value})
    if not doc:
        raise AppException(f"{object_name} not found", status.HTTP_404_NOT_FOUND)
    return doc
