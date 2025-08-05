from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone


class ContactCreateSchema(BaseModel):
    full_name: str
    email: EmailStr
    subject: str
    message: str
    from_app: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Contact(ContactCreateSchema):
    id: str
