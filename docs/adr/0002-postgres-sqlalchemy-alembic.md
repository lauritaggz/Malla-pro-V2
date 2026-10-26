# ADR-0002 · PostgreSQL con SQLAlchemy 2 async y Alembic

- Estado: aceptado (implementado en s01)
- Fecha: 2026-10-26

## Decisión
PostgreSQL 16, SQLAlchemy 2 async (asyncpg) y migraciones con Alembic. Claves UUID y marcas `created_at`/`updated_at` (`IdTimestampMixin`). JSONB para árboles de prerrequisitos y atributos no modelados.

## Consecuencias
- Cada cambio de modelo va con su migración en el mismo PR, con `downgrade` funcional.
- Las pruebas aplican las migraciones sobre `mallapro_test` (`tests/conftest.py`); no se crean tablas con `create_all`.
- Valores cerrados se restringen con `CheckConstraint`, como en `models/catalog.py`.
