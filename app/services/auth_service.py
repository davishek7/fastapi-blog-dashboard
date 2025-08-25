from fastapi import status
from pydantic import EmailStr
from bson import ObjectId
from ..exceptions.custom_exception import AppException
from ..schemas.auth_schema import (
    LoginSchema,
    ResgisterSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
    EmailVerificationSchema,
)
from ..utils.responses import success_response
from ..utils.auth import hash_password, verify_password, generate_auth_tokens
from ..utils.serializers import serialize_access_token, serialize_user
from ..signals.send_email_signal import send_email_signal
from ..services.token_service import TokenService
from ..configs.settings import settings


class AuthService:
    def __init__(self, collection):
        self.collection = collection

    async def authenticate_user(self, email: EmailStr, password: str):
        user = await self.collection.find_one({"email": email})
        if not user or not verify_password(password, user["password"]):
            raise AppException(
                "Invalid email or password!", status.HTTP_401_UNAUTHORIZED
            )
        if user and not user["is_active"]:
            raise AppException(
                "Please verify your email first.", status.HTTP_403_FORBIDDEN
            )

        sub = {
            "user_id": str(user["_id"]),
            "role": user["role"],
        }
        return {
            "user": serialize_user(user),
            "auth_tokens": generate_auth_tokens(sub),
        }

    async def user_login(self, login_schema: LoginSchema):
        login_data = login_schema.model_dump()
        user_with_token = await self.authenticate_user(
            login_data["email"], login_data["password"]
        )
        return success_response(
            "Login successful!", status.HTTP_200_OK, user_with_token
        )
    
    async def refresh(self, sub):
        return success_response("Tokens refreshed successfully.", status.HTTP_200_OK, data=generate_auth_tokens(sub))

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
            f"{settings.DASHBOARD_APP_URL}/auth/verify-email?token={raw_token}"
        )
        self.send_action_email(created_user, verification_link, "verify_account")
        return success_response(
            "Account created successfully. Please check your email to verify your account.",
            status.HTTP_201_CREATED,
        )

    async def verify_email(
        self, token: str, email_verification_token_service: TokenService
    ):
        token_data = await email_verification_token_service.decode_token(token)
        user = await self.collection.find_one({"_id": token_data["user_id"]})
        if not user:
            raise AppException("User not found.", status.HTTP_404_NOT_FOUND)
        if user["is_active"]:
            raise AppException(
                "Your email is already verified. Please log in.",
                status.HTTP_208_ALREADY_REPORTED,
            )
        record = await email_verification_token_service.validate_token(token)
        await self.collection.update_one(
            {"_id": user["_id"]}, {"$set": {"is_active": True}}
        )
        await email_verification_token_service.mark_token_used(token)
        return success_response("Email verified successfully.", status.HTTP_200_OK)

    async def resend_verification_email(
        self,
        email_verification_schema: EmailVerificationSchema,
        email_verification_token_service: TokenService,
    ):
        email = email_verification_schema.model_dump()["email"]
        user = await self.collection.find_one({"email": email})
        if user and not user["is_active"]:
            raw_token = await email_verification_token_service.create_token(user["_id"])
            verification_link = (
                f"{settings.DASHBOARD_APP_URL}/auth/verify-email?token={raw_token}"
            )
            self.send_action_email(user, verification_link, "verify_account")
        return success_response(
            "If an account exists with that email, a verification link has been sent.",
            status.HTTP_200_OK,
        )

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
                f"{settings.DASHBOARD_APP_URL}/auth/reset-password?token={raw_token}"
            )
            self.send_action_email(user, reset_link, "password_reset")
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
        token_data = await password_reset_token_service.decode_token(token)
        user = self.collection.find_one({"_id": token_data["user_id"]})
        if not user:
            raise AppException("User not found.", status.HTTP_404_NOT_FOUND)
        record = await password_reset_token_service.validate_token(token)
        new_password_hash = hash_password(
            reset_password_schema.model_dump()["new_password"]
        )
        await self.collection.update_one(
            {"_id": record["user_id"]}, {"$set": {"password": new_password_hash}}
        )
        await password_reset_token_service.mark_token_used(token)
        return success_response(
            "Password reset successful. Please login with your new password.",
            status.HTTP_200_OK,
        )

    async def profile(self, user_id: str):
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        return success_response(
            "User Profile fetched successfully",
            status.HTTP_200_OK,
            serialize_user(user),
        )

    def send_action_email(self, user: dict, url_with_token: str, action: str):
        if action == "verify_account":
            subject = "Please confirm your email address"
            template_name = "email/email_verification.html"
        elif action == "password_reset":
            subject = "Password Reset Request"
            template_name = "email/password_reset.html"

        send_email_signal.send(
            "services.auth_service",
            subject=subject,
            recipients=[user["email"]],
            template_name=template_name,
            context={
                "subject": subject,
                "title": subject,
                "full_name": user["username"],
                "url_with_token": url_with_token,
            },
        )
