# ADR-0001 · Monolito modular con FastAPI

- Estado: aceptado (implementado en s01)
- Fecha: 2026-10-26

## Contexto
Lo mantiene una sola persona con presupuesto de VPS (NF-12). El frontend React ya existía y funciona sin backend.

## Decisión
Un solo backend Python 3.12 + FastAPI, organizado por capas (`api/v1`, `services`, `models`, `schemas`) y, dentro de ellas, por módulo de negocio (catálogo, usuarios, avance, notas, horario, tutores, equipo). El frontend sigue en React (JavaScript) y conserva el modo sin backend con las mallas estáticas.

## Consecuencias
- La lógica vive en `services/`; las rutas solo validan, autorizan y delegan.
- Un servicio no consulta directamente las tablas de otro módulo: llama a su servicio.
- Separar un módulo más adelante no debe cambiar el modelo de datos.

## Alternativas descartadas
Node + Fastify + Prisma (propuesta original de los requerimientos v1.2): habría que reescribir lo ya hecho. Microservicios: costo y operación.
