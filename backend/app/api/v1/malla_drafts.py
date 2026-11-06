"""PROTOTYPE (spike/ia-mallas): AI draft of a malla from an uploaded PDF or photo.

Enabled only in development with ANTHROPIC_API_KEY set, so nobody else spends the credits.
History (prototype only): each draft is saved as a JSON file under AI_DRAFTS_DIR, in one folder
per user, so it can be reviewed later. The uploaded document itself is never stored (D-08).
The body is the raw file (Content-Type application/pdf or image/*), so no multipart dependency.
"""

import asyncio
import json
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi import Path as PathParam
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.security import get_current_user
from app.models.user import User
from app.services.ai_malla import MEDIA_TYPES, compare, extract, to_draft, validate
from app.services.legacy_import import LEGACY_PROGRAMS

router = APIRouter(prefix="/me/malla-drafts", tags=["prototype"])

MAX_BYTES = 10 * 1024 * 1024
MALLAS_DIR = Path(__file__).resolve().parents[4] / "frontend" / "public" / "mallas"
COMPARABLE = {p.stem for p in LEGACY_PROGRAMS}
ALLOWED_MEDIA = set(MEDIA_TYPES.values())


class Tokens(BaseModel):
    entrada: int
    salida: int


class MallaDraftOut(BaseModel):
    id: uuid.UUID
    creado: datetime
    documento: str
    malla: dict[str, Any]
    advertencias: list[str]
    problemas: list[str]
    desconocidos: int
    modelo: str
    tokens: Tokens
    cortado: bool
    comparacion: dict[str, Any] | None


def get_ai_client() -> Any:
    """Anthropic client; tests override this dependency."""
    import anthropic

    return anthropic.Anthropic(api_key=get_settings().anthropic_api_key)


class MallaDraftSummary(BaseModel):
    id: uuid.UUID
    creado: datetime
    documento: str
    carrera: str
    ramos: int
    desconocidos: int
    modelo: str
    cobertura_pct: float | None


def get_drafts_dir() -> Path:
    """Where the prototype keeps its history; tests override this dependency."""
    return Path(get_settings().ai_drafts_dir)


def _user_dir(base: Path, user: User) -> Path:
    return base / str(user.id)


def _load(path: Path) -> MallaDraftOut:
    return MallaDraftOut.model_validate_json(path.read_text(encoding="utf-8"))


def _not_found() -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe ese borrador.")


def require_ai_enabled() -> None:
    settings = get_settings()
    if settings.environment != "development" or not settings.anthropic_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="La importación con IA no está habilitada en este servidor.",
        )


@router.post("", response_model=MallaDraftOut, dependencies=[Depends(require_ai_enabled)])
async def create_malla_draft(
    request: Request,
    user: Annotated[User, Depends(get_current_user)],
    client: Annotated[Any, Depends(get_ai_client)],
    drafts_dir: Annotated[Path, Depends(get_drafts_dir)],
    compare_with: Annotated[str | None, Query(max_length=64)] = None,
    filename: Annotated[str | None, Query(max_length=200)] = None,
) -> MallaDraftOut:
    media_type = (request.headers.get("content-type") or "").split(";")[0].strip().lower()
    if media_type not in ALLOWED_MEDIA:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Sube un PDF o una imagen (PNG, JPG, WEBP o GIF).",
        )
    if compare_with is not None and compare_with not in COMPARABLE:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe esa malla.")

    body = bytearray()
    async for chunk in request.stream():
        body.extend(chunk)
        if len(body) > MAX_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                detail="El archivo supera los 10 MB.",
            )
    if not body:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El archivo está vacío."
        )

    model = get_settings().ai_model
    try:
        result = await asyncio.to_thread(
            extract, bytes(body), media_type, client=client, model=model
        )
    except Exception as exc:  # API, network or malformed answer: never echo the document
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="No se pudo procesar el documento con la IA. Intenta de nuevo.",
        ) from exc

    draft = to_draft(result.raw)
    comparison = None
    if compare_with:
        verified = json.loads((MALLAS_DIR / f"{compare_with}.json").read_text(encoding="utf-8"))
        comparison = compare(draft.malla, verified)
    out = MallaDraftOut(
        id=uuid.uuid4(),
        creado=datetime.now(UTC),
        documento=Path(filename).name if filename else "documento",
        malla=draft.malla,
        advertencias=draft.warnings,
        problemas=validate(draft.malla),
        desconocidos=draft.unknown_courses,
        modelo=result.model,
        tokens=Tokens(entrada=result.input_tokens, salida=result.output_tokens),
        cortado=result.stop_reason == "max_tokens",
        comparacion=comparison,
    )
    folder = _user_dir(drafts_dir, user)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{out.id}.json").write_text(out.model_dump_json(), encoding="utf-8")
    return out


@router.get("", response_model=list[MallaDraftSummary], dependencies=[Depends(require_ai_enabled)])
async def list_malla_drafts(
    user: Annotated[User, Depends(get_current_user)],
    drafts_dir: Annotated[Path, Depends(get_drafts_dir)],
) -> list[MallaDraftSummary]:
    """The caller's own drafts, newest first."""
    folder = _user_dir(drafts_dir, user)
    items = [_load(p) for p in folder.glob("*.json")] if folder.is_dir() else []
    items.sort(key=lambda d: d.creado, reverse=True)
    return [
        MallaDraftSummary(
            id=d.id,
            creado=d.creado,
            documento=d.documento,
            carrera=d.malla.get("carrera") or "",
            ramos=sum(len(sem.get("cursos") or []) for sem in d.malla.get("semestres") or []),
            desconocidos=d.desconocidos,
            modelo=d.modelo,
            cobertura_pct=(d.comparacion or {}).get("cobertura_pct"),
        )
        for d in items
    ]


DraftId = Annotated[uuid.UUID, PathParam()]


@router.get("/{draft_id}", response_model=MallaDraftOut, dependencies=[Depends(require_ai_enabled)])
async def get_malla_draft(
    draft_id: DraftId,
    user: Annotated[User, Depends(get_current_user)],
    drafts_dir: Annotated[Path, Depends(get_drafts_dir)],
) -> MallaDraftOut:
    # The path is built from the caller's own folder and a parsed UUID: another user's draft,
    # or anything outside the folder, is simply not there (404).
    path = _user_dir(drafts_dir, user) / f"{draft_id}.json"
    if not path.is_file():
        raise _not_found()
    return _load(path)


@router.delete(
    "/{draft_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_ai_enabled)],
)
async def delete_malla_draft(
    draft_id: DraftId,
    user: Annotated[User, Depends(get_current_user)],
    drafts_dir: Annotated[Path, Depends(get_drafts_dir)],
) -> None:
    path = _user_dir(drafts_dir, user) / f"{draft_id}.json"
    if not path.is_file():
        raise _not_found()
    path.unlink()
