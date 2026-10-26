# Verificación de mallas contra documentos oficiales (Banner UNAB)

| Script | Qué hace |
|---|---|
| `grid.py` | Extrae las filas de la tabla "Malla curricular" de un PDF, con la capa de texto (`text`) o con OCR (`ocr`) |
| `oficial.py` | Normaliza códigos, semestres, menciones y requisitos a una malla oficial estructurada (también lee el HTML de Banner) |
| `comparar.py` | Compara la malla oficial con un JSON de `frontend/public/mallas/` y lista diferencias |
| `corregir.py` | Aplica las diferencias verificadas y genera el JSON corregido y la lista de cambios |
| `overrides.json` | Correcciones manuales de códigos leídos mal por OCR |

Son herramientas de datos, no parte de la aplicación. Sirven de base para el parser de V2.1 (importación de mallas). Ver `docs/data/mallas.md`.
