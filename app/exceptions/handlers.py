from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from typing import Union
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)


def http_handler(_: Request, exc: HTTPException) -> JSONResponse:
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return JSONResponse(content={"error": exc.detail}, status_code=exc.status_code)


def validation_handler(_: Request, exc: Union[RequestValidationError, ValidationError]):
    logger.error(f"ValidationError: {exc.errors()[0]['msg']}")
    return JSONResponse(
        content=jsonable_encoder({"error": exc.errors(), "body": exc.body}),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
