from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings

DEV_ORIGIN_REGEX = r"^http://(localhost|127\.0\.0\.1):\d+$"


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="MallaPro API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        # Any local port in development only; production sticks to CORS_ORIGINS.
        allow_origin_regex=DEV_ORIGIN_REGEX if settings.environment == "development" else None,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["Authorization", "Content-Type"],
    )
    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()
