from fastapi import APIRouter, Depends, Security
from ..schemas.auth_schema import (
    LoginSchema,
    ResgisterSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
    EmailVerificationSchema,
)
from ..configs.dependency import (
    get_auth_service,
    get_email_verification_token_service,
    get_password_reset_token_service,
)
from ..configs.settings import settings
from fastapi_jwt import JwtAuthorizationCredentials
from ..utils.auth import access_security, refresh_security


router = APIRouter()


@router.post("/login")
async def login(login_schema: LoginSchema, auth_service=Depends(get_auth_service)):
    return await auth_service.user_login(login_schema)

@router.post("/refresh")
async def refresh(credentials: JwtAuthorizationCredentials = Security(refresh_security), auth_service=Depends(get_auth_service)):
    sub = credentials.subject
    return await auth_service.refresh(sub)

if int(settings.ALLOW_REGISTRATION) == 1:

    @router.post("/register")
    async def register(
        register_schema: ResgisterSchema,
        email_verification_token_service=Depends(get_email_verification_token_service),
        auth_service=Depends(get_auth_service),
    ):
        return await auth_service.user_register(
            register_schema, email_verification_token_service
        )

    @router.get("/verify-email")
    async def verify_email(
        token: str,
        email_verification_token_service=Depends(get_email_verification_token_service),
        auth_service=Depends(get_auth_service),
    ):
        return await auth_service.verify_email(token, email_verification_token_service)

    @router.post("/resend-verification")
    async def resend_verification_email(
        email_verification_schema: EmailVerificationSchema,
        email_verification_token_service=Depends(get_email_verification_token_service),
        auth_service=Depends(get_auth_service),
    ):
        return await auth_service.resend_verification_email(
            email_verification_schema, email_verification_token_service
        )


@router.post("/forgot-password")
async def forgot_password(
    forgot_password_schema: ForgotPasswordSchema,
    password_reset_token_service=Depends(get_password_reset_token_service),
    auth_service=Depends(get_auth_service),
):
    return await auth_service.forgot_password(
        forgot_password_schema, password_reset_token_service
    )


@router.post("/reset-password")
async def reset_password(
    token: str,
    reset_password_schema: ResetPasswordSchema,
    password_reset_token_service=Depends(get_password_reset_token_service),
    auth_service=Depends(get_auth_service),
):
    return await auth_service.reset_password(
        token, reset_password_schema, password_reset_token_service
    )


@router.get("/profile")
async def user_profile(
    credentials: JwtAuthorizationCredentials = Security(access_security),
    auth_service=Depends(get_auth_service),
):
    user_id = credentials["user_id"]
    return await auth_service.profile(user_id)
