from fastapi import status
from pydantic import EmailStr
from ..exceptions.custom_exception import AppException
from ..schemas.auth_schema import (
    LoginSchema,
    ResgisterSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
)
from ..utils.responses import success_response
from ..utils.auth import hash_password, verify_password, generate_access_token
from ..utils.serializers import serialize_access_token
from ..signals.send_email_signal import send_email_signal
from ..services.token_service import TokenService


class AuthService:
    def __init__(self, collection):
        self.collection = collection

    async def authenticate_user(self, email: EmailStr, password: str):
        user = await self.collection.find_one({"email": email})
        if not user or not verify_password(password, user["password"]):
            raise AppException(
                "Invalid email or password!", status.HTTP_401_UNAUTHORIZED
            )

        subject = {
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
        }
        return generate_access_token(subject)

    async def user_login(self, login_schema: LoginSchema):
        login_data = login_schema.model_dump()
        token = await self.authenticate_user(
            login_data["email"], login_data["password"]
        )
        return success_response(
            "Login successful!", status.HTTP_200_OK, serialize_access_token(token)
        )

    async def user_register(
        self,
        register_schema: ResgisterSchema,
        email_verification_token_service: TokenService,
    ):
        user_data = register_schema.model_dump()
        user_data["password"] = hash_password(user_data["password"])
        result = await self.collection.insert_one(user_data)
        created_user = await self.collection.find_one({"_id": result.inserted_id})
        raw_token = await email_verification_token_service.create_token(
            created_user["_id"]
        )
        verification_link = (
            f"http://127.0.0.1:8000/api/auth/verify-email?token={raw_token}"
        )
        send_email_signal.send(
            "services.auth_service",
            subject="Please confirm your email address",
            recipients=[created_user["email"]],
            template_name="email/email_verification.html",
            context={
                "subject": "Please confirm your email address",
                "title": "Please confirm your email address",
                "full_name": created_user["username"],
                "verification_url": verification_link,
            },
        )
        return success_response(
            "Account created successfully. Please check your email to verify your account.",
            status.HTTP_201_CREATED,
        )

    async def verify_email(
        self, token: str, email_verification_token_service: TokenService
    ):
        token_data = await email_verification_token_service.validate_token(token)
        await self.collection.update_one(
            {"_id": token_data["user_id"]}, {"$set": {"is_active": True}}
        )
        await email_verification_token_service.mark_token_used(token)
        return success_response("Email verified successfully.", status.HTTP_200_OK)

    async def forgot_password(
        self,
        forgot_password_schema: ForgotPasswordSchema,
        password_reset_token_service: TokenService,
    ):
        data = forgot_password_schema.model_dump()
        user = await self.collection.find_one({"email": data["email"]})

        if user:
            raw_token = await password_reset_token_service.create_token(user["_id"])

            reset_link = (
                f"http://127.0.0.1:8000/api/auth/reset-password?token={raw_token}"
            )

            send_email_signal.send(
                "services.auth_service",
                subject="Password Reset Request",
                recipients=[user["email"]],
                template_name="email/password_reset.html",
                context={
                    "subject": "Password Reset Request",
                    "title": "Password Reset Request",
                    "full_name": user["username"],
                    "reset_url": reset_link,
                },
            )
        return success_response(
            "If an account exists with that email, a reset link has been sent.",
            status.HTTP_200_OK,
        )

    async def reset_password(
        self,
        token: str,
        reset_password_schema: ResetPasswordSchema,
        password_reset_token_service: TokenService,
    ):
        token_data = await password_reset_token_service.validate_token(token)
        new_password_hash = hash_password(
            reset_password_schema.model_dump()["new_password"]
        )
        await self.collection.update_one(
            {"_id": token_data["user_id"]}, {"$set": {"password": new_password_hash}}
        )
        await password_reset_token_service.mark_token_used(token)
        return success_response("Password reset successful", status.HTTP_200_OK)
