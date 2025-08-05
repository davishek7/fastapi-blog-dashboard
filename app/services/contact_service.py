from fastapi import status
from ..schemas.contact_schema import ContactCreateSchema
from ..utils.contact import serialize_contact
from bson import ObjectId
from ..exceptions.custom_exception import AppException
from ..utils.response import success_response


class ContactService:
    def __init__(self, collection):
        self.collection = collection

    async def create(self, contact_create_schema: ContactCreateSchema):
        contact = contact_create_schema.model_dump()
        result = await self.collection.insert_one(contact)
        return success_response(
            "Message sent successfully",
            status.HTTP_201_CREATED,
            data={"contact_id": str(result.inserted_id)},
        )

    async def get_all(self):
        cursor = self.collection.find()
        contacts = []
        async for doc in cursor:
            contacts.append(serialize_contact(doc))
        if not contacts:
            return success_response("No contacts found", status.HTTP_200_OK, data=[])
        return success_response(
            "Contacts fetched successfully", status.HTTP_200_OK, data=contacts
        )

    async def get(self, contact_id: str):
        contact = await self.collection.find_one({"_id": ObjectId(contact_id)})
        if not contact:
            raise AppException("Contact not found", status.HTTP_404_NOT_FOUND)
        return success_response(
            "Contact fetched successfully",
            status.HTTP_200_OK,
            data=serialize_contact(contact),
        )
