# ADR-0010 · Lo compartido nunca contiene notas

- Estado: aceptado
- Fecha: 2026-10-26

## Decisión
Compartir la configuración de un ramo usa solo nombres de evaluaciones, ponderaciones, escala y reglas (formato `MP1C`, `frontend/src/utils/shareCourseConfig.js`). Importar crea una copia independiente. Las notas solo viven en los datos privados del estudiante.

## Consecuencias
Toda forma de compartir (código, enlace o servidor) tiene una prueba que verifica que el contenido no incluye notas ni identificadores del autor.
