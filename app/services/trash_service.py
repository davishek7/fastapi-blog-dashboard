from fastapi import status
from bson import ObjectId
from ..utils.responses import success_response


class TrashService:
    def __init__(self, collection, lookup_field="_id"):
        self.collection = collection
        self.lookup_field = lookup_field

    async def get_trashed(
        self,
        serializer,
        item_type: str,
        limit: int,
        offset: int,
    ):
        query = {"deleted": True}
        trashed_items_count = await self.collection.count_documents(query)
        trashed_cursor = self.collection.find(query).sort({"deleted_at": -1}).skip(offset).limit(limit)
        trashed_items = [
            serializer(trashed_item) async for trashed_item in trashed_cursor
        ]
        if not trashed_items:
            return success_response(
                f"No trashed {item_type} found",
                status.HTTP_200_OK,
                {
                    f"trashed_{item_type}": [],
                    "limit": limit,
                    "offset": offset,
                    "total": trashed_items_count,
                },
            )
        return success_response(
            f"Trashed {item_type} fetched successfully",
            status.HTTP_200_OK,
            {
                f"trashed_{item_type}": trashed_items,
                "limit": limit,
                "offset": offset,
                "total": trashed_items_count,
            },
        )

    async def restore(self, identifier, item_type: str):
        query = self._build_query(identifier)
        await self.collection.update_one(
            query, {"$set": {"deleted": False, "deleted_at": None}}
        )
        return success_response(
            f"{item_type} restored successfully", status.HTTP_200_OK
        )

    async def delete(self, identifier, item_type: str):
        query = self._build_query(identifier)
        await self.collection.delete_one(query)
        return success_response(f"{item_type} deleted successfully", status.HTTP_200_OK)

    def _build_query(self, identifier):
        if self.lookup_field == "_id":
            return {"_id": ObjectId(identifier)}
        return {self.lookup_field: identifier}
