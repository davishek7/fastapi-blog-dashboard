from ..schemas.contact_schema import Contact
from zoneinfo import ZoneInfo
from ..configs.settings import settings


def serialize_contact(contact: dict) -> Contact:
    contact["id"] = str(contact["_id"])
    del contact["_id"]
    contact["created_at"] = contact["created_at"].astimezone(
        ZoneInfo(settings.TIMEZONE)
    )
    return Contact(**contact)
