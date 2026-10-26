## Tarea

T-0XX · <título> · Riesgo: bajo | medio | alto
Requisitos: <IDs>

## Plan (antes de implementar)

- Archivos a tocar:
- Enfoque:
- Preguntas abiertas:

## Qué cambia

<resumen en 3 a 6 líneas>

## Criterios de aceptación → pruebas

| # | Criterio | Prueba (archivo › caso) | Resultado |
|---|---|---|---|
| 1 | | | ✅ |

## Verificación

- [ ] Backend: `uv run ruff check`, `uv run ruff format --check`, `uv run pytest` (N pruebas)
- [ ] Migración: `alembic upgrade head` y `downgrade -1` probados (si aplica)
- [ ] Frontend: `npm run lint`, `npm test`, `npm run build`
- [ ] Rutas con datos privados registradas en la suite de aislamiento
- [ ] `career_key`, `legacy_id` y formato de `localStorage` intactos, o con migración probada
- [ ] Solo archivos dentro del alcance de la tarea
- [ ] `CHANGELOG.md`, `docs/plan/traceability.md` y documentación del contrato actualizados
- [ ] Dependencias nuevas justificadas (nombre, versión, para qué, alternativa)

## Prueba manual (obligatoria en riesgo alto)

Pasos para que Laura lo pruebe antes del merge.

## Hallazgos fuera de alcance

## Auditoría

Informe: `docs/audits/…` · Veredicto: —
