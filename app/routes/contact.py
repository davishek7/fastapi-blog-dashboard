from fastapi import APIRouter, Depends
from ..configs.dependency import get_contact_service
from ..schemas.contact_schema import ContactCreateSchema


router = APIRouter()


@router.post("/")
async def contact_create(
    contact_create_schema: ContactCreateSchema,
    contact_service=Depends(get_contact_service),
):
    return await contact_service.create(contact_create_schema)
