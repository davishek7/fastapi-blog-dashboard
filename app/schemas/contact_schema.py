from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone
from typing import Optional


class ContactCreateSchema(BaseModel):
    full_name: str
    email: EmailStr
    subject: str
    message: str
    from_app: str
    read_status: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted: bool
    deleted_at: Optional[datetime] = None


class Contact(ContactCreateSchema):
    id: str
    created_at: str
