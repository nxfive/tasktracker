from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import get_settings
from routers import api
from database.setup import get_engine, Base


def get_app() -> FastAPI:
    get_settings.cache_clear()
    settings = get_settings()
    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(api.router)

    if settings.env_state != "test":
        Base.metadata.create_all(bind=get_engine())
    return application


app = get_app()
