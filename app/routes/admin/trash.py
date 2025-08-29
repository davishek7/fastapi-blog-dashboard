from fastapi import APIRouter, Depends, Security, Query
from ...configs.dependency import get_trashed_blog_service, get_trashed_contact_service
from fastapi_jwt import JwtAuthorizationCredentials
from ...utils.auth import access_security
from ...utils.serializers import serialize_trashed_blog, serialize_trashed_contact


router = APIRouter()


@router.get("/blog")
async def trashed_blogs(
    limit: int = Query(10, gt=0),
    offset: int = Query(0, ge=0),
    trash_service=Depends(get_trashed_blog_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await trash_service.get_trashed(
        serialize_trashed_blog, "blogs", limit, offset
    )


@router.patch("/blog/restore/{slug}")
async def restore_trashed_blog(
    slug: str,
    trash_service=Depends(get_trashed_blog_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await trash_service.restore(slug, "Blog")


@router.delete("/blog/delete/{slug}")
async def delete_trashed_blog(
    slug: str,
    trash_service=Depends(get_trashed_blog_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await trash_service.delete(slug, "Blog")


@router.get("/contact")
async def trashed_contacts(
    limit: int = Query(10, gt=0),
    offset: int = Query(0, ge=0),
    trash_service=Depends(get_trashed_contact_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await trash_service.get_trashed(
        serialize_trashed_contact, "contacts", limit, offset
    )


@router.patch("/contact/restore/{contact_id}")
async def restore_trashed_contact(
    contact_id: str,
    trash_service=Depends(get_trashed_contact_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await trash_service.restore(contact_id, "Contact")


@router.delete("/contact/delete/{contact_id}")
async def delete_trashed_contact(
    contact_id: str,
    trash_service=Depends(get_trashed_contact_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await trash_service.delete(contact_id, "Contact")
