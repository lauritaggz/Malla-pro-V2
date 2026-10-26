# Arquitectura

```
Navegador ── React (frontend/) ──────────────── Firebase Auth (Google)
   │  modo sin backend: frontend/public/mallas/*.json + localStorage
   │  modo con backend: Authorization: Bearer <ID token de Firebase>
   ▼
FastAPI (backend/app) ── /api/v1
   ├── api/v1/      rutas: validan (Pydantic), autorizan y delegan
   ├── services/    lógica de negocio por módulo
   ├── models/      SQLAlchemy 2 (async)
   ├── schemas/     Pydantic v2 (entrada y salida)
   └── core/        configuración, Firebase, seguridad
   ▼
PostgreSQL 16 (Alembic) ── cola de tareas en Postgres (ADR-0004)
```

## Estado actual (26-10-2026)

| Parte | Estado | Dónde |
|---|---|---|
| Base del backend: FastAPI, SQLAlchemy async, Alembic, salud, CORS | Hecho (s01) | `backend/app/main.py`, `api/v1/health.py` |
| Login con Google: verificación del token y tabla `users` | Hecho (s02) | `core/security.py`, `api/v1/me.py`, `frontend/src/features/auth/` |
| Catálogo: universidades, carreras, versiones, menciones, cursos, alias; importación de las mallas legadas; API pública | Hecho (s03) | `models/catalog.py`, `services/legacy_import.py`, `api/v1/catalog.py`, `frontend/src/utils/curriculumApi.js` |
| Malla, avance, notas, excepciones, horario, toma de ramos, compartir configuración | Funciona **solo en el navegador** (`localStorage`) | `frontend/src/components/`, `frontend/src/utils/`, `frontend/src/features/academicProgramming/` |
| Directorio de tutores | Maqueta local con datos de ejemplo | `frontend/src/components/tutors/`, `frontend/src/data/tutorsStorage.js` |
| Avance, notas y horario guardados en el backend; roles; auditoría; tutores reales | Pendiente | `docs/plan/backlog.md` |

El frontend usa la API si `VITE_API_URL` responde y, si no, vuelve a las mallas estáticas. Ese modo sin backend se mantiene: es la versión pública actual.

## Reglas de dependencia

| Desde | Puede usar | No puede usar |
|---|---|---|
| `api/v1/*` | `services`, `schemas`, `core.security` | consultas SQL directas a tablas de otro módulo |
| `services/<módulo>` | sus `models`, otros servicios por su interfaz pública | `fastapi` (salvo excepciones de dominio propias) |
| `models` | `db.base` | `services`, `api` |
| Reglas académicas del frontend (`frontend/src/utils/*` puros) | datos que reciben por parámetro | `fetch`, `localStorage`, `Date.now()` implícito |

## Reglas transversales

- **Autorización:** toda ruta con datos de usuario depende de `get_current_user` y filtra por `user.id`. Las rutas del equipo dependen además de un guardia de rol (T-002).
- **Errores:** formato de FastAPI `{"detail": "<mensaje en español>"}`, que es lo que lee `frontend/src/lib/api.js`. Ver `docs/architecture/api.md`.
- **Concurrencia e idempotencia:** ADR-0009.
- **Fechas:** se guardan en UTC (`DateTime(timezone=True)`); la interfaz muestra en `America/Santiago`. Las reglas reciben la fecha como parámetro.
- **Logs:** nunca tokens, notas, correos completos ni contenido de documentos (NF-07).
