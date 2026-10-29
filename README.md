# MallaPro V2

Plataforma web para estudiantes universitarios chilenos: malla curricular con prerrequisitos, avance, notas, horario y toma de ramos.

## Estructura

| Carpeta | Contenido |
|---|---|
| `frontend/` | App React 19 + Vite + Tailwind (ver [frontend/README.md](frontend/README.md)) |
| `backend/` | API FastAPI (ver sección Backend) |
| `docker-compose.yml` | PostgreSQL 16 para desarrollo local |

## Cómo levantar

**Frontend** (Node 22, ver `frontend/.nvmrc`):

```bash
cd frontend
npm install
npm run dev      # http://localhost:5174
npm test         # vitest
npm run build    # salida en frontend/dist
```

**Levantar todo con Docker** (Postgres + backend + frontend, para probar):

```bash
cp .env.example .env          # ajusta POSTGRES_PASSWORD (solo letras y números: va dentro de una URL)
docker compose up --build     # la primera vez tarda: construye las imágenes e instala dependencias
```

- Frontend: http://localhost:5174 · API: http://localhost:8000/api/v1/health
- Al arrancar, el backend aplica las migraciones e importa las mallas de `frontend/public/mallas` (las dos cosas son idempotentes).
- Los cambios en `backend/` y `frontend/src/` se recargan solos.
- Si cambias dependencias: `uv.lock` se sincroniza al reiniciar el backend; `package-lock.json` hace que el frontend ejecute `npm ci` al arrancar.
- Login con Google: igual que sin Docker (`frontend/.env.local` y `backend/firebase-sa.json`); las carpetas están montadas.
- `docker compose down` para todo y conserva la base; `docker compose down -v` la borra.

**Infraestructura local** (solo Postgres, para correr backend y frontend en tu máquina):

```bash
cp .env.example .env   # ajusta POSTGRES_PASSWORD
docker compose up -d postgres
```

**Backend** (Python 3.12 con [uv](https://docs.astral.sh/uv/), FastAPI):

```bash
docker compose up -d postgres          # Postgres (desde la raíz)
cd backend
cp .env.example .env                   # la clave debe coincidir con POSTGRES_PASSWORD
uv sync
uv run alembic upgrade head
uv run python -m app.scripts.import_legacy_mallas ../frontend/public/mallas   # catálogo (idempotente)
uv run uvicorn app.main:app --reload   # http://localhost:8000/api/v1/health
uv run pytest
uv run ruff check
```

Los tests crean la base `mallapro_test` en el mismo Postgres si no existe.

**Login con Google (opcional):** el frontend funciona sin login. Para activarlo copia `frontend/.env.example` a `frontend/.env.local` y coloca `firebase-sa.json` (service account, ignorado por git) en `backend/`. Los tests aplican las migraciones de Alembic sobre `mallapro_test`.

## Despliegue del frontend

Netlify: *Base directory* = `frontend`. Vercel: *Root Directory* = `frontend`. cPanel: `cd frontend && npm run pack:cpanel`.

Reglas del proyecto y stack completo en [CLAUDE.md](CLAUDE.md).

## Documentación y trabajo con agentes

| Documento | Para qué |
|---|---|
| [AGENTS.md](AGENTS.md) | Reglas de trabajo, comandos y definición de terminado |
| [docs/requirements/](docs/requirements/requerimientos-v1.2.md) | Qué se construye (requisitos con ID) |
| [docs/plan/backlog.md](docs/plan/backlog.md) | Tareas con alcance y criterios de aceptación |
| [docs/plan/traceability.md](docs/plan/traceability.md) | Requisito → tarea → prueba |
| [docs/plan/decisions.md](docs/plan/decisions.md) | Decisiones pendientes |
| [docs/process/](docs/process/workflow.md) | Flujo de trabajo y auditoría de cada cambio |
| [docs/architecture/](docs/architecture/architecture.md) | Arquitectura, modelo de datos y API |
| [docs/adr/](docs/adr/README.md) | Decisiones técnicas |
| [docs/data/mallas.md](docs/data/mallas.md) | Mallas del catálogo y cómo verificarlas |
| [docs/audits/](docs/audits/README.md) | Registro de auditorías |

Con Claude Code: `/task T-0XX` implementa una tarea y `/audit T-0XX` la audita en otra sesión.
