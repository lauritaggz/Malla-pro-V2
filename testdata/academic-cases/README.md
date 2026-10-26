# Casos de referencia académicos

Casos en JSON (entrada y resultado esperado) para las reglas académicas: prerrequisitos, avance, notas y topes. Los usan las pruebas del frontend y, cuando exista la misma regla en el backend, también las de Python (ADR-0005), para que ambas implementaciones den el mismo resultado.

Se crean en T-012 (`prerequisites.json`), T-013 (`grades.json`), T-014 (`schedule-overlaps.json`) y T-016 (`progress.json`). Cada caso lleva un `id`, una descripción en español y, si sale de una malla real, la carrera y el curso.
