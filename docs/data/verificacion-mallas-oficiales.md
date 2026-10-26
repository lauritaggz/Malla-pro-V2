# Verificación de mallas contra documentos oficiales

Fecha: 25-10-2026. Fuente: los documentos “Malla curricular” de Banner UNAB que enviaste.

## Cómo se hizo

- **Medicina, Tecnología Médica y Psicología**: el PDF/HTML trae texto, así que se leyó directo.
- **Las 5 ingenierías y Geología**: los PDF son imágenes, así que se leyeron con OCR. Cada ramo donde el OCR y tu JSON no coincidían lo revisé mirando el recorte del PDF. Si ambos coincidían, se dio por verificado.
- Los requisitos oficiales citan códigos de planes antiguos (equivalencias). Para tu malla se dejan solo los ramos del plan vigente, y los códigos antiguos se guardan aparte como equivalencias.
- Después de corregir, volví a comparar cada malla contra su documento: no queda ninguna diferencia, salvo 2 textos oficiales ambiguos (GEOL804 y SPAB111) que se dejaron como estaban a propósito.

## Resumen

| Carrera | Documento | Catálogo | Lectura | Correcciones |
|---|---|---|---|---|
| Ingeniería en Computación e Informática | ICINF.malla.pdf (UNAB11500) | Primer Semestre 2020 | OCR + revisión visual | ninguna |
| Ingeniería Civil Informática | ICF.malla.pdf (UNAB12210) | Primer Semestre 2020 | OCR + revisión visual | 30 |
| Ingeniería Civil Industrial | ICI.malla.pdf (UNAB12100) | Primer Semestre 2020 | OCR + revisión visual | 4 |
| Ingeniería Civil en Minas | ICM.malla.pdf (UNAB11303) | Primer Semestre 2022 | OCR + revisión visual | 1 |
| Geología | GEO.malla.pdf (UNAB11350) | Primer Semestre 2022 | OCR + revisión visual | 5 |
| Ingeniería en Marina Mercante | IMMC.malla.pdf (UNAB14001) | Primer Semestre 2020 | OCR + revisión visual | 4 |
| Medicina | Medicina.pdf (UNAB19710) | Primer Semestre 2025 | texto | ninguna |
| Tecnología Médica | Tecnología Médica.pdf (UNAB19600) | Primer Semestre 2018 | texto | 40 |
| Psicología | Psicología.htm (UNAB11900) | Primer Semestre 2018 | texto | ninguna |

## Ingeniería en Computación e Informática

- Coincide completamente con el documento oficial: códigos, SCT, semestres, prerrequisitos y correquisitos.
- Solo se completó el total de créditos (534 SCT), que estaba en 0.

## Ingeniería Civil Informática

- El documento oficial (catálogo 2020) usa códigos **CINF** para 16 ramos que tu JSON tenía como ICF2xx / INSW4xx. En ese documento, los códigos ICF aparecen solo como equivalencias de planes antiguos.
- La estructura de prerrequisitos de tu JSON era correcta: al cambiar los códigos, todo calza con el documento. Lo que estaba mal era el texto `prereq_expr` (por eso el reporte anterior mostraba INSW410 e INSW421 cruzados).
- Los `id` de cada ramo no cambian, así que el avance guardado por id se conserva.
- SCT corregidos y verificados mirando el PDF; el total pasa de 631 a 669 SCT.

| Ramo | Qué cambió | Antes | Ahora |
|---|---|---|---|
| INSW220 | codigo | INSW220 | CINF100 |
| ICF202 | sct | 12 | 16 |
| ICF202 | codigo | ICF202 | CINF101 |
| ICF201 | sct | 12 | 10 |
| ICF201 | codigo | ICF201 | CINF102 |
| ICF203 | sct | 12 | 19 |
| ICF203 | codigo | ICF203 | CINF103 |
| ICF204 | sct | 12 | 15 |
| ICF204 | codigo | ICF204 | CINF104 |
| ICF205 | sct | 12 | 13 |
| ICF205 | codigo | ICF205 | CINF105 |
| INSW411 | sct | 10 | 14 |
| INSW411 | codigo | INSW411 | CINF107 |
| INSW421 | sct | 14 | 6 |
| INSW421 | codigo | INSW421 | CINF200 |
| INSW421 | nombre | Seminario de Licenciatura en Ingeniería | Integrador II: Seminario de Licenciatura en Ciencias de la Ingeniería |
| INSW410 | sct | 10 | 15 |
| INSW410 | codigo | INSW410 | CINF108 |
| ICF206 | codigo | ICF206 | CINF109 |
| ICF207 | sct | 12 | 14 |
| ICF207 | codigo | ICF207 | CINF110 |
| INSW412 | sct | 10 | 14 |
| INSW412 | codigo | INSW412 | CINF111 |
| INSW413 | sct | 10 | 14 |
| INSW413 | codigo | INSW413 | CINF112 |
| ICF208 | codigo | ICF208 | CINF113 |
| INSW420 | codigo | INSW420 | CINF300 |
| INSW422 | sct | 14 | 28 |
| INSW422 | codigo | INSW422 | CINF400 |

## Ingeniería Civil Industrial

- Práctica I (CIND311) exige además Habilidades Comunicativas (CEGHC11), que faltaba.
- CIND312 (Seminario) y CIND313 (Práctica II) tienen correquisitos en el documento; tu JSON no los tenía.
- El total declarado (400) no correspondía: los ramos suman 673 SCT, igual en el documento y en tu JSON.

| Ramo | Qué cambió | Antes | Ahora |
|---|---|---|---|
| CIND311 | prerrequisitos | CFIS310 y FMMP012 y TDFI101 y TDFI102 y CFIS328 y FMMP112 y QUIM090 y TDFI103 y ACAD101 y CFIS332 y FMMP212 y TDFI104 y CIND100 | CFIS310 y FMMP012 y TDFI101 y TDFI102 y CFIS328 y FMMP112 y QUIM090 y TDFI103 y ACAD101 y CFIS332 y CIND100 y FMMP212 y TDFI104 y CEGHC11 |
| CIND312 | correquisitos | — | IIND414 y CIND213 y CIND214 y CIND215 y CIND313 |
| CIND313 | correquisitos | — | IIND414 y CIND213 y CIND214 y CIND215 y CIND312 |

## Ingeniería Civil en Minas

- Mecánica de Rocas (ICMI311) exige Geología II (ICMI211), no Integrador I (ICMI221).

| Ramo | Qué cambió | Antes | Ahora |
|---|---|---|---|
| ICMI311 | prerrequisitos | CFIS332 y ICMI221 | ICMI211 y CFIS332 |

## Geología

- GEOL302 exige Mineralogía (GEOL201), no GEOL301: eso resuelve el hallazgo de “prerrequisito en el mismo semestre”.
- GEOL401 tiene 16 SCT (no 10) y 4 correquisitos; GEOL603 tiene correquisito GEOL602; GEOL005 exige también Práctica II (GEOL806).
- GEOL804 tiene un texto oficial ambiguo, «GEOL701 o (GEO407 y GEO402) y GEOL601». Se mantuvo tu versión (GEOL701 y GEOL601), que es la lectura razonable.

| Ramo | Qué cambió | Antes | Ahora |
|---|---|---|---|
| GEOL302 | prerrequisitos | GEOL203 y GEOL301 | GEOL201 y GEOL203 |
| GEOL401 | correquisitos | — | ING119 y ACAD102 y CFIS344 y FMMP312 |
| GEOL401 | sct | 10 | 16 |
| GEOL603 | correquisitos | — | GEOL602 |
| GEOL005 | prerrequisitos | GEOL906 | GEOL906 y GEOL806 |

## Ingeniería en Marina Mercante

- Proyecto de Título (IMMQ408) exige Portafolio de Proyecto (IMMQ404), no el Seminario (IMMC404): eso resuelve el hallazgo del mismo semestre.
- Otros 3 ramos de Maquinaria tenían un prerrequisito de más.

| Ramo | Qué cambió | Antes | Ahora |
|---|---|---|---|
| IMMQ305 (MAQ) | prerrequisitos | IMMQ301 y IMMQ303 | IMMQ301 |
| IMMQ404 (MAQ) | prerrequisitos | IMMQ304 y IMMQ305 y IMMQ306 y IMMQ308 | IMMQ305 y IMMQ306 y IMMQ308 |
| IMMQ405 (MAQ) | prerrequisitos | ING249 y IMMQ402 | ING249 |
| IMMQ408 (MAQ) | prerrequisitos | IMMC404 | IMMQ404 |

## Medicina

- Coincide completamente con el documento oficial.
- Los internados de 11° y 12° semestre efectivamente no tienen prerrequisitos en el documento.
- MEDI006 no era ambiguo: el documento tiene los paréntesis y coincide con tu lista. Solo el texto de tu JSON los había perdido.
- Se completó el total de créditos (1.039 SCT).

## Tecnología Médica

- Es el catálogo 2018. Las 40 correcciones salen del texto del PDF (no de OCR) y las revisé contra el texto línea a línea.
- Varias diferencias tienen un patrón: tu JSON tenía los requisitos de un ramo asignados al ramo vecino (p. ej. TMED621/622/623 de OFTA, TMED551/552 de OTORRINO).
- Para confirmar con la carrera, porque el documento dice algo que puede sorprender: (1) Bioquímica (BIOL166) tiene un requisito con ramas por plan; para tu malla solo aplica Química Orgánica (QUIM022). (2) El Integrador II de 10° semestre exige lo mismo que el Seminario de 9° (SPAB303, SPAB103 y los ramos de la mención), no el Seminario.
- SPAB111 tiene un texto oficial ambiguo; se mantuvo tu versión (SPAB110).

| Ramo | Qué cambió | Antes | Ahora |
|---|---|---|---|
| BIOL166 | prerrequisitos | BIOL035 y BIOL130 y TMED001 y MORF122 y QUIM022 | QUIM022 |
| BIOL272 | prerrequisitos | CFIS020 y BIOL166 | MORF122 |
| TMED004 | prerrequisitos | BIOL166 | BIOL130 y BIOL035 |
| TMED433 (IFIME) | prerrequisitos | BIOL166 y BIOL272 | BIOL272 y BIOL166 y TMED003 y TMED004 y ING129 y CFIS020 |
| TMED423 (OFTA) | prerrequisitos | BIOL166 y ING129 | BIOL272 y BIOL166 y TMED003 y TMED004 y ING129 y CFIS020 |
| SPAB110 (BACIMET) | prerrequisitos | ING239 y TMED005 | TMED005 |
| SPAB110 (IFIME) | prerrequisitos | ING239 y TMED005 | TMED005 |
| SPAB110 (MORFO) | prerrequisitos | ING239 y TMED005 | TMED005 |
| SPAB110 (OFTA) | prerrequisitos | ING239 y TMED005 | TMED005 |
| SPAB110 (OTORRINO) | prerrequisitos | ING239 y TMED005 | TMED005 |
| TMED551 (OTORRINO) | prerrequisitos | TMED005 | TMED005 y TMED451 |
| TMED552 (OTORRINO) | prerrequisitos | TMED005 y TMED451 | TMED005 |
| TMED621 (OFTA) | prerrequisitos | TMED521 | TMED521 y TMED523 |
| TMED622 (OFTA) | prerrequisitos | TMED521 y TMED523 | TMED522 |
| TMED623 (OFTA) | prerrequisitos | TMED522 | TMED521 |
| SPAB112 (BACIMET) | prerrequisitos | SPAB111 | SPAB111 y TMED611 |
| TMED002 (BACIMET) | prerrequisitos | — | SPAB111 |
| TMED712 (BACIMET) | prerrequisitos | TMED512 y TMED611 | TMED512 |
| TMED713 (BACIMET) | prerrequisitos | TMED611 y TMED612 y TMED613 | TMED611 |
| SPAB112 (IFIME) | prerrequisitos | SPAB111 | SPAB111 y TMED633 |
| TMED002 (IFIME) | prerrequisitos | — | SPAB111 |
| SPAB112 (MORFO) | prerrequisitos | SPAB111 | SPAB111 y TMED643 |
| TMED002 (MORFO) | prerrequisitos | — | SPAB111 |
| TMED742 (MORFO) | prerrequisitos | TMED641 y TMED642 y TMED643 | TMED642 y TMED643 |
| SPAB112 (OFTA) | prerrequisitos | SPAB111 | SPAB111 y TMED622 |
| TMED002 (OFTA) | prerrequisitos | — | SPAB111 |
| TMED723 (OFTA) | prerrequisitos | TMED621 y TMED622 y TMED623 | TMED623 |
| SPAB112 (OTORRINO) | prerrequisitos | SPAB111 | SPAB111 y TMED552 |
| TMED002 (OTORRINO) | prerrequisitos | — | SPAB111 |
| SPAB303 (BACIMET) | prerrequisitos | SPAB112 y TMED714 | SPAB111 y TMED714 |
| SPAB303 (IFIME) | prerrequisitos | SPAB112 y TMED731 | SPAB111 y TMED731 |
| SPAB303 (MORFO) | prerrequisitos | SPAB112 y TMED744 | SPAB111 y TMED744 |
| SPAB303 (OFTA) | prerrequisitos | SPAB112 y TMED721 | SPAB111 y TMED721 |
| SPAB303 (OTORRINO) | prerrequisitos | SPAB112 y TMED752 | SPAB111 y TMED752 |
| TMED851 (OTORRINO) | prerrequisitos | SPAB112 | TMED751 y TMED753 |
| TMED912 (BACIMET) | prerrequisitos | TMED911 | SPAB303 y SPAB103 y TMED811 y TMED812 |
| TMED932 (IFIME) | prerrequisitos | TMED931 | SPAB303 y SPAB103 y TMED831 y TMED832 |
| TMED942 (MORFO) | prerrequisitos | TMED941 | SPAB303 y SPAB103 y TMED841 y TMED842 |
| TMED922 (OFTA) | prerrequisitos | TMED921 | SPAB303 y SPAB103 y TMED821 y TMED822 y TMED823 |
| TMED952 (OTORRINO) | prerrequisitos | TMED951 | SPAB303 y SPAB103 y TMED851 y TMED852 y TMED853 |

## Psicología

- Coincide completamente con el documento oficial, incluidos los ramos de 6° a 8° sin prerrequisitos.
- Se completó el total de créditos (671 SCT).

## Universidad de Chile

Se sumaron Bioquímica, Ingeniería en Alimentos, Química y Química y Farmacia. Pasan la validación sin errores y los créditos cuadran (330 SCT cada una).
- No venía el documento oficial de estas carreras, así que no se pudieron contrastar como las de la UNAB.
- Tres de ellas usan códigos internos (QF001, IA001, QUI001…) porque la fuente no publica códigos. En el formato nuevo quedan marcadas con `codigosOficiales: false`. Esos ramos no se cruzan entre carreras, aunque Química General I sea el mismo ramo en las cuatro. Bioquímica usa BQ001…, que tampoco parece oficial.
- “Semestre 10 aprobado” (Práctica Profesional y Actividad Final) se guarda como un requisito propio (`semestres hasta 10`), en vez de la lista de 67 ramos.
