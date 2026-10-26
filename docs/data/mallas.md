# Mallas del catálogo

`frontend/public/mallas/` tiene las mallas en el formato JSON de la versión pública. El frontend las usa directamente cuando no hay API, y el backend las importa al catálogo con `uv run python -m app.scripts.import_legacy_mallas ../frontend/public/mallas`.

**Estado (26-10-2026):** las 9 mallas UNAB del repo todavía son las originales. Las versiones verificadas contra los documentos oficiales y las 4 de la U. de Chile entran con la tarea T-010. El detalle de cada corrección está en `docs/data/verificacion-mallas-oficiales.md`.

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
| 4 carreras de la U. de Chile | Bioquímica, Ing. en Alimentos, Química, Química y Farmacia | sin contrastar | códigos internos |

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
