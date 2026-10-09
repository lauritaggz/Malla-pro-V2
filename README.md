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

**Infraestructura local** (Postgres):

```bash
cp .env.example .env   # ajusta POSTGRES_PASSWORD
docker compose up -d
```

**Backend** (Python 3.12 con [uv](https://docs.astral.sh/uv/), FastAPI):

```bash
docker compose up -d                   # Postgres (desde la raíz)
cd backend
cp .env.example .env                   # la clave debe coincidir con POSTGRES_PASSWORD
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload   # http://localhost:8000/api/v1/health
uv run pytest
uv run ruff check
```

Los tests crean la base `mallapro_test` en el mismo Postgres si no existe.

## Despliegue del frontend

Netlify: *Base directory* = `frontend`. Vercel: *Root Directory* = `frontend`. cPanel: `cd frontend && npm run pack:cpanel`.

Reglas del proyecto y stack completo en [CLAUDE.md](CLAUDE.md).
