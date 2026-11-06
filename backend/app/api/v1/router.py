from fastapi import APIRouter

from app.api.v1 import catalog, health, malla_drafts, me

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(catalog.router)
api_router.include_router(me.router)
api_router.include_router(malla_drafts.router)
