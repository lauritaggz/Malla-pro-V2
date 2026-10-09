# MallaPro V2
Plataforma web para estudiantes universitarios chilenos: malla curricular con prerrequisitos, avance, notas (escala 1-7, eximición), horario, toma de ramos, directorio de tutores con contacto por WhatsApp, e importación de mallas y oferta académica desde PDF o imagen con IA. Debe servir para cualquier universidad, no solo UNAB.

## Stack
- frontend/: React 19, Vite, Tailwind, React Router. Auth con Firebase (Google).
- backend/: Python 3.12, FastAPI, SQLAlchemy 2 (async, asyncpg), Alembic, Pydantic v2, pytest, uv, ruff.
- PostgreSQL 16 y Redis 7 vía docker-compose en local.
- Firebase solo identifica al usuario: el backend verifica el ID token con firebase-admin. Todos los datos viven en Postgres.

## Reglas
- Interfaz y textos en español de Chile. Código, nombres de variables y commits en inglés.
- Nunca subir secretos: .env, firebase-sa*.json, claves de IA.
- Cada usuario solo puede leer y modificar sus propios datos; toda consulta de datos personales filtra por el usuario autenticado.
- Reglas académicas explícitas: distinguir "sin prerrequisitos" de "prerrequisitos desconocidos"; nunca inventar reglas.
- La IA nunca modifica datos sin revisión del usuario: produce borradores.
- Tests obligatorios para prerrequisitos, cálculo de notas, topes de horario y permisos.
- Antes de cambios grandes, mostrar un plan y esperar aprobación.
