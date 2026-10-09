import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.catalog import CurriculumRead, ProgramRead, UniversityRead
from app.services import catalog

router = APIRouter(tags=["catalog"])

CACHE_CONTROL = "public, max-age=300"

Db = Annotated[AsyncSession, Depends(get_db)]


@router.get("/universities", response_model=list[UniversityRead])
async def list_universities(response: Response, db: Db) -> list[UniversityRead]:
    response.headers["Cache-Control"] = CACHE_CONTROL
    return await catalog.list_universities(db)


@router.get("/universities/{slug}/programs", response_model=list[ProgramRead])
async def list_programs(slug: str, response: Response, db: Db) -> list[ProgramRead]:
    programs = await catalog.list_programs(db, slug)
    if programs is None:
        raise HTTPException(status_code=404, detail="Universidad no encontrada.")
    response.headers["Cache-Control"] = CACHE_CONTROL
    return programs


@router.get("/programs/{program_id}/curriculum", response_model=CurriculumRead)
async def get_curriculum(program_id: uuid.UUID, response: Response, db: Db) -> CurriculumRead:
    curriculum = await catalog.get_current_curriculum(db, program_id)
    if curriculum is None:
        raise HTTPException(status_code=404, detail="Malla no encontrada.")
    response.headers["Cache-Control"] = CACHE_CONTROL
    return curriculum
