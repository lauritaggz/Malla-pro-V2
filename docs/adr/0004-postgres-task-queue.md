# ADR-0004 · Cola de tareas en PostgreSQL, sin Redis

- Estado: aceptado
- Fecha: 2026-10-26

## Decisión
Las tareas en segundo plano (avisos de la prueba, limpieza de documentos, importaciones con IA) usan una tabla de trabajos en PostgreSQL con `SELECT … FOR UPDATE SKIP LOCKED`. No se agrega Redis por ahora.

## Consecuencias
Una pieza menos que operar. Los trabajos deben ser idempotentes (reintentar no duplica). Si el volumen crece, se reevalúa con un ADR nuevo.
