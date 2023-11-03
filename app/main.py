import logging
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from asgi_correlation_id import CorrelationIdMiddleware

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.routers import api
from app.database.setup import get_engine, Base
from app.exceptions.handlers import http_handler, validation_handler

logger = logging.getLogger(__name__)


def get_app() -> FastAPI:
    get_settings.cache_clear()
    settings = get_settings()
    configure_logging(settings)
    logger.info("Starting Tasktracker application...")
    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(CorrelationIdMiddleware)

    application.add_exception_handler(HTTPException, http_handler)
    application.add_exception_handler(RequestValidationError, validation_handler)

    application.include_router(api.router)

    if settings.env_state != "test":
        Base.metadata.create_all(bind=get_engine())
    return application


app = get_app()
