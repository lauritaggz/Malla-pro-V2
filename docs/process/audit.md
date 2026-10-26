# Auditoría de cambios

Cada PR se audita antes del merge. El auditor es un agente distinto del que implementó, en una sesión nueva, y **no modifica el código**: solo reporta. El resultado queda en un comentario en el PR y en un archivo en `docs/audits/`, que es el registro permanente.

## Entradas del auditor

1. La tarea en `docs/plan/backlog.md` (criterios, alcance, riesgo).
2. Los requisitos que cita, en `docs/requirements/requerimientos-v1.2.md`.
3. Los ADR y documentos de arquitectura relacionados.
4. El diff completo contra `main` (`git diff main...HEAD`) y la descripción del PR.
5. El resultado de CI y la ejecución local de las pruebas.

## Procedimiento

1. **Correr todo** en el lado que toca el cambio. Backend: `uv run ruff check`, `uv run ruff format --check`, `uv run pytest`, y `uv run alembic upgrade head` + `downgrade -1` si hay migración. Frontend: `npm run lint`, `npm test`, `npm run build`. Anotar el resultado real, no el que dice el PR.
2. **Alcance.** Listar los archivos cambiados y compararlos con el alcance de la tarea. Todo archivo fuera de alcance es un hallazgo.
3. **Criterios.** Para cada criterio de aceptación: ¿hay una prueba que lo demuestra? Leer la prueba y confirmar que de verdad falla si el criterio no se cumple (una prueba que no puede fallar no cuenta). Si es posible, romper temporalmente la implementación y ver que la prueba falla; revertir después.
4. **Lista de revisión** (abajo), según el nivel de riesgo.
5. **Escribir el informe** con la plantilla y el veredicto.

## Lista de revisión

### Estándar (toda tarea)

- [ ] Hace lo que pide la tarea, ni más ni menos.
- [ ] Cada criterio de aceptación tiene prueba y la prueba es significativa.
- [ ] Las pruebas cubren casos borde: vacío, nulo, desconocido, límites, repetición.
- [ ] Entradas externas validadas con Pydantic (backend) o con validación explícita (frontend). Código tipado; `ruff` sin advertencias nuevas.
- [ ] Errores manejados con mensaje útil y sin datos sensibles en logs (NF-07).
- [ ] Sin secretos, credenciales ni URL privadas en el código.
- [ ] Dependencias nuevas justificadas, con versión exacta y licencia compatible.
- [ ] Código y nombres en inglés; textos de interfaz en español de Chile.
- [ ] Documentación y `CHANGELOG.md` actualizados si cambió un contrato.
- [ ] Trazabilidad actualizada (`docs/plan/traceability.md`).

### Datos del usuario (si toca la API o la base de datos)

- [ ] Toda consulta de datos privados filtra por el usuario de `get_current_user` en el backend.
- [ ] Existe una prueba con **dos cuentas** donde B no puede leer ni modificar lo de A (NF-01), incluido probar ids de A directamente en la URL o el body.
- [ ] Reintentar la operación no duplica (NF-03). Actualizaciones de modelos con `version` comparan la versión y devuelven 409 ante conflicto.
- [ ] Lo compartido no filtra notas ni datos del autor (NO-04).
- [ ] Migraciones de Alembic: `downgrade` funcional; no borran datos sin respaldo; probadas con el catálogo importado.

### Reglas académicas (cálculo de disponibilidad, avance, notas o topes)

- [ ] Sin efectos secundarios: no hay red, base de datos, `Date.now()` implícito ni aleatoriedad.
- [ ] "Desconocido" nunca se convierte en "disponible" ni en "cumplido".
- [ ] Probado con mallas reales de `frontend/public/mallas/`, no solo con datos inventados.
- [ ] Si existe la misma regla en frontend y backend, ambos pasan los mismos casos de `testdata/academic-cases/` (ADR-0005).
- [ ] Correquisitos tratados según su semántica (pueden cursarse en el mismo período), no como ciclo.

### Profunda (riesgo alto)

- [ ] Modelo de amenazas breve en el informe: qué puede salir mal y cómo lo impide el cambio.
- [ ] Autenticación: toda ruta privada depende de `get_current_user`; el token nunca se registra; las pruebas no llaman a Google.
- [ ] Avance guardado: `career_key` y `legacy_id` no cambian; cualquier cambio de `localStorage` tiene migración, respaldo y prueba de no pérdida.
- [ ] Roles: cada ruta del equipo verifica el rol en el servidor; cada acción escribe en `Auditoria` (NF-11).
- [ ] Pagos: idempotencia por id externo, eventos fuera de orden, la página de retorno no activa nada (CO-02, CO-03).
- [ ] Datos del catálogo: informe de comparación contra la fuente adjunto y sin diferencias no explicadas.
- [ ] Se describe la prueba manual que debe hacer Laura antes del merge.

## Severidad de los hallazgos

| Severidad | Significa | Efecto |
|---|---|---|
| Crítico | Fuga de datos entre usuarios, pérdida de datos, escalamiento de permisos, cobro incorrecto, regla académica que marca disponible algo que no lo es | Veredicto **BLOQUEADO** |
| Mayor | Criterio de aceptación sin cumplir o sin prueba, cambio fuera de alcance, prueba que no puede fallar, error sin manejar en un flujo principal | Veredicto **CAMBIOS** |
| Menor | Nombre confuso, caso borde secundario sin prueba, documentación incompleta | No bloquea; se anota y el implementador decide en la misma ronda |
| Nota | Sugerencia o hallazgo fuera de alcance para una tarea futura | No bloquea |

## Veredictos

- **APROBADO**: sin hallazgos críticos ni mayores. Pasa a Laura para el merge.
- **CAMBIOS**: hay hallazgos mayores. Vuelve al implementador con la lista.
- **BLOQUEADO**: hay un hallazgo crítico, o la tarea no se puede evaluar (requisito contradictorio, falta una decisión). Decide Laura.

## Plantilla del informe

Archivo: `docs/audits/AAAA-MM-DD-T-XXX-rN.md` (N = ronda).

```markdown
# Auditoría T-XXX · ronda N

- PR: #NN · rama: v2/t0xx-… · commit auditado: <sha corto>
- Riesgo de la tarea: bajo | medio | alto
- Auditor: <agente/modelo> · fecha: AAAA-MM-DD
- **Veredicto: APROBADO | CAMBIOS | BLOQUEADO**

## Ejecución
| Comando | Resultado |
|---|---|
| uv run ruff check | ✅ / ❌ (detalle) |
| uv run pytest | N pruebas, N fallidas |
| npm run lint | |
| npm test | |
| npm run build | |

## Alcance
Archivos fuera del alcance de la tarea: ninguno | lista

## Criterios de aceptación
| # | Criterio | Prueba que lo demuestra | ¿Falla si se rompe? | Estado |
|---|---|---|---|---|
| 1 | … | `backend/tests/test_attempts.py::test_other_user_cannot_read` | sí (verificado) | ✅ |

## Hallazgos
| ID | Severidad | Archivo:línea | Descripción | Qué se espera |
|---|---|---|---|---|
| A1 | Mayor | backend/app/api/v1/…:42 | … | … |

## Para Laura
Qué revisar a mano antes del merge (obligatorio en riesgo alto).
```
