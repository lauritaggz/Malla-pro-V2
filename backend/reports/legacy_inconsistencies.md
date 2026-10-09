# Inconsistencias en las mallas legadas

Generado por `uv run python -m app.scripts.import_legacy_mallas`. Los datos se importaron
tal cual (es el comportamiento actual de la app); este archivo es para revisarlos
contra las mallas oficiales. No se corrigió nada.

## Resumen

| Malla | id_duplicado | id_inexistente | autorreferencia | ciclo | prereq_fuera_del_alcance | prereq_mismo_periodo_o_posterior | texto_distinto_de_ids | ids_sin_texto | texto_sin_ids | correq_texto_distinto_de_ids | alternativas_ignoradas | codigo_repetido | campo_no_modelado | creditos_totales_cero |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ingeniería Civil Industrial | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 43 | 0 | 0 | 0 | 0 | 51 | 0 |
| Ingeniería en Computación e Informática | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 16 | 0 | 0 | 0 | 0 | 0 | 1 |
| Geología | 0 | 0 | 0 | 0 | 0 | 1 | 6 | 0 | 0 | 0 | 42 | 0 | 0 | 1 |
| Ingeniería en Marina Mercante | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 29 | 10 | 0 | 0 |
| Ingenería Civil Informática | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 15 | 0 | 0 | 0 | 0 | 0 | 0 |
| Ingeniería Civil en Minas | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 12 | 0 | 0 | 0 |
| Medicina | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 41 | 0 | 0 | 1 |
| Tecnología Médica | 0 | 0 | 0 | 0 | 0 | 2 | 10 | 0 | 0 | 0 | 125 | 13 | 0 | 0 |
| Psicología | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 | 0 | 0 | 1 |

Leyenda de columnas: `id_duplicado` = Id de curso repetido (se ignora la segunda aparición); `id_inexistente` = Prerrequisito apunta a un id que no existe; `autorreferencia` = Curso es prerrequisito de sí mismo; `ciclo` = Ciclo de prerrequisitos; `prereq_fuera_del_alcance` = Prerrequisito de otra mención; `prereq_mismo_periodo_o_posterior` = Prerrequisito en el mismo período o uno posterior; `texto_distinto_de_ids` = El texto prereq_expr no coincide con los ids de prerrequisitos; `ids_sin_texto` = Tiene ids de prerrequisitos pero prereq_expr vacío o ausente; `texto_sin_ids` = Tiene texto en prereq_expr pero ningún id de prerrequisito; `correq_texto_distinto_de_ids` = El texto correq_expr no coincide con los ids de correquisitos; `alternativas_ignoradas` = prereq_expr menciona alternativas ("o"/equivalentes); solo se aplican los ids; `codigo_repetido` = Mismo código con ids distintos (una copia por mención); `campo_no_modelado` = Campo del JSON que el modelo no representa (se conserva en attrs); `creditos_totales_cero` = total_creditos = 0 (se interpreta como desconocido)

## Ingeniería Civil Industrial

### Tiene ids de prerrequisitos pero prereq_expr vacío o ausente (43)

- **CFIS328 — Física Experimental** (id 6, período 2): ids: CFIS310, FMMP012
- **FMMP112 — Cálculo Diferencial** (id 7, período 2): ids: FMMP012
- **TDFI103 — Base de Datos** (id 9, período 2): ids: TDFI102
- **ACAD101 — Taller de Innovación y Emprendimiento I** (id 10, período 3): ids: TDFI101
- **CFIS332 — Mecánica** (id 11, período 3): ids: CFIS328, FMMP112
- **FMMP212 — Cálculo Integral** (id 12, período 3): ids: FMMP112
- **TDFI104 — Compliance & Accountability** (id 13, período 3): ids: TDFI101
- **CIND100 — Procesos Industriales** (id 14, período 3): ids: CFIS310, QUIM090
- **ACAD102 — Taller de Innovación y Emprendimiento II** (id 15, período 4): ids: ACAD101
- **CFIS344 — Electricidad y Magnetismo** (id 16, período 4): ids: CFIS332, FMMP212
- **CIND311 — Práctica I** (id 17, período 4): ids: ACAD101, CFIS310, CFIS328, CFIS332, CIND100, FMMP012, FMMP112, FMMP212, QUIM090, TDFI101, TDFI102, TDFI103, TDFI104
- **FMMP312 — Sistemas y Ecuaciones Diferenciales Lineales** (id 18, período 4): ids: FMMP212
- **CIND111 — Economía Circular** (id 20, período 5): ids: CIND100
- **CIND112 — Investigación de Operaciones** (id 21, período 5): ids: FMMP212
- **CIND411 — Economía** (id 22, período 5): ids: FMMP212
- **FMSP316 — Métodos Cuantitativos** (id 23, período 5): ids: FMMP212
- **ING129 — Inglés II** (id 24, período 5): ids: ING119
- **ACAD103 — Taller de Innovación y Emprendimiento III** (id 25, período 6): ids: ACAD102
- **CIND113 — Gestión de la Cadena de Suministro** (id 26, período 6): ids: CIND112
- **CIND211 — Redes y Sistemas Estocásticos en Ingeniería** (id 27, período 6): ids: CIND112, FMSP316
- **IIND412 — Costos y Presupuestos** (id 28, período 6): ids: FMMP212
- **ING239 — Inglés III** (id 29, período 6): ids: ING129
- **TDFI105 — Minería de Datos** (id 30, período 6): ids: FMSP316, TDFI103
- **CIND114 — Toma de Decisiones en la Cadena de Suministro** (id 32, período 7): ids: CIND113
- **CIND212 — Toma de Decisiones Bajo Incertidumbre** (id 33, período 7): ids: CIND211
- **IIND413 — Ingeniería Económica** (id 34, período 7): ids: IIND412
- **ING249 — Inglés IV** (id 35, período 7): ids: ING239
- **TDFI106 — Gestión de la Transformación Digital** (id 36, período 7): ids: TDFI104
- **CIND213 — Simulación de Sistemas** (id 37, período 8): ids: CIND212
- **CIND214 — Estrategia y Sustentabilidad en Cadena de Suministro** (id 38, período 8): ids: CIND212
- **CIND215 — Analítica** (id 39, período 8): ids: CIND212
- **CIND312 — Seminario de Licenciatura en Ciencias de la Ingeniería** (id 40, período 8): ids: CIND114, CIND212, IIND413, TDFI105
- **CIND313 — Práctica II** (id 41, período 8): ids: CIND114, CIND212, IIND413, TDFI105
- **IIND414 — Evaluación de Proyectos** (id 42, período 8): ids: IIND413
- **CIND216 — Finanzas Corporativas** (id 43, período 9): ids: IIND413
- **CIND217 — Inteligencia de Negocios** (id 44, período 9): ids: CIND215
- **CIND218 — Marketing** (id 45, período 9): ids: CIND411
- **CIND219 — Gestión Estratégica** (id 46, período 9): ids: CIND411
- **CIND220 — Tópicos de Especialidad I** (id 47, período 9): ids: CIND312
- **CIND314 — Portafolio de Proyectos** (id 48, período 9): ids: CIND312
- **CIND221 — Tópicos de Especialidad II** (id 49, período 10): ids: CIND312
- **CIND222 — Tópicos de Especialidad III** (id 50, período 10): ids: CIND312
- **CIND315 — Proyecto de Título** (id 51, período 10): ids: CIND314

### Campo del JSON que el modelo no representa (se conserva en attrs) (51)

- **CFIS310 — Física General** (id 1, período 1): campo de curso `area` = 'fisica'
- **FMMP012 — Introducción a las Matemáticas** (id 2, período 1): campo de curso `area` = 'matematica'
- **TDFI101 — Introducción a la Ingeniería** (id 3, período 1): campo de curso `area` = 'formacion'
- **TDFI102 — Introducción a la Programación** (id 4, período 1): campo de curso `area` = 'computacion'
- **CEGHC11 — Habilidades Comunicativas** (id 5, período 2): campo de curso `area` = 'formacion'
- **CFIS328 — Física Experimental** (id 6, período 2): campo de curso `area` = 'fisica'
- **FMMP112 — Cálculo Diferencial** (id 7, período 2): campo de curso `area` = 'matematica'
- **QUIM090 — Química y Ambiente** (id 8, período 2): campo de curso `area` = 'quimica'
- **TDFI103 — Base de Datos** (id 9, período 2): campo de curso `area` = 'computacion'
- **ACAD101 — Taller de Innovación y Emprendimiento I** (id 10, período 3): campo de curso `area` = 'gestion'
- **CFIS332 — Mecánica** (id 11, período 3): campo de curso `area` = 'fisica'
- **FMMP212 — Cálculo Integral** (id 12, período 3): campo de curso `area` = 'matematica'
- **TDFI104 — Compliance & Accountability** (id 13, período 3): campo de curso `area` = 'formacion'
- **CIND100 — Procesos Industriales** (id 14, período 3): campo de curso `area` = 'industrial'
- **ACAD102 — Taller de Innovación y Emprendimiento II** (id 15, período 4): campo de curso `area` = 'gestion'
- **CFIS344 — Electricidad y Magnetismo** (id 16, período 4): campo de curso `area` = 'fisica'
- **CIND311 — Práctica I** (id 17, período 4): campo de curso `area` = 'industrial'
- **FMMP312 — Sistemas y Ecuaciones Diferenciales Lineales** (id 18, período 4): campo de curso `area` = 'matematica'
- **ING119 — Inglés I** (id 19, período 4): campo de curso `area` = 'formacion'
- **CIND111 — Economía Circular** (id 20, período 5): campo de curso `area` = 'industrial'
- **CIND112 — Investigación de Operaciones** (id 21, período 5): campo de curso `area` = 'industrial'
- **CIND411 — Economía** (id 22, período 5): campo de curso `area` = 'economia'
- **FMSP316 — Métodos Cuantitativos** (id 23, período 5): campo de curso `area` = 'matematica'
- **ING129 — Inglés II** (id 24, período 5): campo de curso `area` = 'formacion'
- **ACAD103 — Taller de Innovación y Emprendimiento III** (id 25, período 6): campo de curso `area` = 'gestion'
- **CIND113 — Gestión de la Cadena de Suministro** (id 26, período 6): campo de curso `area` = 'industrial'
- **CIND211 — Redes y Sistemas Estocásticos en Ingeniería** (id 27, período 6): campo de curso `area` = 'industrial'
- **IIND412 — Costos y Presupuestos** (id 28, período 6): campo de curso `area` = 'economia'
- **ING239 — Inglés III** (id 29, período 6): campo de curso `area` = 'formacion'
- **TDFI105 — Minería de Datos** (id 30, período 6): campo de curso `area` = 'computacion'
- **CEGRS14 — Responsabilidad Social** (id 31, período 7): campo de curso `area` = 'formacion'
- **CIND114 — Toma de Decisiones en la Cadena de Suministro** (id 32, período 7): campo de curso `area` = 'industrial'
- **CIND212 — Toma de Decisiones Bajo Incertidumbre** (id 33, período 7): campo de curso `area` = 'industrial'
- **IIND413 — Ingeniería Económica** (id 34, período 7): campo de curso `area` = 'economia'
- **ING249 — Inglés IV** (id 35, período 7): campo de curso `area` = 'formacion'
- **TDFI106 — Gestión de la Transformación Digital** (id 36, período 7): campo de curso `area` = 'computacion'
- **CIND213 — Simulación de Sistemas** (id 37, período 8): campo de curso `area` = 'industrial'
- **CIND214 — Estrategia y Sustentabilidad en Cadena de Suministro** (id 38, período 8): campo de curso `area` = 'industrial'
- **CIND215 — Analítica** (id 39, período 8): campo de curso `area` = 'computacion'
- **CIND312 — Seminario de Licenciatura en Ciencias de la Ingeniería** (id 40, período 8): campo de curso `area` = 'industrial'
- **CIND313 — Práctica II** (id 41, período 8): campo de curso `area` = 'industrial'
- **IIND414 — Evaluación de Proyectos** (id 42, período 8): campo de curso `area` = 'economia'
- **CIND216 — Finanzas Corporativas** (id 43, período 9): campo de curso `area` = 'economia'
- **CIND217 — Inteligencia de Negocios** (id 44, período 9): campo de curso `area` = 'computacion'
- **CIND218 — Marketing** (id 45, período 9): campo de curso `area` = 'gestion'
- **CIND219 — Gestión Estratégica** (id 46, período 9): campo de curso `area` = 'gestion'
- **CIND220 — Tópicos de Especialidad I** (id 47, período 9): campo de curso `area` = 'industrial'
- **CIND314 — Portafolio de Proyectos** (id 48, período 9): campo de curso `area` = 'industrial'
- **CIND221 — Tópicos de Especialidad II** (id 49, período 10): campo de curso `area` = 'industrial'
- **CIND222 — Tópicos de Especialidad III** (id 50, período 10): campo de curso `area` = 'industrial'
- **CIND315 — Proyecto de Título** (id 51, período 10): campo de curso `area` = 'industrial'

## Ingeniería en Computación e Informática

### El texto prereq_expr no coincide con los ids de prerrequisitos (6)

- **CFIS328 — Física Experimental** (id 7, período 2): texto: 'CFIS310'; ids: ['CFIS310', 'FMMP012']; en ids y no en el texto: ['FMMP012']
- **CFIS332 — Mecánica** (id 11, período 3): texto: 'CFIS310'; ids: ['CFIS328', 'FMMP112']; en el texto y no en ids: ['CFIS310']; en ids y no en el texto: ['CFIS328', 'FMMP112']
- **INSW410 — Portafolio de Proyectos** (id 32, período 7): texto: 'INSW321'; ids: ['INSW321', 'PTEC103', 'PTEC105']; en ids y no en el texto: ['PTEC103', 'PTEC105']
- **PTEC106 — Ingeniería de Software II** (id 36, período 7): texto: 'PTEC105'; ids: ['PTEC103', 'PTEC105']; en ids y no en el texto: ['PTEC103']
- **INSW420 — Práctica II** (id 37, período 8): texto: 'INSW220'; ids: ['ACAD103', 'INSW321', 'PTEC103']; en el texto y no en ids: ['INSW220']; en ids y no en el texto: ['ACAD103', 'INSW321', 'PTEC103']
- **INSW422 — Proyecto de Título** (id 39, período 8): texto: 'INSW421'; ids: ['INSW410']; en el texto y no en ids: ['INSW421']; en ids y no en el texto: ['INSW410']

### Tiene ids de prerrequisitos pero prereq_expr vacío o ausente (16)

- **ACAD101 — Taller de Innovación y Emprendimiento I** (id 5, período 2): ids: TDFI101
- **TDFI104 — Compliance & Accountability** (id 14, período 3): ids: TDFI101
- **FMSP316 — Métodos Cuantitativos** (id 15, período 4): ids: FMMP212
- **INSW220 — Práctica I** (id 17, período 4): ids: ACAD102, TDFI104
- **INSW221 — Tecnologías Disruptivas** (id 18, período 4): ids: TDFI103
- **INSW311 — Disrupción Empresarial** (id 21, período 5): ids: INSW221
- **INSW312 — Conectividad y Soluciones Móviles** (id 22, período 5): ids: INSW221
- **TDFI105 — Minería de Datos** (id 24, período 5): ids: FMSP316, TDFI103
- **INSW321 — Desafío Tecnológico** (id 27, período 6): ids: INSW311
- **PTEC105 — Ingeniería de Software I** (id 29, período 6): ids: PTEC102
- **TDFI106 — Gestión de la Transformación Digital** (id 30, período 6): ids: TDFI104
- **INSW411 — Tópico de Especialidad I** (id 33, período 7): ids: INSW311
- **INSW412 — Tópico de Especialidad II** (id 34, período 7): ids: INSW312
- **PTEC104 — Infraestructura TI** (id 35, período 7): ids: PTEC102
- **INSW421 — Seminario de Licenciatura en Ingeniería** (id 38, período 8): ids: INSW410, PTEC106
- **PTEC107 — Ciberseguridad** (id 40, período 8): ids: PTEC104

### total_creditos = 0 (se interpreta como desconocido) (1)

-: total_creditos = 0

## Geología

### Prerrequisito en el mismo período o uno posterior (1)

- **GEOL302 — Métodos analíticos i: microscopía óptica** (id 15, período 3): GEOL301 Geoquímica endógena (id 14) está en el período 3

### El texto prereq_expr no coincide con los ids de prerrequisitos (6)

- **GEOL704 — Geología de campo ii** (id 36, período 7): texto: '(GEOL603 o GEO403) y (GEOL602 o GEO307). Correquisitos: GEOL703 y GEOL702'; ids: ['GEOL602', 'GEOL603']; en el texto y no en ids: ['GEOL702', 'GEOL703']
- **GEOL803 — Hidrogeología** (id 40, período 8): texto: 'GEOL702 o GEO306. Correquisitos: GEOL804 y GEOL801'; ids: ['GEOL702']; en el texto y no en ids: ['GEOL801', 'GEOL804']
- **GEOL805 — Integrador ii: seminario licenciatura en ciencias geológicas** (id 42, período 8): texto: '(GEOL704 o GEO407) y (GEOL701 o GEO407 y GEO402). Correquisitos: GEOL804 y GEOL803'; ids: ['GEOL701', 'GEOL704']; en el texto y no en ids: ['GEOL803', 'GEOL804']
- **GEOL903 — Geología de campo iii** (id 46, período 9): texto: 'GEOL805 o GEO405. Correquisitos: GEOL901 y GEOL904'; ids: ['GEOL805']; en el texto y no en ids: ['GEOL901', 'GEOL904']
- **GEOL906 — Portafolio de proyectos** (id 49, período 9): texto: 'GEOL805 o GEO405. Correquisito: GEOL903'; ids: ['GEOL805']; en el texto y no en ids: ['GEOL903']
- **GEOL006 — Geología andina e interpretación avanzada** (id 55, período 10): texto: 'GEOL903 o GEO410. Correquisitos: (GEOL001 o GEOLP014) y GEOL003'; ids: ['GEOL903']; en el texto y no en ids: ['GEOL001', 'GEOL003']

### prereq_expr menciona alternativas ("o"/equivalentes); solo se aplican los ids (42)

- **CFIS328 — Física experimental** (id 6, período 2): texto: '(CFIS310 o FMF023 o FMF010 o FMF024) y (FMMP012 o FMM013 o FMM012 o FMM035)'; ids: ['CFIS310', 'FMMP012']
- **FMMP112 — Cálculo diferencial** (id 7, período 2): texto: 'FMMP012 o FMM013 o FMM010 o FMM035 o FMM012'; ids: ['FMMP012']
- **GEOL201 — Mineralogía y cristalografía** (id 8, período 2): texto: '(GEOL101 o GEO101) y (QUIM090 o QUI104)'; ids: ['GEOL101', 'QUIM090']
- **GEOL202 — Paleontología y evolución** (id 9, período 2): texto: 'GEOL101 o GEO101'; ids: ['GEOL101']
- **GEOL203 — Fundamentos de geología** (id 10, período 2): texto: 'GEOL101 o GEO101'; ids: ['GEOL101']
- **ACAD101 — Taller de innovación y emprendimiento i** (id 11, período 3): texto: 'TDFI101 o AUT1301 o INN1201 o ICF121 o INS122 o ICI1201 o IMIN101 o GEOL101 o GEO101 o BIOQ388 o BIOQ398 o LCEBB110 o LCEBB100'; ids: ['GEOL101']
- **CFIS332 — Mecánica** (id 12, período 3): texto: '(CFIS328 o FMF023 o FMF066) y (FMMP112 o FMM033 o FMM112)'; ids: ['CFIS328', 'FMMP112']
- **FMMP212 — Cálculo integral** (id 13, período 3): texto: 'FMMP112 o FMM040 o FMM010 o FMM033 o FMM112'; ids: ['FMMP112']
- **GEOL301 — Geoquímica endógena** (id 14, período 3): texto: '(QUIM090 o QUI104) y (GEOL203 o GEO102)'; ids: ['GEOL203', 'QUIM090']
- **GEOL302 — Métodos analíticos i: microscopía óptica** (id 15, período 3): texto: '(GEOL301 o GEO201) y (GEOL203 o GEO102)'; ids: ['GEOL203', 'GEOL301']
- **ACAD102 — Taller de innovación y emprendimiento ii** (id 16, período 4): texto: 'ACAD101 o INN1201 o ICI1201 o CEGP01'; ids: ['ACAD101']
- **CFIS344 — Electricidad y magnetismo** (id 17, período 4): texto: '(CFIS332 o FMF122 o FMF025) y (FMMP212 o FMM133 o FMM212)'; ids: ['CFIS332', 'FMMP212']
- **FMMP312 — Sistemas y ecuaciones diferenciales lineales** (id 18, período 4): texto: 'FMMP212 o FMM133 o FMM130 o FMM212'; ids: ['FMMP212']
- **GEOL401 — Integrador i: práctica i** (id 19, período 4): texto: '(GEOL301 o GEO302) y (GEOL304 o GEO304) y (GEOL302 o GEO305)'; ids: ['GEOL301', 'GEOL302']
- **GEOL501 — Petrología endógena** (id 21, período 5): texto: 'GEOL401 o GEO499'; ids: ['GEOL401']
- **GEOL502 — Sedimentología y estratigrafía** (id 22, período 5): texto: 'GEOL401 o GEO499'; ids: ['GEOL401']
- **GEOL503 — Métodos analíticos ii: sig y teledetección** (id 23, período 5): texto: 'GEOL302 o GEO305'; ids: ['GEOL302']
- **GEOL504 — Geoquímica exógena y ambiental** (id 24, período 5): texto: 'GEOL301 o GEO302 y GEO304'; ids: ['GEOL301']
- **GEOL505 — Bases de geología de campo** (id 25, período 5): texto: 'GEOL401 o GEO499'; ids: ['GEOL401']
- **ING129 — Inglés ii** (id 26, período 5): texto: 'ING119 o ING111 o ING110 o ING116 o ING117 o CNT021 o ING050 o ING051 o FLG301'; ids: ['ING119']
- **ACAD103 — Taller de innovación y emprendimiento iii** (id 27, período 6): texto: 'ACAD102 o INB1202 o FIC168'; ids: ['ACAD102']
- **GEOL601 — Fundamentos de programación y análisis numérico** (id 28, período 6): texto: '(FMMP312 o FMM254) y (GEOL503 o GEO406)'; ids: ['FMMP312', 'GEOL503']
- **GEOL602 — Deformación de la corteza** (id 29, período 6): texto: '(GEOL501 o GEO403) y (GEOL502 o GEO301)'; ids: ['GEOL501', 'GEOL502']
- **GEOL603 — Geología de campo i** (id 30, período 6): texto: '(GEOL505 o GEO307) y (GEOL503 o GEO406)'; ids: ['GEOL503', 'GEOL505']
- **ING239 — Inglés iii** (id 31, período 6): texto: 'ING129 o ING121 o ING120 o ING216 o ING126 o ING134 o ING127 o CNT026 o ETU181 y ETU182'; ids: ['ING129']
- **GEOL701 — Depósitos minerales y metalogénesis andina** (id 33, período 7): texto: '(GEOL603 o GEO403) y (GEOL602 o GEO307)'; ids: ['GEOL602', 'GEOL603']
- **GEOL702 — Geomorfología** (id 34, período 7): texto: '(GEOL602 o GEO307) y (GEOL504 o GEO506)'; ids: ['GEOL504', 'GEOL602']
- **GEOL703 — Paleoclima y ambiente** (id 35, período 7): texto: 'GEOL504 o GEO506'; ids: ['GEOL504']
- **ING249 — Inglés iv** (id 37, período 7): texto: 'ING239 o ING210 o ING216 o ING224 o ING126 o ING134 o otros equivalentes'; ids: ['ING239']
- **GEOL801 — Recursos energéticos** (id 38, período 8): texto: 'GEOL701 o GEO407 y GEO402'; ids: ['GEOL701']
- **GEOL802 — Geología de chile** (id 39, período 8): texto: '(GEOL704 o GEO407) y (GEOL701 o GEO407 y GEO402)'; ids: ['GEOL701', 'GEOL704']
- **GEOL804 — Métodos de exploración geofísica** (id 41, período 8): texto: 'GEOL701 o GEO407 y GEO402 y GEOL601'; ids: ['GEOL601', 'GEOL701']
- **GEOL806 — Práctica ii** (id 43, período 8): texto: 'GEOL704 o GEO407'; ids: ['GEOL704']
- **GEOL901 — Geología de minas** (id 44, período 9): texto: '(GEOL804 o GEO308) y (GEOL801 o GEO408)'; ids: ['GEOL801', 'GEOL804']
- **GEOL902 — Geoestadística y modelamiento geológico** (id 45, período 9): texto: 'GEOL804 o GEO308'; ids: ['GEOL804']
- **GEOL904 — Peligros geológicos y planificación territorial** (id 47, período 9): texto: 'GEOL803 o GEO502'; ids: ['GEOL803']
- **GEOL905 — Tópicos de especialidad i** (id 48, período 9): texto: 'GEOL802 o GEO411'; ids: ['GEOL802']
- **GEOL001 — Tópicos de especialidad ii** (id 50, período 10): texto: 'GEOL905 o GEOLP001 o GEOLP002 o GEOLP003 o GEOLP004 o GEOLP005 o GEOLP006 o GEOLP007 o GEOLP008'; ids: ['GEOL905']
- **GEOL002 — Economía y evaluación de proyectos geológicos** (id 51, período 10): texto: '(GEOL901 o GEO412 y GEO501) y (GEOL903 o GEO410)'; ids: ['GEOL901', 'GEOL903']
- **GEOL003 — Tópicos de especialidad iii** (id 52, período 10): texto: 'GEOL905 o GEOLP001 o GEOLP002 o GEOLP003 o GEOLP004 o GEOLP005 o GEOLP006 o GEOLP007 o GEOLP008'; ids: ['GEOL905']
- **GEOL004 — Geoética y geopatrimonio** (id 53, período 10): texto: 'GEOL905 o GEOLP001 o GEOLP002 o GEOLP003 o GEOLP004 o GEOLP005 o GEOLP006 o GEOLP007 o GEOLP008'; ids: ['GEOL905']
- **GEOL005 — Integrador iii: proyecto de título** (id 54, período 10): texto: '(GEOL906 o GEO505) y (GEOL906 o GEO599)'; ids: ['GEOL906']

### total_creditos = 0 (se interpreta como desconocido) (1)

-: total_creditos = 0

## Ingeniería en Marina Mercante

### Prerrequisito en el mismo período o uno posterior (1)

- **IMMQ408 — Proyecto de Título** (id 45, período 8, mención MAQ): IMMC404 Seminario de Licenciatura en Ingeniería (id 41) está en el período 8

### prereq_expr menciona alternativas ("o"/equivalentes); solo se aplican los ids (29)

- **CFIS328 — Física Experimental** (id 6, período 2): texto: 'CFIS310 y FMMP012 (o equivalentes)'; ids: ['CFIS310', 'FMMP012']
- **FMMP112 — Cálculo Diferencial** (id 7, período 2): texto: 'FMMP012 (o equivalentes)'; ids: ['FMMP012']
- **IMMC102 — Procesos de Ingeniería en Marina Mercante** (id 8, período 2): texto: 'CFIS310 (o equivalentes)'; ids: ['CFIS310']
- **ING129 — Inglés II** (id 10, período 2): texto: 'ING119 (o equivalentes)'; ids: ['ING119']
- **ING239 — Inglés III** (id 15, período 3): texto: 'ING129 (o equivalentes)'; ids: ['ING129']
- **IMMC205 — Construcción Naval y Flotabilidad** (id 47, período 4, mención CUBI): texto: 'IMMC201 e IMMC202 (o equivalentes)'; ids: ['IMMC201', 'IMMC202']
- **IMMP201 — Meteorología y Oceanografía** (id 48, período 4, mención CUBI): texto: 'FMMP112 (o equivalentes)'; ids: ['FMMP112']
- **IMMP202 — Fundamentos de Navegación** (id 49, período 4, mención CUBI): texto: 'IMMC204 y FMMP112 (o equivalentes)'; ids: ['FMMP112', 'IMMC204']
- **IMMP203 — Planificación y Estiba de la Carga** (id 50, período 4, mención CUBI): texto: 'IMMC202 (o equivalentes)'; ids: ['IMMC202']
- **ING249 — Inglés IV** (id 52, período 4, mención CUBI): texto: 'ING239 (o equivalentes)'; ids: ['ING239']
- **IMMC301 — Cuidado del Medio Ambiente (OMI I.01)** (id 54, período 5, mención CUBI): texto: 'IMMC203 y/o IMMC205 (según equivalencias indicadas en la malla)'; ids: ['IMMC203', 'IMMC205']
- **IMMC303 — Costos y Finanzas** (id 60, período 6, mención CUBI): texto: 'FMMP112 (o equivalentes)'; ids: ['FMMP112']
- **IMMC404 — Seminario de Licenciatura en Ingeniería** (id 72, período 8, mención CUBI): texto: 'IMMC402 (o equivalentes)'; ids: ['IMMC402']
- **IMMP407 — Gestión del Transporte Marítimo** (id 75, período 8, mención CUBI): texto: 'IMMP404 (o equivalentes)'; ids: ['IMMP404']
- **IMMP408 — Proyecto de Título** (id 76, período 8, mención CUBI): texto: 'IMMP403 e IMMC402 (o equivalentes)'; ids: ['IMMC402', 'IMMP403']
- **IMMP409 — Práctica II** (id 77, período 8, mención CUBI): texto: 'IMMP204 e IMMP301 (o equivalentes)'; ids: ['IMMP204', 'IMMP301']
- **IMMC205 — Construcción Naval y Flotabilidad** (id 16, período 4, mención MAQ): texto: 'IMMC201 e IMMC202 (o equivalentes)'; ids: ['IMMC201', 'IMMC202']
- **IMMQ201 — Termodinámica Aplicada** (id 17, período 4, mención MAQ): texto: 'FMMP112 e IMMC202 (o equivalentes)'; ids: ['FMMP112', 'IMMC202']
- **IMMQ202 — Elasticidad y Resistencia de Materiales** (id 18, período 4, mención MAQ): texto: 'FMMP112 e IMMC202 (o equivalentes)'; ids: ['FMMP112', 'IMMC202']
- **IMMQ203 — Electrotecnia** (id 19, período 4, mención MAQ): texto: 'IMMC204 (o equivalentes)'; ids: ['IMMC204']
- **ING249 — Inglés IV** (id 21, período 4, mención MAQ): texto: 'ING239 (o equivalentes)'; ids: ['ING239']
- **IMMC301 — Cuidado del Medio Ambiente (OMI I.01)** (id 23, período 5, mención MAQ): texto: 'IMMC203 y/o IMMC205 (según equivalencias indicadas en la malla)'; ids: ['IMMC203', 'IMMC205']
- **IMMQ303 — Engine Room Management** (id 26, período 5, mención MAQ): texto: 'IMMQ203 e IMMQ201 (o equivalentes)'; ids: ['IMMQ201', 'IMMQ203']
- **IMMQ304 — Combustión Interna I** (id 27, período 5, mención MAQ): texto: 'IMMQ201 (o equivalentes)'; ids: ['IMMQ201']
- **IMMC303 — Costos y Finanzas** (id 29, período 6, mención MAQ): texto: 'FMMP112 (o equivalentes)'; ids: ['FMMP112']
- **IMMQ306 — Electrónica** (id 31, período 6, mención MAQ): texto: 'IMMQ302 (o equivalentes)'; ids: ['IMMQ302']
- **IMMQ307 — Plantas a Vapor** (id 32, período 6, mención MAQ): texto: 'IMMQ304 (o equivalentes)'; ids: ['IMMQ304']
- **IMMQ308 — Combustión Interna II** (id 33, período 6, mención MAQ): texto: 'IMMQ304 (o equivalentes)'; ids: ['IMMQ304']
- **IMMC404 — Seminario de Licenciatura en Ingeniería** (id 41, período 8, mención MAQ): texto: 'IMMC402 (o equivalentes)'; ids: ['IMMC402']

### Mismo código con ids distintos (una copia por mención) (10)

- **CEGPC13 — Pensamiento Crítico**: ids: 22 (MAQ), 53 (CUBI)
- **IMMC205 — Construcción Naval y Flotabilidad**: ids: 16 (MAQ), 47 (CUBI)
- **IMMC301 — Cuidado del Medio Ambiente (OMI I.01)**: ids: 23 (MAQ), 54 (CUBI)
- **IMMC302 — Primeros Auxilios y Cuidados Médicos a Bordo (OMI 1.13-1.14)**: ids: 28 (MAQ), 59 (CUBI)
- **IMMC303 — Costos y Finanzas**: ids: 29 (MAQ), 60 (CUBI)
- **IMMC401 — Seguridad de las Personas y Medio Ambiente (OMI 1.21, 3.26, 1.39, 1.38)**: ids: 34 (MAQ), 65 (CUBI)
- **IMMC402 — Evaluación de Inversiones Marítimo Portuario**: ids: 35 (MAQ), 66 (CUBI)
- **IMMC403 — Sistemas de Gestión Integrado**: ids: 40 (MAQ), 71 (CUBI)
- **IMMC404 — Seminario de Licenciatura en Ingeniería**: ids: 41 (MAQ), 72 (CUBI)
- **ING249 — Inglés IV**: ids: 21 (MAQ), 52 (CUBI)

## Ingenería Civil Informática

### El texto prereq_expr no coincide con los ids de prerrequisitos (5)

- **CFIS332 — Mecánica** (id 13, período 3): texto: 'CFIS310'; ids: ['CFIS328', 'FMMP112']; en el texto y no en ids: ['CFIS310']; en ids y no en el texto: ['CFIS328', 'FMMP112']
- **INSW421 — Seminario de Licenciatura en Ingeniería** (id 39, período 8): texto: 'PTEC106 & INSW410'; ids: ['CFIS344', 'ICF203', 'PTEC105', 'TDFI105']; en el texto y no en ids: ['INSW410', 'PTEC106']; en ids y no en el texto: ['CFIS344', 'ICF203', 'PTEC105', 'TDFI105']
- **INSW410 — Portafolio de Proyectos** (id 41, período 9): texto: 'PTEC103 & PTEC105'; ids: ['INSW421', 'PTEC106', 'TDFI106']; en el texto y no en ids: ['PTEC103', 'PTEC105']; en ids y no en el texto: ['INSW421', 'PTEC106', 'TDFI106']
- **INSW413 — Tópicos de Especialidad III** (id 45, período 9): texto: 'INSW411 & INSW412'; ids: ['ICF203']; en el texto y no en ids: ['INSW411', 'INSW412']; en ids y no en el texto: ['ICF203']
- **INSW420 — Práctica II** (id 48, período 10): texto: 'INSW220'; ids: ['ICF206', 'ICF207', 'INSW220', 'INSW410', 'INSW412', 'INSW413']; en ids y no en el texto: ['ICF206', 'ICF207', 'INSW410', 'INSW412', 'INSW413']

### Tiene ids de prerrequisitos pero prereq_expr vacío o ausente (15)

- **CFIS328 — Física Experimental** (id 7, período 2): ids: CFIS310, FMMP012
- **ACAD101 — Taller de Innovación y Emprendimiento I** (id 14, período 3): ids: TDFI101
- **INSW220 — Práctica I** (id 17, período 4): ids: ACAD101, CFIS332, FMMP212, PTEC101, TDFI103, TDFI104
- **FMSP316 — Métodos Cuantitativos** (id 20, período 5): ids: FMMP212
- **ICF201 — Fundamentos de Computación de Alto Desempeño** (id 22, período 5): ids: PTEC101
- **ICF202 — Análisis y Diseño de Algoritmos** (id 23, período 5): ids: PTEC101
- **ICF203 — Fundamentos de Inteligencia Artificial** (id 28, período 6): ids: ICF202
- **PTEC105 — Ingeniería de Software I** (id 30, período 7): ids: PTEC102
- **ICF204 — Aprendizaje de Máquina** (id 31, período 7): ids: ICF203
- **ICF205 — Optimización** (id 32, período 7): ids: ICF202
- **INSW411 — Tópicos de Especialidad I** (id 38, período 8): ids: ICF203
- **ICF206 — Administración Financiera de Proyectos I+D+i** (id 42, período 9): ids: PTEC106
- **ICF207 — Ciencia de Datos** (id 43, período 9): ids: ICF203, TDFI105
- **INSW412 — Tópicos de Especialidad II** (id 44, período 9): ids: ICF203
- **ICF208 — Taller de Transferencia Tecnológica** (id 47, período 10): ids: ICF206

## Ingeniería Civil en Minas

### prereq_expr menciona alternativas ("o"/equivalentes); solo se aplican los ids (12)

- **CFIS328 — Física Experimental** (id 6, período 2): texto: '(CFIS310 o equivalentes) y (FMMP012 o equivalentes)'; ids: ['CFIS310', 'FMMP012']
- **FMMP112 — Cálculo Diferencial** (id 7, período 2): texto: 'FMMP012 o equivalentes'; ids: ['FMMP012']
- **TDFI103 — Base de Datos** (id 9, período 2): texto: 'TDFI102 o equivalentes'; ids: ['TDFI102']
- **CFIS332 — Mecánica** (id 10, período 3): texto: '(CFIS328 o equivalentes) y (FMMP112 o equivalentes)'; ids: ['CFIS328', 'FMMP112']
- **FMMP212 — Cálculo Integral** (id 11, período 3): texto: 'FMMP112 o equivalentes'; ids: ['FMMP112']
- **TDFI104 — Compliance & Accountability** (id 14, período 3): texto: 'TDFI101 o equivalentes'; ids: ['TDFI101']
- **FMSP316 — Métodos Cuantitativos** (id 15, período 4): texto: 'FMMP212 o equivalentes'; ids: ['FMMP212']
- **FMMP312 — Sistemas y Ecuaciones Diferenciales Lineales** (id 20, período 5): texto: 'FMMP212 o equivalentes'; ids: ['FMMP212']
- **ING129 — Inglés II** (id 24, período 5): texto: 'ING119 o equivalentes'; ids: ['ING119']
- **ACAD101 — Taller de Innovación y Emprendimiento I** (id 25, período 6): texto: 'TDFI101 o asignaturas base equivalentes'; ids: ['TDFI101']
- **ING239 — Inglés III** (id 28, período 6): texto: 'ING129 o equivalentes'; ids: ['ING129']
- **ING249 — Inglés IV** (id 33, período 7): texto: 'ING239 o equivalentes'; ids: ['ING239']

## Medicina

### prereq_expr menciona alternativas ("o"/equivalentes); solo se aplican los ids (41)

- **BIOL148 — Genética y Biología Molecular Humana** (id 7, período 2): texto: 'BIOL132 o (BIO130 y BIO131)'; ids: ['BIOL132']
- **CFIS350 — Física Aplicada a la Medicina** (id 8, período 2): texto: 'MAT007 o FMM007'; ids: ['MAT007']
- **MEDI002 — Fundamentos de la Medicina II** (id 9, período 2): texto: 'MEDI001 o MED016'; ids: ['MEDI001']
- **MORF336 — Bases Morfológicas y Estructurales II** (id 10, período 2): texto: 'MORF335 o (MOR330 y MOR331 y BIO320 y BIO321)'; ids: ['MORF335']
- **SPAB305 — Bioestadística** (id 11, período 2): texto: 'MAT007 o FMM007'; ids: ['MAT007']
- **BIOL259 — Microbiología y Parasitología** (id 12, período 3): texto: 'BIOL132 o (BIO130 y BIO131)'; ids: ['BIOL132']
- **BIOL276 — Bases Funcionales I** (id 13, período 3): texto: '(BIOL148 o (BIO148 y BIO242)) y (QUIM500 o (QUI109 y QUI024)) y (CFIS350 o FMF019)'; ids: ['BIOL148', 'CFIS350', 'QUIM500']
- **MEDI003 — Psicología Médica** (id 15, período 3): texto: 'MEDI002 o (MED017 o MED121 o MED122)'; ids: ['MEDI002']
- **SPAB306 — Epidemiología** (id 16, período 3): texto: 'SPAB305 o MED293'; ids: ['SPAB305']
- **BIOL376 — Bases Funcionales II** (id 17, período 4): texto: 'BIOL276 o (BIO376 y BIO266)'; ids: ['BIOL276']
- **ING129 — Inglés II** (id 18, período 4): texto: 'ING119 o ING111 o ING110 o ING116 o ING117 o CNT021 o (ING050 y ING051) o (FLG301 y FLG302) o (BMA281 y BMA282) o (ETU081 y ETU082)'; ids: ['ING119']
- **MEDI004 — Medicina Familiar y Comunitaria** (id 19, período 4): texto: '(MEDI002 o (MED017 o MED121 o MED122)) y (MEDI003 o MED131)'; ids: ['MEDI002', 'MEDI003']
- **MEDI005 — Medicina y Sociedad** (id 20, período 4): texto: 'MEDI002 o (MED017 o MED121 o MED122)'; ids: ['MEDI002']
- **SPAB307 — Salud Pública** (id 21, período 4): texto: 'SPAB306 o MED293'; ids: ['SPAB306']
- **FARM131 — Farmacología** (id 22, período 5): texto: 'BIOL376 o (MED294 y BIO377)'; ids: ['BIOL376']
- **ING239 — Inglés III** (id 23, período 5): texto: 'ING129 o ING121 o ING120 o ING216 o ING126 o ING134 o ING127 o CNT026 o (ETU181 y ETU182) o ING229'; ids: ['ING129']
- **MEDI006 — Semiología** (id 24, período 5): texto: 'MEDI002 o (MED017 o MED121 o MED122) y BIOL376'; ids: ['BIOL376', 'MEDI002']
- **MEDI007 — Bases Funcionales III** (id 25, período 5): texto: 'BIOL376 o (MED294 y BIO377)'; ids: ['BIOL376']
- **MEDI0100 — Integrador I** (id 26, período 5): texto: '(MEDI002 o (MED017 o MED121 o MED122)) y (MEDI003 o MED131) y (MEDI004 o MED292) y (BIOL259 o (BIO250 y BIO251)) y (MEDI005 o (MED131 o HUF124)) y (BIOL376 o (MED294 y BIO377)) y (MORF336 o (MOR332 y MOR333)) y (SPAB307 o MED292)'; ids: ['BIOL259', 'BIOL376', 'MEDI002', 'MEDI003', 'MEDI004', 'MEDI005', 'MORF336', 'SPAB307']
- **ING249 — Inglés IV** (id 27, período 6): texto: 'ING239 o ING210 o ING216 o ING224 o ING126 o CNT126 o (ETU281 y ETU282) o ING217'; ids: ['ING239']
- **MEDI008 — Ética Médica** (id 28, período 6): texto: 'MEDI002 o (MED017 o MED121 o MED122)'; ids: ['MEDI002']
- **MEDI009 — Clínica Médico Quirúrgica I** (id 29, período 6): texto: 'MEDI007 o (MED260 y MED295 y MED257)'; ids: ['MEDI007']
- **MEDI010 — Neurología** (id 30, período 6): texto: 'MEDI007 o (MED260 y MED295 y MED257)'; ids: ['MEDI007']
- **MEDI011 — Métodos de Investigación** (id 31, período 6): texto: 'SPAB305 o MED293'; ids: ['SPAB305']
- **SPAB308 — Gestión en Salud** (id 32, período 6): texto: '(SPAB307 o MED292) y (FARM131 o BIO288)'; ids: ['FARM131', 'SPAB307']
- **MEDI012 — Clínica Médico Quirúrgica II** (id 33, período 7): texto: 'MEDI009 o (MED257 y MED249)'; ids: ['MEDI009']
- **MEDI013 — Dermatología** (id 34, período 7): texto: 'MEDI009 o (MED257 y MED249)'; ids: ['MEDI009']
- **MEDI014 — Otorrinolaringología** (id 35, período 7): texto: 'MEDI009 o (MED257 y MED249)'; ids: ['MEDI009']
- **MEDI015 — Psiquiatría** (id 36, período 7): texto: 'MEDI003 o MED131'; ids: ['MEDI003']
- **MEDI016 — Medicina Basada en la Evidencia** (id 37, período 7): texto: 'MEDI011 o (MED278 y MED279)'; ids: ['MEDI011']
- **MEDI017 — Clínica Médico Quirúrgica III** (id 39, período 8): texto: 'MEDI012 o (MED296 y MED287 y MED257)'; ids: ['MEDI012']
- **MEDI018 — Traumatología y Ortopedia** (id 40, período 8): texto: 'MEDI012 o (MED296 y MED287 y MED257)'; ids: ['MEDI012']
- **MEDI019 — Oftalmología** (id 41, período 8): texto: 'MEDI012 o (MED296 y MED287 y MED257)'; ids: ['MEDI012']
- **MEDI020 — Urología** (id 42, período 8): texto: 'MEDI012 o (MED296 y MED287 y MED257)'; ids: ['MEDI012']
- **MEDI021 — Medicina Legal y Forense** (id 43, período 8): texto: 'MEDI012 o (MED296 y MED287 y MED257)'; ids: ['MEDI012']
- **MEDI0200 — Integrador II** (id 44, período 9): texto: '(MEDI008 o (MED258 y MED259)) y (MEDI009 o (MED257 y MED249)) y (MEDI010 o MED244) y (MEDI012 o (MED296 y MED287 y MED257)) y (MEDI015 o MED245) y (MEDI017 o (MED296 o MED287 o MED257)) y (MEDI018 o MED296) y SPAB308 y MEDI016'; ids: ['MEDI008', 'MEDI009', 'MEDI010', 'MEDI012', 'MEDI015', 'MEDI016', 'MEDI017', 'MEDI018', 'SPAB308']
- **MEDI022 — Pediatría y Cirugía Infantil** (id 45, período 9): texto: 'MEDI017 o (MED296 o MED287 o MED257)'; ids: ['MEDI017']
- **MEDI023 — Obstetricia y Ginecología** (id 46, período 9): texto: 'MEDI017 o (MED296 o MED287 o MED257)'; ids: ['MEDI017']
- **MEDI024 — Internado de Pediatría** (id 47, período 10): texto: 'MEDI022 o MED297'; ids: ['MEDI022']
- **MEDI025 — Internado de Obstetricia y Ginecología** (id 48, período 10): texto: 'MEDI023 o MED298'; ids: ['MEDI023']
- **MEDI0300 — Integrador III** (id 54, período 12): texto: '(MEDI004 o MED292) y (MEDI007 o (MED260 y MED295 y MED257)) y (SPAB306 o MED293) y (SPAB307 o MED292) y (MEDI024 o MED374) y (MEDI025 o MED376) y (MEDI026 o MED375) y (MEDI027 o MED377)'; ids: ['MEDI004', 'MEDI007', 'MEDI024', 'MEDI025', 'MEDI026', 'MEDI027', 'SPAB306', 'SPAB307']

### total_creditos = 0 (se interpreta como desconocido) (1)

-: total_creditos = 0

## Tecnología Médica

### Prerrequisito en el mismo período o uno posterior (2)

- **BIOL272 — Fisiología humana** (id 13, período 3): BIOL166 Bioquímica (id 12) está en el período 3
- **TMED004 — Infectología** (id 17, período 3): BIOL166 Bioquímica (id 12) está en el período 3

### El texto prereq_expr no coincide con los ids de prerrequisitos (10)

- **SPAB103 — Gestión y aseguramiento de la calidad** (id 39, período 8, mención BACIMET): texto: 'SPAB112 y (TMED714 o TMED721 o TMED731 o TMED744 o TMED752)'; ids: ['SPAB112', 'TMED714']; en el texto y no en ids: ['TMED721', 'TMED731', 'TMED744', 'TMED752']
- **SPAB303 — Metodología de la investigación** (id 40, período 8, mención BACIMET): texto: 'SPAB112 y (TMED714 o TMED721 o TMED731 o TMED744 o TMED752)'; ids: ['SPAB112', 'TMED714']; en el texto y no en ids: ['TMED721', 'TMED731', 'TMED744', 'TMED752']
- **SPAB103 — Gestión y aseguramiento de la calidad** (id 70, período 8, mención IFIME): texto: 'SPAB112 y (TMED714 o TMED721 o TMED731 o TMED744 o TMED752)'; ids: ['SPAB112', 'TMED731']; en el texto y no en ids: ['TMED714', 'TMED721', 'TMED744', 'TMED752']
- **SPAB303 — Metodología de la investigación** (id 71, período 8, mención IFIME): texto: 'SPAB112 y (TMED714 o TMED721 o TMED731 o TMED744 o TMED752)'; ids: ['SPAB112', 'TMED731']; en el texto y no en ids: ['TMED714', 'TMED721', 'TMED744', 'TMED752']
- **SPAB103 — Gestión y aseguramiento de la calidad** (id 98, período 8, mención MORFO): texto: 'SPAB112 y (TMED714 o TMED721 o TMED731 o TMED744 o TMED752)'; ids: ['SPAB112', 'TMED744']; en el texto y no en ids: ['TMED714', 'TMED721', 'TMED731', 'TMED752']
- **SPAB303 — Metodología de la investigación** (id 99, período 8, mención MORFO): texto: 'SPAB112 y (TMED714 o TMED721 o TMED731 o TMED744 o TMED752)'; ids: ['SPAB112', 'TMED744']; en el texto y no en ids: ['TMED714', 'TMED721', 'TMED731', 'TMED752']
- **SPAB103 — Gestión y aseguramiento de la calidad** (id 129, período 8, mención OFTA): texto: 'SPAB112 y (TMED714 o TMED721 o TMED731 o TMED744 o TMED752)'; ids: ['SPAB112', 'TMED721']; en el texto y no en ids: ['TMED714', 'TMED731', 'TMED744', 'TMED752']
- **SPAB303 — Metodología de la investigación** (id 130, período 8, mención OFTA): texto: 'SPAB112 y (TMED714 o TMED721 o TMED731 o TMED744 o TMED752)'; ids: ['SPAB112', 'TMED721']; en el texto y no en ids: ['TMED714', 'TMED731', 'TMED744', 'TMED752']
- **SPAB103 — Gestión y aseguramiento de la calidad** (id 158, período 8, mención OTORRINO): texto: 'SPAB112 y (TMED714 o TMED721 o TMED731 o TMED744 o TMED752)'; ids: ['SPAB112', 'TMED752']; en el texto y no en ids: ['TMED714', 'TMED721', 'TMED731', 'TMED744']
- **SPAB303 — Metodología de la investigación** (id 159, período 8, mención OTORRINO): texto: 'SPAB112 y (TMED714 o TMED721 o TMED731 o TMED744 o TMED752)'; ids: ['SPAB112', 'TMED752']; en el texto y no en ids: ['TMED714', 'TMED721', 'TMED731', 'TMED744']

### prereq_expr menciona alternativas ("o"/equivalentes); solo se aplican los ids (125)

- **CFIS020 — Física general** (id 8, período 2): texto: 'FMMP101 o (FMM032 y FMM134)'; ids: ['FMMP101']
- **MORF122 — Histoembriología** (id 10, período 2): texto: '(MORF010 o (BIO010 y BIO013)) y (BIOL130 o BIO034)'; ids: ['BIOL130', 'MORF010']
- **QUIM022 — Química orgánica** (id 11, período 2): texto: 'QUIM102 o QUI102'; ids: ['QUIM102']
- **BIOL166 — Bioquímica** (id 12, período 3): texto: '(TMED001 o TMD001) y (BIOL130 o BIO034) y (BIOL035 o BIO131) y QUIM022 y (MORF122 o (BIO122 y BIO125))'; ids: ['BIOL035', 'BIOL130', 'MORF122', 'QUIM022', 'TMED001']
- **BIOL272 — Fisiología humana** (id 13, período 3): texto: '(CFIS020 o FMF020) y (BIOL166 o BIO268)'; ids: ['BIOL166', 'CFIS020']
- **ING129 — Inglés II** (id 15, período 3): texto: 'ING119 o equivalentes'; ids: ['ING119']
- **TMED003 — Bioética** (id 16, período 3): texto: 'TMED001 o TMD001'; ids: ['TMED001']
- **TMED004 — Infectología** (id 17, período 3): texto: 'BIOL166 o BIO268'; ids: ['BIOL166']
- **FARM171 — Farmacología general** (id 18, período 4, mención BACIMET): texto: 'BIOL166 o BIO268'; ids: ['BIOL166']
- **ING239 — Inglés III** (id 19, período 4, mención BACIMET): texto: 'ING129 o equivalentes'; ids: ['ING129']
- **TMED005 — Fisiopatología** (id 20, período 4, mención BACIMET): texto: 'BIOL272 o (BIO372 y BIO171)'; ids: ['BIOL272']
- **TMED411 — Parasitología** (id 21, período 4, mención BACIMET): texto: '(CFIS020 o FMF020) y BIOL272 y BIOL166 y TMED003 y TMED004 y ING129'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **TMED412 — Inmunología diagnóstica** (id 22, período 4, mención BACIMET): texto: '(CFIS020 o FMF020) y BIOL272 y BIOL166 y TMED003 y TMED004 y ING129'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **ING249 — Inglés IV** (id 23, período 5, mención BACIMET): texto: 'ING239 o equivalentes'; ids: ['ING239']
- **SPAB110 — Salud pública I** (id 24, período 5, mención BACIMET): texto: 'ING239 o equivalentes y (TMED005 o TMD110)'; ids: ['ING239', 'TMED005']
- **TMED006 — Procedimientos de tecnología médica y bioseguridad** (id 25, período 5, mención BACIMET): texto: 'FARM171 o BIO184'; ids: ['FARM171']
- **TMED511 — Microbiología I** (id 26, período 5, mención BACIMET): texto: '(TMED411 o TMD225) y (FARM171 o BIO184)'; ids: ['FARM171', 'TMED411']
- **TMED512 — Hematología I** (id 27, período 5, mención BACIMET): texto: '(TMED412 o (BIO286 y TMD255)) y (TMED005 o TMD110)'; ids: ['TMED005', 'TMED412']
- **SPAB111 — Salud pública II** (id 28, período 6, mención BACIMET): texto: 'SPAB110 o equivalentes'; ids: ['SPAB110']
- **TMED611 — Bioquímica clínica I** (id 29, período 6, mención BACIMET): texto: 'TMED412 o (BIO286 y TMD255)'; ids: ['TMED412']
- **TMED612 — Microbiología II** (id 30, período 6, mención BACIMET): texto: 'TMED511 o TMD329'; ids: ['TMED511']
- **TMED613 — Hematología II** (id 31, período 6, mención BACIMET): texto: 'TMED512 o TMD233'; ids: ['TMED512']
- **SPAB112 — Administración y gestión en salud** (id 32, período 7, mención BACIMET): texto: 'SPAB111 o equivalentes'; ids: ['SPAB111']
- **TMED711 — Biología molecular** (id 34, período 7, mención BACIMET): texto: 'TMED611 o TMD204'; ids: ['TMED611']
- **TMED712 — Inmunohematología** (id 35, período 7, mención BACIMET): texto: '(TMED512 o TMD233) y (TMED611 o TMD204)'; ids: ['TMED512', 'TMED611']
- **TMED713 — Bioquímica clínica II** (id 36, período 7, mención BACIMET): texto: '(TMED613 o TMD301) y (TMED612 o TMD329) y (TMED611 o TMD204)'; ids: ['TMED611', 'TMED612', 'TMED613']
- **TMED714 — Integrador I: caso clínico BACIMET** (id 37, período 7, mención BACIMET): texto: '(TMED613 o TMD301) y (TMED612 o TMD329) y (TMED611 o TMD204)'; ids: ['TMED611', 'TMED612', 'TMED613']
- **TMED811 — Medicina transfusional** (id 41, período 8, mención BACIMET): texto: '(TMED712 o TMD325) y TMED714'; ids: ['TMED712', 'TMED714']
- **TMED812 — Diagnóstico molecular clínico** (id 42, período 8, mención BACIMET): texto: 'TMED711 y TMED714 y (TMED713 o TMD231)'; ids: ['TMED711', 'TMED713', 'TMED714']
- **TMED911 — Seminario de investigación BACIMET** (id 44, período 9, mención BACIMET): texto: 'SPAB303 y SPAB103 y (TMED811 o TMD325) y TMED812'; ids: ['SPAB103', 'SPAB303', 'TMED811', 'TMED812']
- **FARM171 — Farmacología general** (id 46, período 4, mención IFIME): texto: 'BIOL166 o BIO268'; ids: ['BIOL166']
- **ING239 — Inglés III** (id 47, período 4, mención IFIME): texto: 'ING129 o equivalentes'; ids: ['ING129']
- **TMED005 — Fisiopatología** (id 48, período 4, mención IFIME): texto: 'BIOL272 o (BIO372 y BIO171)'; ids: ['BIOL272']
- **TMED431 — Protección radiológica** (id 49, período 4, mención IFIME): texto: '(CFIS020 o FMF020) y BIOL272 y BIOL166 y TMED003 y TMED004 y ING129'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **TMED432 — Radiodiagnóstico I** (id 50, período 4, mención IFIME): texto: '(CFIS020 o FMF020) y BIOL272 y BIOL166 y TMED003 y TMED004 y ING129'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **TMED433 — Física electromagnética** (id 51, período 4, mención IFIME): texto: 'BIOL166 o BIO268 y BIOL272 o equivalentes'; ids: ['BIOL166', 'BIOL272']
- **ING249 — Inglés IV** (id 52, período 5, mención IFIME): texto: 'ING239 o equivalentes'; ids: ['ING239']
- **SPAB110 — Salud pública I** (id 53, período 5, mención IFIME): texto: 'ING239 o equivalentes y (TMED005 o TMD110)'; ids: ['ING239', 'TMED005']
- **TMED006 — Procedimientos de tecnología médica y bioseguridad** (id 54, período 5, mención IFIME): texto: 'FARM171 o BIO184'; ids: ['FARM171']
- **TMED531 — Física moderna** (id 55, período 5, mención IFIME): texto: '(TMED431 o TMD223) y (TMED433 o TMD200)'; ids: ['TMED431', 'TMED433']
- **TMED532 — Radiodiagnóstico II** (id 56, período 5, mención IFIME): texto: '(TMED432 o TMD222) y (FARM171 o BIO184)'; ids: ['FARM171', 'TMED432']
- **TMED533 — Anatomía imagenológica** (id 57, período 5, mención IFIME): texto: '(TMED432 o TMD222) y (TMED005 o TMD110)'; ids: ['TMED005', 'TMED432']
- **SPAB111 — Salud pública II** (id 58, período 6, mención IFIME): texto: 'SPAB110 o equivalentes'; ids: ['SPAB110']
- **TMED631 — Física nuclear** (id 59, período 6, mención IFIME): texto: 'TMED531 o TMD264'; ids: ['TMED531']
- **TMED632 — Tomografía computada** (id 60, período 6, mención IFIME): texto: '(TMED532 o TMD249) y (TMED533 o (TMD251 y TMD282))'; ids: ['TMED532', 'TMED533']
- **TMED633 — Sistema informático en radiología** (id 61, período 6, mención IFIME): texto: 'TMED532 o TMD249'; ids: ['TMED532']
- **TMED634 — Patología imagenológica** (id 62, período 6, mención IFIME): texto: '(TMED532 o TMD249) y (TMED533 o (TMD251 y TMD282))'; ids: ['TMED532', 'TMED533']
- **SPAB112 — Administración y gestión en salud** (id 63, período 7, mención IFIME): texto: 'SPAB111 o equivalentes'; ids: ['SPAB111']
- **TMED731 — Medicina nuclear** (id 65, período 7, mención IFIME): texto: 'TMED631 o TMD264'; ids: ['TMED631']
- **TMED732 — Intervencionismo endovascular** (id 66, período 7, mención IFIME): texto: 'TMED634 o (TMD251 y TMD282)'; ids: ['TMED634']
- **TMED733 — Integrador I: caso clínico IFIME** (id 67, período 7, mención IFIME): texto: '(TMED632 o TMD297) y TMED633 y (TMED634 o (TMD251 y TMD282))'; ids: ['TMED632', 'TMED633', 'TMED634']
- **TMED734 — Ultrasonido** (id 68, período 7, mención IFIME): texto: 'TMED634 o (TMD251 y TMD282)'; ids: ['TMED634']
- **TMED831 — Radioterapia** (id 72, período 8, mención IFIME): texto: '(TMED732 o TMD298) y TMED733'; ids: ['TMED732', 'TMED733']
- **TMED832 — Resonancia magnética** (id 73, período 8, mención IFIME): texto: 'TMED733 y (TMED734 o TMD297)'; ids: ['TMED733', 'TMED734']
- **TMED931 — Seminario de investigación IFIME** (id 75, período 9, mención IFIME): texto: 'SPAB303 y SPAB103 y (TMED831 o TMD339) y (TMED832 o TMD297)'; ids: ['SPAB103', 'SPAB303', 'TMED831', 'TMED832']
- **FARM171 — Farmacología general** (id 77, período 4, mención MORFO): texto: 'BIOL166 o BIO268'; ids: ['BIOL166']
- **ING239 — Inglés III** (id 78, período 4, mención MORFO): texto: 'ING129 o equivalentes'; ids: ['ING129']
- **TMED005 — Fisiopatología** (id 79, período 4, mención MORFO): texto: 'BIOL272 o (BIO372 y BIO171)'; ids: ['BIOL272']
- **TMED441 — Técnicas histológicas y citológicas I** (id 80, período 4, mención MORFO): texto: '(BIOL272 o (BIO372 y BIO171)) y (BIOL166 o BIO268) y (TMED003 o (TMD020 y TMD250)) y (TMED004 o BIO058) y ING129 y (CFIS020 o FMF020)'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **TMED442 — Histología clínica** (id 81, período 4, mención MORFO): texto: '(BIOL272 o (BIO372 y BIO171)) y (BIOL166 o BIO268) y (TMED003 o (TMD020 y TMD250)) y (TMED004 o BIO058) y ING129 y (CFIS020 o FMF020)'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **ING249 — Inglés IV** (id 82, período 5, mención MORFO): texto: 'ING239 o equivalentes'; ids: ['ING239']
- **SPAB110 — Salud pública I** (id 83, período 5, mención MORFO): texto: 'ING239 o equivalentes y (TMED005 o TMD110)'; ids: ['ING239', 'TMED005']
- **TMED006 — Procedimientos de tecnología médica y bioseguridad** (id 84, período 5, mención MORFO): texto: 'FARM171 o BIO184'; ids: ['FARM171']
- **TMED541 — Técnicas histológicas y citológicas II** (id 85, período 5, mención MORFO): texto: 'TMED441 o TMD197'; ids: ['TMED441']
- **TMED542 — Anatomía patológica I** (id 86, período 5, mención MORFO): texto: '(TMED442 o TMD199) y (TMED005 o TMD110)'; ids: ['TMED005', 'TMED442']
- **SPAB111 — Salud pública II** (id 88, período 6, mención MORFO): texto: 'SPAB110 o equivalentes'; ids: ['SPAB110']
- **TMED641 — Biología molecular y genética** (id 89, período 6, mención MORFO): texto: 'TMED541 o TMD197'; ids: ['TMED541']
- **TMED642 — Diagnóstico histoquímico** (id 90, período 6, mención MORFO): texto: '(TMED541 o TMD197) y (TMED542 o TMD256)'; ids: ['TMED541', 'TMED542']
- **TMED643 — Anatomía patológica II** (id 91, período 6, mención MORFO): texto: 'TMED542 o TMD256'; ids: ['TMED542']
- **SPAB112 — Administración y gestión en salud** (id 92, período 7, mención MORFO): texto: 'SPAB111 o equivalentes'; ids: ['SPAB111']
- **TMED741 — Fundamentos de citogénetica** (id 94, período 7, mención MORFO): texto: 'TMED641 o BIO040'; ids: ['TMED641']
- **TMED742 — Diagnóstico inmunohistoquímico** (id 95, período 7, mención MORFO): texto: '(TMED641 o BIO040) y (TMED642 o TMD248) y (TMED643 o TMD256)'; ids: ['TMED641', 'TMED642', 'TMED643']
- **TMED743 — Citopatología I** (id 96, período 7, mención MORFO): texto: 'TMED643 o TMD256'; ids: ['TMED643']
- **TMED744 — Integrador I: caso clínico MORFO** (id 97, período 7, mención MORFO): texto: '(TMED641 o BIO040) y (TMED642 o TMD248) y (TMED643 o TMD256)'; ids: ['TMED641', 'TMED642', 'TMED643']
- **TMED841 — Diagnóstico citogenético** (id 100, período 8, mención MORFO): texto: '(TMED741 o TMD294) y TMED744'; ids: ['TMED741', 'TMED744']
- **TMED842 — Diagnóstico molecular** (id 101, período 8, mención MORFO): texto: '(TMED741 o TMD294) y (TMED742 o TMD327) y TMED744'; ids: ['TMED741', 'TMED742', 'TMED744']
- **TMED843 — Citopatología II** (id 102, período 8, mención MORFO): texto: '(TMED743 o TMD321) y TMED744'; ids: ['TMED743', 'TMED744']
- **TMED941 — Seminario de investigación MORFO** (id 104, período 9, mención MORFO): texto: 'SPAB303 y SPAB103 y (TMED841 o TMD326) y TMED842 y (TMED843 o TMD322)'; ids: ['SPAB103', 'SPAB303', 'TMED841', 'TMED842', 'TMED843']
- **FARM171 — Farmacología general** (id 106, período 4, mención OFTA): texto: 'BIOL166 o BIO268'; ids: ['BIOL166']
- **ING239 — Inglés III** (id 107, período 4, mención OFTA): texto: 'ING129 o equivalentes'; ids: ['ING129']
- **TMED005 — Fisiopatología** (id 108, período 4, mención OFTA): texto: 'BIOL272 o (BIO372 y BIO171)'; ids: ['BIOL272']
- **TMED421 — Morfofisiología ocular** (id 109, período 4, mención OFTA): texto: '(CFIS020 o FMF020) y (BIOL272 o (BIO372 y BIO171)) y (BIOL166 o BIO268) y (TMED003 o (TMD020 y TMD250)) y (TMED004 o BIO058) y ING129'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **TMED422 — Oftalmología general** (id 110, período 4, mención OFTA): texto: '(CFIS020 o FMF020) y (BIOL272 o (BIO372 y BIO171)) y (BIOL166 o BIO268) y (TMED003 o (TMD020 y TMD250)) y (TMED004 o BIO058) y ING129'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **TMED423 — Biofísica óptica** (id 111, período 4, mención OFTA): texto: '(BIOL166 o BIO268) y ING129'; ids: ['BIOL166', 'ING129']
- **ING249 — Inglés IV** (id 112, período 5, mención OFTA): texto: 'ING239 o equivalentes'; ids: ['ING239']
- **SPAB110 — Salud pública I** (id 113, período 5, mención OFTA): texto: 'ING239 o equivalentes y (TMED005 o TMD110)'; ids: ['ING239', 'TMED005']
- **TMED006 — Procedimientos de tecnología médica y bioseguridad** (id 114, período 5, mención OFTA): texto: 'FARM171 o BIO184'; ids: ['FARM171']
- **TMED521 — Morfofisiopatología ocular** (id 115, período 5, mención OFTA): texto: '(TMED005 o TMD110) y (TMED421 o TMD193)'; ids: ['TMED005', 'TMED421']
- **TMED522 — Exploración del sistema visual** (id 116, período 5, mención OFTA): texto: '(TMED422 o TMD195) y (TMED423 o TMD192)'; ids: ['TMED422', 'TMED423']
- **TMED523 — Oftalmofarmacología** (id 117, período 5, mención OFTA): texto: '(FARM171 o BIO184) y (TMED421 o TMD193)'; ids: ['FARM171', 'TMED421']
- **SPAB111 — Salud pública II** (id 118, período 6, mención OFTA): texto: 'SPAB110 o equivalentes'; ids: ['SPAB110']
- **TMED621 — Estudio del campo visual** (id 119, período 6, mención OFTA): texto: 'TMED521 o TMD258'; ids: ['TMED521']
- **TMED622 — Estrabismo y ortóptica** (id 120, período 6, mención OFTA): texto: '(TMED521 o TMD258) y (TMED523 o TMD263)'; ids: ['TMED521', 'TMED523']
- **TMED623 — Optometría I** (id 121, período 6, mención OFTA): texto: 'TMED522 o TMD194'; ids: ['TMED522']
- **SPAB112 — Administración y gestión en salud** (id 123, período 7, mención OFTA): texto: 'SPAB111 o equivalentes'; ids: ['SPAB111']
- **TMED721 — Neurooftalmología** (id 125, período 7, mención OFTA): texto: '(TMED621 o TMD268) y (TMED622 o TMD265)'; ids: ['TMED621', 'TMED622']
- **TMED722 — Optometría II** (id 126, período 7, mención OFTA): texto: 'TMED623 o TMD295'; ids: ['TMED623']
- **TMED723 — Procedimientos de apoyo en cirugía refractiva** (id 127, período 7, mención OFTA): texto: '(TMED623 o TMD295) y (TMED622 o TMD265) y (TMED621 o TMD268)'; ids: ['TMED621', 'TMED622', 'TMED623']
- **TMED724 — Integrador I: atención primaria en oftalmología** (id 128, período 7, mención OFTA): texto: '(TMED621 o TMD268) y (TMED622 o TMD265) y (TMED623 o TMD295)'; ids: ['TMED621', 'TMED622', 'TMED623']
- **TMED821 — Formulación y evaluación de proyectos en oftalmología** (id 131, período 8, mención OFTA): texto: 'SPAB112 o TMD320'; ids: ['SPAB112']
- **TMED823 — Imagenología ocular** (id 133, período 8, mención OFTA): texto: '(TMED723 o (TMD323 y TMD296)) y TMED724'; ids: ['TMED723', 'TMED724']
- **TMED921 — Seminario de investigación OFTA** (id 135, período 9, mención OFTA): texto: 'SPAB303 y SPAB103 y TMED821 y (TMED822 o TMD356) y (TMED823 o TMD357)'; ids: ['SPAB103', 'SPAB303', 'TMED821', 'TMED822', 'TMED823']
- **FARM171 — Farmacología general** (id 137, período 4, mención OTORRINO): texto: 'BIOL166 o BIO268'; ids: ['BIOL166']
- **ING239 — Inglés III** (id 138, período 4, mención OTORRINO): texto: 'ING129 o equivalentes'; ids: ['ING129']
- **TMED005 — Fisiopatología** (id 139, período 4, mención OTORRINO): texto: 'BIOL272 o (BIO372 y BIO171)'; ids: ['BIOL272']
- **TMED451 — Psicoacústica y fonología** (id 140, período 4, mención OTORRINO): texto: '(CFIS020 o FMF020) y (BIOL272 o (BIO372 y BIO171)) y (BIOL166 o BIO268) y (TMED003 o (TMD020 y TMD250)) y (TMED004 o BIO058) y ING129'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **TMED452 — Neuroanatomía otorrinolaringológica** (id 141, período 4, mención OTORRINO): texto: '(CFIS020 o FMF020) y (BIOL272 o (BIO372 y BIO171)) y (BIOL166 o BIO268) y (TMED003 o (TMD020 y TMD250)) y (TMED004 o BIO058) y ING129'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **TMED453 — Lengua de señas** (id 142, período 4, mención OTORRINO): texto: '(CFIS020 o FMF020) y (BIOL272 o (BIO372 y BIO171)) y (BIOL166 o BIO268) y (TMED003 o (TMD020 y TMD250)) y (TMED004 o BIO058) y ING129'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **ING249 — Inglés IV** (id 143, período 5, mención OTORRINO): texto: 'ING239 o equivalentes'; ids: ['ING239']
- **SPAB110 — Salud pública I** (id 144, período 5, mención OTORRINO): texto: 'ING239 o equivalentes y (TMED005 o TMD110)'; ids: ['ING239', 'TMED005']
- **TMED006 — Procedimientos de tecnología médica y bioseguridad** (id 145, período 5, mención OTORRINO): texto: 'FARM171 o BIO184'; ids: ['FARM171']
- **TMED551 — Morfofisiopatología orl** (id 146, período 5, mención OTORRINO): texto: 'TMED005 o TMD110'; ids: ['TMED005']
- **TMED552 — Función nasal** (id 147, período 5, mención OTORRINO): texto: '(TMED005 o TMD110) y (TMED451 o FMF120)'; ids: ['TMED005', 'TMED451']
- **TMED553 — Neurofisiología aplicada a la orl** (id 148, período 5, mención OTORRINO): texto: 'TMED452 o TMD196'; ids: ['TMED452']
- **SPAB111 — Salud pública II** (id 150, período 6, mención OTORRINO): texto: 'SPAB110 o equivalentes'; ids: ['SPAB110']
- **TMED651 — Audiología básica** (id 151, período 6, mención OTORRINO): texto: '(TMED551 o TMD202) y (TMED553 o TMD196) y (TMED453 o TMD267)'; ids: ['TMED453', 'TMED551', 'TMED553']
- **TMED652 — Otoneurología I** (id 152, período 6, mención OTORRINO): texto: '(TMED551 o TMD202) y (TMED553 o TMD196)'; ids: ['TMED551', 'TMED553']
- **SPAB112 — Administración y gestión en salud** (id 153, período 7, mención OTORRINO): texto: 'SPAB111 o equivalentes'; ids: ['SPAB111']
- **TMED751 — Audiología avanzada y electrofisiología** (id 155, período 7, mención OTORRINO): texto: 'TMED651 o (TMD252 y TMD253)'; ids: ['TMED651']
- **TMED752 — Otoneurología II** (id 156, período 7, mención OTORRINO): texto: '(TMED651 o (TMD252 y TMD253)) y (TMED652 o (TMD202 y TMD316))'; ids: ['TMED651', 'TMED652']
- **TMED753 — Integrador I: caso clínico OTO** (id 157, período 7, mención OTORRINO): texto: '(TMED651 o (TMD252 y TMD253)) y (TMED652 o (TMD202 y TMD316))'; ids: ['TMED651', 'TMED652']
- **TMED851 — Salud ocupacional** (id 160, período 8, mención OTORRINO): texto: 'SPAB112 o TMD320'; ids: ['SPAB112']
- **TMED852 — Prótesis y ortesis auditivas** (id 161, período 8, mención OTORRINO): texto: '(TMED751 o TMD324) y TMED753'; ids: ['TMED751', 'TMED753']
- **TMED853 — Rehabilitación vestibular auditiva** (id 162, período 8, mención OTORRINO): texto: '(TMED751 o TMD324) y (TMED752 o TMD316)'; ids: ['TMED751', 'TMED752']
- **TMED951 — Seminario de investigación OTO** (id 164, período 9, mención OTORRINO): texto: 'SPAB303 y SPAB103 y (TMED851 o TMD280) y (TMED852 o TMD259) y (TMED853 o (TMD259 y TMD253))'; ids: ['SPAB103', 'SPAB303', 'TMED851', 'TMED852', 'TMED853']

### Mismo código con ids distintos (una copia por mención) (13)

- **CEGPC13 — Pensamiento crítico**: ids: 38 (BACIMET), 69 (IFIME), 87 (MORFO), 122 (OFTA), 149 (OTORRINO)
- **CEGRS14 — Responsabilidad social**: ids: 43 (BACIMET), 74 (IFIME), 103 (MORFO), 134 (OFTA), 163 (OTORRINO)
- **FARM171 — Farmacología general**: ids: 18 (BACIMET), 46 (IFIME), 77 (MORFO), 106 (OFTA), 137 (OTORRINO)
- **ING239 — Inglés III**: ids: 19 (BACIMET), 47 (IFIME), 78 (MORFO), 107 (OFTA), 138 (OTORRINO)
- **ING249 — Inglés IV**: ids: 23 (BACIMET), 52 (IFIME), 82 (MORFO), 112 (OFTA), 143 (OTORRINO)
- **SPAB103 — Gestión y aseguramiento de la calidad**: ids: 39 (BACIMET), 70 (IFIME), 98 (MORFO), 129 (OFTA), 158 (OTORRINO)
- **SPAB110 — Salud pública I**: ids: 24 (BACIMET), 53 (IFIME), 83 (MORFO), 113 (OFTA), 144 (OTORRINO)
- **SPAB111 — Salud pública II**: ids: 28 (BACIMET), 58 (IFIME), 88 (MORFO), 118 (OFTA), 150 (OTORRINO)
- **SPAB112 — Administración y gestión en salud**: ids: 32 (BACIMET), 63 (IFIME), 92 (MORFO), 123 (OFTA), 153 (OTORRINO)
- **SPAB303 — Metodología de la investigación**: ids: 40 (BACIMET), 71 (IFIME), 99 (MORFO), 130 (OFTA), 159 (OTORRINO)
- **TMED002 — Educación en salud**: ids: 33 (BACIMET), 64 (IFIME), 93 (MORFO), 124 (OFTA), 154 (OTORRINO)
- **TMED005 — Fisiopatología**: ids: 20 (BACIMET), 48 (IFIME), 79 (MORFO), 108 (OFTA), 139 (OTORRINO)
- **TMED006 — Procedimientos de tecnología médica y bioseguridad**: ids: 25 (BACIMET), 54 (IFIME), 84 (MORFO), 114 (OFTA), 145 (OTORRINO)

## Psicología

### prereq_expr menciona alternativas ("o"/equivalentes); solo se aplican los ids (25)

- **ING129 — Inglés II** (id 7, período 2): texto: 'ING119 o ING111 o ING110 o ING116 o ING117 o CNT021 o (ING050 y ING051) o (FLG301 y FLG302) o (BMA281 y BMA282) o (ETU081 y ETU082)'; ids: ['ING119']
- **PSIC122 — Procesos psicológicos y neurociencias** (id 9, período 2): texto: 'BIOL080 o BIO036'; ids: ['BIOL080']
- **ING239 — Inglés III** (id 12, período 3): texto: 'ING129 o ING121 o ING120 o ING216 o ING126 o ING134 o ING127 o CNT026 o (ETU181 y ETU182) o ING229'; ids: ['ING129']
- **PSIC213 — Investigación I** (id 15, período 3): texto: 'PSIC123 o HUF136 o PSL006'; ids: ['PSIC123']
- **ING249 — Inglés IV** (id 17, período 4): texto: 'ING239 o ING210 o ING216 o ING224 o ING126 o CNT126 o (ETU281 y ETU282) o ING217'; ids: ['ING239']
- **PSIC221 — Psicoanálisis II** (id 18, período 4): texto: 'PSIC211 o PSL104'; ids: ['PSIC211']
- **PSIC222 — Psicología del desarrollo II** (id 19, período 4): texto: 'PSIC212 o PSL111'; ids: ['PSIC212']
- **PSIC223 — Investigación II** (id 20, período 4): texto: 'PSIC213 o FMS180'; ids: ['PSIC213']
- **PSIC313 — Taller de integración** (id 24, período 5): texto: '(PSIC211 o PSL104) y (PSIC222 o PSL112) y (PSIC223 o PSL105)'; ids: ['PSIC211', 'PSIC222', 'PSIC223']
- **PSIC321 — Psicodiagnóstico clínico II** (id 26, período 6): texto: 'PSIC311 o PSL131 o PSL233'; ids: ['PSIC311']
- **PSIC322 — Psicopatología y psiquiatría II** (id 27, período 6): texto: 'PSIC312 o PSL232'; ids: ['PSIC312']
- **PSIC324 — Diagnóstico e intervención social** (id 29, período 6): texto: 'PSIC314 o PSL240'; ids: ['PSIC314']
- **PSIC412 — Psicopatología infanto juvenil** (id 32, período 7): texto: 'PSIC312 o PSL232'; ids: ['PSIC312']
- **PSIC413 — Diagnóstico e intervención educacional** (id 33, período 7): texto: 'PSIC323 o PSL213'; ids: ['PSIC323']
- **PSIC415 — Diagnóstico e intervención organizacional** (id 35, período 7): texto: 'PSIC325 o PSL344'; ids: ['PSIC325']
- **PSIC422 — Clínica infanto juvenil** (id 37, período 8): texto: 'PSIC412 o PSL314'; ids: ['PSIC412']
- **PSIC423 — Taller de investigación** (id 38, período 8): texto: 'PSIC313 y (PSIC321 o PSL234) y (PSIC322 o PSL235) y (PSIC323 o PSL213) y (PSIC325 o PSL344) y (PSIC414 o PSL242)'; ids: ['PSIC313', 'PSIC321', 'PSIC322', 'PSIC323', 'PSIC325', 'PSIC414']
- **PSIC424 — Diagnóstico e intervención jurídica** (id 39, período 8): texto: 'PSIC414 o PSL242'; ids: ['PSIC414']
- **PSIC425 — Intervención clínica sistémica** (id 40, período 8): texto: 'PSIC411 o PSL206'; ids: ['PSIC411']
- **PSIC511 — Taller de intervención clínica** (id 41, período 9): texto: '(PSIC411 o PSL206) y (PSIC412 o PSL314) y (PSIC413 o PSL204) y (PSIC414 o PSL242) y (PSIC415 o PSL345) y (PSIC421 o PSL334 o (PSL331 y PSL335)) y (PSIC422 o PSL315) y (PSIC423 o PSL348) y PSIC424 y (PSIC425 o PSL333)'; ids: ['PSIC411', 'PSIC412', 'PSIC413', 'PSIC414', 'PSIC415', 'PSIC421', 'PSIC422', 'PSIC423', 'PSIC424', 'PSIC425']
- **PSIC512 — Psicología y salud** (id 42, período 9): texto: '(PSIC411 o PSL206) y (PSIC412 o PSL314) y (PSIC413 o PSL204) y (PSIC414 o PSL242) y (PSIC415 o PSL345) y (PSIC421 o PSL334 o (PSL331 y PSL335)) y (PSIC422 o PSL315) y (PSIC423 o PSL348) y PSIC424 y (PSIC425 o PSL333)'; ids: ['PSIC411', 'PSIC412', 'PSIC413', 'PSIC414', 'PSIC415', 'PSIC421', 'PSIC422', 'PSIC423', 'PSIC424', 'PSIC425']
- **PSIC513 — Taller de diagnóstico e intervención psicosocial** (id 43, período 9): texto: '(PSIC411 o PSL206) y (PSIC412 o PSL314) y (PSIC413 o PSL204) y (PSIC414 o PSL242) y (PSIC415 o PSL345) y (PSIC421 o PSL334 o (PSL331 y PSL335)) y (PSIC422 o PSL315) y (PSIC423 o PSL348) y PSIC424 y (PSIC425 o PSL333)'; ids: ['PSIC411', 'PSIC412', 'PSIC413', 'PSIC414', 'PSIC415', 'PSIC421', 'PSIC422', 'PSIC423', 'PSIC424', 'PSIC425']
- **PSIC514 — Electivo de formación profesional I** (id 44, período 9): texto: '(PSIC411 o PSL206) y (PSIC412 o PSL314) y (PSIC413 o PSL204) y (PSIC414 o PSL242) y (PSIC415 o PSL345) y (PSIC421 o PSL334 o (PSL331 y PSL335)) y (PSIC422 o PSL315) y (PSIC423 o PSL348) y PSIC424 y (PSIC425 o PSL333)'; ids: ['PSIC411', 'PSIC412', 'PSIC413', 'PSIC414', 'PSIC415', 'PSIC421', 'PSIC422', 'PSIC423', 'PSIC424', 'PSIC425']
- **PSIC515 — Electivo de formación profesional II** (id 45, período 9): texto: '(PSIC411 o PSL206) y (PSIC412 o PSL314) y (PSIC413 o PSL204) y (PSIC414 o PSL242) y (PSIC415 o PSL345) y (PSIC421 o PSL334 o (PSL331 y PSL335)) y (PSIC422 o PSL315) y (PSIC423 o PSL348) y PSIC424 y (PSIC425 o PSL333)'; ids: ['PSIC411', 'PSIC412', 'PSIC413', 'PSIC414', 'PSIC415', 'PSIC421', 'PSIC422', 'PSIC423', 'PSIC424', 'PSIC425']
- **PSIC521 — Práctica profesional** (id 46, período 10): texto: '(PSIC511 o MPC531) y (PSIC512 o MPC532) y PSIC513 y (PSIC514 o PSL323 o PSIC P011 o PSIC P012 o PSIC P036 o PSIC P097 o PSIC P098) y (PSIC515 o PSL332 o PSIC P007 o PSIC P008 o PSIC P009 o PSIC P010 o PSIC P049 o PSIC P096)'; ids: ['PSIC511', 'PSIC512', 'PSIC513', 'PSIC514', 'PSIC515']

### total_creditos = 0 (se interpreta como desconocido) (1)

-: total_creditos = 0
