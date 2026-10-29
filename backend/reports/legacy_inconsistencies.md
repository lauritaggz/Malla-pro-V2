# Inconsistencias en las mallas legadas

Generado por `uv run python -m app.scripts.import_legacy_mallas`. Los datos se importaron
tal cual (es el comportamiento actual de la app); este archivo es para revisarlos
contra las mallas oficiales. No se corrigió nada.

## Resumen

| Malla | id_duplicado | id_inexistente | autorreferencia | ciclo | prereq_fuera_del_alcance | prereq_mismo_periodo_o_posterior | texto_distinto_de_ids | ids_sin_texto | texto_sin_ids | correq_texto_distinto_de_ids | alternativas_ignoradas | codigo_repetido | campo_no_modelado | equivalencia_sin_curso | creditos_totales_cero |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ingeniería Civil Industrial | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 38 | 0 | 0 | 0 | 0 |
| Ingeniería en Computación e Informática | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 32 | 0 | 0 | 0 | 0 |
| Geología | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 48 | 0 | 0 | 0 | 0 |
| Ingeniería en Marina Mercante | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 59 | 10 | 0 | 0 | 0 |
| Ingeniería Civil Informática | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 39 | 0 | 0 | 0 | 0 |
| Ingeniería Civil en Minas | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 16 | 0 | 0 | 0 | 0 |
| Medicina | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 41 | 0 | 0 | 0 | 0 |
| Tecnología Médica | 0 | 0 | 0 | 0 | 0 | 0 | 21 | 0 | 0 | 0 | 123 | 13 | 0 | 0 | 0 |
| Psicología | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 | 0 | 0 | 0 | 0 |
| Bioquímica | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 48 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Ingeniería en Alimentos | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 56 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Química | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 46 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Química y Farmacia | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 55 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Leyenda de columnas: `id_duplicado` = Id de curso repetido (se ignora la segunda aparición); `id_inexistente` = Prerrequisito apunta a un id que no existe; `autorreferencia` = Curso es prerrequisito de sí mismo; `ciclo` = Ciclo de prerrequisitos; `prereq_fuera_del_alcance` = Prerrequisito de otra mención; `prereq_mismo_periodo_o_posterior` = Prerrequisito en el mismo período o uno posterior; `texto_distinto_de_ids` = El texto prereq_expr no coincide con los ids de prerrequisitos; `ids_sin_texto` = Tiene ids de prerrequisitos pero prereq_expr vacío o ausente; `texto_sin_ids` = Tiene texto en prereq_expr pero ningún id de prerrequisito; `correq_texto_distinto_de_ids` = El texto correq_expr no coincide con los ids de correquisitos; `alternativas_ignoradas` = prereq_expr menciona alternativas ("o"/equivalentes); solo se aplican los ids; `codigo_repetido` = Mismo código con ids distintos (una copia por mención); `campo_no_modelado` = Campo del JSON que el modelo no representa (se conserva en attrs); `equivalencia_sin_curso` = Equivalencia declarada para un código que no está en la malla; `creditos_totales_cero` = total_creditos = 0 (se interpreta como desconocido)

## Ingeniería Civil Industrial

### El texto correq_expr no coincide con los ids de correquisitos (3)

- **CIND311 — Práctica I** (id 17, período 4): texto: '( CFIS344 o FMF144 ) y ( FMMP312 o FMMP312 ) y ING119 y ( ACAD102 o IND1202 )'; ids: ['ACAD102', 'CFIS344', 'FMMP312', 'ING119']
- **CIND312 — Seminario de Licenciatura en Ciencias de la Ingeniería** (id 40, período 8): texto: '( IIND414 o IND2104 ) y ( CIND213 o ICI3217 ) y ( CIND214 o ICI2215 ) y CIND215 y ( CIND313 o ICI2611 )'; ids: ['CIND213', 'CIND214', 'CIND215', 'CIND313', 'IIND414']
- **CIND313 — Práctica II** (id 41, período 8): texto: '( IIND414 o IND2104 ) y ( CIND213 o ICI3217 ) y ( CIND214 o ICI2215 ) y CIND215 y CIND312'; ids: ['CIND213', 'CIND214', 'CIND215', 'CIND312', 'IIND414']

### prereq_expr menciona alternativas ("o"/equivalentes); solo se aplican los ids (38)

- **CFIS328 — Física Experimental** (id 6, período 2): texto: '( CFIS310 o FMF023 o FMF010 o FMF024 ) y ( FMMP012 o FMM013 o FMM012 o FMM035 )'; ids: ['CFIS310', 'FMMP012']
- **FMMP112 — Cálculo Diferencial** (id 7, período 2): texto: 'FMMP012 o FMM013 o FMM010 o FMM035 o FMM012'; ids: ['FMMP012']
- **TDFI103 — Base de Datos** (id 9, período 2): texto: 'TDFI102 o IND1401 o ICF122 o INS121 o AUT1302'; ids: ['TDFI102']
- **ACAD101 — Taller de Innovación y Emprendimiento I** (id 10, período 3): texto: 'TDFI101 o AUT1301 o TIN1201 o ICF121 o INS122 o ICI1201 o IMIN101 o ( GEOL101 o GEO101 ) o ( BIOQ388 o BIOQ398 ) o ( LCBB110 o LCBB100 )'; ids: ['TDFI101']
- **CFIS332 — Mecánica** (id 11, período 3): texto: '( ( CFIS328 o FMF023 o FME086 ) y ( FMMP112 o FMM033 o FMM112 ) ) o ( ( IAUT101 o AUT1303 ) y ( FMMP112 o FMM112 ) )'; ids: ['CFIS328', 'FMMP112']
- **FMMP212 — Cálculo Integral** (id 12, período 3): texto: 'FMMP112 o FMM030 o FMM010 o FMM033 o FMM112'; ids: ['FMMP112']
- **TDFI104 — Compliance & Accountability** (id 13, período 3): texto: 'TDFI101 o LIN1201 o ICF121 o INS122 o ICI1201 o IMIN101 o AUT1301'; ids: ['TDFI101']
- **CIND100 — Procesos Industriales** (id 14, período 3): texto: '( QUIM090 o QUI070 ) y ( CFIS310 o FMF024 )'; ids: ['CFIS310', 'QUIM090']
- **ACAD102 — Taller de Innovación y Emprendimiento II** (id 15, período 4): texto: 'ACAD101 o IIN1201 o ICT1201 o CEGP01'; ids: ['ACAD101']
- **CFIS344 — Electricidad y Magnetismo** (id 16, período 4): texto: '( ( CFIS332 o FMF122 o FMF025 ) y ( FMMP212 o FMM133 o FMM212 ) )'; ids: ['CFIS332', 'FMMP212']
- **CIND311 — Práctica I** (id 17, período 4): texto: '( CFIS310 o FMF024 ) y ( FMMP012 o FMM012 ) y ( TDFI101 o ICI1201 ) y ( TDFI102 o IND1401 ) y ( CFIS328 o FMF086 ) y ( FMMP112 o FMM112 ) y ( QUIM090 o QUI070 ) y ( TDFI103 o ICI2402 ) y ( ACAD101 o ICI1201 ) y ( CFIS332 o FMF025 ) y ( CIND100 o IND1205 ) y ( FMMP212 o FMM212 ) y TDFI104 y ( CEGHC11 o CEGHC01 o FIC1604 )'; ids: ['ACAD101', 'CEGHC11', 'CFIS310', 'CFIS328', 'CFIS332', 'CIND100', 'FMMP012', 'FMMP112', 'FMMP212', 'QUIM090', 'TDFI101', 'TDFI102', 'TDFI103', 'TDFI104']
- **FMMP312 — Sistemas y Ecuaciones Diferenciales Lineales** (id 18, período 4): texto: '( FMMP212 o FMM133 ) o ( FMMP212 o FMM130 ) o FMM212'; ids: ['FMMP212']
- **CIND111 — Economía Circular** (id 20, período 5): texto: 'CIND100 o IND1205'; ids: ['CIND100']
- **CIND112 — Investigación de Operaciones** (id 21, período 5): texto: 'FMMP212 o FMM212'; ids: ['FMMP212']
- **CIND411 — Economía** (id 22, período 5): texto: 'FMMP212 o FMM212'; ids: ['FMMP212']
- **FMSP316 — Métodos Cuantitativos** (id 23, período 5): texto: 'FMMP212 o FMM212 o FMM214'; ids: ['FMMP212']
- **ING129 — Inglés II** (id 24, período 5): texto: 'ING119 o ING111 o ING110 o ING116 o ING117 o CNT021 o ( ING050 y ING051 ) o ( FLG301 y FLG302 ) o ( BMA281 y BMA282 ) o ( ETU081 y ETU082 )'; ids: ['ING119']
- **ACAD103 — Taller de Innovación y Emprendimiento III** (id 25, período 6): texto: 'ACAD102 o IND1202 o FIC168'; ids: ['ACAD102']
- **CIND113 — Gestión de la Cadena de Suministro** (id 26, período 6): texto: 'CIND112 o IND2209'; ids: ['CIND112']
- **CIND211 — Redes y Sistemas Estocásticos en Ingeniería** (id 27, período 6): texto: '( CIND112 o IND2209 ) y ( FMSP316 o ( EMS176 y ICI2206 ) )'; ids: ['CIND112', 'FMSP316']
- **IIND412 — Costos y Presupuestos** (id 28, período 6): texto: 'FMMP212 o FMM212'; ids: ['FMMP212']
- **ING239 — Inglés III** (id 29, período 6): texto: 'ING129 o ING121 o ING120 o ING216 o ING126 o ING134 o ING127 o CNT026 o ( ETU181 y ETU182 ) o ING229'; ids: ['ING129']
- **TDFI105 — Minería de Datos** (id 30, período 6): texto: '( FMSP316 o ( FMS176 y ICI2206 ) o ( FMM214 ) ) y ( TDFI103 o ICI2402 o INS128 o ( ICF132 y ICF231 ) )'; ids: ['FMSP316', 'TDFI103']
- **CIND114 — Toma de Decisiones en la Cadena de Suministro** (id 32, período 7): texto: 'CIND113 o IND2211'; ids: ['CIND113']
- **CIND212 — Toma de Decisiones Bajo Incertidumbre** (id 33, período 7): texto: 'CIND211 o ICI2212'; ids: ['CIND211']
- **IIND413 — Ingeniería Económica** (id 34, período 7): texto: 'IIND412 o IND2102'; ids: ['IIND412']
- **ING249 — Inglés IV** (id 35, período 7): texto: 'ING239 o ING210 o ING216 o ING224 o ING126 o CNT126 o ( ETU281 y ETU282 ) o ING217'; ids: ['ING239']
- **TDFI106 — Gestión de la Transformación Digital** (id 36, período 7): texto: 'TDFI104 o CEGS01 o ICF253'; ids: ['TDFI104']
- **CIND213 — Simulación de Sistemas** (id 37, período 8): texto: 'CIND212 o CI2212'; ids: ['CIND212']
- **CIND214 — Estrategia y Sustentabilidad en Cadena de Suministro** (id 38, período 8): texto: 'CIND212 o ICT2212'; ids: ['CIND212']
- **CIND215 — Analítica** (id 39, período 8): texto: 'CIND212 o IC2212'; ids: ['CIND212']
- **CIND312 — Seminario de Licenciatura en Ciencias de la Ingeniería** (id 40, período 8): texto: 'TDFI105 y ( IIND413 o IND2103 ) y ( CIND212 o ICI2212 ) y ( CIND114 o IND2213 )'; ids: ['CIND114', 'CIND212', 'IIND413', 'TDFI105']
- **CIND313 — Práctica II** (id 41, período 8): texto: 'TDFI105 y ( IIND413 o IND2103 ) y ( CIND212 o ICI2212 ) y ( CIND114 o IND2213 )'; ids: ['CIND114', 'CIND212', 'IIND413', 'TDFI105']
- **IIND414 — Evaluación de Proyectos** (id 42, período 8): texto: 'IIND413 o IND2103'; ids: ['IIND413']
- **CIND216 — Finanzas Corporativas** (id 43, período 9): texto: 'IIND413 o IND2103'; ids: ['IIND413']
- **CIND218 — Marketing** (id 45, período 9): texto: 'CIND411 o IND1101'; ids: ['CIND411']
- **CIND219 — Gestión Estratégica** (id 46, período 9): texto: 'CIND411 o IND1101'; ids: ['CIND411']
- **CIND315 — Proyecto de Título** (id 51, período 10): texto: 'CIND314 o ICI3003'; ids: ['CIND314']

## Ingeniería en Computación e Informática

### El texto correq_expr no coincide con los ids de correquisitos (3)

- **INSW220 — Práctica I** (id 17, período 4): texto: 'ING129 y ( FMSP316 o FMM214 ) y ( INSW221 o INS122 ) y ( PTEC101 o INS126 y INS127 )'; ids: ['FMSP316', 'ING129', 'INSW221', 'PTEC101']
- **INSW410 — Portafolio de Proyectos** (id 32, período 7): texto: '( PTEC106 o INS238 )'; ids: ['PTEC106']
- **INSW421 — Seminario de Licenciatura en Ingeniería** (id 38, período 8): texto: '( INSW422 o INS244 )'; ids: ['INSW422']

### prereq_expr menciona alternativas ("o"/equivalentes); solo se aplican los ids (32)

- **ACAD101 — Taller de Innovación y Emprendimiento I** (id 5, período 2): texto: 'TDFI101 o AUT1301 o IN1201 o ICF121 o INS122 o ICI1201 o IMIN101 o ( GEOL101 o GEO101 ) o ( BIOQ388 o BIOQ398 ) o ( LCBB110 o LCBB100 )'; ids: ['TDFI101']
- **CFIS328 — Física Experimental** (id 7, período 2): texto: '( CFIS310 o FMF023 o FMF010 o FMF024 ) y ( FMMP012 o FMM013 o FMM012 o FMM035 )'; ids: ['CFIS310', 'FMMP012']
- **FMMP112 — Cálculo Diferencial** (id 8, período 2): texto: 'FMMP012 o FMM013 o FMM010 o FMM035 o FMM012'; ids: ['FMMP012']
- **TDFI103 — Base de Datos** (id 9, período 2): texto: 'TDFI102 o IND1401 o ICF122 o INS121 o AUT1302'; ids: ['TDFI102']
- **ACAD102 — Taller de Innovación y Emprendimiento II** (id 10, período 3): texto: 'ACAD101 o IIN1201 o ICI1201 o CEGP01'; ids: ['ACAD101']
- **CFIS332 — Mecánica** (id 11, período 3): texto: '( ( CFIS328 o FMF023 o FMF086 ) y ( FMMP112 o FMM033 o FMM112 ) ) o ( ( AUT101 o AUT1303 ) y ( FMMP112 o FMM112 ) )'; ids: ['CFIS328', 'FMMP112']
- **FMMP212 — Cálculo Integral** (id 12, período 3): texto: 'FMMP112 o FMM030 o FMM010 o FMM033 o FMM112'; ids: ['FMMP112']
- **TDFI104 — Compliance & Accountability** (id 14, período 3): texto: 'TDFI101 o IIN1201 o ICF121 o INS122 o ICT1201 o IMIN101 o AUT1301'; ids: ['TDFI101']
- **FMSP316 — Métodos Cuantitativos** (id 15, período 4): texto: 'FMMP212 o FMM212 o FMM214'; ids: ['FMMP212']
- **ING129 — Inglés II** (id 16, período 4): texto: 'ING119 o ING111 o ING110 o ING116 o ING117 o CNT021 o ( ING050 y ING051 ) o ( FLG301 y FLG302 ) o ( BMA281 y BMA282 ) o ( ETU081 y ETU082 )'; ids: ['ING119']
- **INSW220 — Práctica I** (id 17, período 4): texto: '( TDFI104 o CEGS01 ) y ( ACAD102 o FIC168 )'; ids: ['ACAD102', 'TDFI104']
- **INSW221 — Tecnologías Disruptivas** (id 18, período 4): texto: 'TDFI103 o INS128'; ids: ['TDFI103']
- **PTEC101 — Algoritmos y Estructuras de Datos** (id 19, período 4): texto: 'TDFI102 o INS121 o ICF122'; ids: ['TDFI102']
- **ING239 — Inglés III** (id 20, período 5): texto: 'ING129 o ING121 o ING120 o ING216 o ING126 o ING134 o ING127 o CNT026 o ( ETU181 y ETU182 ) o ING229'; ids: ['ING129']
- **INSW311 — Disrupción Empresarial** (id 21, período 5): texto: 'INSW221 o INS122'; ids: ['INSW221']
- **PTEC102 — Paradigmas de Programación** (id 23, período 5): texto: 'PTEC101 o ( INS126 y INS127 ) o ICF123'; ids: ['PTEC101']
- **TDFI105 — Minería de Datos** (id 24, período 5): texto: '( FMSP316 o ( FMS176 y ICI2206 ) o ( FMM214 ) ) y ( TDFI103 o ICI2402 o INS128 o ( ICF132 y ICF231 ) )'; ids: ['FMSP316', 'TDFI103']
- **ACAD103 — Taller de Innovación y Emprendimiento III** (id 25, período 6): texto: 'ACAD102 o IND1202 o FIC168'; ids: ['ACAD102']
- **ING249 — Inglés IV** (id 26, período 6): texto: 'ING239 o ING210 o ING216 o ING224 o ING126 o CNT126 o ( ETU281 y ETU282 ) o ING217'; ids: ['ING239']
- **INSW321 — Desafío Tecnológico** (id 27, período 6): texto: 'INSW311 o INS236'; ids: ['INSW311']
- **PTEC103 — Desarrollo Web y Móvil** (id 28, período 6): texto: 'PTEC102 o ( INS124 y INS125 ) o ICF131'; ids: ['PTEC102']
- **PTEC105 — Ingeniería de Software I** (id 29, período 6): texto: 'PTEC102 o ( INS124 y INS125 ) o ICF131'; ids: ['PTEC102']
- **TDFI106 — Gestión de la Transformación Digital** (id 30, período 6): texto: 'TDFI104 o CEGS01 o ICF253'; ids: ['TDFI104']
- **INSW410 — Portafolio de Proyectos** (id 32, período 7): texto: '( INSW321 o INS242 ) y ( PTEC105 o ( INS232 o INS235 ) ) y ( PTEC103 o INS234 )'; ids: ['INSW321', 'PTEC103', 'PTEC105']
- **INSW411 — Tópico de Especialidad I** (id 33, período 7): texto: 'INSW311 o INS236'; ids: ['INSW311']
- **INSW412 — Tópico de Especialidad II** (id 34, período 7): texto: 'INSW312 o ITC1701'; ids: ['INSW312']
- **PTEC104 — Infraestructura TI** (id 35, período 7): texto: 'PTEC102 o ( INS124 y INS125 ) o ICF131'; ids: ['PTEC102']
- **PTEC106 — Ingeniería de Software II** (id 36, período 7): texto: '( PTEC103 o INS234 o ICF331 ) y ( PTEC105 o INS232 o INS235 o ICF232 )'; ids: ['PTEC103', 'PTEC105']
- **INSW420 — Práctica II** (id 37, período 8): texto: '( INSW321 o INS242 ) y ( PTEC103 o INS234 ) y ( ACAD103 o FIC168 )'; ids: ['ACAD103', 'INSW321', 'PTEC103']
- **INSW421 — Seminario de Licenciatura en Ingeniería** (id 38, período 8): texto: '( INSW410 o INS237 ) y ( PTEC106 o INS238 )'; ids: ['INSW410', 'PTEC106']
- **INSW422 — Proyecto de Título** (id 39, período 8): texto: 'INSW410 o INS237'; ids: ['INSW410']
- **PTEC107 — Ciberseguridad** (id 40, período 8): texto: 'PTEC104 o ( ICF243 y ICF341 ) o INF1203'; ids: ['PTEC104']

## Geología

### El texto correq_expr no coincide con los ids de correquisitos (1)

- **GEOL006 — Geología andina e interpretación avanzada** (id 55, período 10): texto: '( GEOL001 o GEOLP014 ) y GEOL003'; ids: ['GEOL001', 'GEOL003']

### prereq_expr menciona alternativas ("o"/equivalentes); solo se aplican los ids (48)

- **CFIS328 — Física experimental** (id 6, período 2): texto: '( CFIS310 o FMF023 o FMF010 o FMF024 ) y ( FMMP012 o FMM013 o FMM012 o FMM035 )'; ids: ['CFIS310', 'FMMP012']
- **FMMP112 — Cálculo diferencial** (id 7, período 2): texto: 'FMMP012 o FMM013 o FMM010 o FMM035 o FMM012'; ids: ['FMMP012']
- **GEOL201 — Mineralogía y cristalografía** (id 8, período 2): texto: '( ( GEOL101 o GEO101 ) y ( QUIM090 o QUI104 ) )'; ids: ['GEOL101', 'QUIM090']
- **GEOL202 — Paleontología y evolución** (id 9, período 2): texto: 'GEOL101 o GEO101'; ids: ['GEOL101']
- **GEOL203 — Fundamentos de geología** (id 10, período 2): texto: 'GEOL101 o GEO101'; ids: ['GEOL101']
- **ACAD101 — Taller de innovación y emprendimiento i** (id 11, período 3): texto: 'TDFI101 o AUT1301 o IIN1201 o ICF121 o INS122 o ICI1201 o IMIN101 o ( GEOL101 o GEO101 ) o ( BIOQ388 o BIOQ398 ) o ( LCBB110 o LCBB100 )'; ids: ['GEOL101']
- **CFIS332 — Mecánica** (id 12, período 3): texto: '( ( CFIS328 o FMF023 o FMF086 ) y ( FMMP112 o FMM033 o FMM112 ) ) o ( ( IAUT101 o AUT1303 ) y ( FMMP112 o FMM112 ) )'; ids: ['CFIS328', 'FMMP112']
- **FMMP212 — Cálculo integral** (id 13, período 3): texto: 'FMMP112 o FMM030 o FMM010 o FMM033 o FMM112'; ids: ['FMMP112']
- **GEOL301 — Geoquímica endógena** (id 14, período 3): texto: '( ( QUIM090 o QUI104 ) y ( GEOL203 o GEO102 ) )'; ids: ['GEOL203', 'QUIM090']
- **GEOL302 — Métodos analíticos i: microscopía óptica** (id 15, período 3): texto: '( GEOL201 o GEO201 ) y ( GEOL203 o GEO102 )'; ids: ['GEOL201', 'GEOL203']
- **ACAD102 — Taller de innovación y emprendimiento ii** (id 16, período 4): texto: 'ACAD101 o TIN1201 o ICI1201 o'; ids: ['ACAD101']
- **CFIS344 — Electricidad y magnetismo** (id 17, período 4): texto: '( ( CFIS332 o FMF122 o FMF025 ) y ( FMMP212 o FMM133 o FMM212 ) )'; ids: ['CFIS332', 'FMMP212']
- **FMMP312 — Sistemas y ecuaciones diferenciales lineales** (id 18, período 4): texto: '( FMMP212 o FMM133 ) o ( FMMP212 o FMM130 ) o FMM212'; ids: ['FMMP212']
- **GEOL401 — Integrador i: práctica i** (id 19, período 4): texto: '( GEOL301 o ( GEO302 y GEO304 ) ) y ( GEOL302 o GEO305 )'; ids: ['GEOL301', 'GEOL302']
- **GEOL501 — Petrología endógena** (id 21, período 5): texto: 'GEOL401 o GEO499'; ids: ['GEOL401']
- **GEOL502 — Sedimentología y estratigrafía** (id 22, período 5): texto: 'GEOL401 o GEO499'; ids: ['GEOL401']
- **GEOL503 — Métodos analíticos ii: sig y teledetección** (id 23, período 5): texto: 'GEOL302 o GEO305'; ids: ['GEOL302']
- **GEOL504 — Geoquímica exógena y ambiental** (id 24, período 5): texto: '( GEOL301 o ( GEO302 y GEO304 ) )'; ids: ['GEOL301']
- **GEOL505 — Bases de geología de campo** (id 25, período 5): texto: 'GEOL401 o GEO499'; ids: ['GEOL401']
- **ING129 — Inglés ii** (id 26, período 5): texto: 'ING119 o ING111 o ING110 o ING116 o ING117 o CNT021 o ( ING050 y ING051 ) o ( FLG301 y FLG302 ) o ( BMA281 y BMA282 ) o ( ETU081 y ETU082 )'; ids: ['ING119']
- **ACAD103 — Taller de innovación y emprendimiento iii** (id 27, período 6): texto: 'ACAD102 o IND1202 o FIC168'; ids: ['ACAD102']
- **GEOL601 — Fundamentos de programación y análisis numérico** (id 28, período 6): texto: '( ( FMMP312 o FMM254 ) y ( GEOL503 o GEO406 ) )'; ids: ['FMMP312', 'GEOL503']
- **GEOL602 — Deformación de la corteza** (id 29, período 6): texto: '( ( GEOL501 o GEO403 ) y ( GEOL502 o GEO301 ) )'; ids: ['GEOL501', 'GEOL502']
- **GEOL603 — Geología de campo i** (id 30, período 6): texto: '( ( GEOL505 o GEO307 ) y ( GEOL503 o GEO406 ) )'; ids: ['GEOL503', 'GEOL505']
- **ING239 — Inglés iii** (id 31, período 6): texto: 'ING129 o ING121 o ING120 o ING216 o ING126 o ING134 o ING127 o CNT026 o ( ETU181 y ETU182 ) o ING229'; ids: ['ING129']
- **GEOL701 — Depósitos minerales y metalogénesis andina** (id 33, período 7): texto: '( ( GEOL603 o GEO403 ) y ( GEOL602 o GEO307 ) )'; ids: ['GEOL602', 'GEOL603']
- **GEOL702 — Geomorfología** (id 34, período 7): texto: '( ( GEOL602 o GEO307 ) y ( GEOL504 o GEO506 ) )'; ids: ['GEOL504', 'GEOL602']
- **GEOL703 — Paleoclima y ambiente** (id 35, período 7): texto: 'GEOL504 o GEO506'; ids: ['GEOL504']
- **GEOL704 — Geología de campo ii** (id 36, período 7): texto: '( ( GEOL603 o GEO403 ) y ( GEOL602 o GEO307 ) )'; ids: ['GEOL602', 'GEOL603']
- **ING249 — Inglés iv** (id 37, período 7): texto: 'ING239 o ING210 o ING216 o ING224 o ING126 o CNT126 o ( ETU281 y ETU282 ) o ING217'; ids: ['ING239']
- **GEOL801 — Recursos energéticos** (id 38, período 8): texto: '( GEOL701 o ( GEO407 y GEO402 ) )'; ids: ['GEOL701']
- **GEOL802 — Geología de chile** (id 39, período 8): texto: '( ( GEOL704 o GEO407 ) y ( GEOL701 o ( GEO407 y GEO402 ) ) )'; ids: ['GEOL701', 'GEOL704']
- **GEOL803 — Hidrogeología** (id 40, período 8): texto: '( GEOL702 o GEO306 )'; ids: ['GEOL702']
- **GEOL804 — Métodos de exploración geofísica** (id 41, período 8): texto: '( GEOL701 o ( GEO407 y GEO402 ) y GEOL601 )'; ids: ['GEOL601', 'GEOL701']
- **GEOL805 — Integrador ii: seminario licenciatura en ciencias geológicas** (id 42, período 8): texto: '( ( GEOL704 o GEO407 ) y ( GEOL701 o ( GEO407 y GEO402 ) ) )'; ids: ['GEOL701', 'GEOL704']
- **GEOL806 — Práctica ii** (id 43, período 8): texto: 'GEOL704 o GEO407'; ids: ['GEOL704']
- **GEOL901 — Geología de minas** (id 44, período 9): texto: '( ( GEOL804 o GEO308 ) y ( GEOL801 o GEO408 ) )'; ids: ['GEOL801', 'GEOL804']
- **GEOL902 — Geoestadística y modelamiento geológico** (id 45, período 9): texto: 'GEOL804 o GEO308'; ids: ['GEOL804']
- **GEOL903 — Geología de campo iii** (id 46, período 9): texto: 'GEOL805 o GEO405'; ids: ['GEOL805']
- **GEOL904 — Peligros geológicos y planificación territorial** (id 47, período 9): texto: 'GEOL803 o GEO502'; ids: ['GEOL803']
- **GEOL905 — Tópicos de especialidad i** (id 48, período 9): texto: 'GEOL802 o GEO411'; ids: ['GEOL802']
- **GEOL906 — Portafolio de proyectos** (id 49, período 9): texto: 'GEOL805 o GEO405'; ids: ['GEOL805']
- **GEOL001 — Tópicos de especialidad ii** (id 50, período 10): texto: 'GEOL905 o GEOLP001 o GEOLP002 o GEOLP003 o GEOLP004 o GEOLP005 o GEOLP006 o GEOLP007 o GEOLP008'; ids: ['GEOL905']
- **GEOL002 — Economía y evaluación de proyectos geológicos** (id 51, período 10): texto: '( GEOL901 o ( GEO412 y GEO501 ) ) y ( GEOL903 o GEO410 )'; ids: ['GEOL901', 'GEOL903']
- **GEOL003 — Tópicos de especialidad iii** (id 52, período 10): texto: 'GEOL905 o GEOLP001 o GEOLP002 o GEOLP003 o GEOLP004 o GEOLP005 o GEOLP006 o GEOLP007 o GEOLP008'; ids: ['GEOL905']
- **GEOL004 — Geoética y geopatrimonio** (id 53, período 10): texto: 'GEOL905 o GEOLP001 o GEOLP002 o GEOLP003 o GEOLP004 o GEOLP005 o GEOLP006 o GEOLP007 o GEOLP008'; ids: ['GEOL905']
- **GEOL005 — Integrador iii: proyecto de título** (id 54, período 10): texto: '( ( GEOL906 o GEO505 ) y ( GEOL806 o GEO599 ) )'; ids: ['GEOL806', 'GEOL906']
- **GEOL006 — Geología andina e interpretación avanzada** (id 55, período 10): texto: '( GEOL903 o GEO410 )'; ids: ['GEOL903']

## Ingeniería en Marina Mercante

### El texto correq_expr no coincide con los ids de correquisitos (1)

- **IMMP302 — Comunicaciones I** (id 56, período 5, mención CUBI): texto: '( IMMP301 o MMP152 )'; ids: ['IMMP301']

### prereq_expr menciona alternativas ("o"/equivalentes); solo se aplican los ids (59)

- **CFIS328 — Física Experimental** (id 6, período 2): texto: '( CFIS310 o FMF023 o FMF010 o FMF024 ) y ( FMMP012 o FMM013 o FMM012 o FMM035 )'; ids: ['CFIS310', 'FMMP012']
- **FMMP112 — Cálculo Diferencial** (id 7, período 2): texto: 'FMMP012 o FMM013 o FMM010 o FMM035 o FMM012'; ids: ['FMMP012']
- **IMMC102 — Procesos de Ingeniería en Marina Mercante** (id 8, período 2): texto: 'CFIS310 o FMF010'; ids: ['CFIS310']
- **IMMC103 — Reglamentación y Legislación** (id 9, período 2): texto: 'IMMC101 o ( MMC121 y MMC122 y MMC181 )'; ids: ['IMMC101']
- **ING129 — Inglés II** (id 10, período 2): texto: 'ING119 o ING111 o ING110 o ING116 o ING117 o CNT021 o ( ING050 y ING051 ) o ( FLG301 y FLG302 ) o ( BMA281 y BMA282 ) o ( ETU081 y ETU082 )'; ids: ['ING119']
- **IMMC201 — Interpretación de Planos y Dibujo Técnico** (id 11, período 3): texto: 'IMMC102 o QUI103'; ids: ['IMMC102']
- **IMMC202 — Mecánica Técnica Naval** (id 12, período 3): texto: 'CFIS328 o FMF110'; ids: ['CFIS328']
- **IMMC203 — Incendio y Abandono (OMI 1.19-1.23-1.20-2.03)** (id 13, período 3): texto: 'IMMC103 o ( MMC162 y MMC164 )'; ids: ['IMMC103']
- **IMMC204 — Electricidad** (id 14, período 3): texto: 'CFIS328 o FMF110'; ids: ['CFIS328']
- **ING239 — Inglés III** (id 15, período 3): texto: 'ING129 o ING121 o ING120 o ING216 o ING126 o ING134 o ING127 o CNT026 o ( ETU181 y ETU182 ) o ING229'; ids: ['ING129']
- **IMMC205 — Construcción Naval y Flotabilidad** (id 47, período 4, mención CUBI): texto: '( IMMC201 o MMP170 ) y ( IMMC202 o MMC192 )'; ids: ['IMMC201', 'IMMC202']
- **IMMP201 — Meteorología y Oceanografía** (id 48, período 4, mención CUBI): texto: 'FMMP112 o FMM030'; ids: ['FMMP112']
- **IMMP202 — Fundamentos de Navegación** (id 49, período 4, mención CUBI): texto: '( IMMC204 o MMP242 ) y ( FMMP112 o FMM030 )'; ids: ['FMMP112', 'IMMC204']
- **IMMP203 — Planificación y Estiba de la Carga** (id 50, período 4, mención CUBI): texto: 'IMMC202 o MMC192'; ids: ['IMMC202']
- **IMMP204 — Práctica I** (id 51, período 4, mención CUBI): texto: 'IMMC101 o ( MMC121 y MMC122 y MMC181 )'; ids: ['IMMC101']
- **ING249 — Inglés IV** (id 52, período 4, mención CUBI): texto: 'ING239 o ING210 o ING216 o ING224 o ING126 o CNT126 o ( ETU281 y ETU282 ) o ING217'; ids: ['ING239']
- **IMMC301 — Cuidado del Medio Ambiente (OMI I.01)** (id 54, período 5, mención CUBI): texto: 'IMMC203 y ( IMMC205 o ( MMP272 ) o ( MMQ272 y MMQ372 ) )'; ids: ['IMMC203', 'IMMC205']
- **IMMP301 — Posicionamiento y Pilotaje** (id 55, período 5, mención CUBI): texto: 'IMMP202 o MMP151'; ids: ['IMMP202']
- **IMMP302 — Comunicaciones I** (id 56, período 5, mención CUBI): texto: '( IMMP202 o MMP151 )'; ids: ['IMMP202']
- **IMMP303 — Estiba de los Pesos a Bordo** (id 57, período 5, mención CUBI): texto: '( IMMP203 o MMP394 ) y ( IMMC205 o MMP272 )'; ids: ['IMMC205', 'IMMP203']
- **IMMP304 — Navegación Electrónica (OMI 1.07-1.27)** (id 58, período 5, mención CUBI): texto: 'IMMP202 o MMP151'; ids: ['IMMP202']
- **IMMC303 — Costos y Finanzas** (id 60, período 6, mención CUBI): texto: '( FMMP112 o FMM030 )'; ids: ['FMMP112']
- **IMMP305 — Navegación Ortodrómica y Loxodrómica** (id 61, período 6, mención CUBI): texto: 'IMMP301 o MMP152'; ids: ['IMMP301']
- **IMMP307 — Maniobrabilidad de la Nave** (id 63, período 6, mención CUBI): texto: '( IMMP201 o MMP358 ) y ( IMMP301 o MMP152 )'; ids: ['IMMP201', 'IMMP301']
- **IMMP308 — Esfuerzos y Averías Estructurales** (id 64, período 6, mención CUBI): texto: 'IMMP303 o ( MMP394 y MMP372 )'; ids: ['IMMP303']
- **IMMC402 — Evaluación de Inversiones Marítimo Portuario** (id 66, período 7, mención CUBI): texto: 'IMMC303 o MMC134'; ids: ['IMMC303']
- **IMMP401 — Navegación Astronómica** (id 67, período 7, mención CUBI): texto: 'IMMP305 o MMP253'; ids: ['IMMP305']
- **IMMP402 — Búsqueda y Salvamento (OMI 1.08)** (id 68, período 7, mención CUBI): texto: 'IMMP304 o MMP254'; ids: ['IMMP304']
- **IMMP403 — Portafolio de Proyecto** (id 69, período 7, mención CUBI): texto: '( IMMP305 o MMP253 ) y ( IMMP308 o MMP374 ) y ( IMMC303 o MMC134 )'; ids: ['IMMC303', 'IMMP305', 'IMMP308']
- **IMMP404 — Seguros del Transporte Marítimo** (id 70, período 7, mención CUBI): texto: 'IMMP303 o ( MMP394 y MMP372 )'; ids: ['IMMP303']
- **IMMC404 — Seminario de Licenciatura en Ingeniería** (id 72, período 8, mención CUBI): texto: 'IMMC402 o MMC230'; ids: ['IMMC402']
- **IMMP405 — Inglés Marítimo Portuario** (id 73, período 8, mención CUBI): texto: '( ING249 o ING229 ) y ( IMMP402 o MMP382 )'; ids: ['IMMP402', 'ING249']
- **IMMP406 — Bridge Resource Management (OMI 1.22-BRM)** (id 74, período 8, mención CUBI): texto: '( IMMP402 o MMP382 ) y ( IMMP307 o MMP292 ) y IMMP306'; ids: ['IMMP306', 'IMMP307', 'IMMP402']
- **IMMP407 — Gestión del Transporte Marítimo** (id 75, período 8, mención CUBI): texto: 'IMMP404 o MMC330'; ids: ['IMMP404']
- **IMMP408 — Proyecto de Título** (id 76, período 8, mención CUBI): texto: 'IMMP403 y ( IMMC402 o MMC230 )'; ids: ['IMMC402', 'IMMP403']
- **IMMP409 — Práctica II** (id 77, período 8, mención CUBI): texto: 'IMMP204 y ( IMMP301 o MMP152 )'; ids: ['IMMP204', 'IMMP301']
- **IMMC205 — Construcción Naval y Flotabilidad** (id 16, período 4, mención MAQ): texto: '( IMMC201 o MMP170 ) y ( IMMC202 o MMC192 )'; ids: ['IMMC201', 'IMMC202']
- **IMMQ201 — Termodinámica Aplicada** (id 17, período 4, mención MAQ): texto: '( FMMP112 o FMM030 ) y ( IMMC202 o MMC192 )'; ids: ['FMMP112', 'IMMC202']
- **IMMQ202 — Elasticidad y Resistencia de Materiales** (id 18, período 4, mención MAQ): texto: '( FMMP112 o FMM030 ) y ( IMMC202 o MMC192 )'; ids: ['FMMP112', 'IMMC202']
- **IMMQ203 — Electrotecnia** (id 19, período 4, mención MAQ): texto: 'IMMC204 o MMP242'; ids: ['IMMC204']
- **IMMQ204 — Práctica I** (id 20, período 4, mención MAQ): texto: 'IMMC101 o ( MMC121 y MMC122 y MMC181 )'; ids: ['IMMC101']
- **ING249 — Inglés IV** (id 21, período 4, mención MAQ): texto: 'ING239 o ING210 o ING216 o ING224 o ING126 o CNT126 o ( ETU281 y ETU282 ) o ING217'; ids: ['ING239']
- **IMMC301 — Cuidado del Medio Ambiente (OMI I.01)** (id 23, período 5, mención MAQ): texto: 'IMMC203 y ( IMMC205 o ( MMP272 ) o ( MMQ272 y MMQ372 ) )'; ids: ['IMMC203', 'IMMC205']
- **IMMQ302 — Máquinas Eléctricas I** (id 25, período 5, mención MAQ): texto: 'IMMQ203 o MMQ240'; ids: ['IMMQ203']
- **IMMQ303 — Engine Room Management** (id 26, período 5, mención MAQ): texto: '( IMMQ203 o MMQ240 ) y ( IMMQ201 o ( MMQ212 y MMQ213 ) )'; ids: ['IMMQ201', 'IMMQ203']
- **IMMQ304 — Combustión Interna I** (id 27, período 5, mención MAQ): texto: 'IMMQ201 o ( MMQ212 y MMQ213 )'; ids: ['IMMQ201']
- **IMMC303 — Costos y Finanzas** (id 29, período 6, mención MAQ): texto: '( FMMP112 o FMM030 )'; ids: ['FMMP112']
- **IMMQ305 — Mantención de Motores I** (id 30, período 6, mención MAQ): texto: 'IMMQ301 o MMQ103'; ids: ['IMMQ301']
- **IMMQ306 — Electrónica** (id 31, período 6, mención MAQ): texto: 'IMMQ302 o MMQ244'; ids: ['IMMQ302']
- **IMMQ307 — Plantas a Vapor** (id 32, período 6, mención MAQ): texto: 'IMMQ304 o MMQ214'; ids: ['IMMQ304']
- **IMMQ308 — Combustión Interna II** (id 33, período 6, mención MAQ): texto: 'IMMQ304 o MMQ214'; ids: ['IMMQ304']
- **IMMC402 — Evaluación de Inversiones Marítimo Portuario** (id 35, período 7, mención MAQ): texto: 'IMMC303 o MMC134'; ids: ['IMMC303']
- **IMMQ401 — Mantención de Motores II** (id 36, período 7, mención MAQ): texto: 'IMMQ305 o MMQ104'; ids: ['IMMQ305']
- **IMMQ402 — Control Automático** (id 37, período 7, mención MAQ): texto: 'IMMQ306 o MMQ341'; ids: ['IMMQ306']
- **IMMQ403 — Máquinas Marinas** (id 38, período 7, mención MAQ): texto: 'IMMQ308 o MMQ216'; ids: ['IMMQ308']
- **IMMQ404 — Portafolio de Proyecto** (id 39, período 7, mención MAQ): texto: '( IMMQ305 o MMQ104 ) y ( IMMQ306 o MMQ341 ) y ( IMMQ308 o MMQ216 )'; ids: ['IMMQ305', 'IMMQ306', 'IMMQ308']
- **IMMC404 — Seminario de Licenciatura en Ingeniería** (id 41, período 8, mención MAQ): texto: 'IMMC402 o MMC230'; ids: ['IMMC402']
- **IMMQ405 — Inglés Técnico Marítimo** (id 42, período 8, mención MAQ): texto: '( ING249 o ING229 )'; ids: ['ING249']
- **IMMQ406 — Máquinas Eléctricas II** (id 43, período 8, mención MAQ): texto: 'IMMQ402 o MMQ342'; ids: ['IMMQ402']

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

## Ingeniería Civil Informática

### El texto correq_expr no coincide con los ids de correquisitos (3)

- **CINF100 — Práctica I** (id 17, período 4): texto: 'ING119 y ( FMMP312 o FMMP312 ) y ACAD102 y ( CFIS344 o FMF144 )'; ids: ['ACAD102', 'CFIS344', 'FMMP312', 'ING119']
- **CINF200 — Integrador II: Seminario de Licenciatura en Ciencias de la Ingeniería** (id 39, período 8): texto: '( TDFI106 o ICF352 ) y ( PTEC106 o ICF233 ) y ( PTEC107 o ICF342 ) y ( CINF107 o ICF321 o ICF331 o ICF353 o ICF343 o CINFP01 o o o o )'; ids: ['CINF107', 'PTEC106', 'PTEC107', 'TDFI106']
- **CINF109 — Administración Financiera de Proyectos I+D+i** (id 42, período 9): texto: '( CINF108 o ICF361 )'; ids: ['CINF108']

### prereq_expr menciona alternativas ("o"/equivalentes); solo se aplican los ids (39)

- **TDFI103 — Base de Datos** (id 5, período 2): texto: 'TDFI102 o IND1401 o ICF122 o INS121 o AUT1302'; ids: ['TDFI102']
- **FMMP112 — Cálculo Diferencial** (id 6, período 2): texto: 'FMMP012 o FMM013 o FMM010 o FMM035 o FMM012'; ids: ['FMMP012']
- **CFIS328 — Física Experimental** (id 7, período 2): texto: '( CFIS310 o FMF023 o FMF010 o FMF024 ) y ( FMMP012 o FMM013 o FMM012 o FMM035 )'; ids: ['CFIS310', 'FMMP012']
- **TDFI104 — Compliance & Accountability** (id 10, período 3): texto: 'TDFI101 o TIN1201 o ICF121 o INS122 o ICI1201 o IMIN101 o AUT1301'; ids: ['TDFI101']
- **PTEC101 — Algoritmos y Estructuras de Datos** (id 11, período 3): texto: 'TDFI102 o INS121 o ICF122'; ids: ['TDFI102']
- **FMMP212 — Cálculo Integral** (id 12, período 3): texto: 'FMMP112 o FMM030 o FMM010 o FMM033 o FMM112'; ids: ['FMMP112']
- **CFIS332 — Mecánica** (id 13, período 3): texto: '( ( CFIS328 o FMF023 o FME086 ) y ( FMMP112 o FMM033 o FMM112 ) ) o ( ( IAUT101 o AUT1303 ) y ( FMMP112 o FMM112 ) )'; ids: ['CFIS328', 'FMMP112']
- **ACAD101 — Taller de Innovación y Emprendimiento I** (id 14, período 3): texto: 'TDFI101 o AUT1301 o TIN1201 o ICF121 o INS122 o ICI1201 o IMIN101 o ( GEOL101 o GEO101 ) o ( BIOQ388 o BIOQ398 ) o ( LCBB110 o LCBB100 )'; ids: ['TDFI101']
- **FMMP312 — Sistemas y Ecuaciones Diferenciales Lineales** (id 15, período 4): texto: '( FMMP212 o FMM133 ) o ( FMMP212 o FMM130 ) o FMM212'; ids: ['FMMP212']
- **CFIS344 — Electricidad y Magnetismo** (id 16, período 4): texto: '( ( CFIS332 o FMF122 o FMF025 ) y ( FMMP212 o FMM133 o FMM212 ) )'; ids: ['CFIS332', 'FMMP212']
- **CINF100 — Práctica I** (id 17, período 4): texto: '( PTEC101 o ICF123 ) y ( TDFI103 o ( ICF132 y ICF231 ) ) y ( TDFI104 o ICF253 ) y ( FMMP212 o FMM212 ) y ( CFIS332 o FMF025 ) y ACAD101'; ids: ['ACAD101', 'CFIS332', 'FMMP212', 'PTEC101', 'TDFI103', 'TDFI104']
- **ACAD102 — Taller de Innovación y Emprendimiento II** (id 18, período 4): texto: 'ACAD101 o TIN1201 o ICI1201 o CEGP01'; ids: ['ACAD101']
- **FMSP316 — Métodos Cuantitativos** (id 20, período 5): texto: 'FMMP212 o FMM212 o FMM214'; ids: ['FMMP212']
- **PTEC102 — Paradigmas de Programación** (id 21, período 5): texto: 'PTEC101 o ( INS126 y INS127 ) o ICF123'; ids: ['PTEC101']
- **CINF102 — Fundamentos de Computación de Alto Desempeño** (id 22, período 5): texto: 'PTEC101 o ICF123'; ids: ['PTEC101']
- **CINF101 — Análisis y Diseño de Algoritmos** (id 23, período 5): texto: 'PTEC101 o ICF123'; ids: ['PTEC101']
- **ING129 — Inglés II** (id 24, período 5): texto: 'ING119 o ING111 o ING110 o ING116 o ING117 o CNT021 o ( ING050 y ING051 ) o ( FLG301 y FLG302 ) o ( BMA281 y BMA282 ) o ( ETU081 y ETU082 )'; ids: ['ING119']
- **TDFI105 — Minería de Datos** (id 25, período 6): texto: '( FMSP316 o ( FMS176 y ICI2206 ) o ( FMM214 ) ) y ( TDFI103 o ICI2402 o INS128 o ( ICF132 y ICF231 ) )'; ids: ['FMSP316', 'TDFI103']
- **PTEC103 — Desarrollo Web y Móvil** (id 26, período 6): texto: 'PTEC102 o ( INS124 y INS125 ) o ICF131'; ids: ['PTEC102']
- **PTEC104 — Infraestructura TI** (id 27, período 6): texto: 'PTEC102 o ( INS124 y INS125 ) o ICF131'; ids: ['PTEC102']
- **CINF103 — Fundamentos de Inteligencia Artificial** (id 28, período 6): texto: 'CINF101 o ICF124'; ids: ['CINF101']
- **ING239 — Inglés III** (id 29, período 6): texto: 'ING129 o ING121 o ING120 o ING216 o ING126 o ING134 o ING127 o CNT026 o ( ETU181 y ETU182 ) o ING229'; ids: ['ING129']
- **PTEC105 — Ingeniería de Software I** (id 30, período 7): texto: 'PTEC102 o ( INS124 y INS125 ) o ICF131'; ids: ['PTEC102']
- **CINF104 — Aprendizaje de Máquina** (id 31, período 7): texto: 'CINF103 o ICF222'; ids: ['CINF103']
- **CINF105 — Optimización** (id 32, período 7): texto: '( CINF101 o ICF124 )'; ids: ['CINF101']
- **ACAD103 — Taller de Innovación y Emprendimiento III** (id 33, período 7): texto: 'ACAD102 o IND1202 o FIC168'; ids: ['ACAD102']
- **ING249 — Inglés IV** (id 34, período 7): texto: 'ING239 o ING210 o ING216 o ING224 o ING126 o CNT126 o ( ETU281 y ETU282 ) o ING217'; ids: ['ING239']
- **TDFI106 — Gestión de la Transformación Digital** (id 35, período 8): texto: 'TDFI104 o CEGS01 o ICF253'; ids: ['TDFI104']
- **PTEC106 — Ingeniería de Software II** (id 36, período 8): texto: '( PTEC103 o INS234 o ICF331 ) y ( PTEC105 o INS232 o INS235 o ICF232 )'; ids: ['PTEC103', 'PTEC105']
- **PTEC107 — Ciberseguridad** (id 37, período 8): texto: 'PTEC104 o ( ICF243 y ICF341 ) o INF1203'; ids: ['PTEC104']
- **CINF107 — Tópicos de Especialidad I** (id 38, período 8): texto: 'CINF103 o ICF222'; ids: ['CINF103']
- **CINF200 — Integrador II: Seminario de Licenciatura en Ciencias de la Ingeniería** (id 39, período 8): texto: '( CINF103 o ICE222 ) y ( PTEC105 o ICF232 ) y ( TDFI105 o ( ICF321 y ICF353 ) ) y ( CFIS344 o FMF144 )'; ids: ['CFIS344', 'CINF103', 'PTEC105', 'TDFI105']
- **CINF108 — Portafolio de Proyectos** (id 41, período 9): texto: '( PTEC106 o ICF233 ) y ( TDFI106 o ICF352 ) y ( CINF200 o ICF361 )'; ids: ['CINF200', 'PTEC106', 'TDFI106']
- **CINF109 — Administración Financiera de Proyectos I+D+i** (id 42, período 9): texto: '( PTEC106 o ICF233 )'; ids: ['PTEC106']
- **CINF110 — Ciencia de Datos** (id 43, período 9): texto: '( TDFI105 o ICF321 o ICF353 o ICFP028 ) y ( CINF103 o ICF222 )'; ids: ['CINF103', 'TDFI105']
- **CINF111 — Tópicos de Especialidad II** (id 44, período 9): texto: 'CINF103 o ICF222'; ids: ['CINF103']
- **CINF112 — Tópicos de Especialidad III** (id 45, período 9): texto: 'CINF103 o ICF222'; ids: ['CINF103']
- **CINF400 — Proyecto de Título** (id 46, período 10): texto: 'CINF108 o ICF361'; ids: ['CINF108']
- **CINF300 — Práctica II** (id 48, período 10): texto: '( CINF100 o ICF161 ) y ( CINF108 o ICF361 ) y ( CINF109 o ICF254 ) y ( CINF110 o ICF321 o ICF353 ) y ( CINF111 o ICF321 o o o o o ICF331 o ICF353 o ICF343 ) y ( CINF112 o o o o o o o o ICF321 o ICF331 o ICF353 o ICF343 )'; ids: ['CINF100', 'CINF108', 'CINF109', 'CINF110', 'CINF111', 'CINF112']

## Ingeniería Civil en Minas

### prereq_expr menciona alternativas ("o"/equivalentes); solo se aplican los ids (16)

- **CFIS328 — Física Experimental** (id 6, período 2): texto: '( CFIS310 o FMF023 o FMF010 o FMF024 ) y ( FMMP012 o FMM013 o FMM012 o FMM035 )'; ids: ['CFIS310', 'FMMP012']
- **FMMP112 — Cálculo Diferencial** (id 7, período 2): texto: 'FMMP012 o FMM013 o FMM010 o FMM035 o FMM012'; ids: ['FMMP012']
- **TDFI103 — Base de Datos** (id 9, período 2): texto: 'TDFI102 o IND1401 o ICF122 o INS121 o AUT1302'; ids: ['TDFI102']
- **CFIS332 — Mecánica** (id 10, período 3): texto: '( ( CFIS328 o FMF023 o FMF086 ) y ( FMMP112 o FMM033 o FMM112 ) ) o ( ( JAUT101 o AUT1303 ) y ( FMMP112 o FMM112 ) )'; ids: ['CFIS328', 'FMMP112']
- **FMMP212 — Cálculo Integral** (id 11, período 3): texto: 'FMMP112 o FMM030 o FMM010 o FMM033 o FMM112'; ids: ['FMMP112']
- **TDFI104 — Compliance & Accountability** (id 14, período 3): texto: 'TDFI101 o IIN1201 o ICF121 o INS122 o ICI1201 o IMIN101 o AUT1301'; ids: ['TDFI101']
- **FMSP316 — Métodos Cuantitativos** (id 15, período 4): texto: 'FMMP212 o FMM212 o FMM214'; ids: ['FMMP212']
- **FMMP312 — Sistemas y Ecuaciones Diferenciales Lineales** (id 20, período 5): texto: '( FMMP212 o FMM133 ) o ( FMMP212 o FMM130 ) o FMM212'; ids: ['FMMP212']
- **ING129 — Inglés II** (id 24, período 5): texto: 'ING119 o ING111 o ING110 o ING116 o ING117 o CNT021 o ( ING050 y ING051 ) o ( FLG301 y FLG302 ) o ( BMA281 y BMA282 ) o ( ETU081 y ETU082 )'; ids: ['ING119']
- **ACAD101 — Taller de Innovación y Emprendimiento I** (id 25, período 6): texto: 'TDFI101 o AUT1301 o IIN1201 o ICF121 o INS122 o ICI1201 o IMIN101 o ( GEOL101 o GEO101 ) o ( BIOQ388 o BIOQ398 ) o ( LCBB110 o LCBB100 )'; ids: ['TDFI101']
- **ING239 — Inglés III** (id 28, período 6): texto: 'ING129 o ING121 o ING120 o ING216 o ING126 o ING134 o ING127 o CNT026 o ( ETU181 y ETU182 ) o ING229'; ids: ['ING129']
- **TDFI105 — Minería de Datos** (id 29, período 6): texto: '( FMSP316 o ( FMS176 y ICI2206 ) o ( FMM214 ) ) y ( TDFI103 o ICI2402 o INS128 o ( ICF132 y ICF231 ) )'; ids: ['FMSP316', 'TDFI103']
- **ACAD102 — Taller de Innovación y Emprendimiento II** (id 30, período 7): texto: 'ACAD101 o TIN1201 o ICI1201 o'; ids: ['ACAD101']
- **ING249 — Inglés IV** (id 33, período 7): texto: 'ING239 o ING210 o ING216 o ING224 o ING126 o CNT126 o ( ETU281 y ETU282 ) o ING217'; ids: ['ING239']
- **TDFI106 — Gestión de la Transformación Digital** (id 34, período 7): texto: 'TDFI104 o CEGS01 o ICF253'; ids: ['TDFI104']
- **ACAD103 — Taller de Innovación y Emprendimiento III** (id 35, período 8): texto: 'ACAD102 o IND1202 o FIC168'; ids: ['ACAD102']

## Medicina

### prereq_expr menciona alternativas ("o"/equivalentes); solo se aplican los ids (41)

- **BIOL148 — Genética y Biología Molecular Humana** (id 7, período 2): texto: 'BIOL132 o ( BIO130 y BIO131 )'; ids: ['BIOL132']
- **CFIS350 — Física Aplicada a la Medicina** (id 8, período 2): texto: 'MAT007 o FMM007'; ids: ['MAT007']
- **MEDI002 — Fundamentos de la Medicina II** (id 9, período 2): texto: 'MEDI001 o MED016'; ids: ['MEDI001']
- **MORF336 — Bases Morfológicas y Estructurales II** (id 10, período 2): texto: 'MORF335 o ( MOR330 y MOR331 y BIO320 y BIO321 )'; ids: ['MORF335']
- **SPAB305 — Bioestadística** (id 11, período 2): texto: 'MAT007 o FMM007'; ids: ['MAT007']
- **BIOL259 — Microbiología y Parasitología** (id 12, período 3): texto: 'BIOL132 o ( BIO130 y BIO131 )'; ids: ['BIOL132']
- **BIOL276 — Bases Funcionales I** (id 13, período 3): texto: '( BIOL148 o ( BIO148 y BIO242 ) ) y ( QUIM500 o ( QUI109 y QUI024 ) ) y ( CFIS350 o FMF019 )'; ids: ['BIOL148', 'CFIS350', 'QUIM500']
- **MEDI003 — Psicología Médica** (id 15, período 3): texto: 'MEDI002 o ( MED017 o MED121 o MED122 )'; ids: ['MEDI002']
- **SPAB306 — Epidemiología** (id 16, período 3): texto: 'SPAB305 o MED293'; ids: ['SPAB305']
- **BIOL376 — Bases Funcionales II** (id 17, período 4): texto: 'BIOL276 o ( BIO376 y BIO266 )'; ids: ['BIOL276']
- **ING129 — Inglés II** (id 18, período 4): texto: 'ING119 o ING111 o ING110 o ING116 o ING117 o CNT021 o ( ING050 y ING051 ) o ( FLG301 y FLG302 ) o ( BMA281 y BMA282 ) o ( ETU081 y ETU082 )'; ids: ['ING119']
- **MEDI004 — Medicina Familiar y Comunitaria** (id 19, período 4): texto: '( MEDI002 o ( MED017 o MED121 o MED122 ) ) y ( MEDI003 o MED131 )'; ids: ['MEDI002', 'MEDI003']
- **MEDI005 — Medicina y Sociedad** (id 20, período 4): texto: 'MEDI002 o ( MED017 o MED121 o MED122 )'; ids: ['MEDI002']
- **SPAB307 — Salud Pública** (id 21, período 4): texto: 'SPAB306 o MED293'; ids: ['SPAB306']
- **FARM131 — Farmacología** (id 22, período 5): texto: 'BIOL376 o ( MED294 y BIO377 )'; ids: ['BIOL376']
- **ING239 — Inglés III** (id 23, período 5): texto: 'ING129 o ING121 o ING120 o ING216 o ING126 o ING134 o ING127 o CNT026 o ( ETU181 y ETU182 ) o ING229'; ids: ['ING129']
- **MEDI006 — Semiología** (id 24, período 5): texto: '( MEDI002 o ( MED017 o MED121 o MED122 ) ) y ( BIOL376 o ( MED294 y BIO377 ) )'; ids: ['BIOL376', 'MEDI002']
- **MEDI007 — Bases Funcionales III** (id 25, período 5): texto: 'BIOL376 o ( MED294 y BIO377 )'; ids: ['BIOL376']
- **MEDI0100 — Integrador I** (id 26, período 5): texto: '( MEDI002 o ( MED017 o MED121 o MED122 ) ) y ( MEDI003 o MED131 ) y ( MEDI004 o MED292 ) y ( BIOL259 o ( BIO250 y BIO251 ) ) y ( MEDI005 o ( MED131 o HUF124 ) ) y ( BIOL376 o ( MED294 y BIO377 ) ) y ( MORF336 o ( MOR332 y MOR333 ) ) y ( SPAB307 o MED292 )'; ids: ['BIOL259', 'BIOL376', 'MEDI002', 'MEDI003', 'MEDI004', 'MEDI005', 'MORF336', 'SPAB307']
- **ING249 — Inglés IV** (id 27, período 6): texto: 'ING239 o ING210 o ING216 o ING224 o ING126 o CNT126 o ( ETU281 y ETU282 ) o ING217'; ids: ['ING239']
- **MEDI008 — Ética Médica** (id 28, período 6): texto: 'MEDI002 o ( MED017 o MED121 o MED122 )'; ids: ['MEDI002']
- **MEDI009 — Clínica Médico Quirúrgica I** (id 29, período 6): texto: 'MEDI007 o ( MED260 y MED295 y MED257 )'; ids: ['MEDI007']
- **MEDI010 — Neurología** (id 30, período 6): texto: 'MEDI007 o ( MED260 y MED295 y MED257 )'; ids: ['MEDI007']
- **MEDI011 — Métodos de Investigación** (id 31, período 6): texto: 'SPAB305 o MED293'; ids: ['SPAB305']
- **SPAB308 — Gestión en Salud** (id 32, período 6): texto: '( SPAB307 o MED292 ) y ( FARM131 o BIO288 )'; ids: ['FARM131', 'SPAB307']
- **MEDI012 — Clínica Médico Quirúrgica II** (id 33, período 7): texto: 'MEDI009 o ( MED257 y MED249 )'; ids: ['MEDI009']
- **MEDI013 — Dermatología** (id 34, período 7): texto: 'MEDI009 o ( MED257 y MED249 )'; ids: ['MEDI009']
- **MEDI014 — Otorrinolaringología** (id 35, período 7): texto: 'MEDI009 o ( MED257 y MED249 )'; ids: ['MEDI009']
- **MEDI015 — Psiquiatría** (id 36, período 7): texto: 'MEDI003 o MED131'; ids: ['MEDI003']
- **MEDI016 — Medicina Basada en la Evidencia** (id 37, período 7): texto: 'MEDI011 o ( MED278 y MED279 )'; ids: ['MEDI011']
- **MEDI017 — Clínica Médico Quirúrgica III** (id 39, período 8): texto: 'MEDI012 o ( MED296 y MED287 y MED257 )'; ids: ['MEDI012']
- **MEDI018 — Traumatología y Ortopedia** (id 40, período 8): texto: 'MEDI012 o ( MED296 y MED287 y MED257 )'; ids: ['MEDI012']
- **MEDI019 — Oftalmología** (id 41, período 8): texto: 'MEDI012 o ( MED296 y MED287 y MED257 )'; ids: ['MEDI012']
- **MEDI020 — Urología** (id 42, período 8): texto: 'MEDI012 o ( MED296 y MED287 y MED257 )'; ids: ['MEDI012']
- **MEDI021 — Medicina Legal y Forense** (id 43, período 8): texto: 'MEDI012 o ( MED296 y MED287 y MED257 )'; ids: ['MEDI012']
- **MEDI0200 — Integrador II** (id 44, período 9): texto: '( MEDI008 o ( MED258 y MED259 ) ) y ( MEDI009 o ( MED257 y MED249 ) ) y ( MEDI010 o MED244 ) y ( MEDI012 o ( MED296 y MED287 y MED257 ) ) y ( MEDI015 o MED245 ) y ( MEDI017 o ( MED296 o MED287 o MED257 ) ) y ( MEDI018 o MED296 ) y SPAB308 y MEDI016'; ids: ['MEDI008', 'MEDI009', 'MEDI010', 'MEDI012', 'MEDI015', 'MEDI016', 'MEDI017', 'MEDI018', 'SPAB308']
- **MEDI022 — Pediatría y Cirugía Infantil** (id 45, período 9): texto: 'MEDI017 o ( MED296 o MED287 o MED257 )'; ids: ['MEDI017']
- **MEDI023 — Obstetricia y Ginecología** (id 46, período 9): texto: 'MEDI017 o ( MED296 o MED287 o MED257 )'; ids: ['MEDI017']
- **MEDI024 — Internado de Pediatría** (id 47, período 10): texto: 'MEDI022 o MED297'; ids: ['MEDI022']
- **MEDI025 — Internado de Obstetricia y Ginecología** (id 48, período 10): texto: 'MEDI023 o MED298'; ids: ['MEDI023']
- **MEDI0300 — Integrador III** (id 54, período 12): texto: '( MEDI004 o MED292 ) y ( MEDI007 o ( MED260 y MED295 y MED257 ) ) ) y ( SPAB306 o MED293 ) y ( SPAB307 o MED292 ) y ( MEDI024 o MED374 ) y ( MEDI025 o MED376 ) y ( MEDI026 o MED375 ) y ( MEDI027 o MED377 )'; ids: ['MEDI004', 'MEDI007', 'MEDI024', 'MEDI025', 'MEDI026', 'MEDI027', 'SPAB306', 'SPAB307']

## Tecnología Médica

### El texto prereq_expr no coincide con los ids de prerrequisitos (21)

- **BIOL166 — Bioquímica** (id 12, período 3): texto: '( ( BIOL034 o BIO130 ) y ( QUIM002 o ( QUI001 y QUI002 ) ) y ( BIOL035 o BIO131 ) ) o ( ( QUIM001 o ( QUI001 y QUI002 ) ) y ( BIOL034 o BIOL132 o BIO034 ) ) o ( QUIM022 o ( QUI022 y QUI108 ) )'; ids: ['QUIM022']; en el texto y no en ids: ['BIOL035']
- **SPAB111 — Salud pública II** (id 28, período 6, mención BACIMET): texto: '( SPAB110 o ODT150 y ( ODOT501 o ( ODT120 y ODT122 ) ) ) o ( SPAB110 o QYF331 y ( FARM701 o QYF333 ) ) o ( SPAB110 o FMS117 y ( EFER301 o ( ENF111 y ENF117 ) ) ) o ( SPAB110 o ( NUT040 y FMS171 ) y ( NUYD034 o NUT027 ) ) o ( SPAB110 o FMS171 y ( TMED006 o TMD198 ) )'; ids: ['SPAB110']; en el texto y no en ids: ['TMED006']
- **SPAB112 — Administración y gestión en salud** (id 32, período 7, mención BACIMET): texto: '( ( SPAB111 o ODT251 ) y ( ODOT901 o ODT285 ) ) o ( ( FARM801 o QYF339 ) y ( SPAB111 o QYF331 ) ) o ( ( SPAB111 o NUT046 ) y ( NUYD043 o NUT110 ) ) o ( ( SPAB111 o TMD103 ) y ( TMED552 o TMD266 o TMED643 o TMD256 o TMED611 o TMD204 o TMED622 o TMD265 o TMED633 ) ) o ( SPAB301 o MED279 ) o ( SPAB113 o SPAB101 )'; ids: ['SPAB111', 'TMED611']; en el texto y no en ids: ['TMED552', 'TMED622', 'TMED633', 'TMED643']
- **SPAB103 — Gestión y aseguramiento de la calidad** (id 39, período 8, mención BACIMET): texto: '( SPAB112 o TMD320 ) y ( TMED714 o TMED721 o TMD293 o TMED731 o TMD337 o TMED744 o TMED752 o TMED316 )'; ids: ['SPAB112', 'TMED714']; en el texto y no en ids: ['TMED721', 'TMED731', 'TMED744', 'TMED752']
- **SPAB303 — Metodología de la investigación** (id 40, período 8, mención BACIMET): texto: '( ( SPAB111 o ODT251 ) y ( ODOT702 o ODT270 ) ) o ( ( SPAB111 o NUT046 ) y ( NUYD043 o NUT110 ) ) o ( ( SPAB111 o TMD103 ) y ( ( TMED714 o TMED721 o TMD293 o TMED731 o TMD337 o TMED744 o TMED752 ) o TMD316 ) ) o ( SPAB300 y OBST006 )'; ids: ['SPAB111', 'TMED714']; en el texto y no en ids: ['TMED721', 'TMED731', 'TMED744', 'TMED752']
- **SPAB111 — Salud pública II** (id 58, período 6, mención IFIME): texto: '( SPAB110 o ODT150 y ( ODOT501 o ( ODT120 y ODT122 ) ) ) o ( SPAB110 o QYF331 y ( FARM701 o QYF333 ) ) o ( SPAB110 o FMS117 y ( EFER301 o ( ENF111 y ENF117 ) ) ) o ( SPAB110 o ( NUT040 y FMS171 ) y ( NUYD034 o NUT027 ) ) o ( SPAB110 o FMS171 y ( TMED006 o TMD198 ) )'; ids: ['SPAB110']; en el texto y no en ids: ['TMED006']
- **SPAB112 — Administración y gestión en salud** (id 63, período 7, mención IFIME): texto: '( ( SPAB111 o ODT251 ) y ( ODOT901 o ODT285 ) ) o ( ( FARM801 o QYF339 ) y ( SPAB111 o QYF331 ) ) o ( ( SPAB111 o NUT046 ) y ( NUYD043 o NUT110 ) ) o ( ( SPAB111 o TMD103 ) y ( TMED552 o TMD266 o TMED643 o TMD256 o TMED611 o TMD204 o TMED622 o TMD265 o TMED633 ) ) o ( SPAB301 o MED279 ) o ( SPAB113 o SPAB101 )'; ids: ['SPAB111', 'TMED633']; en el texto y no en ids: ['TMED552', 'TMED611', 'TMED622', 'TMED643']
- **SPAB103 — Gestión y aseguramiento de la calidad** (id 70, período 8, mención IFIME): texto: '( SPAB112 o TMD320 ) y ( TMED714 o TMED721 o TMD293 o TMED731 o TMD337 o TMED744 o TMED752 o TMED316 )'; ids: ['SPAB112', 'TMED731']; en el texto y no en ids: ['TMED714', 'TMED721', 'TMED744', 'TMED752']
- **SPAB303 — Metodología de la investigación** (id 71, período 8, mención IFIME): texto: '( ( SPAB111 o ODT251 ) y ( ODOT702 o ODT270 ) ) o ( ( SPAB111 o NUT046 ) y ( NUYD043 o NUT110 ) ) o ( ( SPAB111 o TMD103 ) y ( ( TMED714 o TMED721 o TMD293 o TMED731 o TMD337 o TMED744 o TMED752 ) o TMD316 ) ) o ( SPAB300 y OBST006 )'; ids: ['SPAB111', 'TMED731']; en el texto y no en ids: ['TMED714', 'TMED721', 'TMED744', 'TMED752']
- **SPAB111 — Salud pública II** (id 88, período 6, mención MORFO): texto: '( SPAB110 o ODT150 y ( ODOT501 o ( ODT120 y ODT122 ) ) ) o ( SPAB110 o QYF331 y ( FARM701 o QYF333 ) ) o ( SPAB110 o FMS117 y ( EFER301 o ( ENF111 y ENF117 ) ) ) o ( SPAB110 o ( NUT040 y FMS171 ) y ( NUYD034 o NUT027 ) ) o ( SPAB110 o FMS171 y ( TMED006 o TMD198 ) )'; ids: ['SPAB110']; en el texto y no en ids: ['TMED006']
- **SPAB112 — Administración y gestión en salud** (id 92, período 7, mención MORFO): texto: '( ( SPAB111 o ODT251 ) y ( ODOT901 o ODT285 ) ) o ( ( FARM801 o QYF339 ) y ( SPAB111 o QYF331 ) ) o ( ( SPAB111 o NUT046 ) y ( NUYD043 o NUT110 ) ) o ( ( SPAB111 o TMD103 ) y ( TMED552 o TMD266 o TMED643 o TMD256 o TMED611 o TMD204 o TMED622 o TMD265 o TMED633 ) ) o ( SPAB301 o MED279 ) o ( SPAB113 o SPAB101 )'; ids: ['SPAB111', 'TMED643']; en el texto y no en ids: ['TMED552', 'TMED611', 'TMED622', 'TMED633']
- **SPAB103 — Gestión y aseguramiento de la calidad** (id 98, período 8, mención MORFO): texto: '( SPAB112 o TMD320 ) y ( TMED714 o TMED721 o TMD293 o TMED731 o TMD337 o TMED744 o TMED752 o TMED316 )'; ids: ['SPAB112', 'TMED744']; en el texto y no en ids: ['TMED714', 'TMED721', 'TMED731', 'TMED752']
- **SPAB303 — Metodología de la investigación** (id 99, período 8, mención MORFO): texto: '( ( SPAB111 o ODT251 ) y ( ODOT702 o ODT270 ) ) o ( ( SPAB111 o NUT046 ) y ( NUYD043 o NUT110 ) ) o ( ( SPAB111 o TMD103 ) y ( ( TMED714 o TMED721 o TMD293 o TMED731 o TMD337 o TMED744 o TMED752 ) o TMD316 ) ) o ( SPAB300 y OBST006 )'; ids: ['SPAB111', 'TMED744']; en el texto y no en ids: ['TMED714', 'TMED721', 'TMED731', 'TMED752']
- **SPAB111 — Salud pública II** (id 118, período 6, mención OFTA): texto: '( SPAB110 o ODT150 y ( ODOT501 o ( ODT120 y ODT122 ) ) ) o ( SPAB110 o QYF331 y ( FARM701 o QYF333 ) ) o ( SPAB110 o FMS117 y ( EFER301 o ( ENF111 y ENF117 ) ) ) o ( SPAB110 o ( NUT040 y FMS171 ) y ( NUYD034 o NUT027 ) ) o ( SPAB110 o FMS171 y ( TMED006 o TMD198 ) )'; ids: ['SPAB110']; en el texto y no en ids: ['TMED006']
- **SPAB112 — Administración y gestión en salud** (id 123, período 7, mención OFTA): texto: '( ( SPAB111 o ODT251 ) y ( ODOT901 o ODT285 ) ) o ( ( FARM801 o QYF339 ) y ( SPAB111 o QYF331 ) ) ) o ( ( SPAB111 o NUT046 ) y ( NUYD043 o NUT110 ) ) o ( ( SPAB111 o TMD103 ) y ( TMED552 o TMD266 o TMED643 o TMD256 o TMED611 o TMD204 o TMED622 o TMD265 o TMED633 ) ) o ( SPAB301 o MED279 ) o ( SPAB113 o SPAB101 )'; ids: ['SPAB111', 'TMED622']; en el texto y no en ids: ['TMED552', 'TMED611', 'TMED633', 'TMED643']
- **SPAB103 — Gestión y aseguramiento de la calidad** (id 129, período 8, mención OFTA): texto: '( SPAB112 o TMD320 ) y ( TMED714 o TMED721 o TMD293 o TMED731 o TMD337 o TMED744 o TMED752 o TMED316 )'; ids: ['SPAB112', 'TMED721']; en el texto y no en ids: ['TMED714', 'TMED731', 'TMED744', 'TMED752']
- **SPAB303 — Metodología de la investigación** (id 130, período 8, mención OFTA): texto: '( ( SPAB111 o ODT251 ) y ( ODOT702 o ODT270 ) ) o ( ( SPAB111 o NUT046 ) y ( NUYD043 o NUT110 ) ) o ( ( SPAB111 o TMD103 ) y ( ( TMED714 o TMED721 o TMD293 o TMED731 o TMD337 o TMED744 o TMED752 ) o TMD316 ) ) o ( SPAB300 y OBST006 )'; ids: ['SPAB111', 'TMED721']; en el texto y no en ids: ['TMED714', 'TMED731', 'TMED744', 'TMED752']
- **SPAB111 — Salud pública II** (id 150, período 6, mención OTORRINO): texto: '( SPAB110 o ODT150 y ( ODOT501 o ( ODT120 y ODT122 ) ) ) o ( SPAB110 o QYF331 y ( FARM701 o QYF333 ) ) o ( SPAB110 o FMS117 y ( EFER301 o ( ENF111 y ENF117 ) ) ) o ( SPAB110 o ( NUT040 y FMS171 ) y ( NUYD034 o NUT027 ) ) o ( SPAB110 o FMS171 y ( TMED006 o TMD198 ) )'; ids: ['SPAB110']; en el texto y no en ids: ['TMED006']
- **SPAB112 — Administración y gestión en salud** (id 153, período 7, mención OTORRINO): texto: '( ( SPAB111 o ODT251 ) y ( ODOT901 o ODT285 ) ) o ( ( FARM801 o QYF339 ) y ( SPAB111 o QYF331 ) ) o ( ( SPAB111 o NUT046 ) y ( NUYD043 o NUT110 ) ) o ( ( SPAB111 o TMD103 ) y ( TMED552 o TMD266 o TMED643 o TMD256 o TMED611 o TMD204 o TMED622 o TMD265 o TMED633 ) ) o ( SPAB301 o MED279 ) o ( SPAB113 o SPAB101 )'; ids: ['SPAB111', 'TMED552']; en el texto y no en ids: ['TMED611', 'TMED622', 'TMED633', 'TMED643']
- **SPAB103 — Gestión y aseguramiento de la calidad** (id 158, período 8, mención OTORRINO): texto: '( SPAB112 o TMD320 ) y ( TMED714 o TMED721 o TMD293 o TMED731 o TMD337 o TMED744 o TMED752 o TMED316 )'; ids: ['SPAB112', 'TMED752']; en el texto y no en ids: ['TMED714', 'TMED721', 'TMED731', 'TMED744']
- **SPAB303 — Metodología de la investigación** (id 159, período 8, mención OTORRINO): texto: '( ( SPAB111 o ODT251 ) y ( ODOT702 o ODT270 ) ) o ( ( SPAB111 o NUT046 ) y ( NUYD043 o NUT110 ) ) o ( ( SPAB111 o TMD103 ) y ( ( TMED714 o TMED721 o TMD293 o TMED731 o TMD337 o TMED744 o TMED752 ) o TMD316 ) ) o ( SPAB300 y OBST006 )'; ids: ['SPAB111', 'TMED752']; en el texto y no en ids: ['TMED714', 'TMED721', 'TMED731', 'TMED744']

### prereq_expr menciona alternativas ("o"/equivalentes); solo se aplican los ids (123)

- **CFIS020 — Física general** (id 8, período 2): texto: 'FMMP101 o ( FMM032 y FMM134 )'; ids: ['FMMP101']
- **MORF122 — Histoembriología** (id 10, período 2): texto: '( MORF010 o ( BIO010 y BIO013 ) ) y ( BIOL130 o BIO034 )'; ids: ['BIOL130', 'MORF010']
- **QUIM022 — Química orgánica** (id 11, período 2): texto: 'QUIM102 o QUI102'; ids: ['QUIM102']
- **BIOL272 — Fisiología humana** (id 13, período 3): texto: '( MORF014 o BIO014 ) o ( MORF122 o ( BIO122 y BIO125 ) )'; ids: ['MORF122']
- **ING129 — Inglés II** (id 15, período 3): texto: 'ING119 o ING111 o ING110 o ING116 o ING117 o CNT021 o ( ING050 y ING051 ) o ( FLG301 y FLG302 ) o ( BMA281 y BMA282 ) o ( ETU081 y ETU082 )'; ids: ['ING119']
- **TMED003 — Bioética** (id 16, período 3): texto: '( TMED001 o TMD001 )'; ids: ['TMED001']
- **TMED004 — Infectología** (id 17, período 3): texto: '( BIOL130 o BIO034 ) y ( BIOL035 o BIO035 )'; ids: ['BIOL035', 'BIOL130']
- **FARM171 — Farmacología general** (id 18, período 4, mención BACIMET): texto: 'BIOL166 o BIO268'; ids: ['BIOL166']
- **ING239 — Inglés III** (id 19, período 4, mención BACIMET): texto: 'ING129 o ING121 o ING120 o ING216 o ING126 o ING134 o ING127 o CNT026 o ( ETU181 y ETU182 ) o ING229'; ids: ['ING129']
- **TMED005 — Fisiopatología** (id 20, período 4, mención BACIMET): texto: 'BIOL272 o ( BIO372 y BIO171 )'; ids: ['BIOL272']
- **TMED411 — Parasitología** (id 21, período 4, mención BACIMET): texto: '( CFIS020 o FMF020 ) y ( BIOL272 o ( BIO372 y BIO171 ) ) y ( BIOL166 o BIO268 ) y ( TMED003 o ( TMD020 y TMD250 ) ) y ( TMED004 o BIO058 ) y ING129'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **TMED412 — Inmunología diagnóstica** (id 22, período 4, mención BACIMET): texto: '( CFIS020 o FMF020 ) y ( BIOL272 o ( BIO372 y BIO171 ) ) y ( BIOL166 o BIO268 ) y ( TMED003 o ( TMD020 y TMD250 ) ) y ( TMED004 o BIO058 ) y ING129'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **ING249 — Inglés IV** (id 23, período 5, mención BACIMET): texto: 'ING239 o ING210 o ING216 o ING224 o ING126 o CNT126 o ( ETU281 y ETU282 ) o ING217'; ids: ['ING239']
- **SPAB110 — Salud pública I** (id 24, período 5, mención BACIMET): texto: '( ODOT602 o ODT116 ) o ( FARM401 o QYF181 ) o ( ( EFER203 o ENF012 ) y ( FMMP001 o MAT002 o ( FMM003 o ENF040 ) ) ) o ( ( FMMP005 o FMM002 ) y ( NUYD011 o NUT012 ) ) o ( TMED005 o TMD110 ) o ( FMMP007 o FMM007 )'; ids: ['TMED005']
- **TMED006 — Procedimientos de tecnología médica y bioseguridad** (id 25, período 5, mención BACIMET): texto: 'FARM171 o BIO184'; ids: ['FARM171']
- **TMED511 — Microbiología I** (id 26, período 5, mención BACIMET): texto: '( TMED411 o TMD225 ) y ( FARM171 o BIO184 )'; ids: ['FARM171', 'TMED411']
- **TMED512 — Hematología I** (id 27, período 5, mención BACIMET): texto: '( TMED412 o ( BIO286 y TMD255 ) ) y ( TMED005 o TMD110 )'; ids: ['TMED005', 'TMED412']
- **TMED611 — Bioquímica clínica I** (id 29, período 6, mención BACIMET): texto: 'TMED412 o ( BIO286 y TMD255 )'; ids: ['TMED412']
- **TMED612 — Microbiología II** (id 30, período 6, mención BACIMET): texto: 'TMED511 o TMD329'; ids: ['TMED511']
- **TMED613 — Hematología II** (id 31, período 6, mención BACIMET): texto: 'TMED512 o TMD233'; ids: ['TMED512']
- **TMED002 — Educación en salud** (id 33, período 7, mención BACIMET): texto: 'SPAB111 o TMD103'; ids: ['SPAB111']
- **TMED711 — Biología molecular** (id 34, período 7, mención BACIMET): texto: 'TMED611 o TMD204'; ids: ['TMED611']
- **TMED712 — Inmunohematología** (id 35, período 7, mención BACIMET): texto: 'TMED512 o TMD233'; ids: ['TMED512']
- **TMED713 — Bioquímica clínica II** (id 36, período 7, mención BACIMET): texto: 'TMED611 o TMD204'; ids: ['TMED611']
- **TMED714 — Integrador I: caso clínico BACIMET** (id 37, período 7, mención BACIMET): texto: '( TMED613 o TMD301 ) y ( TMED612 o TMD329 ) y ( TMED611 o TMD204 )'; ids: ['TMED611', 'TMED612', 'TMED613']
- **TMED811 — Medicina transfusional** (id 41, período 8, mención BACIMET): texto: '( TMED712 o TMD325 ) y TMED714'; ids: ['TMED712', 'TMED714']
- **TMED812 — Diagnóstico molecular clínico** (id 42, período 8, mención BACIMET): texto: 'TMED711 y TMED714 y ( TMED713 o TMD231 )'; ids: ['TMED711', 'TMED713', 'TMED714']
- **TMED911 — Seminario de investigación BACIMET** (id 44, período 9, mención BACIMET): texto: 'SPAB303 y SPAB103 y ( TMED811 o TMD325 ) y TMED812'; ids: ['SPAB103', 'SPAB303', 'TMED811', 'TMED812']
- **TMED912 — Integrador II: internado clínico BACIMET** (id 45, período 10, mención BACIMET): texto: 'SPAB303 y SPAB103 y ( TMED811 o TMD325 ) y TMED812'; ids: ['SPAB103', 'SPAB303', 'TMED811', 'TMED812']
- **FARM171 — Farmacología general** (id 46, período 4, mención IFIME): texto: 'BIOL166 o BIO268'; ids: ['BIOL166']
- **ING239 — Inglés III** (id 47, período 4, mención IFIME): texto: 'ING129 o ING121 o ING120 o ING216 o ING126 o ING134 o ING127 o CNT026 o ( ETU181 y ETU182 ) o ING229'; ids: ['ING129']
- **TMED005 — Fisiopatología** (id 48, período 4, mención IFIME): texto: 'BIOL272 o ( BIO372 y BIO171 )'; ids: ['BIOL272']
- **TMED431 — Protección radiológica** (id 49, período 4, mención IFIME): texto: '( BIOL272 o ( BIO372 y BIO171 ) ) y ( BIOL166 o BIO268 ) y ( TMED003 o ( TMD020 y TMD250 ) ) y ( TMED004 o BIO058 ) y ING129 y ( CFIS020 o FMF020 )'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **TMED432 — Radiodiagnóstico I** (id 50, período 4, mención IFIME): texto: '( BIOL272 o ( BIO372 y BIO171 ) ) y ( BIOL166 o BIO268 ) y ( TMED003 o ( TMD020 y TMD250 ) ) y ( TMED004 o BIO058 ) y ING129 y ( CFIS020 o FMF020 )'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **TMED433 — Física electromagnética** (id 51, período 4, mención IFIME): texto: '( BIOL272 o ( BIO372 y BIO171 ) ) y ( BIOL166 o BIO268 ) y ( TMED003 o ( TMD020 y TMD250 ) ) y ( TMED004 o BIO058 ) y ING129 y ( CFIS020 o FMF020 )'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **ING249 — Inglés IV** (id 52, período 5, mención IFIME): texto: 'ING239 o ING210 o ING216 o ING224 o ING126 o CNT126 o ( ETU281 y ETU282 ) o ING217'; ids: ['ING239']
- **SPAB110 — Salud pública I** (id 53, período 5, mención IFIME): texto: '( ODOT602 o ODT116 ) o ( FARM401 o QYF181 ) o ( ( EFER203 o ENF012 ) y ( FMMP001 o MAT002 o ( FMM003 o ENF040 ) ) ) ) o ( ( FMMP005 o FMM002 ) y ( NUYD011 o NUT012 ) ) o ( TMED005 o TMD110 ) o ( FMMP007 o FMM007 )'; ids: ['TMED005']
- **TMED006 — Procedimientos de tecnología médica y bioseguridad** (id 54, período 5, mención IFIME): texto: 'FARM171 o BIO184'; ids: ['FARM171']
- **TMED531 — Física moderna** (id 55, período 5, mención IFIME): texto: '( TMED431 o TMD223 ) y ( TMED433 o TMD200 )'; ids: ['TMED431', 'TMED433']
- **TMED532 — Radiodiagnóstico II** (id 56, período 5, mención IFIME): texto: '( TMED432 o TMD222 ) y ( FARM171 o BIO184 )'; ids: ['FARM171', 'TMED432']
- **TMED533 — Anatomía imagenológica** (id 57, período 5, mención IFIME): texto: '( TMED432 o TMD222 ) y ( TMED005 o TMD110 )'; ids: ['TMED005', 'TMED432']
- **TMED632 — Tomografía computada** (id 60, período 6, mención IFIME): texto: '( TMED532 o TMD249 ) y ( TMED533 o ( TMD251 y TMD282 ) )'; ids: ['TMED532', 'TMED533']
- **TMED633 — Sistema informático en radiología** (id 61, período 6, mención IFIME): texto: 'TMED532 o TMD249'; ids: ['TMED532']
- **TMED634 — Patología imagenológica** (id 62, período 6, mención IFIME): texto: '( TMED532 o TMD249 ) y ( TMED533 o ( TMD251 y TMD282 ) )'; ids: ['TMED532', 'TMED533']
- **TMED002 — Educación en salud** (id 64, período 7, mención IFIME): texto: 'SPAB111 o TMD103'; ids: ['SPAB111']
- **TMED731 — Medicina nuclear** (id 65, período 7, mención IFIME): texto: 'TMED631 o TMD264'; ids: ['TMED631']
- **TMED732 — Intervencionismo endovascular** (id 66, período 7, mención IFIME): texto: 'TMED634 o ( TMD251 y TMD282 )'; ids: ['TMED634']
- **TMED733 — Integrador I: caso clínico IFIME** (id 67, período 7, mención IFIME): texto: '( TMED632 o TMD297 ) y TMED633 y ( TMED634 o ( TMD251 y TMD282 ) )'; ids: ['TMED632', 'TMED633', 'TMED634']
- **TMED734 — Ultrasonido** (id 68, período 7, mención IFIME): texto: 'TMED634 o ( TMD251 y TMD282 )'; ids: ['TMED634']
- **TMED831 — Radioterapia** (id 72, período 8, mención IFIME): texto: '( TMED732 o TMD298 ) y TMED733'; ids: ['TMED732', 'TMED733']
- **TMED832 — Resonancia magnética** (id 73, período 8, mención IFIME): texto: 'TMED733 y ( TMED734 o TMD298 )'; ids: ['TMED733', 'TMED734']
- **TMED931 — Seminario de investigación IFIME** (id 75, período 9, mención IFIME): texto: 'SPAB303 y SPAB103 y ( TMED831 o TMD339 ) y ( TMED832 o TMD297 )'; ids: ['SPAB103', 'SPAB303', 'TMED831', 'TMED832']
- **TMED932 — Integrador II: internado clínico IFIME** (id 76, período 10, mención IFIME): texto: 'SPAB303 y SPAB103 y ( TMED831 o TMD339 ) y ( TMED832 o TMD297 )'; ids: ['SPAB103', 'SPAB303', 'TMED831', 'TMED832']
- **FARM171 — Farmacología general** (id 77, período 4, mención MORFO): texto: 'BIOL166 o BIO268'; ids: ['BIOL166']
- **ING239 — Inglés III** (id 78, período 4, mención MORFO): texto: 'ING129 o ING121 o ING120 o ING216 o ING126 o ING134 o ING127 o CNT026 o ( ETU181 y ETU182 ) o ING229'; ids: ['ING129']
- **TMED005 — Fisiopatología** (id 79, período 4, mención MORFO): texto: 'BIOL272 o ( BIO372 y BIO171 )'; ids: ['BIOL272']
- **TMED441 — Técnicas histológicas y citológicas I** (id 80, período 4, mención MORFO): texto: '( BIOL272 o ( BIO372 y BIO171 ) ) y ( BIOL166 o BIO268 ) y ( TMED003 o ( TMD020 y TMD250 ) ) y ( TMED004 o BIO058 ) y ING129 y ( CFIS020 o FMF020 )'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **TMED442 — Histología clínica** (id 81, período 4, mención MORFO): texto: '( BIOL272 o ( BIO372 y BIO171 ) ) y ( BIOL166 o BIO268 ) y ( TMED003 o ( TMD020 y TMD250 ) ) y ( TMED004 o BIO058 ) y ING129 y ( CFIS020 o FMF020 )'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **ING249 — Inglés IV** (id 82, período 5, mención MORFO): texto: 'ING239 o ING210 o ING216 o ING224 o ING126 o CNT126 o ( ETU281 y ETU282 ) o ING217'; ids: ['ING239']
- **SPAB110 — Salud pública I** (id 83, período 5, mención MORFO): texto: '( ODOT602 o ODT116 ) o ( FARM401 o QYF181 ) o ( ( EFER203 o ENF012 ) y ( FMMP001 o MAT002 o ( FMM003 o ENF040 ) ) ) o ( ( FMMP005 o FMM002 ) y ( NUYD011 o NUT012 ) ) o ( TMED005 o TMD110 ) o ( FMMP007 o FMM007 )'; ids: ['TMED005']
- **TMED006 — Procedimientos de tecnología médica y bioseguridad** (id 84, período 5, mención MORFO): texto: 'FARM171 o BIO184'; ids: ['FARM171']
- **TMED541 — Técnicas histológicas y citológicas II** (id 85, período 5, mención MORFO): texto: 'TMED441 o TMD197'; ids: ['TMED441']
- **TMED542 — Anatomía patológica I** (id 86, período 5, mención MORFO): texto: '( TMED442 o TMD199 ) y ( TMED005 o TMD110 )'; ids: ['TMED005', 'TMED442']
- **TMED641 — Biología molecular y genética** (id 89, período 6, mención MORFO): texto: 'TMED541 o TMD197'; ids: ['TMED541']
- **TMED642 — Diagnóstico histoquímico** (id 90, período 6, mención MORFO): texto: '( TMED541 o TMD197 ) y ( TMED542 o TMD256 )'; ids: ['TMED541', 'TMED542']
- **TMED643 — Anatomía patológica II** (id 91, período 6, mención MORFO): texto: 'TMED542 o TMD256'; ids: ['TMED542']
- **TMED002 — Educación en salud** (id 93, período 7, mención MORFO): texto: 'SPAB111 o TMD103'; ids: ['SPAB111']
- **TMED741 — Fundamentos de citogénetica** (id 94, período 7, mención MORFO): texto: 'TMED641 o BIO040'; ids: ['TMED641']
- **TMED742 — Diagnóstico inmunohistoquímico** (id 95, período 7, mención MORFO): texto: '( TMED642 o TMD248 ) y ( TMED643 o TMD256 )'; ids: ['TMED642', 'TMED643']
- **TMED743 — Citopatología I** (id 96, período 7, mención MORFO): texto: 'TMED643 o TMD256'; ids: ['TMED643']
- **TMED744 — Integrador I: caso clínico MORFO** (id 97, período 7, mención MORFO): texto: '( TMED641 o BIO040 ) y ( TMED642 o TMD248 ) y ( TMED643 o TMD256 )'; ids: ['TMED641', 'TMED642', 'TMED643']
- **TMED841 — Diagnóstico citogenético** (id 100, período 8, mención MORFO): texto: '( TMED741 o TMD294 ) y TMED744'; ids: ['TMED741', 'TMED744']
- **TMED842 — Diagnóstico molecular** (id 101, período 8, mención MORFO): texto: '( TMED741 o TMD294 ) y ( TMED742 o TMD327 ) y TMED744'; ids: ['TMED741', 'TMED742', 'TMED744']
- **TMED843 — Citopatología II** (id 102, período 8, mención MORFO): texto: '( TMED743 o TMD321 ) y TMED744'; ids: ['TMED743', 'TMED744']
- **TMED941 — Seminario de investigación MORFO** (id 104, período 9, mención MORFO): texto: 'SPAB303 y SPAB103 y ( TMED841 o TMD326 ) y TMED842 y ( TMED843 o TMD322 )'; ids: ['SPAB103', 'SPAB303', 'TMED841', 'TMED842', 'TMED843']
- **TMED942 — Integrador II: internado clínico MORFO** (id 105, período 10, mención MORFO): texto: 'SPAB303 y SPAB103 y ( TMED841 o TMD326 ) y TMED842 y ( TMED842 o TMD322 )'; ids: ['SPAB103', 'SPAB303', 'TMED841', 'TMED842']
- **FARM171 — Farmacología general** (id 106, período 4, mención OFTA): texto: 'BIOL166 o BIO268'; ids: ['BIOL166']
- **ING239 — Inglés III** (id 107, período 4, mención OFTA): texto: 'ING129 o ING121 o ING120 o ING216 o ING126 o ING134 o ING127 o CNT026 o ( ETU181 y ETU182 ) o ING229'; ids: ['ING129']
- **TMED005 — Fisiopatología** (id 108, período 4, mención OFTA): texto: 'BIOL272 o ( BIO372 y BIO171 )'; ids: ['BIOL272']
- **TMED421 — Morfofisiología ocular** (id 109, período 4, mención OFTA): texto: '( BIOL272 o ( BIO372 y BIO171 ) ) y ( BIOL166 o BIO268 ) y ( TMED003 o ( TMD020 y TMD250 ) ) y ( TMED004 o BIO058 ) y ING129 y ( CFIS020 o FMF020 )'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **TMED422 — Oftalmología general** (id 110, período 4, mención OFTA): texto: '( BIOL272 o ( BIO372 y BIO171 ) ) y ( BIOL166 o BIO268 ) y ( TMED003 o ( TMD020 y TMD250 ) ) y ( TMED004 o BIO058 ) y ING129 y ( CFIS020 o FMF020 )'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **TMED423 — Biofísica óptica** (id 111, período 4, mención OFTA): texto: '( BIOL272 o ( BIO372 y BIO171 ) ) y ( BIOL166 o BIO268 ) y ( TMED003 o ( TMD020 y TMD250 ) ) y ( TMED004 o BIO058 ) y ING129 y ( CFIS020 o FMF020 )'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **ING249 — Inglés IV** (id 112, período 5, mención OFTA): texto: 'ING239 o ING210 o ING216 o ING224 o ING126 o CNT126 o ( ETU281 y ETU282 ) o ING217'; ids: ['ING239']
- **SPAB110 — Salud pública I** (id 113, período 5, mención OFTA): texto: '( ODOT602 o ODT116 ) o ( FARM401 o QYF181 ) o ( ( EFER203 o ENF012 ) y ( FMMP001 o MAT002 o ( FMM003 o ENF040 ) ) ) o ( ( FMMP005 o FMM002 ) y ( NUYD011 o NUT012 ) ) o ( TMED005 o TMD110 ) o ( FMMP007 o FMM007 )'; ids: ['TMED005']
- **TMED006 — Procedimientos de tecnología médica y bioseguridad** (id 114, período 5, mención OFTA): texto: 'FARM171 o BIO184'; ids: ['FARM171']
- **TMED521 — Morfofisiopatología ocular** (id 115, período 5, mención OFTA): texto: '( TMED005 o TMD110 ) y ( TMED421 o TMD193 )'; ids: ['TMED005', 'TMED421']
- **TMED522 — Exploración del sistema visual** (id 116, período 5, mención OFTA): texto: '( TMED422 o TMD195 ) y ( TMED423 o TMD192 )'; ids: ['TMED422', 'TMED423']
- **TMED523 — Oftalmofarmacología** (id 117, período 5, mención OFTA): texto: '( FARM171 o BIO184 ) y ( TMED421 o TMD193 )'; ids: ['FARM171', 'TMED421']
- **TMED621 — Estudio del campo visual** (id 119, período 6, mención OFTA): texto: '( TMED521 o TMD258 ) y ( TMED523 o TMD263 )'; ids: ['TMED521', 'TMED523']
- **TMED622 — Estrabismo y ortóptica** (id 120, período 6, mención OFTA): texto: 'TMED522 o TMD194'; ids: ['TMED522']
- **TMED623 — Optometría I** (id 121, período 6, mención OFTA): texto: 'TMED521 o TMD258'; ids: ['TMED521']
- **TMED002 — Educación en salud** (id 124, período 7, mención OFTA): texto: 'SPAB111 o TMD103'; ids: ['SPAB111']
- **TMED721 — Neurooftalmología** (id 125, período 7, mención OFTA): texto: '( TMED621 o TMD268 ) y ( TMED622 o TMD265 )'; ids: ['TMED621', 'TMED622']
- **TMED722 — Optometría II** (id 126, período 7, mención OFTA): texto: 'TMED623 o TMD295'; ids: ['TMED623']
- **TMED723 — Procedimientos de apoyo en cirugía refractiva** (id 127, período 7, mención OFTA): texto: 'TMED623 o TMD295'; ids: ['TMED623']
- **TMED724 — Integrador I: atención primaria en oftalmología** (id 128, período 7, mención OFTA): texto: '( TMED623 o TMD295 ) y ( TMED622 o TMD265 ) y ( TMED621 o TMD268 )'; ids: ['TMED621', 'TMED622', 'TMED623']
- **TMED821 — Formulación y evaluación de proyectos en oftalmología** (id 131, período 8, mención OFTA): texto: 'SPAB112 o TMD320'; ids: ['SPAB112']
- **TMED823 — Imagenología ocular** (id 133, período 8, mención OFTA): texto: '( TMED723 o ( TMD323 y TMD296 ) ) y TMED724'; ids: ['TMED723', 'TMED724']
- **TMED921 — Seminario de investigación OFTA** (id 135, período 9, mención OFTA): texto: 'SPAB303 y SPAB103 y TMED821 y ( TMED822 o TMD356 ) y ( TMED823 o TMD357 )'; ids: ['SPAB103', 'SPAB303', 'TMED821', 'TMED822', 'TMED823']
- **TMED922 — Integrador II: internado clínico OFTA** (id 136, período 10, mención OFTA): texto: 'SPAB303 y SPAB103 y TMED821 y ( TMED822 o TMD356 ) y ( TMED823 o TMD357 )'; ids: ['SPAB103', 'SPAB303', 'TMED821', 'TMED822', 'TMED823']
- **FARM171 — Farmacología general** (id 137, período 4, mención OTORRINO): texto: 'BIOL166 o BIO268'; ids: ['BIOL166']
- **ING239 — Inglés III** (id 138, período 4, mención OTORRINO): texto: 'ING129 o ING121 o ING120 o ING216 o ING126 o ING134 o ING127 o CNT026 o ( ETU181 y ETU182 ) o ING229'; ids: ['ING129']
- **TMED005 — Fisiopatología** (id 139, período 4, mención OTORRINO): texto: 'BIOL272 o ( BIO372 y BIO171 )'; ids: ['BIOL272']
- **TMED451 — Psicoacústica y fonología** (id 140, período 4, mención OTORRINO): texto: '( BIOL272 o ( BIO372 y BIO171 ) ) y ( BIOL166 o BIO268 ) y ( TMED003 o ( TMD020 y TMD250 ) ) y ( TMED004 o BIO058 ) y ING129 y ( CFIS020 o FMF020 )'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **TMED452 — Neuroanatomía otorrinolaringológica** (id 141, período 4, mención OTORRINO): texto: '( BIOL272 o ( BIO372 y BIO171 ) ) y ( BIOL166 o BIO268 ) y ( TMED003 o ( TMD020 y TMD250 ) ) y ( TMED004 o BIO058 ) y ING129 y ( CFIS020 o FMF020 )'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **TMED453 — Lengua de señas** (id 142, período 4, mención OTORRINO): texto: '( BIOL272 o ( BIO372 y BIO171 ) ) y ( BIOL166 o BIO268 ) y ( TMED003 o ( TMD020 y TMD250 ) ) y ( TMED004 o BIO058 ) y ING129 y ( CFIS020 o FMF020 )'; ids: ['BIOL166', 'BIOL272', 'CFIS020', 'ING129', 'TMED003', 'TMED004']
- **ING249 — Inglés IV** (id 143, período 5, mención OTORRINO): texto: 'ING239 o ING210 o ING216 o ING224 o ING126 o CNT126 o ( ETU281 y ETU282 ) o ING217'; ids: ['ING239']
- **SPAB110 — Salud pública I** (id 144, período 5, mención OTORRINO): texto: '( ODOT602 o ODT116 ) o ( FARM401 o QYF181 ) o ( ( EFER203 o ENF012 ) y ( FMMP001 o MAT002 o ( FMM003 o ENF040 ) ) ) o ( ( FMMP005 o FMM002 ) y ( NUYD011 o NUT012 ) ) o ( TMED005 o TMD110 ) o ( FMMP007 o FMM007 )'; ids: ['TMED005']
- **TMED006 — Procedimientos de tecnología médica y bioseguridad** (id 145, período 5, mención OTORRINO): texto: 'FARM171 o BIO184'; ids: ['FARM171']
- **TMED551 — Morfofisiopatología orl** (id 146, período 5, mención OTORRINO): texto: '( TMED005 o TMD110 ) y ( TMED451 o FMF120 )'; ids: ['TMED005', 'TMED451']
- **TMED552 — Función nasal** (id 147, período 5, mención OTORRINO): texto: 'TMED005 o TMD110'; ids: ['TMED005']
- **TMED553 — Neurofisiología aplicada a la orl** (id 148, período 5, mención OTORRINO): texto: 'TMED452 o TMD196'; ids: ['TMED452']
- **TMED651 — Audiología básica** (id 151, período 6, mención OTORRINO): texto: '( TMED551 o TMD202 ) y ( TMED553 o TMD196 ) y ( TMED453 o TMD267 )'; ids: ['TMED453', 'TMED551', 'TMED553']
- **TMED652 — Otoneurología I** (id 152, período 6, mención OTORRINO): texto: '( TMED551 o TMD202 ) y ( TMED553 o TMD196 )'; ids: ['TMED551', 'TMED553']
- **TMED002 — Educación en salud** (id 154, período 7, mención OTORRINO): texto: 'SPAB111 o TMD103'; ids: ['SPAB111']
- **TMED751 — Audiología avanzada y electrofisiología** (id 155, período 7, mención OTORRINO): texto: 'TMED651 o ( TMD252 y TMD253 )'; ids: ['TMED651']
- **TMED752 — Otoneurología II** (id 156, período 7, mención OTORRINO): texto: '( TMED651 o ( TMD252 y TMD253 ) ) y ( TMED652 o ( TMD202 y TMD316 ) )'; ids: ['TMED651', 'TMED652']
- **TMED753 — Integrador I: caso clínico OTO** (id 157, período 7, mención OTORRINO): texto: '( TMED651 o ( TMD252 y TMD253 ) ) y ( TMED652 o ( TMD202 y TMD316 ) )'; ids: ['TMED651', 'TMED652']
- **TMED851 — Salud ocupacional** (id 160, período 8, mención OTORRINO): texto: '( TMED751 o TMD324 ) y TMED753'; ids: ['TMED751', 'TMED753']
- **TMED852 — Prótesis y ortesis auditivas** (id 161, período 8, mención OTORRINO): texto: '( TMED751 o TMD324 ) y TMED753'; ids: ['TMED751', 'TMED753']
- **TMED853 — Rehabilitación vestibular auditiva** (id 162, período 8, mención OTORRINO): texto: '( TMED751 o TMD324 ) y ( TMED752 o TMD316 )'; ids: ['TMED751', 'TMED752']
- **TMED951 — Seminario de investigación OTO** (id 164, período 9, mención OTORRINO): texto: 'SPAB303 y SPAB103 y ( TMED851 o TMD280 ) y ( TMED852 o TMD259 ) y ( TMED853 o ( TMD259 y TMD253 ) )'; ids: ['SPAB103', 'SPAB303', 'TMED851', 'TMED852', 'TMED853']
- **TMED952 — Integrador II: internado clínico OTO** (id 165, período 10, mención OTORRINO): texto: 'SPAB303 y SPAB103 y ( TMED851 o TMD280 ) y ( TMED852 o TMD259 ) y ( TMED853 o ( TMD259 y TMD253 ) )'; ids: ['SPAB103', 'SPAB303', 'TMED851', 'TMED852', 'TMED853']

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

- **ING129 — Inglés II** (id 7, período 2): texto: 'ING119 o ING111 o ING110 o ING116 o ING117 o CNT021 o ( ING050 y ING051 ) o ( FLG301 y FLG302 ) o ( BMA281 y BMA282 ) o ( ETU081 y ETU082 )'; ids: ['ING119']
- **PSIC122 — Procesos psicológicos y neurociencias** (id 9, período 2): texto: 'BIOL080 o BIO036'; ids: ['BIOL080']
- **ING239 — Inglés III** (id 12, período 3): texto: 'ING129 o ING121 o ING120 o ING216 o ING126 o ING134 o ING127 o CNT026 o ( ETU181 y ETU182 ) o ING229'; ids: ['ING129']
- **PSIC213 — Investigación I** (id 15, período 3): texto: 'PSIC123 o ( HUF136 o PSL006 )'; ids: ['PSIC123']
- **ING249 — Inglés IV** (id 17, período 4): texto: 'ING239 o ING210 o ING216 o ING224 o ING126 o CNT126 o ( ETU281 y ETU282 ) o ING217'; ids: ['ING239']
- **PSIC221 — Psicoanálisis II** (id 18, período 4): texto: 'PSIC211 o PSL104'; ids: ['PSIC211']
- **PSIC222 — Psicología del desarrollo II** (id 19, período 4): texto: 'PSIC212 o PSL111'; ids: ['PSIC212']
- **PSIC223 — Investigación II** (id 20, período 4): texto: 'PSIC213 o FMS180'; ids: ['PSIC213']
- **PSIC313 — Taller de integración** (id 24, período 5): texto: '( PSIC211 o PSL104 ) y ( PSIC222 o PSL112 ) y ( PSIC223 o PSL105 )'; ids: ['PSIC211', 'PSIC222', 'PSIC223']
- **PSIC321 — Psicodiagnóstico clínico II** (id 26, período 6): texto: 'PSIC311 o ( PSL131 o PSL233 )'; ids: ['PSIC311']
- **PSIC322 — Psicopatología y psiquiatría II** (id 27, período 6): texto: 'PSIC312 o PSL232'; ids: ['PSIC312']
- **PSIC324 — Diagnóstico e intervención social** (id 29, período 6): texto: 'PSIC314 o PSL240'; ids: ['PSIC314']
- **PSIC412 — Psicopatología infanto juvenil** (id 32, período 7): texto: 'PSIC312 o PSL232'; ids: ['PSIC312']
- **PSIC413 — Diagnóstico e intervención educacional** (id 33, período 7): texto: 'PSIC323 o PSL213'; ids: ['PSIC323']
- **PSIC415 — Diagnóstico e intervención organizacional** (id 35, período 7): texto: 'PSIC325 o PSL344'; ids: ['PSIC325']
- **PSIC422 — Clínica infanto juvenil** (id 37, período 8): texto: 'PSIC412 o PSL314'; ids: ['PSIC412']
- **PSIC423 — Taller de investigación** (id 38, período 8): texto: 'PSIC313 y ( PSIC321 o PSL234 ) y ( PSIC322 o PSL235 ) y ( PSIC323 o PSL213 ) y ( PSIC325 o PSL344 ) y ( PSIC414 o PSL242 )'; ids: ['PSIC313', 'PSIC321', 'PSIC322', 'PSIC323', 'PSIC325', 'PSIC414']
- **PSIC424 — Diagnóstico e intervención jurídica** (id 39, período 8): texto: 'PSIC414 o PSL242'; ids: ['PSIC414']
- **PSIC425 — Intervención clínica sistémica** (id 40, período 8): texto: 'PSIC411 o PSL206'; ids: ['PSIC411']
- **PSIC511 — Taller de intervención clínica** (id 41, período 9): texto: '( PSIC411 o PSL206 ) y ( PSIC412 o PSL314 ) y ( PSIC413 o PSL204 ) y ( PSIC414 o PSL242 ) y ( PSIC415 o PSL345 ) y ( PSIC421 o PSL334 o ( PSL331 y PSL335 ) ) y ( PSIC422 o PSL315 ) y ( PSIC423 o PSL348 ) y PSIC424 y ( PSIC425 o PSL333 )'; ids: ['PSIC411', 'PSIC412', 'PSIC413', 'PSIC414', 'PSIC415', 'PSIC421', 'PSIC422', 'PSIC423', 'PSIC424', 'PSIC425']
- **PSIC512 — Psicología y salud** (id 42, período 9): texto: '( PSIC411 o PSL206 ) y ( PSIC412 o PSL314 ) y ( PSIC413 o PSL204 ) y ( PSIC414 o PSL242 ) y ( PSIC415 o PSL345 ) y ( PSIC421 o PSL334 o ( PSL331 y PSL335 ) ) y ( PSIC422 o PSL315 ) y ( PSIC423 o PSL348 ) y PSIC424 y ( PSIC425 o PSL333 )'; ids: ['PSIC411', 'PSIC412', 'PSIC413', 'PSIC414', 'PSIC415', 'PSIC421', 'PSIC422', 'PSIC423', 'PSIC424', 'PSIC425']
- **PSIC513 — Taller de diagnóstico e intervención psicosocial** (id 43, período 9): texto: '( PSIC411 o PSL206 ) y ( PSIC412 o PSL314 ) y ( PSIC413 o PSL204 ) y ( PSIC414 o PSL242 ) y ( PSIC415 o PSL345 ) y ( PSIC421 o PSL334 o ( PSL331 y PSL335 ) ) y ( PSIC422 o PSL315 ) y ( PSIC423 o PSL348 ) y PSIC424 y ( PSIC425 o PSL333 )'; ids: ['PSIC411', 'PSIC412', 'PSIC413', 'PSIC414', 'PSIC415', 'PSIC421', 'PSIC422', 'PSIC423', 'PSIC424', 'PSIC425']
- **PSIC514 — Electivo de formación profesional I** (id 44, período 9): texto: '( PSIC411 o PSL206 ) y ( PSIC412 o PSL314 ) y ( PSIC413 o PSL204 ) y ( PSIC414 o PSL242 ) y ( PSIC415 o PSL345 ) y ( PSIC421 o PSL334 o ( PSL331 y PSL335 ) ) y ( PSIC422 o PSL315 ) y ( PSIC423 o PSL348 ) y PSIC424 y ( PSIC425 o PSL333 )'; ids: ['PSIC411', 'PSIC412', 'PSIC413', 'PSIC414', 'PSIC415', 'PSIC421', 'PSIC422', 'PSIC423', 'PSIC424', 'PSIC425']
- **PSIC515 — Electivo de formación profesional II** (id 45, período 9): texto: '( PSIC411 o PSL206 ) y ( PSIC412 o PSL314 ) y ( PSIC413 o PSL204 ) y ( PSIC414 o PSL242 ) y ( PSIC415 o PSL345 ) y ( PSIC421 o PSL334 o ( PSL331 y PSL335 ) ) y ( PSIC422 o PSL315 ) y ( PSIC423 o PSL348 ) y PSIC424 y ( PSIC425 o PSL333 )'; ids: ['PSIC411', 'PSIC412', 'PSIC413', 'PSIC414', 'PSIC415', 'PSIC421', 'PSIC422', 'PSIC423', 'PSIC424', 'PSIC425']
- **PSIC521 — Práctica profesional** (id 46, período 10): texto: '( PSIC511 o MPC531 ) y ( PSIC512 o MPC532 ) y PSIC513 y ( PSIC514 o PSL323 o PSICP011 o PSICP012 o PSICP036 o PSICP097 o PSICP098 ) y ( PSIC515 o PSL332 o PSICP007 o PSICP008 o PSICP009 o PSICP010 o PSICP049 o PSICP096 )'; ids: ['PSIC511', 'PSIC512', 'PSIC513', 'PSIC514', 'PSIC515']

## Bioquímica

### Tiene ids de prerrequisitos pero prereq_expr vacío o ausente (48)

- **BQ007 — Química General II** (id 7, período 2): ids: BQ001
- **BQ008 — Laboratorio de Química General** (id 8, período 2): ids: BQ001, BQ002
- **BQ009 — Física General** (id 9, período 2): ids: BQ003
- **BQ010 — Cálculo Diferencial e Integral** (id 10, período 2): ids: BQ003
- **BQ011 — Biología Celular** (id 11, período 2): ids: BQ002
- **BQ013 — Inglés II** (id 13, período 2): ids: BQ006
- **BQ014 — Química Orgánica I** (id 14, período 3): ids: BQ007
- **BQ015 — Química Analítica I** (id 15, período 3): ids: BQ007, BQ008
- **BQ016 — Laboratorio I de Química Orgánica** (id 16, período 3): ids: BQ007, BQ008
- **BQ017 — Estadística y Análisis de Datos** (id 17, período 3): ids: BQ010
- **BQ018 — Física Aplicada a la Bioquímica** (id 18, período 3): ids: BQ009
- **BQ019 — Fisiología Celular** (id 19, período 3): ids: BQ009, BQ011
- **BQ020 — Cultura Científica: Divulgación y Enseñanza** (id 20, período 3): ids: BQ004, BQ005
- **BQ021 — Química Orgánica II** (id 21, período 4): ids: BQ014
- **BQ022 — Laboratorio de Análisis Químico** (id 22, período 4): ids: BQ008, BQ015, BQ017
- **BQ023 — Química Analítica II** (id 23, período 4): ids: BQ015
- **BQ024 — Fisicoquímica I** (id 24, período 4): ids: BQ009, BQ010, BQ014
- **BQ025 — Fisiología de Sistemas** (id 25, período 4): ids: BQ019
- **BQ026 — Taller de Cultura Científica** (id 26, período 4): ids: BQ020
- **BQ028 — Laboratorio de Análisis Instrumental** (id 28, período 5): ids: BQ022, BQ023
- **BQ029 — Bioquímica General** (id 29, período 5): ids: BQ021, BQ024
- **BQ030 — Estructura y Función de Organelos Celulares** (id 30, período 5): ids: BQ021, BQ025
- **BQ031 — Fisicoquímica para Ciencias Biológicas** (id 31, período 5): ids: BQ018, BQ024
- **BQ032 — Inglés III** (id 32, período 5): ids: BQ013
- **BQ033 — Estructura y Función de Proteínas** (id 33, período 6): ids: BQ029, BQ031
- **BQ034 — Genética Molecular** (id 34, período 6): ids: BQ029
- **BQ035 — Inmunología Celular y Molecular** (id 35, período 6): ids: BQ030
- **BQ036 — Microbiología General** (id 36, período 6): ids: BQ030
- **BQ037 — Inglés IV** (id 37, período 6): ids: BQ032
- **BQ038 — Química Fisiológica y Patológica** (id 38, período 7): ids: BQ033, BQ035
- **BQ039 — Genética Molecular de Eucariontes** (id 39, período 7): ids: BQ034
- **BQ040 — Fisiología y Genética Microbiana** (id 40, período 7): ids: BQ034, BQ036
- **BQ041 — Administración y Gestión** (id 41, período 7): ids: BQ026
- **BQ042 — Unidad de Investigación en Bioquímica** (id 42, período 7): ids: BQ028, BQ029
- **BQ043 — Bioquímica Clínica y Patológica** (id 43, período 8): ids: BQ038
- **BQ044 — Fisiología y Bioquímica Vegetal** (id 44, período 8): ids: BQ039
- **BQ045 — Bioética** (id 45, período 8): ids: BQ038
- **BQ046 — Formulación y Evaluación de Proyectos Científicos** (id 46, período 8): ids: BQ033
- **BQ047 — Bioinformática** (id 47, período 8): ids: BQ033, BQ039
- **BQ048 — Práctica Profesional I** (id 48, período 8): ids: BQ033, BQ034
- **BQ049 — Laboratorio de Bioquímica Clínica** (id 49, período 9): ids: BQ041, BQ043
- **BQ050 — Tópicos de Farmacología** (id 50, período 9): ids: BQ043, BQ045
- **BQ051 — Biotecnología** (id 51, período 9): ids: BQ043, BQ045
- **BQ054 — Práctica Profesional II** (id 54, período 9): ids: BQ043, BQ047, BQ048
- **BQ055 — Unidad de Investigación Avanzada en Bioquímica** (id 55, período 10): ids: BQ042, BQ049, BQ051
- **BQ056 — Bioprocesos Industriales** (id 56, período 10): ids: BQ041, BQ051
- **BQ059 — Proyecto de Memoria de Título** (id 59, período 10): ids: BQ046, BQ049, BQ050, BQ051
- **BQ060 — Memoria de Título** (id 60, período 11): ids: BQ059

## Ingeniería en Alimentos

### El texto prereq_expr no coincide con los ids de prerrequisitos (2)

- **IA068 — Práctica Profesional** (id 68, período 11): texto: 'Semestre 10 aprobado'; ids: ['IA001', 'IA002', 'IA003', 'IA004', 'IA005', 'IA006', 'IA007', 'IA008', 'IA009', 'IA010', 'IA011', 'IA012', 'IA013', 'IA014', 'IA015', 'IA016', 'IA017', 'IA018', 'IA019', 'IA020', 'IA021', 'IA022', 'IA023', 'IA024', 'IA025', 'IA026', 'IA027', 'IA028', 'IA029', 'IA030', 'IA031', 'IA032', 'IA033', 'IA034', 'IA035', 'IA036', 'IA037', 'IA038', 'IA039', 'IA040', 'IA041', 'IA042', 'IA043', 'IA044', 'IA045', 'IA046', 'IA047', 'IA048', 'IA049', 'IA050', 'IA051', 'IA052', 'IA053', 'IA054', 'IA055', 'IA056', 'IA057', 'IA058', 'IA059', 'IA060', 'IA061', 'IA062', 'IA063', 'IA064', 'IA065', 'IA066', 'IA067']; en ids y no en el texto: ['IA001', 'IA002', 'IA003', 'IA004', 'IA005', 'IA006', 'IA007', 'IA008', 'IA009', 'IA010', 'IA011', 'IA012', 'IA013', 'IA014', 'IA015', 'IA016', 'IA017', 'IA018', 'IA019', 'IA020', 'IA021', 'IA022', 'IA023', 'IA024', 'IA025', 'IA026', 'IA027', 'IA028', 'IA029', 'IA030', 'IA031', 'IA032', 'IA033', 'IA034', 'IA035', 'IA036', 'IA037', 'IA038', 'IA039', 'IA040', 'IA041', 'IA042', 'IA043', 'IA044', 'IA045', 'IA046', 'IA047', 'IA048', 'IA049', 'IA050', 'IA051', 'IA052', 'IA053', 'IA054', 'IA055', 'IA056', 'IA057', 'IA058', 'IA059', 'IA060', 'IA061', 'IA062', 'IA063', 'IA064', 'IA065', 'IA066', 'IA067']
- **IA069 — Actividad Final de Titulación** (id 69, período 11): texto: 'Semestre 10 aprobado'; ids: ['IA001', 'IA002', 'IA003', 'IA004', 'IA005', 'IA006', 'IA007', 'IA008', 'IA009', 'IA010', 'IA011', 'IA012', 'IA013', 'IA014', 'IA015', 'IA016', 'IA017', 'IA018', 'IA019', 'IA020', 'IA021', 'IA022', 'IA023', 'IA024', 'IA025', 'IA026', 'IA027', 'IA028', 'IA029', 'IA030', 'IA031', 'IA032', 'IA033', 'IA034', 'IA035', 'IA036', 'IA037', 'IA038', 'IA039', 'IA040', 'IA041', 'IA042', 'IA043', 'IA044', 'IA045', 'IA046', 'IA047', 'IA048', 'IA049', 'IA050', 'IA051', 'IA052', 'IA053', 'IA054', 'IA055', 'IA056', 'IA057', 'IA058', 'IA059', 'IA060', 'IA061', 'IA062', 'IA063', 'IA064', 'IA065', 'IA066', 'IA067']; en ids y no en el texto: ['IA001', 'IA002', 'IA003', 'IA004', 'IA005', 'IA006', 'IA007', 'IA008', 'IA009', 'IA010', 'IA011', 'IA012', 'IA013', 'IA014', 'IA015', 'IA016', 'IA017', 'IA018', 'IA019', 'IA020', 'IA021', 'IA022', 'IA023', 'IA024', 'IA025', 'IA026', 'IA027', 'IA028', 'IA029', 'IA030', 'IA031', 'IA032', 'IA033', 'IA034', 'IA035', 'IA036', 'IA037', 'IA038', 'IA039', 'IA040', 'IA041', 'IA042', 'IA043', 'IA044', 'IA045', 'IA046', 'IA047', 'IA048', 'IA049', 'IA050', 'IA051', 'IA052', 'IA053', 'IA054', 'IA055', 'IA056', 'IA057', 'IA058', 'IA059', 'IA060', 'IA061', 'IA062', 'IA063', 'IA064', 'IA065', 'IA066', 'IA067']

### Tiene ids de prerrequisitos pero prereq_expr vacío o ausente (56)

- **IA007 — Química General II** (id 7, período 2): ids: IA001
- **IA008 — Laboratorio de Química General** (id 8, período 2): ids: IA001, IA002
- **IA009 — Física General** (id 9, período 2): ids: IA003
- **IA010 — Cálculo Diferencial e Integral** (id 10, período 2): ids: IA003
- **IA011 — Biología Celular** (id 11, período 2): ids: IA002
- **IA013 — Inglés II** (id 13, período 2): ids: IA006
- **IA014 — Química Orgánica I** (id 14, período 3): ids: IA007
- **IA015 — Química Analítica I** (id 15, período 3): ids: IA007, IA008
- **IA016 — Laboratorio I de Química Orgánica** (id 16, período 3): ids: IA007, IA008
- **IA017 — Estadística y Análisis de Datos** (id 17, período 3): ids: IA010
- **IA018 — Física Aplicada a la Química** (id 18, período 3): ids: IA009
- **IA019 — Cálculo Avanzado Multivariado** (id 19, período 3): ids: IA010
- **IA021 — Química Orgánica II** (id 21, período 4): ids: IA014
- **IA022 — Laboratorio de Análisis Químico** (id 22, período 4): ids: IA008, IA015, IA017
- **IA023 — Química Analítica II** (id 23, período 4): ids: IA015
- **IA024 — Fisicoquímica I** (id 24, período 4): ids: IA009, IA010, IA014
- **IA025 — Álgebra Lineal y Métodos Numéricos** (id 25, período 4): ids: IA019
- **IA026 — Computación y Programación** (id 26, período 4): ids: IA017
- **IA028 — Laboratorio de Análisis Instrumental** (id 28, período 5): ids: IA022, IA023
- **IA029 — Materias Primas Vegetales y Animales** (id 29, período 5): ids: IA011, IA021
- **IA030 — Fisicoquímica Orientada a los Alimentos** (id 30, período 5): ids: IA018, IA024
- **IA031 — Dibujo en Ingeniería** (id 31, período 5): ids: IA019, IA026
- **IA032 — Comunicación en Ciencia y Tecnología de los Alimentos** (id 32, período 5): ids: IA013, IA017
- **IA033 — Ecuaciones Diferenciales** (id 33, período 5): ids: IA025
- **IA034 — Módulo Gestión I (Gestión Administrativa y Gestión Económica)** (id 34, período 5): ids: IA017
- **IA035 — Bioquímica General** (id 35, período 6): ids: IA024, IA029
- **IA036 — Química y Análisis de los Alimentos** (id 36, período 6): ids: IA028
- **IA037 — Operaciones Unitarias I** (id 37, período 6): ids: IA028, IA030, IA033
- **IA038 — Propiedades Físicas de los Alimentos** (id 38, período 6): ids: IA026, IA032
- **IA039 — Módulo Gestión II (Gestión Contable y Costos, Gestión Comercial)** (id 39, período 6): ids: IA034
- **IA040 — Práctica I / Unidad de Investigación** (id 40, período 6): ids: IA032
- **IA041 — Bioquímica de los Alimentos** (id 41, período 7): ids: IA035
- **IA042 — Nutrición** (id 42, período 7): ids: IA036
- **IA043 — Operaciones Unitarias II** (id 43, período 7): ids: IA037
- **IA044 — Envases y Embalajes** (id 44, período 7): ids: IA030, IA038
- **IA045 — Gestión Financiera** (id 45, período 7): ids: IA039
- **IA046 — Legislación Alimentaria** (id 46, período 7): ids: IA036
- **IA047 — Inglés III** (id 47, período 7): ids: IA013
- **IA048 — Microbiología e Inocuidad de los Alimentos** (id 48, período 8): ids: IA041
- **IA049 — Higiene y Sanidad Industrial** (id 49, período 8): ids: IA041
- **IA050 — Procesos de Conservación por Bajas Temperaturas** (id 50, período 8): ids: IA043
- **IA051 — Procesos de Conservación por Altas Temperaturas** (id 51, período 8): ids: IA043
- **IA052 — Diseño de Plantas** (id 52, período 8): ids: IA031, IA043
- **IA053 — Diseño de Experimentos** (id 53, período 8): ids: IA026, IA043
- **IA054 — Práctica II** (id 54, período 8): ids: IA040
- **IA055 — Inglés IV** (id 55, período 8): ids: IA047
- **IA056 — Evaluación Sensorial** (id 56, período 9): ids: IA017, IA050, IA051
- **IA057 — Ingeniería de Procesos de Conservación de Alimentos** (id 57, período 9): ids: IA048, IA050, IA051
- **IA058 — Ingeniería de Procesos en Grasas y Aceites** (id 58, período 9): ids: IA050, IA051
- **IA059 — Ingeniería de Procesos en Cereales** (id 59, período 9): ids: IA050, IA051
- **IA060 — Ingeniería de Procesos de Productos Cárnicos** (id 60, período 9): ids: IA050, IA051
- **IA061 — Evaluación de Proyectos** (id 61, período 9): ids: IA045, IA052
- **IA063 — Ingeniería de Procesos de Lácteos** (id 63, período 10): ids: IA050, IA051
- **IA064 — Ingeniería de Procesos en Productos del Mar** (id 64, período 10): ids: IA050, IA051
- **IA065 — Ingeniería de Procesos en Fermentaciones** (id 65, período 10): ids: IA048, IA049
- **IA066 — Gestión de la Calidad** (id 66, período 10): ids: IA046, IA056

## Química

### Tiene ids de prerrequisitos pero prereq_expr vacío o ausente (46)

- **QUI007 — Química General II** (id 7, período 2): ids: QUI001
- **QUI008 — Laboratorio de Química General** (id 8, período 2): ids: QUI001, QUI002
- **QUI009 — Física General** (id 9, período 2): ids: QUI003
- **QUI010 — Cálculo Diferencial e Integral** (id 10, período 2): ids: QUI003
- **QUI011 — Introducción a las Ciencias Químicas** (id 11, período 2): ids: QUI004
- **QUI013 — Inglés II** (id 13, período 2): ids: QUI006
- **QUI014 — Química Orgánica I** (id 14, período 3): ids: QUI007
- **QUI015 — Química Analítica I** (id 15, período 3): ids: QUI007, QUI008
- **QUI016 — Laboratorio I de Química Orgánica** (id 16, período 3): ids: QUI007, QUI008
- **QUI017 — Estadística y Análisis de Datos** (id 17, período 3): ids: QUI010
- **QUI018 — Física Aplicada a la Química** (id 18, período 3): ids: QUI009
- **QUI019 — Cálculo Multivariado** (id 19, período 3): ids: QUI010
- **QUI020 — Química Inorgánica I** (id 20, período 3): ids: QUI007, QUI011
- **QUI021 — Química Orgánica II** (id 21, período 4): ids: QUI014
- **QUI022 — Laboratorio de Análisis Químico** (id 22, período 4): ids: QUI008, QUI015, QUI017
- **QUI023 — Química Analítica II** (id 23, período 4): ids: QUI015
- **QUI024 — Fisicoquímica I** (id 24, período 4): ids: QUI009, QUI010, QUI014
- **QUI025 — Álgebra Lineal y Métodos Numéricos** (id 25, período 4): ids: QUI019
- **QUI026 — Laboratorio de Química Inorgánica** (id 26, período 4): ids: QUI008, QUI020
- **QUI028 — Laboratorio de Análisis Instrumental** (id 28, período 5): ids: QUI022, QUI023
- **QUI029 — Química Orgánica III** (id 29, período 5): ids: QUI021
- **QUI030 — Laboratorio II de Química Orgánica** (id 30, período 5): ids: QUI016, QUI021
- **QUI031 — Fisicoquímica II** (id 31, período 5): ids: QUI018, QUI024
- **QUI032 — Química Inorgánica II** (id 32, período 5): ids: QUI026
- **QUI033 — Ecuaciones Diferenciales** (id 33, período 5): ids: QUI025
- **QUI034 — Análisis Orgánico** (id 34, período 6): ids: QUI029
- **QUI035 — Química Analítica III** (id 35, período 6): ids: QUI028
- **QUI036 — Introducción a la Química Cuántica** (id 36, período 6): ids: QUI025, QUI033
- **QUI037 — Laboratorio Fisicoquímica** (id 37, período 6): ids: QUI028, QUI031
- **QUI038 — Operaciones Unitarias I** (id 38, período 6): ids: QUI028, QUI031
- **QUI039 — Elementos de Bioquímica y Microbiología** (id 39, período 7): ids: QUI029
- **QUI040 — Electroquímica** (id 40, período 7): ids: QUI037
- **QUI041 — Fisicoquímica III** (id 41, período 7): ids: QUI031, QUI036
- **QUI042 — Operaciones Unitarias II** (id 42, período 7): ids: QUI038
- **QUI044 — Inglés III** (id 44, período 7): ids: QUI013
- **QUI045 — Química de Polímeros** (id 45, período 8): ids: QUI029, QUI037
- **QUI046 — Tópicos de Análisis Instrumental Avanzado** (id 46, período 8): ids: QUI035
- **QUI047 — Aseguramiento y Gestión de Calidad** (id 47, período 8): ids: QUI035
- **QUI048 — Unidad de Investigación** (id 48, período 8): ids: QUI040, QUI041, QUI042
- **QUI049 — Laboratorio III de Química Orgánica** (id 49, período 8): ids: QUI030, QUI034
- **QUI050 — Inglés IV** (id 50, período 8): ids: QUI044
- **QUI051 — Legislación Ambiental** (id 51, período 9): ids: QUI042, QUI047
- **QUI052 — Procesos y Formulación de Proyectos en la Industria Química** (id 52, período 9): ids: QUI042, QUI046, QUI047
- **QUI054 — Memoria de Título I** (id 54, período 10): ids: QUI048, QUI051, QUI052
- **QUI056 — Memoria de Título II** (id 56, período 11): ids: QUI054
- **QUI057 — Práctica Profesional** (id 57, período 11): ids: QUI045, QUI046, QUI047, QUI048

## Química y Farmacia

### El texto prereq_expr no coincide con los ids de prerrequisitos (1)

- **QF066 — Actividad Final de Titulación** (id 66, período 11): texto: '10 semestres aprobados'; ids: ['QF001', 'QF002', 'QF003', 'QF004', 'QF005', 'QF006', 'QF007', 'QF008', 'QF009', 'QF010', 'QF011', 'QF012', 'QF013', 'QF014', 'QF015', 'QF016', 'QF017', 'QF018', 'QF019', 'QF020', 'QF021', 'QF022', 'QF023', 'QF024', 'QF025', 'QF026', 'QF027', 'QF028', 'QF029', 'QF030', 'QF031', 'QF032', 'QF033', 'QF034', 'QF035', 'QF036', 'QF037', 'QF038', 'QF039', 'QF040', 'QF041', 'QF042', 'QF043', 'QF044', 'QF045', 'QF046', 'QF047', 'QF048', 'QF049', 'QF050', 'QF051', 'QF052', 'QF053', 'QF054', 'QF055', 'QF056', 'QF057', 'QF058', 'QF059', 'QF060', 'QF061', 'QF062', 'QF063', 'QF064', 'QF065']; en ids y no en el texto: ['QF001', 'QF002', 'QF003', 'QF004', 'QF005', 'QF006', 'QF007', 'QF008', 'QF009', 'QF010', 'QF011', 'QF012', 'QF013', 'QF014', 'QF015', 'QF016', 'QF017', 'QF018', 'QF019', 'QF020', 'QF021', 'QF022', 'QF023', 'QF024', 'QF025', 'QF026', 'QF027', 'QF028', 'QF029', 'QF030', 'QF031', 'QF032', 'QF033', 'QF034', 'QF035', 'QF036', 'QF037', 'QF038', 'QF039', 'QF040', 'QF041', 'QF042', 'QF043', 'QF044', 'QF045', 'QF046', 'QF047', 'QF048', 'QF049', 'QF050', 'QF051', 'QF052', 'QF053', 'QF054', 'QF055', 'QF056', 'QF057', 'QF058', 'QF059', 'QF060', 'QF061', 'QF062', 'QF063', 'QF064', 'QF065']

### Tiene ids de prerrequisitos pero prereq_expr vacío o ausente (55)

- **QF007 — Química General II** (id 7, período 2): ids: QF001
- **QF008 — Laboratorio de Química General** (id 8, período 2): ids: QF001, QF002
- **QF009 — Física General** (id 9, período 2): ids: QF003
- **QF010 — Cálculo Diferencial e Integral** (id 10, período 2): ids: QF003
- **QF012 — Biología Celular** (id 12, período 2): ids: QF002
- **QF013 — Inglés II** (id 13, período 2): ids: QF006
- **QF014 — Química Orgánica I** (id 14, período 3): ids: QF007
- **QF015 — Química Analítica I** (id 15, período 3): ids: QF007, QF008
- **QF016 — Laboratorio I de Química Orgánica** (id 16, período 3): ids: QF007, QF008
- **QF017 — Estadística y Análisis de Datos** (id 17, período 3): ids: QF010
- **QF018 — Fundamentos de Ciencias Farmacéuticas** (id 18, período 3): ids: QF004, QF011
- **QF019 — Fisiología Celular** (id 19, período 3): ids: QF009, QF012
- **QF021 — Inglés III** (id 21, período 3): ids: QF013
- **QF022 — Química Orgánica II** (id 22, período 4): ids: QF014
- **QF023 — Laboratorio de Análisis Químico** (id 23, período 4): ids: QF008, QF015, QF017
- **QF024 — Química Analítica II** (id 24, período 4): ids: QF015
- **QF025 — Fisicoquímica I** (id 25, período 4): ids: QF009, QF010, QF014
- **QF026 — Fisiología de Sistemas** (id 26, período 4): ids: QF019
- **QF027 — Práctica Intermedia** (id 27, período 4): ids: QF018
- **QF028 — Inglés IV** (id 28, período 4): ids: QF021
- **QF029 — Laboratorio de Análisis Instrumental** (id 29, período 5): ids: QF023, QF024
- **QF030 — Botánica y Farmacognosia** (id 30, período 5): ids: QF022, QF024
- **QF031 — Química de Heterocíclicos y Análisis Espectroscópico** (id 31, período 5): ids: QF022
- **QF032 — Bioquímica** (id 32, período 5): ids: QF022
- **QF033 — Farmacología General** (id 33, período 5): ids: QF023, QF026
- **QF034 — Gestión de Calidad** (id 34, período 5): ids: QF018
- **QF035 — Microbiología** (id 35, período 6): ids: QF032
- **QF036 — Farmacoquímica I** (id 36, período 6): ids: QF031, QF033
- **QF037 — Farmacología de Sistemas I** (id 37, período 6): ids: QF033
- **QF038 — Fisiopatología Molecular** (id 38, período 6): ids: QF026, QF032
- **QF039 — Legislación Farmacéutica** (id 39, período 6): ids: QF027, QF034
- **QF040 — Fisicoquímica Farmacéutica** (id 40, período 6): ids: QF025
- **QF041 — Fisiopatología y Semiología** (id 41, período 7): ids: QF038
- **QF042 — Farmacoquímica II** (id 42, período 7): ids: QF036
- **QF043 — Farmacología de Sistemas II** (id 43, período 7): ids: QF035, QF037
- **QF044 — Salud Pública** (id 44, período 7): ids: QF039
- **QF045 — Tecnología Farmacéutica I** (id 45, período 7): ids: QF039, QF040
- **QF046 — Operaciones Unitarias para Q&F** (id 46, período 7): ids: QF040
- **QF047 — Análisis de Medicamento, Doping y Drogas de Abuso** (id 47, período 8): ids: QF029, QF042
- **QF048 — Nutrición Clínica** (id 48, período 8): ids: QF041
- **QF049 — Bioquímica Clínica** (id 49, período 8): ids: QF041
- **QF050 — Biofarmacia y Farmacocinética** (id 50, período 8): ids: QF033, QF045
- **QF051 — Tecnología Farmacéutica II** (id 51, período 8): ids: QF045, QF046
- **QF052 — Administración y Gestión Farmacéutica** (id 52, período 8): ids: QF045
- **QF053 — Estadística Farmacéutica** (id 53, período 8): ids: QF017, QF044
- **QF054 — Farmacología Clínica** (id 54, período 9): ids: QF043, QF049, QF050
- **QF055 — Bromatología** (id 55, período 9): ids: QF029, QF048
- **QF056 — Toxicología** (id 56, período 9): ids: QF043, QF049
- **QF057 — Farmacia Asistencial** (id 57, período 9): ids: QF044, QF052
- **QF058 — Tecnología Cosmética** (id 58, período 9): ids: QF051
- **QF060 — Farmacia Clínica** (id 60, período 10): ids: QF054
- **QF061 — Práctica Profesional en Farmacia Comunitaria** (id 61, período 10): ids: QF052, QF054, QF056
- **QF062 — Biotecnología Farmacéutica** (id 62, período 10): ids: QF038, QF051
- **QF063 — Economía en Salud y Marketing Farmacéutico** (id 63, período 10): ids: QF044, QF052, QF054
- **QF064 — Innovación y Proyectos** (id 64, período 10): ids: QF053
