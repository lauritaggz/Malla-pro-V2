# ADR-0006 · Catálogo versionado con cursos normalizados

- Estado: aceptado (implementado en s03)
- Fecha: 2026-10-26

## Decisión
`universities` → `programs` → `curriculum_versions` → `tracks` (menciones) y `courses`. Una sola versión `is_current` por carrera. Cada curso guarda `prereq_status` (`none` / `known` / `unknown`), el árbol `prereq_expr` (JSONB), el texto original `prereq_raw` y lo no modelado en `attrs`. Los códigos alternativos van en `course_aliases`.

## Consecuencias
- Una versión publicada no se edita: un cambio crea otra versión (CA-03).
- `legacy_id` conserva el id numérico del JSON, porque el avance guardado en el navegador depende de él.
- `prereq_status = "unknown"` nunca se muestra como disponible.
