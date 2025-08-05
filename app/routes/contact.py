from fastapi import APIRouter, Depends
from typing import List
from ..configs.dependency import get_contact_service
from ..schemas.contact_schema import ContactCreateSchema, Contact


router = APIRouter()


@router.post("/")
async def contact_create(
    contact_create_schema: ContactCreateSchema,
    contact_service=Depends(get_contact_service),
):
    return await contact_service.create(contact_create_schema)


@router.get("/", response_model=List[Contact])
async def contact_list(contact_service=Depends(get_contact_service)):
    return await contact_service.get_all()


@router.get("/{contact_id}", response_model=Contact)
async def get_contact(contact_id: str, contact_service=Depends(get_contact_service)):
    return await contact_service.get(contact_id)
