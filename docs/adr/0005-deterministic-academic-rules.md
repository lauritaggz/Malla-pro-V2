# ADR-0005 · Reglas académicas deterministas, separadas de la IA

- Estado: aceptado
- Fecha: 2026-10-26

## Contexto
Disponibilidad, notas y topes tienen que ser reproducibles y explicables (AV-04, NO-01, HO-02, PA-03). La IA puede inventar. Hay dos lenguajes (JS en el frontend, Python en el backend).

## Decisión
- En V2.0 las reglas que ve el estudiante (disponibilidad, avance, notas, topes) se calculan en el frontend con módulos JS puros y probados.
- El backend valida la **estructura** (árbol de prerrequisitos, referencias, ciclos) y guarda los datos, pero no recalcula disponibilidad.
- Cuando el backend necesite calcular (planificación en V2.2), se porta la lógica a Python y ambas implementaciones se prueban contra los **mismos casos de referencia en JSON** (`testdata/academic-cases/`).
- La IA solo extrae datos en importaciones y produce borradores.

## Consecuencias
"Desconocido" es un resultado válido y nunca se convierte en "disponible". Ninguna regla depende de la hora del sistema sin recibirla como parámetro.
