from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
from .configs.settings import settings
from .routes import blog, contact, auth
from .routes.admin import blog as blog_admin, contact as contact_admin
from .configs.database import lifespan
from .exceptions.handlers import register_exception_handlers

# this import will load the signals listeners
from .listeners import send_email_listener  # noqa


app = FastAPI(
    title="Blog, Contact and Dashboard API",
    description="This API handles blogs, dashboard, and more.",
    version="1.0.0",
    contact={
        "name": "Avishek Das",
        "email": "davishek7@gmail.com",
    },
    lifespan=lifespan,
)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

origins = [settings.BLOG_APP_URL, settings.RESUME_APP_URL, "http://localhost:5173"]
print(origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Avishek Das - FastAPI server with docs.",
            "subtitle": "This API handles blogs, dashboard, and more.",
            "resume_app_url": settings.RESUME_APP_URL,
            "blog_app_url": settings.BLOG_APP_URL,
            "resume_url": settings.RESUME_URL,
            "api_docs": "/docs",
            "current_year": datetime.now().year,
        },
    )


@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": status.HTTP_200_OK, "message": "OK"}


URL_PREFIX = "/api"
ADMIN_PREFIX = f"{URL_PREFIX}/admin"

# Auth routes
app.include_router(auth.router, prefix=f"{URL_PREFIX}/auth", tags=["Authentication"])

# Public routes
app.include_router(blog.router, prefix=f"{URL_PREFIX}/blog", tags=["Blog"])
app.include_router(contact.router, prefix=f"{URL_PREFIX}/contact", tags=["Contact"])

# Admin routes
app.include_router(
    blog_admin.router, prefix=f"{ADMIN_PREFIX}/blog", tags=["Blog Admin"]
)
app.include_router(
    contact_admin.router, prefix=f"{ADMIN_PREFIX}/contact", tags=["Contact Admin"]
)
