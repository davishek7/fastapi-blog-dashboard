from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
from .routes import blog, contact
from .configs.database import lifespan
from .exceptions.handlers import register_exception_handlers


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

origins = ["https://avishek-blog.vercel.app"]

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
            "resume_url": "https://davishek7.github.io",
            "blog_url": "https://avishek-blog.vercel.app",
            "api_docs": "/docs",
            "current_year": datetime.now().year,
        },
    )


URL_PREFIX = "/api"

app.include_router(contact.router, prefix=f"{URL_PREFIX}/contact", tags=["Contact"])
app.include_router(blog.router, prefix=f"{URL_PREFIX}/blog", tags=["Blog"])
