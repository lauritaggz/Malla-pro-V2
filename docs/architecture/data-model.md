# Modelo de datos

Fuente de verdad: `backend/app/models/` y las migraciones de `backend/alembic/versions/`. Todas las tablas usan `IdTimestampMixin` (UUID, `created_at`, `updated_at`).

## Tablas existentes

| Tabla | Para qué | Requisitos | Notas |
|---|---|---|---|
| `users` | Usuario identificado por Firebase | CU-01 | `firebase_uid` único; `is_admin` se reemplaza por `role` en T-002 |
| `universities` | Institución | CA-01 | `slug` único |
| `programs` | Carrera | CA-01 | `career_key` único e inmutable (ADR-0007); `legacy_url` para las mallas estáticas |
| `curriculum_versions` | Versión del plan | CA-03, sección 6 | `period_regime`, `credit_system`, `status` (draft/published/archived), una sola `is_current` por carrera, `source_type` y fuente, `attrs` (JSONB: fuente oficial, equivalencias y otros campos del archivo sin columna, T-010) |
| `tracks` | Mención | sección 6 | Cursos comunes sin `track_id` |
| `courses` | Curso dentro de una versión | sección 6 | `legacy_id` (id del JSON, del que depende el avance guardado), `prereq_status` none/known/unknown, `prereq_expr`/`coreq_expr` (JSONB, ADR-0008), `prereq_raw`/`coreq_raw`, `attrs` |
| `course_aliases` | Otra forma de escribir el código de un mismo curso (`courseCodeAliases` del JSON; los usa la importación del horario) | sección 6 | Único por (versión, alias, curso). Las equivalencias de planes antiguos **no** van aquí: quedan en `curriculum_versions.attrs.equivalencias` (T-010) |

## Tablas planificadas

Se crean en la tarea indicada, con su migración. Nombres y campos son la propuesta de partida; la tarea puede ajustarlos explicándolo en el PR.

| Tabla | Campos principales | Requisitos | Tarea |
|---|---|---|---|
| `users.role` | `student` / `curator` / `superadmin` | AD-01, AD-03 | T-002 |
| `audit_log` | actor, acción, entidad, id, antes, después (JSONB), fecha | NF-11 | T-002 |
| `academic_profiles` | usuario, versión de malla, mención, año de ingreso, activo, `local_import_hash`, `version` | CU-02, CU-05 | T-020 |
| `course_attempts` | perfil, curso, período, estado (in_progress/passed/failed/withdrawn/validated), nota final, `version` | AV-01, AV-02 | T-021 |
| `assessments` | intento, nombre, ponderación, nota (nullable), grupo, orden | NO-01 a NO-03 | T-025 |
| `personal_exceptions` | perfil, curso, tipo, motivo, alcance (JSONB) | AV-05 | T-023 |
| `schedules` / `schedule_blocks` | perfil, período; curso, sección, día, inicio, fin, sala | HO-01 a HO-04 | T-027 |
| `period_plans` / `period_plan_items` | perfil, período, nombre, principal; curso, sección opcional | PL-01 | T-028 |
| `personal_curricula` | dueño, contenido (JSONB en el formato de malla), estado, `version` | MP-01, CA-02 | T-029 |
| `reports` | usuario, entidad, id, categoría, motivo, contexto (JSONB), estado | MP-03, AD-02, TU-09 | T-031 |
| `tutor_profiles` / `tutor_services` / `tutor_service_links` | perfil público, WhatsApp con consentimiento, estado de publicación; servicio, precio y unidad; vínculo explícito con curso, carrera o institución | TU-01 a TU-10 | T-040 |
| `product_events` | usuario o anónimo, nombre (lista cerrada), props sin datos personales | AN-01, AD-07 | T-051 |
| `jobs` | tipo, payload, estado, intentos, bloqueo (cola en Postgres, ADR-0004) | IA-05, PR-02 | cuando se necesite |
| `imports`, `course_offers`, `offer_sections`, `section_blocks` | importaciones con IA y oferta | IA, OF | V2.1 |
| `subscriptions`, `payments` | prueba y cobro; `payments.external_id` único para idempotencia | PR, CO | V2.2 |

## Reglas

- Tablas con datos de usuario: toda consulta filtra por el usuario dueño, y hay prueba de aislamiento (T-004).
- El estado actual de un curso se **calcula** desde `course_attempts`; no se guarda una columna "estado" que se sobrescriba. Reprobar y volver a cursar conserva ambos intentos.
- Lo compartido (configuraciones de ramo, mallas comunitarias) nunca guarda notas (ADR-0010).
- El avance importado desde el navegador se vincula por `career_key` + `legacy_id`; nunca por nombre.
