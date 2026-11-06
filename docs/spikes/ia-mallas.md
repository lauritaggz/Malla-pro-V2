# Prototipo: mallas desde PDF o foto con IA (rama `spike/ia-mallas`)

**Estado:** prototipo para medir, no es una tarea del backlog ni va a `main` sin diseño (épica V2.1, IA-01 a IA-05, D-07, D-08) y auditoría.

## Qué hace

`app.scripts.ai_extract_malla` manda un PDF o una foto a Claude y recibe la malla en un formato fijo (herramienta con esquema). Luego:

1. La convierte al formato de `frontend/public/mallas/` y la marca como **borrador** (`"estado": "borrador"`). No se importa ni se guarda en la base.
2. Aplica las reglas de no inventar: un requisito ilegible, uno que apunta a un ramo que no está en el documento o uno "conocido" sin ramos listados queda como **desconocido** (`prereq_status: "unknown"`), nunca como "sin requisitos". "Semestre N aprobado" se convierte en todos los ramos hasta el semestre N, como en las mallas verificadas.
3. Revisa la estructura con los mismos chequeos del importador (ids repetidos o inexistentes, autorreferencias, ciclos, requisitos en el mismo semestre o después, códigos repetidos) y que los créditos sumen el total.
4. Con `--compare`, mide el acierto contra una malla verificada: cobertura de ramos, ramos inventados, semestre, créditos y prerrequisitos (correctos, incorrectos y desconocidos).

No muestra el contenido del documento en la salida (NF-07). El borrador sí lo contiene: guárdalo en `backend/ia-pruebas/`, que está en `.gitignore`.

## Cómo probarlo (en tu computador)

1. En `backend/.env` agrega `ANTHROPIC_API_KEY=...` (nunca en git ni en el chat).
2. Copia los documentos a `backend/ia-pruebas/` (por ejemplo, desde tu carpeta "Mallas PDF").
3. Con Docker: `docker compose restart backend` (instala el SDK `anthropic`, que es dependencia nueva) y luego:

```bash
docker compose exec backend uv run --no-sync python -m app.scripts.ai_extract_malla \
  "ia-pruebas/MALLA Q - corregido (1).pdf" \
  --compare /app/frontend/public/mallas/QuimicaUCH.json \
  --out ia-pruebas/quimica.borrador.json
```

Sin Docker, desde `backend/`: `uv sync` y el mismo comando con `uv run python -m ...` y `--compare ../frontend/public/mallas/QuimicaUCH.json`.

## Ruta para la pantalla de la demo

`POST /api/v1/me/malla-drafts?compare_with=<Malla>` con el archivo como cuerpo (`Content-Type: application/pdf` o `image/png|jpeg|webp|gif`, máximo 10 MB). Exige sesión y **solo responde en desarrollo y con `ANTHROPIC_API_KEY`** (si no, 503), para que nadie más gaste los créditos. Parámetro opcional `filename` (nombre del archivo, para reconocerlo en el historial). Devuelve `id`, `creado`, `documento`, `malla` (borrador), `advertencias`, `problemas`, `desconocidos`, `modelo`, `tokens`, `cortado` y, con `compare_with` (nombre de un archivo de `public/mallas`, sin `.json`), `comparacion`. Errores en español: 415 formato, 413 tamaño, 400 vacío, 404 malla para comparar desconocida, 502 si falla la IA (sin texto del documento).

La pantalla se hace con el diseño de Laura en Figma.

### Historial de prueba

Cada borrador que sale bien se guarda como JSON en `backend/ia-pruebas/historial/<id de usuario>/<id>.json` (carpeta ignorada por git; se cambia con `AI_DRAFTS_DIR`). **Nunca se guarda el documento subido**, solo el borrador (D-08). Las rutas solo funcionan en desarrollo y con la clave, igual que la de arriba, y cada usuario ve solo lo suyo (registradas en las pruebas de aislamiento):

- `GET /api/v1/me/malla-drafts`: lista, del más nuevo al más antiguo, con `id`, `creado`, `documento`, `carrera`, `ramos`, `desconocidos`, `modelo`, `cobertura_pct` (o `null` si no se comparó).
- `GET /api/v1/me/malla-drafts/{id}`: el borrador completo, igual a lo que devolvió el `POST`.
- `DELETE /api/v1/me/malla-drafts/{id}`: lo borra (204).

Un borrador de otro usuario, o un id que no existe, da 404. Para revisar a mano basta abrir los JSON de la carpeta.

## Pruebas sugeridas para la demo

| Documento | Comparar con | Por qué |
|---|---|---|
| `MALLA Q - corregido (1).pdf` | `QuimicaUCH.json` | PDF con texto, ramos numerados |
| `imagen-20260428-001.webp` | `QuimicaFarmaciaUCH.json` | Imagen (foto o captura) |
| `ICINF.malla.pdf` (Banner) | `CInf.json` | Formato Banner de la UNAB, con códigos oficiales |
| `Tecnología Médica.pdf` | `TM.json` | Tiene menciones: el prototipo todavía no las separa (aparecerá como advertencia o con ramos sin cruzar) |

## Resultados

| Fecha | Documento | Modelo | Ramos (cruzados / verificados) | Inventados | Semestre | Créditos | Prerrequisitos correctos | Desconocidos | Tokens (entrada / salida) |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

## Límites conocidos

- No separa menciones ni planes con especialidades.
- Una sola llamada por documento, con `max_tokens` de 16 000: una malla muy grande puede cortarse (el script avisa).
- Las alternativas ("A o B") quedan como texto en `prereq_expr` y solo se exigen los ramos obligatorios; el formato actual no tiene árboles (T-012).
- Sin caché, cola de tareas, límites de uso ni pantalla de revisión: eso es el diseño de la V2.1.
