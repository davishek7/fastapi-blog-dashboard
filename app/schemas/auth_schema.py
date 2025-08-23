from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime, timezone


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class ResgisterSchema(LoginSchema):
    username: str
    role: str = Field(default="admin")
    is_active: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    role: str
    is_active: bool
    created_at: datetime


class ForgotPasswordSchema(BaseModel):
    email: EmailStr


class ResetPasswordSchema(BaseModel):
    new_password: str


class EmailVerificationSchema(ForgotPasswordSchema):
    pass
