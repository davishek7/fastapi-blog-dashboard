from fastapi import APIRouter, Depends, Security, Query
from typing import List
from ...configs.dependency import get_contact_service
from ...schemas.contact_schema import Contact
from fastapi_jwt import JwtAuthorizationCredentials
from ...utils.auth import access_security


router = APIRouter()


@router.get("/", response_model=List[Contact])
async def contact_list(
    limit: int = Query(5, gt=0),
    offset: int = Query(0, ge=0),
    contact_service=Depends(get_contact_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await contact_service.get_all(limit, offset)


@router.get("/{contact_id}", response_model=Contact)
async def get_contact(
    contact_id: str,
    contact_service=Depends(get_contact_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await contact_service.get(contact_id)


@router.patch("/{contact_id}")
async def update_contact(
    contact_id: str,
    contact_service=Depends(get_contact_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await contact_service.update(contact_id)


@router.delete("/{contact_id}")
async def delete_contact(
    contact_id: str,
    contact_service=Depends(get_contact_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await contact_service.delete(contact_id)
