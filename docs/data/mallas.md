# Mallas del catálogo

`frontend/public/mallas/` tiene las mallas en el formato JSON de la versión pública. El frontend las usa directamente cuando no hay API, y el backend las importa al catálogo con `uv run python -m app.scripts.import_legacy_mallas ../frontend/public/mallas`.

**Estado (29-10-2026, T-010):** las 9 mallas UNAB son las verificadas contra los documentos oficiales y están las 4 de la U. de Chile, 3 de ellas verificadas. Las UNAB son idénticas, byte a byte, a las que publica la versión pública (repo `Malla_Pro`, commit `543e5e6`); las 3 UCH verificadas solo agregan el campo `fuente_oficial`. El detalle de cada corrección está en `docs/data/verificacion-mallas-oficiales.md`.

| Archivo | Carrera | Documento oficial | Lectura |
|---|---|---|---|
| Comp.json | Ingeniería en Computación e Informática | UNAB11500, catálogo 2020 | OCR + revisión manual |
| CInf.json | Ingeniería Civil Informática | UNAB12210, 2020 | OCR + revisión manual |
| Industrial.json | Ingeniería Civil Industrial | UNAB12100, 2020 | OCR + revisión manual |
| Minas.json | Ingeniería Civil en Minas | UNAB11303, 2022 | OCR + revisión manual |
| Geo.json | Geología | UNAB11350, 2022 | OCR + revisión manual |
| MM.json | Ingeniería en Marina Mercante | UNAB14001, 2020 | OCR + revisión manual |
| Med.json | Medicina | UNAB19710, 2025 | texto |
| TM.json | Tecnología Médica | UNAB19600, 2018 | texto |
| Psicologia.json | Psicología | UNAB11900, 2018 | texto |
| BioquimicaUCH.json | Bioquímica (U. de Chile) | `MALLA BQ - corregido (1).pdf` | revisión visual (29-10-2026) |
| IngenieriaAlimentosUCH.json | Ingeniería en Alimentos (U. de Chile) | `malla ing en alimentos uch}.pdf` | revisión visual (29-10-2026) |
| QuimicaFarmaciaUCH.json | Química y Farmacia (U. de Chile) | `imagen-20260428-001.webp` | revisión visual (29-10-2026) |
| QuimicaUCH.json | Química (U. de Chile) | **sin contrastar** | — |

Regla: una malla con `fuente_oficial` fue verificada contra un documento; sin `fuente_oficial`, no. El importador lo deja escrito en `source_note`.

## Campos y cómo los importa el backend

| Campo | Dónde queda |
|---|---|
| `carrera`, `codigo_programa`, `totalSemestres`, `total_creditos`, `total_creditos_por_mencion`, `semestres`, `semestres_comunes`, `menciones`, `menciones_disponibles` | columnas de `programs`, `curriculum_versions`, `tracks` y `courses` |
| `universidad` | se compara con la universidad registrada para el archivo en `LEGACY_PROGRAMS`; si no coincide, la importación falla. Se guarda también en `curriculum_versions.attrs` |
| `fuente_oficial` | `curriculum_versions.attrs` tal cual, y un resumen en `source_note` (`source_type` sigue siendo `legacy_json`: el dato viene del JSON) |
| `nota_codigos` | `curriculum_versions.attrs` tal cual |
| `equivalencias` (`{código: [[códigos antiguos], …]}`) | `curriculum_versions.attrs` tal cual. **No** se convierten en `course_aliases`: ver abajo |
| `courseCodeAliases` | `course_aliases` (los usa la importación del horario para cruzar códigos) |
| Campos de curso `area`, `linea` y cualquier otro sin columna | `courses.attrs` |
| Cualquier otra clave de primer nivel | `curriculum_versions.attrs`, y aparece en el informe como `campo_no_modelado` |

Las equivalencias son "aprobar estos ramos de un plan antiguo cuenta como este ramo"; un alias es "este ramo también se escribe así". Si fueran alias, con la API la importación del horario cruzaría códigos que sin la API no cruza, y un código antiguo puede ser equivalente de dos ramos (p. ej. FMF023 de CFIS310 y de CFIS328). Usarlas para el avance es una regla académica nueva y va en su propia tarea.

## Universidad y `career_key`

| Universidad (`slug`) | Archivos | `career_key` |
|---|---|---|
| `unab` | `/mallas/<Nombre>.json` | `unab-<nombre>` |
| `uch` | `/mallas/<Nombre>UCH.json` | `unab-<nombre>uch` |

Las de la U. de Chile no están en una carpeta `uch/` porque la versión pública ya las sirve en `/mallas/<Nombre>UCH.json` y guarda el avance con la clave que sale de esa URL. El prefijo `unab-` es histórico: el `career_key` es un identificador opaco y no indica la universidad (eso lo hace `programs.university_id`). Una malla nueva de otra universidad sí puede ir en `/mallas/<uni>/<Nombre>.json` (`<uni>-<nombre>`).

## Reglas

- Los `id` numéricos de los cursos y el nombre del archivo (del que sale el `career_key`) no cambian nunca: de ellos depende el avance guardado de los usuarios (ADR-0007).
- Una corrección es una tarea de tipo `data`: cita el documento oficial, adjunta la comparación y no mezcla otro código.

## Cómo verificar o corregir una malla

Herramientas en `tools/verificacion-oficial/` (requieren `poppler-utils`, `tesseract` y `pytesseract`):

1. `python3 tools/verificacion-oficial/grid.py MALLA.pdf raw.json text` (`ocr` si el PDF es una imagen).
2. `python3 tools/verificacion-oficial/oficial.py raw.json frontend/public/mallas/X.json oficial.json`
3. `python3 tools/verificacion-oficial/comparar.py oficial.json frontend/public/mallas/X.json diferencias.json`
4. Revisar en el PDF cada diferencia que venga de OCR; luego `corregir.py` o editar el JSON.
5. Volver a comparar: cero diferencias, salvo las explicadas en el PR.
