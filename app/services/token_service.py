import secrets
import hashlib
from fastapi import status
from datetime import datetime, timedelta, timezone
from ..configs.settings import settings
from ..exceptions.custom_exception import AppException


class TokenService:
    def __init__(self, collection):
        self.collection = collection

    @staticmethod
    def _generate_token_hash(token: str):
        return hashlib.sha256(token.encode()).hexdigest()

    @staticmethod
    def _generate_token():
        token = secrets.token_urlsafe(32)
        token_hash = TokenService._generate_token_hash(token)
        return token, token_hash

    async def create_token(self, user_id):
        token, token_hash = TokenService._generate_token()
        token_data = {
            "user_id": user_id,
            "token_hash": token_hash,
            "expires_at": datetime.now(timezone.utc)
            + timedelta(hours=int(settings.VERIFICATION_TOKEN_EXPIRE_TIMEDELTA)),
            "used": False,
        }
        await self.collection.insert_one(token_data)
        return token

    async def validate_token(self, token: str):
        token_hash = TokenService._generate_token_hash(token)
        record = await self.collection.find_one(
            {"token_hash": token_hash, "used": False}
        )
        if not record or record["expires_at"].replace(
            tzinfo=timezone.utc
        ) < datetime.now(timezone.utc):
            raise AppException(
                "Verification link has expired. Please request a new one.",
                status.HTTP_410_GONE,
            )
        return record

    async def mark_token_used(self, token: str):
        token_hash = TokenService._generate_token_hash(token)
        await self.collection.update_one(
            {"token_hash": token_hash}, {"$set": {"used": True}}
        )
