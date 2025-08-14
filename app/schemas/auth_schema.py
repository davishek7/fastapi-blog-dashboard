from pydantic import BaseModel, EmailStr, Field
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


class UserResponse(ResgisterSchema):
    pass


class ForgotPasswordSchema(BaseModel):
    email: EmailStr


class ResetPasswordSchema(BaseModel):
    new_password: str
