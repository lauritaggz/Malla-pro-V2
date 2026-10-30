# Backlog

Tareas para llegar a la beta **V2.0** (sección 3 de los requerimientos), partiendo de lo que ya existe en el repo. V2.1 y V2.2 están como épicas y se dividen cuando V2.0 esté en piloto.

Reglas: una tarea = una rama = un PR. Solo se trabaja en tareas en estado **ready**. El alcance indica las rutas que la tarea puede modificar; tocar otras es un hallazgo de auditoría. Cada criterio necesita una prueba (ver `docs/process/audit.md`).

Estados: `todo` · `ready` · `in progress` · `blocked` · `to audit` · `to merge` · `done`.

## Hecho antes de este backlog

| Entrega | Qué | Rama |
|---|---|---|
| s01 | Base del backend: FastAPI, SQLAlchemy async, Alembic, salud, CORS | `v2/s01-backend-base` |
| s02 | Login con Google (Firebase), verificación del token, tabla `users`, `/me` | `v2/s02-auth` |
| s03 | Catálogo en Postgres, importación de mallas legadas, API pública, adaptador del frontend | `v2/s03-catalogo` |
| T-001 | CI en GitHub Actions (backend y frontend) | `docs/agent-workflow` |

## Resumen

| ID | Tarea | Tipo | Riesgo | Depende de | Estado |
|---|---|---|---|---|---|
| D-01 | Confirmar con Tecnología Médica los 2 requisitos dudosos | decision | — | — | done (se sigue el documento oficial) |
| D-02 | Crear malla manual gratis en el nivel básico | decision | bajo | — | todo |
| D-03 | ¿Solo Google o también correo y contraseña? | decision | bajo | — | todo |
| T-006 | Corregir los errores de lint del frontend | code | bajo | T-001 | ready |
| T-007 | Sincronizar el frontend de la V2 con la versión pública (v1) | code | alto | T-010 | done |
| T-002 | Roles del equipo y registro de auditoría | code | alto | T-001 | to audit |
| T-003 | Manejo de errores y logs sin datos sensibles | code | medio | T-001 | ready |
| T-004 | Pruebas de aislamiento entre dos usuarios | code | alto | T-001 | done |
| T-005 | Concurrencia optimista e idempotencia | code | medio | T-001 | todo |
| T-010 | Mallas verificadas y mallas de la U. de Chile | data | alto | T-001 | done |
| T-011 | Portar a la V2 los cambios de frontend de v1 para la U. de Chile | code | medio | T-010 | done (en T-007) |
| T-012 | Evaluar árboles de prerrequisitos en el frontend | code | medio | T-001 | ready |
| T-013 | Cálculo de notas como módulo puro con casos de referencia | code | medio | T-001 | ready |
| T-014 | Detección de topes de horario con pruebas | code | bajo | T-001 | ready |
| T-015 | Validación estructural de mallas en el backend | code | medio | T-001 | todo |
| T-016 | Avance y créditos como módulo puro | code | medio | T-012 | todo |
| T-020 | Perfil académico | code | medio | T-004, T-005 | todo |
| T-021 | Intentos y avance en el backend | code | alto | T-020 | todo |
| T-022 | Sincronizar el avance del frontend con la API | code | alto | T-021 | todo |
| T-023 | Importar el avance guardado en el navegador | code | alto | T-022 | todo |
| T-024 | Excepciones personales en el backend | code | medio | T-021 | todo |
| T-025 | Notas en el backend | code | medio | T-013, T-021 | todo |
| T-026 | Cambios masivos con deshacer | code | medio | T-022 | todo |
| T-027 | Horario en el backend y exportación | code | medio | T-014, T-020 | todo |
| T-028 | Plan del próximo período | code | medio | T-012, T-021 | todo |
| T-029 | Revisar compartir e importar configuraciones de ramo | code | medio | T-001 | ready |
| T-030 | Búsqueda en el catálogo y etiquetas de origen | code | medio | T-010 | todo |
| T-031 | Publicar versiones del catálogo | code | alto | T-002, T-015 | todo |
| T-032 | Malla personal: crear y editar | code | medio | T-015, T-020, D-02 | todo |
| T-033 | Vista de la malla: dependencias y accesibilidad | code | medio | T-012 | todo |
| T-034 | Reportes de error y propuestas de malla | code | medio | T-002 | todo |
| T-040 | Perfil de tutor y servicios | code | alto | T-002, T-004 | todo |
| T-041 | Buscar tutores, ficha y WhatsApp | code | medio | T-040 | todo |
| T-042 | Moderación de tutores y reportes | code | alto | T-040, T-034 | todo |
| T-050 | Panel básico del equipo | code | alto | T-002, T-031, T-034 | todo |
| T-051 | Eventos de producto | code | medio | T-003 | todo |
| T-052 | Métricas de uso agregadas | code | medio | T-050, T-051 | todo |
| T-053 | Exportar datos y eliminar cuenta | code | alto | T-021, T-025, T-027 | todo |
| T-060 | Despliegue del backend en VPS | infra | alto | T-003 | todo |
| T-061 | Respaldos y restauración probada | infra | alto | T-060 | todo |
| T-062 | Monitoreo de errores y disponibilidad | infra | medio | T-060 | todo |
| T-063 | Pruebas de extremo a extremo | code | medio | T-022, T-025, T-027 | todo |

---

## Decisiones (las cierra Laura)

### D-01 · Requisitos dudosos de Tecnología Médica
El documento oficial (catálogo 2018) dice que Bioquímica (BIOL166) solo exige Química Orgánica y que el Integrador II de 10° semestre exige lo mismo que el Seminario de 9°, no el Seminario. **Cerrada el 29-10-2026:** se sigue el documento oficial, incluida la excepción de TMED942, que se importa tal como está escrito y queda por confirmar con la carrera (ver `docs/plan/decisions.md`).

### D-02 · Malla manual en el nivel básico
La recomendación del documento es que sea gratis, porque alimenta la base comunitaria. Afecta T-032.

### D-03 · Métodos de inicio de sesión
Hoy solo hay Google (ADR-0003). CU-01 pide al menos un método, así que basta. Decidir si se agrega correo y contraseña con Firebase.

---

## E0 · Base

### T-002 · Roles del equipo y registro de auditoría
- Tipo: code · Riesgo: alto · Requisitos: AD-01, AD-03, NF-11, CO-04 · Depende de: T-001
- Alcance: `backend/app/models/user.py`, `backend/app/models/audit.py`, `backend/app/core/security.py`, `backend/app/services/audit.py`, `backend/app/api/v1/admin.py`, `backend/app/schemas/`, `backend/alembic/versions/`, `backend/tests/`.
- Criterios:
  1. `users.role` con valores `student`, `curator` y `superadmin` (CheckConstraint). La migración pasa a `superadmin` a los usuarios con `is_admin = true` y elimina `is_admin`. El `downgrade` lo revierte.
  2. Dependencia `require_role(*roles)` que responde 403 si el usuario no tiene el rol.
  3. Tabla `audit_log` (actor, acción, entidad, id de entidad, antes y después en JSONB, fecha) y servicio `record_audit(...)`.
  4. `PATCH /api/v1/admin/users/{id}/role`: solo `superadmin`; un superadmin no puede quitarse su propio rol; cada cambio queda en `audit_log`.
  5. `GET /me` incluye `role`.
- Pruebas: matriz rol × ruta (permitido/denegado); el cambio de rol queda auditado; migración `upgrade` y `downgrade`.

### T-003 · Manejo de errores y logs sin datos sensibles
- Tipo: code · Riesgo: medio · Requisitos: NF-07 · Depende de: T-001
- Alcance: `backend/app/main.py`, `backend/app/core/logging.py`, `backend/app/core/errors.py`, `backend/tests/`, `docs/architecture/api.md`.
- Criterios:
  1. Un error no controlado responde 500 con `{"detail": "Ocurrió un error inesperado. Intenta de nuevo."}`, sin trazas.
  2. Los errores de validación (422) mantienen el formato de FastAPI y un mensaje legible en español.
  3. Logs estructurados (JSON en producción) con un identificador de request; nunca incluyen el encabezado `Authorization`, tokens, correos completos ni cuerpos con notas.
- Pruebas: ruta de prueba que lanza una excepción; un log capturado no contiene el token enviado.

### T-004 · Pruebas de aislamiento entre dos usuarios
- Tipo: code · Riesgo: alto · Requisitos: NF-01 · Depende de: T-001
- Alcance: `backend/tests/conftest.py`, `backend/tests/isolation/`.
- Criterios:
  1. Fixtures `user_a` y `user_b`, con clientes HTTP autenticados (reemplazando `verify_firebase_token`, sin llamar a Google).
  2. Utilidad que, dada una lista de rutas privadas y un recurso creado por A, verifica que B recibe 404 al leer, modificar y borrar (con el id en la URL y en el cuerpo).
  3. Registro central de rutas privadas: una prueba falla si existe una ruta que depende de `get_current_user` y no está registrada ni marcada explícitamente como "propia del usuario" (como `/me`).
- Pruebas: la propia suite, en CI.

### T-005 · Concurrencia optimista e idempotencia
- Tipo: code · Riesgo: medio · Requisitos: NF-03, CU-03 · Depende de: T-001
- Alcance: `backend/app/core/concurrency.py`, `backend/app/models/idempotency.py`, `backend/alembic/versions/`, `backend/app/main.py` (CORS), `backend/tests/`.
- Criterios:
  1. Mixin `VersionedMixin` (`version` entero) y helper de actualización que responde 409 con el estado actual si la versión no coincide.
  2. Soporte de `Idempotency-Key` en creaciones: repetir con la misma clave y el mismo usuario devuelve la respuesta original sin crear otro recurso. Las claves expiran a las 24 h.
  3. `Idempotency-Key` permitida en CORS.
- Pruebas: dos actualizaciones con la misma versión (la segunda da 409); reintento con la misma clave.

### T-007 · Sincronizar el frontend de la V2 con la versión pública (v1)
- Tipo: code · Riesgo: alto · Requisitos: CA-01, NO-04, NF-05 · Depende de: T-010 · Aprobada por Laura el 29-10-2026.
- Origen: el frontend de la V2 se copió de v1 en `ddcaebc` (9-10-2026). Desde entonces v1 sumó 29 commits hasta `543e5e6` (Rediseño Tinta, selector de carreras, Horario, panel de notas, U. de Chile). Incluye T-011.
- Alcance: `frontend/` salvo `public/mallas/` (las mallas ya llegaron con T-010). Se conserva lo propio de la V2: login con Google (`features/auth`, `lib/`), catálogo desde la API (`curriculumApi.js`, `mallasLoader.js`), `career_key` de la API (`storageKeys.js`).
- Criterios:
  1. Sin backend, la V2 se ve igual que v1 en `543e5e6`: mismas pantallas en escritorio y móvil (comparación de capturas).
  2. El login sigue visible y usable: en escritorio en el riel lateral, en móvil en la barra inferior (la barra superior de v1 ahora es solo móvil).
  3. Con la API, el selector muestra lo mismo que sin ella (área y semestres de las mallas legadas) y no inventa datos para mallas que solo existen en la API.
  4. Las mallas de la U. de Chile se identifican como tales en la etiqueta de universidad, al compartir configuraciones (`UCH`) y en analítica; no ofrecen toma de ramos.
  5. Sin dependencias nuevas; las pruebas de v1 y de la V2 pasan; el lint no suma errores.
- Pruebas: `universityDetection.test.js`, pruebas de v1 incluidas (`courseColors.test.js`, `shareCourseConfig.test.js`), suites existentes; capturas comparadas.

### T-006 · Corregir los errores de lint del frontend
- Tipo: code · Riesgo: bajo · Requisitos: NF-09 · Depende de: T-001
- Alcance: archivos con errores de `npm run lint` en `frontend/src/`, `frontend/eslint.config.js`, `.github/workflows/ci.yml` (solo para quitar `continue-on-error` del lint y los disparadores del job `catalog-data`).
- Criterios:
  1. `npm run lint` termina sin errores. Hoy (después de T-007) hay 8: variables sin usar en `App.jsx` (`progreso`, `cursosCursando`, `handleVerProgresoNav`), `Navbar.jsx` (`cantidadSemestres`) y `academicProgressStorage.js` (`emptyProgress`); `react-refresh/only-export-components` en `ImportCourseConfigModal.jsx`; `Buffer` no definido en `shareCourseConfig.js`, que es un respaldo para Node y se resuelve en la configuración de ESLint o con `globalThis.Buffer`, sin cambiar el comportamiento.
  2. Ningún cambio de comportamiento: si quitar una variable sin usar revela una función que se perdió (p. ej. `handleVerProgresoNav`), se reporta en el PR en vez de borrarla a ciegas.
  3. El lint pasa a ser bloqueante en CI.
  4. El job `catalog-data` también corre al agregar o quitar una etiqueta (`pull_request: types: [opened, synchronize, reopened, labeled, unlabeled]`), para que poner `type:data` después de abrir el PR no deje el CI en rojo (auditoría T-010, A12).
- Pruebas: `npm test` y `npm run build` siguen en verde; CI con el lint bloqueante en verde.

## E1 · Datos y reglas académicas

### T-010 · Mallas verificadas y mallas de la U. de Chile
- Tipo: data · Riesgo: alto · Requisitos: sección 6, CA-01 · Depende de: T-001
- Alcance: `frontend/public/mallas/`, `frontend/src/utils/__fixtures__/curriculum/`, `frontend/src/utils/mallasLoader.js` (solo para listar las nuevas), `backend/app/services/legacy_import.py`, `backend/reports/legacy_inconsistencies.md`, `backend/tests/`, `frontend/src/**/*.test.js`, `docs/data/`.
- Criterios:
  1. Las 9 mallas UNAB se reemplazan por las verificadas (`docs/data/verificacion-mallas-oficiales.md`). Los `id` de los cursos no cambian; el `career_key` de cada carrera tampoco.
  2. Se agregan Bioquímica, Ingeniería en Alimentos, Química y Química y Farmacia de la U. de Chile, con su propia universidad en el catálogo (`slug` `uch`) y un `career_key` estable.
  3. El importador reconoce `universidad`, `linea`, `nota_codigos`, `fuente_oficial` y `equivalencias`. Las equivalencias se guardan completas en `curriculum_versions.attrs` y **no** pasan a `course_aliases` (decisión de Laura, 29-10-2026: un alias cambiaría el cruce del horario con la API y no representa grupos "A y B"; usarlas en el avance va en otra tarea). La fuente oficial se resume en `source_note` (`source_type` sigue `legacy_json`) y se guarda completa en `attrs`. Lo demás se conserva en `attrs`. Ningún campo se pierde en silencio.
  4. Un avance guardado antes del cambio en Ingeniería Civil Informática (códigos ICF → CINF, mismos ids) y en Tecnología Médica se conserva (prueba con datos de `localStorage` simulados).
  5. El frontend lista las carreras agrupadas o rotuladas por universidad, sin asumir que todo es UNAB.
  6. `legacy_inconsistencies.md` se regenera; ningún test existente falla.
- Pruebas: importación de las 13 mallas; idempotencia del importador; conservación del avance; listado por universidad.

### T-011 · Portar a la V2 los cambios de frontend de v1 para la U. de Chile
- Tipo: code · Riesgo: medio · Requisitos: CA-01, NO-04 · Depende de: T-010
- Origen: auditoría de T-010 (A9) y commit `543e5e6` de la versión pública.
- Alcance: `frontend/src/utils/shareCourseConfig.js`, `frontend/src/utils/analytics.js`, `frontend/src/utils/mallasLoader.js`, `frontend/src/components/MallaSelector.jsx`, `Navbar.jsx`, `MobileBottomNav.jsx`, `SideRail.jsx`, `App.jsx`, pruebas.
- Criterios:
  1. Compartir o importar la configuración de un ramo de la U. de Chile la identifica como `UCH`, no como UNAB; una configuración UNAB no se acepta en un ramo UCH ni al revés.
  2. `inferUniversidadFromUrl` reconoce las mallas UCH (`...UCH.json` y `/mallas/uch/`).
  3. Toma de ramos (programación académica UNAB) no se ofrece en mallas de la U. de Chile.
  4. El selector muestra lo mismo que la versión pública (universidad, área, semestres), usable desde 360 px y con teclado.
- Pruebas: compatibilidad de configuraciones entre universidades; detección de universidad por URL y por `universidad`; visibilidad de toma de ramos.

### T-012 · Evaluar árboles de prerrequisitos en el frontend
- Tipo: code · Riesgo: medio · Requisitos: AV-04, sección 6 · Depende de: T-001
- Alcance: `frontend/src/utils/prerequisites.js` (nuevo), `frontend/src/utils/curriculumProgress.js`, `frontend/src/utils/curriculumApi.js`, componentes que hoy duplican la regla (`MallaViewer`, `PeriodoActualView`, `Semestre`), `testdata/academic-cases/`, pruebas.
- Criterios:
  1. Función pura `evaluatePrerequisites(tree, state)` → `{ status: "met" | "missing" | "unknown", detail }` para nodos `and`, `or`, `course`, `min_credits` y el estado `unknown` del curso.
  2. `prereq_status = "unknown"` nunca da `met`; en la malla se muestra como "disponibilidad desconocida", distinto de "bloqueado".
  3. Las excepciones del estudiante cuentan como hoy (misma semántica que `meetsPrerequisites`).
  4. Una sola implementación: los componentes dejan de tener su propia copia de la regla.
  5. `curriculumApi.js` ya no lanza `UnsupportedPrereqError` con OR o créditos: los representa con el nuevo evaluador.
  6. Casos de referencia en `testdata/academic-cases/prerequisites.json`, pensados para reutilizarse en Python (ADR-0005).
- Pruebas: tabla de casos por tipo de nodo; casos reales de Medicina (MEDI0300) y de Tecnología Médica por mención.

### T-013 · Cálculo de notas como módulo puro
- Tipo: code · Riesgo: medio · Requisitos: NO-01, NO-02, NO-03 · Depende de: T-001
- Alcance: `frontend/src/utils/grades.js` (nuevo), `frontend/src/utils/gradeUtils.js`, `frontend/src/components/NotasModal.jsx`, `testdata/academic-cases/grades.json`, pruebas.
- Criterios:
  1. La lógica de promedio ponderado, nota necesaria y eximición sale de `NotasModal.jsx` a funciones puras, sin cambiar el resultado para los datos existentes. Ojo: con T-007 (paridad con v1) la nota necesaria para eximirse se divide por lo que falta **calificar** (evaluaciones sin nota más el porcentaje sin asignar, `pesoPendiente`) y ya no solo por lo que faltaba **asignar**; ese comportamiento es el caso de referencia.
  2. Aviso si las ponderaciones no suman 100 %.
  3. Nota necesaria: informa "imposible" si no alcanza ni con 7,0 y "falta información" si hay ponderaciones desconocidas.
  4. Escala y umbral configurables (por defecto 1,0–7,0, aprueba con 4,0); redondeo documentado y probado en los bordes (3,95 / 3,949).
  5. La nota calculada no marca el ramo como aprobado.
- Pruebas: casos de referencia escritos a mano; regresión con configuraciones reales guardadas.

### T-014 · Detección de topes de horario
- Tipo: code · Riesgo: bajo · Requisitos: HO-02 · Depende de: T-001
- Alcance: `frontend/src/utils/scheduleUtils.js`, `frontend/src/features/academicProgramming/services/`, pruebas.
- Criterios: una función pura de topes usada por el horario y por la toma de ramos; bloques superpuestos generan tope; bloques contiguos (uno termina 09:50 y otro empieza 09:50) no; devuelve los pares en conflicto.
- Pruebas: superposición parcial, total, contigua y en días distintos.

### T-015 · Validación estructural de mallas en el backend
- Tipo: code · Riesgo: medio · Requisitos: sección 6, MC-01, IA-04 · Depende de: T-001
- Alcance: `backend/app/services/curriculum_validation.py` (nuevo), `backend/app/services/legacy_import.py`, `backend/tests/`.
- Criterios: las detecciones que hoy hace `legacy_import` (referencias, ciclos, alcance por mención, mismo período) se extraen a un validador reutilizable con severidad `error`/`warning`; los correquisitos mutuos no son ciclo; las 13 mallas pasan sin errores.
- Pruebas: casos sintéticos por regla y las mallas reales.

### T-016 · Avance y créditos como módulo puro
- Tipo: code · Riesgo: medio · Requisitos: AV-03 · Depende de: T-012
- Alcance: `frontend/src/utils/progress.js` (nuevo), `frontend/src/components/ResumenProgreso.jsx`, `frontend/src/components/MallaProgressStats.jsx`, `frontend/src/components/StatsDisplay.jsx`, pruebas.
- Criterios: ramos y créditos aprobados se calculan por separado, en la unidad de la versión; si un curso no tiene créditos, el total se muestra como parcial ("al menos N") y no como cero confirmado; con mención, cuenta tronco común más la mención activa; los componentes usan una sola implementación.
- Pruebas: Computación, Tecnología Médica con dos menciones, malla con un curso sin créditos.

## E2 · Avance del estudiante en el backend

### T-020 · Perfil académico
- Tipo: code · Riesgo: medio · Requisitos: CU-02 · Depende de: T-004, T-005
- Criterios: tabla `academic_profiles`; `GET/POST/PATCH /me/profiles`; elegir carrera, versión y mención; un perfil activo por usuario; el régimen de períodos sale de la versión.
- Pruebas: CRUD; aislamiento registrado en T-004; conflicto de versión.

### T-021 · Intentos y avance en el backend
- Tipo: code · Riesgo: alto · Requisitos: AV-01, AV-02 · Depende de: T-020
- Criterios: tabla `course_attempts`; API para crear, editar y borrar intentos por período; reprobar y volver a cursar conserva ambos; el curso se identifica por `course_id` y se acepta `legacy_id` + `career_key` para el frontend; idempotencia en creaciones.
- Pruebas: reprobar y repetir; reintento; aislamiento.

### T-022 · Sincronizar el avance del frontend con la API
- Tipo: code · Riesgo: alto · Requisitos: CU-03, NF-03 · Depende de: T-021
- Criterios: con sesión iniciada, el avance se lee y guarda en la API; la interfaz muestra guardado, pendiente o fallido y permite reintentar; sin sesión o sin API, sigue funcionando con `localStorage` como hoy; ante conflicto de versión se ofrece recargar, nunca se sobrescribe en silencio.
- Pruebas: fallo de red simulado; conflicto entre dos pestañas; modo sin sesión intacto.

### T-023 · Importar el avance guardado en el navegador
- Tipo: code · Riesgo: alto · Requisitos: CU-05, sección 14 · Depende de: T-022
- Criterios: al iniciar sesión por primera vez se detecta el avance local, se muestra qué se importará y a qué carrera corresponde; los cursos se vinculan por `career_key` + `legacy_id`; los que no tienen correspondencia se muestran; repetir no duplica (huella guardada en el perfil); los datos locales no se borran hasta que el usuario confirma.
- Pruebas: importar dos veces; carrera con códigos renombrados (Civil Informática); datos locales corruptos.

### T-024 · Excepciones personales en el backend
- Tipo: code · Riesgo: medio · Requisitos: AV-05 · Depende de: T-021
- Criterios: tabla `personal_exceptions` con tipo, motivo y alcance; misma semántica que el modo excepción actual (`exceptionSelection.js`); no aprueba ramos ni cambia el catálogo.
- Pruebas: equivalencia con el comportamiento local; aislamiento.

### T-025 · Notas en el backend
- Tipo: code · Riesgo: medio · Requisitos: NO-01, NO-02, NO-03 · Depende de: T-013, T-021
- Criterios: tabla `assessments` por intento; la interfaz de notas guarda en la API con sesión y en `localStorage` sin ella; el cálculo usa el módulo de T-013.
- Pruebas: flujo de un ramo con 4 evaluaciones; aislamiento.

### T-026 · Cambios masivos con deshacer
- Tipo: code · Riesgo: medio · Requisitos: AV-06 · Depende de: T-022
- Criterios: aprobar varios cursos muestra la cantidad antes de confirmar; la operación se puede deshacer completa, con o sin sesión.
- Pruebas: aprobar un semestre completo y deshacer.

### T-027 · Horario en el backend y exportación
- Tipo: code · Riesgo: medio · Requisitos: HO-01, HO-03, HO-04 · Depende de: T-014, T-020
- Criterios: tablas `schedules` y `schedule_blocks`; varias sesiones por ramo; la exportación (PDF actual) contiene los mismos cursos, días y horas que lo guardado; el horario nunca se presenta como inscripción oficial.
- Pruebas: exportar y comparar; aislamiento.

### T-028 · Plan del próximo período
- Tipo: code · Riesgo: medio · Requisitos: PL-01 · Depende de: T-012, T-021
- Criterios: la toma de ramos actual guarda el plan en el backend con sesión; muestra carga y disponibilidad con el evaluador de T-012; un ramo bloqueado o desconocido no se ofrece como disponible.
- Pruebas: ramo bloqueado; ramo con requisitos desconocidos.

### T-029 · Revisar compartir e importar configuraciones de ramo
- Tipo: code · Riesgo: medio · Requisitos: NO-04, NO-05, NF-01 · Depende de: T-001
- Alcance: `frontend/src/utils/shareCourseConfig.js`, `frontend/src/components/ShareCourseConfigModal.jsx`, `frontend/src/components/ImportCourseConfigModal.jsx`, pruebas.
- Criterios: prueba de que un código `MP1C` nunca contiene notas, ids de curso ni datos del autor; al importar se muestra carrera, período y fecha; la copia importada es editable e independiente; disponible sin sesión.
- Pruebas: inspección del contenido decodificado; editar la copia no cambia el original.

## E3 · Catálogo

### T-030 · Búsqueda en el catálogo y etiquetas de origen
- Tipo: code · Riesgo: medio · Requisitos: CA-01, CA-02 · Depende de: T-010
- Criterios: buscar por universidad y carrera sin importar tildes ni mayúsculas; cada resultado muestra versión, fuente y etiqueta "Verificada por MallaPro" o "Comunitaria" (nunca "oficial"); las mallas personales no aparecen.
- Pruebas: "informatica" encuentra ambas carreras de informática; una malla personal no aparece.

### T-031 · Publicar versiones del catálogo
- Tipo: code · Riesgo: alto · Requisitos: CA-03, AD-01, NF-11 · Depende de: T-002, T-015
- Criterios: solo `curator` y `superadmin` publican, archivan o cambian la versión actual; editar una versión publicada crea una nueva; publicar exige validación sin errores; los perfiles existentes siguen en su versión; todo queda auditado.
- Pruebas: estudiante recibe 403; edición crea versión; auditoría.

### T-032 · Malla personal: crear y editar
- Tipo: code · Riesgo: medio · Requisitos: MP-01, CA-02 · Depende de: T-015, T-020, D-02
- Criterios: crear desde cero o duplicar del catálogo; editar períodos, cursos, códigos y créditos opcionales y requisitos; se guarda como borrador aunque tenga errores, pero no se planifica sobre ella hasta corregirlos; privada de su dueño.
- Pruebas: crear, editar, duplicar; aislamiento; conflicto de versión.

### T-033 · Vista de la malla: dependencias y accesibilidad
- Tipo: code · Riesgo: medio · Requisitos: MP-02, NF-04, NF-05 · Depende de: T-012
- Criterios: al seleccionar un curso se ven sus requisitos y lo que desbloquea, con toque en móvil y con teclado (sin depender de clic largo ni de Ctrl+clic); los estados no dependen solo del color; malla de 100 cursos interactiva en menos de 3 s en el perfil móvil documentado.
- Pruebas: prueba de componente con teclado; medición documentada en el PR.

### T-034 · Reportes de error y propuestas de malla
- Tipo: code · Riesgo: medio · Requisitos: MP-03, AD-02 · Depende de: T-002
- Criterios: tabla `reports` (categoría, motivo, contexto mínimo, estado); un usuario reporta un error de una malla o propone la suya; el reporte es privado y no publica datos del autor; reemplaza el formulario actual de contacto para mallas nuevas si corresponde.
- Pruebas: crear reporte; otro estudiante no lo ve.

## E4 · Tutores

### T-040 · Perfil de tutor y servicios
- Tipo: code · Riesgo: alto · Requisitos: TU-01, TU-02, TU-06, TU-07, TU-10 · Depende de: T-002, T-004
- Criterios: tablas `tutor_profiles`, `tutor_services`, `tutor_service_links`; consentimiento explícito antes de publicar el WhatsApp, validado en formato internacional; pausar o retirar oculta ficha y contacto; el tutor solo edita lo suyo; se reemplaza la maqueta local (`tutorsStorage.js`) y se **quitan las calificaciones**, porque las reseñas están fuera de alcance (sección 5.2).
- Pruebas: sin consentimiento no publica; ficha pausada no expone el número; aislamiento.

### T-041 · Buscar tutores, ficha y WhatsApp
- Tipo: code · Riesgo: medio · Requisitos: TU-03, TU-04, TU-05, TU-10 · Depende de: T-040
- Criterios: filtros por texto, asignatura, carrera, universidad, modalidad y precio; "a convenir" separado; buscar un ramo devuelve servicios vinculados por curso, no por nombre; botón `wa.me` con mensaje editable que no envía nada solo.
- Pruebas: vínculo por curso frente a materia genérica; sin resultados permite ampliar filtros.

### T-042 · Moderación de tutores y reportes
- Tipo: code · Riesgo: alto · Requisitos: TU-08, TU-09, NF-11 · Depende de: T-040, T-034
- Criterios: estados borrador, pendiente, publicado, rechazado y suspendido, con motivo; reportes privados con seguimiento; cada acción del equipo auditada.
- Pruebas: flujo de revisión; estudiante no puede moderar.

## E5 · Equipo y datos personales

### T-050 · Panel básico del equipo
- Tipo: code · Riesgo: alto · Requisitos: AD-01, AD-02, AD-03 · Depende de: T-002, T-031, T-034
- Criterios: listas de mallas, reportes y tutores pendientes; acciones auditadas; sin acceso a notas ni avance de estudiantes.
- Pruebas: matriz de permisos; acciones auditadas.

### T-051 · Eventos de producto
- Tipo: code · Riesgo: medio · Requisitos: AN-01, sección 13 · Depende de: T-003
- Criterios: tabla `product_events` y función de registro con lista cerrada de nombres (sección 13); solo se registra al completar la operación; sin datos personales en las propiedades; convive con GA4 (`frontend/src/utils/analytics.js`).
- Pruebas: un nombre fuera de la lista falla; propiedades con correo se rechazan.

### T-052 · Métricas de uso agregadas
- Tipo: code · Riesgo: medio · Requisitos: AD-07, NF-10 · Depende de: T-050, T-051
- Criterios: usuarios activos diarios y mensuales, registros, mallas más usadas, búsquedas sin resultado y configuraciones compartidas e importadas, solo agregadas y ocultas bajo un mínimo configurable de usuarios.
- Pruebas: un agregado bajo el mínimo no se muestra; un curador no ve métricas comerciales.

### T-053 · Exportar datos y eliminar cuenta
- Tipo: code · Riesgo: alto · Requisitos: CU-04 · Depende de: T-021, T-025, T-027
- Criterios: exportación JSON con perfil, avance, notas, excepciones y horario; solicitud de eliminación con plazo informado y borrado efectivo (incluido el usuario en Firebase, si se decide).
- Pruebas: la exportación contiene todo lo creado; tras el borrado no quedan datos del usuario.

## E6 · Operación

### T-060 · Despliegue del backend en VPS
- Tipo: infra · Riesgo: alto · Requisitos: NF-12, NF-02 · Depende de: T-003
- Criterios: Docker Compose de producción con Caddy (HTTPS), backend y PostgreSQL; credenciales de Firebase en base64 por variable de entorno; migraciones al desplegar; entorno de prueba separado; el frontend apunta a la API con `VITE_API_URL`.
- Pruebas: despliegue documentado paso a paso y verificado en el entorno de prueba.

### T-061 · Respaldos y restauración probada
- Tipo: infra · Riesgo: alto · Requisitos: NF-06 · Depende de: T-060
- Criterios: `pg_dump` diario cifrado a almacenamiento externo; restauración probada en una base limpia, con el tiempo medido.
- Pruebas: registro de una restauración real.

### T-062 · Monitoreo de errores y disponibilidad
- Tipo: infra · Riesgo: medio · Requisitos: NF-07 · Depende de: T-060
- Criterios: Sentry en backend y frontend con datos sensibles filtrados; Uptime Kuma sobre `/api/v1/health`.
- Pruebas: error de prueba visible en Sentry sin token ni notas.

### T-063 · Pruebas de extremo a extremo
- Tipo: code · Riesgo: medio · Requisitos: NF-09, sección 16 · Depende de: T-022, T-025, T-027
- Criterios: Playwright cubre elegir malla, marcar avance, notas, compartir configuración y horario, con y sin sesión, en escritorio y a 360 px.
- Pruebas: la propia suite en CI.

---

## Épicas posteriores

- **V2.1 · Importación con IA de mallas** — IA-01…IA-07, NF-08. Base: `tools/verificacion-oficial/` (Banner por texto u OCR).
- **V2.1 · Importación de oferta** — OF-01…OF-05. Base: los parsers de `frontend/src/features/academicProgramming/parsers/`.
- **V2.1 · Mallas comunitarias y curaduría** — MC-01…MC-06, AD-04…AD-06.
- **V2.2 · Prueba de 2 meses y suscripción** — PR-01…PR-06, CO-01…CO-07, AD-08.
- **V2.2 · Planificación avanzada y generador de horarios** — PA-01…PA-09.
- **Posterior · Sugerencias por coincidencia** — SC-01…SC-05, NF-10.
