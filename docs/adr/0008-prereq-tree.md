# ADR-0008 · Árbol de prerrequisitos y equivalencias

- Estado: aceptado
- Fecha: 2026-10-26

## Decisión
Nodos: `{"op": "and"|"or", "items": [...]}`, `{"course": <uuid>}`, `{"min_credits": n}` (`app/schemas/prereq.py`). Se agregará `{"semesters_completed": n}` para "Semestre 10 aprobado" (U. de Chile) cuando se cargue esa malla. Los requisitos oficiales de Banner se **podan** al plan vigente: los códigos de planes antiguos no van en el árbol, sino como `course_aliases` (equivalencias), y el texto oficial completo queda en `prereq_raw`.

## Consecuencias
- La UI hoy solo representa AND de cursos (`curriculumApi.js` lanza `UnsupportedPrereqError` con OR o créditos). Mientras eso no cambie, los árboles con OR se cargan como `unknown` o se mantiene el JSON estático.
- Ver `docs/data/verificacion-mallas-oficiales.md` para el criterio usado con textos ambiguos.
