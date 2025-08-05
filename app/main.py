from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import blog, contact, resume
from .configs.database import lifespan
from .exceptions.handlers import register_exception_handlers

app = FastAPI(
    title="Blog and Resume API",
    description="This API handles blogs, resumes, and more.",
    version="1.0.0",
    contact={
        "name": "Avishek Das",
        "email": "davishek7@gmail.com",
    },
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://avishek-blog.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

URL_PREFIX = "/api"

app.include_router(resume.router, prefix=f"{URL_PREFIX}/resume", tags=["Resume"])
app.include_router(contact.router, prefix=f"{URL_PREFIX}/contact", tags=["Contact"])
app.include_router(blog.router, prefix=f"{URL_PREFIX}/blog", tags=["Blog"])
