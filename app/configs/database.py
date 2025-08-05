from pymongo import AsyncMongoClient  # type: ignore
from fastapi import FastAPI
from .settings import settings
from contextlib import asynccontextmanager

client: AsyncMongoClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global client
    client = AsyncMongoClient(settings.MONGODB_URI)
    yield
    await client.close()


def get_db():
    if client is None:
        raise RuntimeError("MongoDB client is not initialized.")
    return client[settings.DB_NAME]
