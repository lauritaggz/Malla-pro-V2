# Flujo de trabajo con agentes

## Roles

| Rol | Quién | Hace | No hace |
|---|---|---|---|
| Dueña del producto | Laura | Prioriza el backlog, responde preguntas abiertas, cierra decisiones, aprueba y hace merge de cada PR | — |
| Implementador | Agente (`.claude/agents/implementer.md`) | Toma **una** tarea, la planifica, implementa, prueba y abre el PR | Hacer merge, cambiar requisitos o ADR, tocar código fuera del alcance |
| Auditor | Agente distinto, sesión nueva (`.claude/agents/auditor.md`) | Revisa el PR contra la tarea, los requisitos y la lista de auditoría; escribe el informe con veredicto | Corregir el código del PR (solo reporta), aprobar su propio trabajo |
| CI | GitHub Actions | Lint, pruebas, migraciones, importación del catálogo y build en cada push | — |

El auditor no ve la conversación del implementador: solo la tarea, el diff, las pruebas y el PR. Así el trabajo no se califica a sí mismo.

## Ciclo de una tarea

```
backlog (todo)
  → Laura marca la tarea como lista (ready)
  → implementador: rama v2/t0XX-…, PR en borrador con el plan (in progress)
      ↳ si hay preguntas abiertas o el cambio es grande: espera aprobación (blocked)
  → implementador: código + pruebas + plantilla del PR completa, CI en verde (to audit)
  → auditor: informe en docs/audits/ + comentario en el PR
      ↳ CAMBIOS → vuelve al implementador (máximo 3 rondas; luego decide Laura)
      ↳ BLOQUEADO → Laura decide
      ↳ APROBADO → (to merge)
  → Laura revisa, prueba si corresponde y hace merge (done)
```

El estado vive en la columna "Estado" del backlog (todo, ready, in progress, blocked, to audit, to merge, done) y en las etiquetas del PR (`status:in-progress`, `status:blocked`, `status:to-audit`, `status:to-merge`).

## Ramas, commits y PR

- Rama: `v2/t014-prereq-evaluation` (convención del repo `v2/<id>-<nombre>`). Una rama por tarea. Una tarea por PR.
- Commits en inglés, Conventional Commits con el ID: `feat(frontend): evaluate "or" prerequisites (T-014)`, `fix(backend): …`, `test: …`, `docs: …`, `chore: …`.
- Merge a `main` con merge commit o squash, como prefiera Laura; el título lleva el ID de la tarea.
- El PR usa `.github/pull_request_template.md`. Un PR sin la tabla de criterios → pruebas no se audita.
- Tamaño orientativo: hasta ~400 líneas de cambio sin contar pruebas ni datos. Si la tarea crece más, el implementador propone dividirla en el PR.

## Tipos de tarea

| Tipo | Ejemplo | Regla adicional |
|---|---|---|
| `code` | Endpoint, pantalla, regla académica | La regla general |
| `data` | Agregar o corregir una malla del catálogo | Cita la fuente oficial, adjunta el informe de `tools/verificacion-oficial` y no mezcla código salvo el ajuste mínimo del importador |
| `decision` | Elegir proveedor de pagos, cambiar un requisito | Produce un ADR o un cambio en `docs/requirements/` con aprobación explícita de Laura en el PR; no mezcla código |
| `infra` | Docker, CI, despliegue, respaldos | Prueba documentada del procedimiento (p. ej. una restauración real) |

## Nivel de riesgo y revisión humana

Cada tarea del backlog declara su riesgo. El riesgo **alto** exige que Laura revise el diff además de la auditoría, y el auditor usa el nivel profundo de la lista.

| Riesgo | Cuándo | Qué se exige |
|---|---|---|
| Bajo | Documentación, componentes de UI sin datos, refactor con pruebas existentes | Auditoría estándar |
| Medio | Reglas académicas, endpoints con datos del usuario, migraciones que solo agregan | Auditoría estándar + pruebas de casos borde |
| Alto | Autenticación, permisos y roles, aislamiento de datos, migraciones que alteran o borran, cambios en el formato de `localStorage` o importación de datos locales (CU-05), `career_key` y `legacy_id`, pagos, datos del catálogo | Auditoría profunda + revisión humana del diff + prueba manual descrita en el PR |

## Qué hacer con lo que no está en la tarea

- **Bug fuera de alcance:** anótalo en "Hallazgos" del PR. Laura decide si crea una tarea.
- **Requisito ambiguo:** "Preguntas abiertas" en el PR, con el supuesto que propones. No sigas en esa parte.
- **Necesitas cambiar un ADR o un requisito:** abre una tarea de tipo `decision`. No lo cambies dentro de una tarea de código.
- **Necesitas una dependencia nueva:** justifícala en el PR (versión exacta, para qué, alternativa descartada). El auditor la revisa.

## Trazabilidad

`docs/plan/traceability.md` relaciona cada requisito con sus tareas y sus pruebas. Al cerrar una tarea, el implementador agrega en esa tabla las pruebas que cubren cada requisito (ruta del archivo de prueba). El auditor verifica que existan.
