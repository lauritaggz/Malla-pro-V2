# AGENTS.md — Instrucciones para agentes de desarrollo

Contrato de trabajo para cualquier agente (o persona) que modifique este repositorio. Complementa `CLAUDE.md`, que sigue vigente: si algo de aquí choca con `CLAUDE.md` o con una tarea, **detente y pregunta en el PR**.

## 1. El proyecto

Malla Pro es una plataforma web para estudiantes universitarios de Chile: malla con prerrequisitos, avance, notas (escala 1–7, eximición), horario, toma de ramos, configuraciones de ramo compartidas y directorio de tutores. La versión pública (mallapro.cl) funciona sin cuenta y guarda todo en el navegador. Este repo es la **V2**: el mismo frontend, ahora con backend, cuentas y base de datos.

Dueña del producto: Laura Gonzalez Vergara. Aprueba alcance, decisiones y cada merge a `main`.

## 2. Fuentes de verdad (en orden)

1. `CLAUDE.md` y este archivo.
2. `docs/requirements/requerimientos-v1.2.md`: qué se construye; cada requisito tiene un ID (CU-01, AV-04, NF-01…).
3. `docs/adr/`: decisiones técnicas tomadas. No las contradigas; si una no sirve, propón un ADR nuevo.
4. `docs/architecture/`: cómo está organizado el sistema y el modelo de datos.
5. `docs/plan/backlog.md`: las tareas (T-xxx). **Solo trabajas en una tarea asignada.**
6. El código y sus pruebas.

Si dos fuentes se contradicen, gana la de número menor y reportas la contradicción en el PR.

## 3. Estructura y comandos

```
frontend/   React 19 + Vite + Tailwind + React Router (JavaScript). Auth con Firebase (Google).
backend/    Python 3.12, FastAPI, SQLAlchemy 2 async, Alembic, Pydantic v2, pytest, uv, ruff.
docs/       Requerimientos, arquitectura, ADR, proceso, plan, datos y auditorías.
tools/      Herramientas de datos (verificación de mallas contra documentos oficiales).
```

```bash
# Infraestructura (raíz)
docker compose up -d postgres                # solo PostgreSQL 16
docker compose up --build                    # todo: Postgres + backend (8000) + frontend (5174)

# Backend (backend/)
uv sync
uv run alembic upgrade head
uv run python -m app.scripts.import_legacy_mallas ../frontend/public/mallas
uv run ruff check && uv run ruff format --check
uv run pytest

# Frontend (frontend/)
npm ci
npm run lint
npm test
npm run build
```

Antes de abrir un PR, todos los comandos del lado que tocaste deben pasar. CI los corre en cada push (`.github/workflows/ci.yml`).

## 4. Reglas que no se negocian

Si una tarea te obliga a romper alguna, no la rompas: explica el conflicto en el PR.

**Datos y privacidad**
- Toda lectura o escritura de datos de un usuario filtra por el usuario autenticado (`get_current_user`) **en el backend**. Nunca confíes en un id enviado por el cliente sin verificar que es suyo (NF-01).
- Notas, avance, horarios, excepciones y mallas personales son privados. Lo compartido (configuraciones de ramo, mallas comunitarias) nunca incluye notas ni datos del autor más allá de un alias opcional (NO-04).
- No registres en logs, errores ni eventos: notas, contenido de documentos subidos, tokens de Firebase ni correos completos (NF-07).
- Nunca subas secretos: `.env`, `firebase-sa*.json`, claves de IA.

**Avance guardado de usuarios reales**
- La versión pública guarda el avance en `localStorage` con claves por carrera (`frontend/src/utils/storageKeys.js`) y por `id` numérico de curso. Ese `id` y el `career_key` de cada carrera **no pueden cambiar** (`backend/app/services/career_key.py` debe seguir idéntico a `getCareerId()`).
- Cualquier cambio en el formato de `localStorage` incluye migración, respaldo de los datos anteriores y pruebas de que no se pierde nada.

**Reglas académicas**
- Nunca inventes una regla. "Sin prerrequisitos" (`prereq_status = "none"`) y "desconocidos" (`"unknown"`) son distintos: si no se sabe, el resultado es desconocido, no disponible (AV-04, sección 6).
- El cálculo de disponibilidad, notas y topes es determinista y puro: sin red, sin reloj implícito, sin IA (ADR-0005).
- Una nota calculada no aprueba un ramo (NO-03). Una excepción no aprueba un ramo ni cambia el catálogo (AV-05).
- No unas cursos, tutores u ofertas por nombres parecidos: por código, alias declarado o elección explícita del usuario.
- La IA solo produce borradores que el usuario revisa.

**Mallas del catálogo**
- `frontend/public/mallas/` es la fuente que importa el backend y que usa la versión sin backend. Solo se modifica en una tarea de tipo `data`, con la fuente oficial citada y el informe de comparación (`docs/data/mallas.md`).

**Permisos**
- Roles y permisos se validan en el backend. Pagar nunca da permisos de equipo.
- Toda acción de curador o superadministrador queda en el registro de auditoría (NF-11).

**Código**
- Código, nombres y commits en inglés; interfaz y mensajes al usuario en español de Chile (`CLAUDE.md`).
- Backend: tipado completo, Pydantic para toda entrada y salida, `ruff` sin advertencias. Cada cambio de modelo va con su migración de Alembic en el mismo PR, reversible (`downgrade`) y probada.
- Frontend: sin dependencias nuevas sin justificar; lógica de dominio en funciones puras con pruebas en Vitest, fuera de los componentes.
- No agregues dependencias sin decirlo en el PR (nombre, versión, para qué, alternativa descartada).
- Archivos en UTF-8 sin BOM y saltos LF.

## 5. Cómo trabajas una tarea

Detalle en `docs/process/workflow.md`. Resumen:

1. Lee la tarea en `docs/plan/backlog.md`, los requisitos que cita y los ADR relacionados. Confirma que está **ready** y que sus dependencias están **done**.
2. Rama `v2/t0XX-short-name` desde `main`.
3. Antes de escribir código, deja el plan en el PR en borrador: archivos que vas a tocar, enfoque, pruebas por criterio y preguntas abiertas. Si la tarea es ambigua o el cambio es grande, **espera la aprobación** (regla de `CLAUDE.md`).
4. Implementa **solo** lo que pide la tarea. Lo que encuentres fuera de alcance va a "Hallazgos" en el PR.
5. Cada criterio de aceptación tiene al menos una prueba que falla si el criterio no se cumple.
6. Corre lint, pruebas y build. Completa la plantilla del PR.
7. Pide la auditoría (`/audit T-0XX`). Corrige y vuelve a pedirla.
8. Laura revisa y hace el merge. Tú no haces merge a `main` ni force-push.

## 6. Definición de terminado

- [ ] Cada criterio de aceptación tiene una prueba automatizada que pasa, o una verificación manual documentada en el PR si no es automatizable.
- [ ] CI en verde (backend y frontend).
- [ ] Sin cambios fuera del alcance de la tarea.
- [ ] Endpoints nuevos: Pydantic en entrada y salida, dependencia de autenticación o rol explícita y, si tocan datos privados, prueba de aislamiento con dos usuarios.
- [ ] Pantallas nuevas: usables desde 360 px, con teclado, y los estados no dependen solo del color (NF-05).
- [ ] Errores con mensaje útil en español y sin datos sensibles en los logs (NF-07).
- [ ] Documentación actualizada si cambió un contrato (API, formato de malla, modelo de datos, `localStorage`), y una línea en `CHANGELOG.md`.
- [ ] Informe de auditoría con veredicto **APROBADO** en `docs/audits/`.

## 7. Cuando no sabes algo

No adivines. Escribe la pregunta en el PR bajo "Preguntas abiertas" con el supuesto que tomarías, y no avances en esa parte hasta que Laura responda. Ante datos académicos dudosos, la respuesta segura siempre es "desconocido".
