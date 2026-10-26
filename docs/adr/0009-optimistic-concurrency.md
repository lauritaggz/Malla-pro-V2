# ADR-0009 · Concurrencia optimista e idempotencia

- Estado: aceptado
- Fecha: 2026-10-26

## Contexto
El mismo usuario puede editar desde dos dispositivos y la red puede reintentar (NF-03, CU-03).

## Decisión
Las tablas editables por el usuario tienen una columna `version`. Toda actualización envía la versión leída; si cambió, la API responde 409 con el estado actual. Las creaciones aceptan la cabecera `Idempotency-Key`.

## Consecuencias
Ninguna escritura sobrescribe en silencio. Cada endpoint de escritura tiene prueba de conflicto y de reintento.
