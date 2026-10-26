# Registro de decisiones (ADR)

Una decisión por archivo. Un ADR aceptado no se edita: si cambia, se escribe uno nuevo que lo reemplaza. Plantilla: `0000-template.md`.

| ADR | Decisión | Estado |
|---|---|---|
| [0001](0001-modular-monolith-fastapi.md) | Monolito modular con FastAPI | aceptado (implementado en s01) |
| [0002](0002-postgres-sqlalchemy-alembic.md) | PostgreSQL con SQLAlchemy 2 async y Alembic | aceptado (implementado en s01) |
| [0003](0003-firebase-auth.md) | Firebase solo identifica; los datos viven en Postgres | aceptado (implementado en s02) |
| [0004](0004-postgres-task-queue.md) | Cola de tareas en PostgreSQL, sin Redis | aceptado |
| [0005](0005-deterministic-academic-rules.md) | Reglas académicas deterministas, separadas de la IA | aceptado |
| [0006](0006-catalog-versioned.md) | Catálogo versionado con cursos normalizados | aceptado (implementado en s03) |
| [0007](0007-career-key.md) | `career_key` estable para el avance guardado | aceptado (implementado en s03) |
| [0008](0008-prereq-tree.md) | Árbol de prerrequisitos y equivalencias | aceptado |
| [0009](0009-optimistic-concurrency.md) | Concurrencia optimista e idempotencia | aceptado |
| [0010](0010-shared-without-grades.md) | Lo compartido nunca contiene notas | aceptado |
