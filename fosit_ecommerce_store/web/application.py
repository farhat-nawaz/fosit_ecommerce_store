from importlib import metadata
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from fosit_ecommerce_store.db.config import TORTOISE_CONFIG
from fosit_ecommerce_store.logging import configure_logging
from fosit_ecommerce_store.web.api.router import api_router
from fosit_ecommerce_store.web.lifetime import (
    register_shutdown_event,
    register_startup_event,
)

APP_ROOT = Path(__file__).parent.parent


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="fosit_ecommerce_store",
        version=metadata.version("fosit_ecommerce_store"),
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    # Adds static directory.
    # This directory is used to access swagger files.
    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT / "static"),
        name="static",
    )

    # Configures tortoise orm.
    register_tortoise(
        app,
        config=TORTOISE_CONFIG,
        add_exception_handlers=True,
    )

    return app
