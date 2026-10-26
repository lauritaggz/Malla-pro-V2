# ADR-0007 · `career_key` estable para el avance guardado

- Estado: aceptado (implementado en s03)
- Fecha: 2026-10-26

## Contexto
La versión pública guarda el avance en `localStorage` por carrera e id de curso. Si la clave de carrera cambia, el estudiante pierde su avance.

## Decisión
Cada carrera tiene un `career_key` único e inmutable. Para las mallas legadas se calcula desde su URL con la misma función en el frontend (`getCareerId`) y en el backend (`career_key_from_url`); las nuevas usan `universidad-carrera`.

## Consecuencias
Ambas funciones tienen pruebas con los mismos casos y no se modifican sin una migración de `localStorage`. Renombrar una carrera o un archivo de malla no cambia su `career_key`.
