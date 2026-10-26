> Fuente: `MallaPro_V2_Requerimientos_v1.2.docx` convertido a Markdown. Es la versión de trabajo para los agentes; un requisito solo cambia aquí mediante una tarea de tipo `decision` (ver `docs/process/workflow.md`).
>
> **Actualización 26-10-2026:** la sección 10.1 se ajustó al stack real del repositorio (Python/FastAPI, Firebase), que reemplaza la propuesta Node/Prisma del documento original. Ver ADR-0001 a ADR-0004.

# MallaPro V2 – Plan de requerimientos

Versión 1.2 · 25 de octubre de 2026 · Propuesta de alcance para revisión

**Cómo leer esta versión.** Se conservan la estructura y los IDs de la
v1.1. Los requisitos agregados se marcan **NUEVO**, los modificados
**ACTUALIZADO** y los reemplazados **RETIRADO**. El Anexo A evalúa cada
propuesta nueva con su valor, riesgos y entrega recomendada.

## 1. Definición del producto

MallaPro V2 será una plataforma web de organización académica para
estudiantes universitarios. Permitirá seleccionar, importar o crear una
malla, registrar avance y notas, compartir la configuración de los ramos
con compañeros, organizar horarios y planificar próximos períodos.
Tendrá cuentas personales, sincronización entre dispositivos y una
suscripción que habilita la herramienta completa, con una prueba
gratuita de dos meses. Incluirá una base colaborativa de mallas y un
directorio donde tutores ofrecen servicios y los estudiantes los
contactan por WhatsApp. MallaPro no incluirá publicidad.

**Propuesta de valor:** Tu carrera, organizada.

**Objetivo comercial confirmado:** que eventualmente genere ingresos. El
modelo de referencia, definido en el informe de modelo de negocios (Lean
Canvas), es una prueba gratuita de 2 meses con todo incluido y luego una
suscripción de \$3.490 al mes, con un nivel básico gratuito permanente.
El precio es una hipótesis por validar en el piloto; proveedores y
condiciones comerciales aún no están aprobados.

**Punto de partida real.** La versión pública actual es el MVP: está
hecha en React y alojada en Netlify, sin servidor propio, para validar
la propuesta antes de invertir en infraestructura. Funciona solo con
mallas de la UNAB, que se pasan a JSON desde el documento oficial de
cada malla, no tiene cuentas y guarda los datos únicamente en el
navegador. Este plan no depende del código anterior, que está
desactualizado; mallas, progreso, toma de ramos, notas y tutorías se
consideran referencias funcionales, no funcionalidades auditadas.

## 2. Público y objetivos

**Público inicial:** estudiantes universitarios de Chile que necesitan
entender prerrequisitos, registrar avance y notas, y preparar su próximo
período, partiendo por la UNAB. Se admitirán universidades nuevas
mediante mallas personales, importadas y comunitarias; no se prometerá
compatibilidad completa con cualquier reglamento desde el inicio.

Objetivos de V2:

1.  Mantener el avance académico disponible entre dispositivos.

2.  Permitir utilizar MallaPro aunque una carrera no esté en el
    catálogo.

3.  Integrar malla, progreso, horario y notas en un mismo espacio, con
    prueba gratuita de 2 meses y suscripción para la herramienta
    completa.

4.  Ofrecer planificación basada en reglas explícitas y datos revisados.

5.  Medir uso real, recurrencia y disposición a pagar.

6.  Controlar costos de procesamiento y esfuerzo de soporte.

7.  Conectar estudiantes con tutores del catálogo mediante contacto
    directo por WhatsApp.

8.  **NUEVO** Reducir el trabajo repetido entre estudiantes con
    configuraciones de ramos compartidas y una base colaborativa de
    mallas.

9.  **NUEVO** Dar al equipo de MallaPro herramientas para curar mallas y
    tomar decisiones con métricas de uso y de venta.

## 3. Alcance por entrega

| **Entrega**                   | **Resultado**                                                      | **Incluye**                                                                                                                                                                                                                                                                 | **Condición para avanzar**                                                 |
|-------------------------------|--------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| V2.0: beta gratuita           | Organización académica persistente                                 | Cuentas, catálogo, mallas personales manuales, progreso, prerrequisitos, notas y horario, **compartir configuración de ramos** **ACTUALIZADO**, directorio de tutores, exportación, **migración de datos locales** **ACTUALIZADO**, administración básica y métricas de uso | Flujo completo probado y datos aislados entre usuarios                     |
| V2.1: importación y comunidad | Crear mallas y ofertas horarias desde documentos; compartir mallas | Importación de mallas desde PDF e imagen con IA, **importación de oferta de secciones** **NUEVO**, revisión y cupos, **mallas comunitarias** **NUEVO**, comparación y promoción de mallas en el panel                                                                       | Documentos de prueba procesados sin inventar reglas ni perder correcciones |
| V2.2: lanzamiento comercial   | Cobrar la suscripción                                              | Prueba de 2 meses y suscripción, escenarios, comparación, **generador de horarios sin topes** **NUEVO**, generación de planes, pagos y **métricas comerciales** **NUEVO**                                                                                                   | Piloto que valide valor y cobro probado de extremo a extremo               |
| Posterior                     | Ampliar distribución y servicios                                   | Excel, enlaces, integraciones, **sugerencias de configuración por coincidencia** **NUEVO**, eventual cobro de tutorías y cuentas institucionales                                                                                                                            | Demanda, volumen de datos y viabilidad comprobados                         |

La beta V2.0 constituye el MVP. Durante el piloto todas las funciones
pueden estar abiertas con fecha de término explícita; no representan un
plan gratuito permanente. La importación y los pagos no bloquean su
lanzamiento.

## 4. Roles y permisos

| **Rol**                                           | **Puede hacer**                                                                                                                                                      |
|---------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Visitante                                         | Explorar catálogo público de mallas (verificadas y comunitarias) y tutores, consultar perfiles y contactar por WhatsApp; iniciar registro                            |
| Estudiante – nivel básico                         | Gestionar un perfil académico, su malla y progreso; compartir e importar configuraciones de ramos; buscar y contactar tutores; consultar y exportar lo ya registrado |
| Estudiante – en prueba o suscrito **ACTUALIZADO** | Herramienta completa: notas y calculadora, registro histórico, horario y toma de ramos, importación con IA según cupo, escenarios y generador de horarios            |
| Tutor                                             | Crear y gestionar su perfil, servicios, asignaturas, tarifas y contacto público de WhatsApp; pausar o retirar su publicación                                         |
| Curador del equipo MallaPro **NUEVO**             | Revisar propuestas y mallas comunitarias, compararlas, editarlas y promoverlas a verificadas; gestionar reportes y tutores; ver métricas de uso agregadas            |
| Superadministrador **NUEVO**                      | Todo lo anterior, más asignar y revocar roles del equipo, configurar planes, precios y cupos, y ver métricas comerciales                                             |

Las cuentas suscritas siguen siendo cuentas de estudiante: pagar no
otorga permisos de publicación ni acceso a datos de otros usuarios. El
acceso del equipo a datos privados se limita a soporte, con registro de
cada acción.

## 5. Requerimientos funcionales de V2.0

Prioridad obligatoria: requisito necesario para entregar la etapa. Cada
fila incluye un criterio mínimo verificable.

| **ID** | **Requerimiento** | **Criterio de aceptación** |
|---|---|---|
| CU-01 | Registro, inicio y cierre de sesión; al menos un método de autenticación | El usuario recupera su espacio al iniciar sesión en otro dispositivo y el cierre invalida la sesión local |
| CU-02 | Perfil académico con institución, carrera, versión de malla y régimen de períodos | Se pueden configurar semestres o trimestres sin asumir dos períodos por año |
| CU-03 | Sincronización y estado de guardado | Un cambio confirmado aparece al recargar y en otro dispositivo; un fallo se muestra como pendiente o fallido |
| CU-04 | Exportar datos y solicitar eliminación de cuenta | La exportación contiene malla personal, progreso, notas y horario; la eliminación sigue un procedimiento y plazo informado |
| CU-05 **NUEVO** | Importar datos guardados en el navegador por la versión actual | Al crear la cuenta se detectan los datos locales, se muestra qué se importará y a qué malla corresponde, y repetir la importación no duplica información |
| CA-01 | Buscar catálogo por institución y carrera | El resultado identifica versión, modalidad cuando corresponda, fuente y estado: verificada, comunitaria o en revisión |
| CA-02 | Separar mallas de catálogo y mallas personales | Crear una malla privada no la añade a la búsqueda pública |
| CA-03 | Versionar el catálogo | Una edición genera una nueva versión y no modifica silenciosamente el plan de estudiantes existentes |
| MP-01 | Crear y editar una malla personal manualmente | Permite gestionar períodos, cursos, códigos opcionales, créditos opcionales y reglas académicas |
| MP-02 | Mostrar malla y conexiones | El estudiante puede consultar dependencias y cursos que una asignatura desbloquea, tanto en móvil como en escritorio |
| MP-03 | Reportar un error o proponer una malla para revisión | La propuesta queda pendiente; un curador debe revisar fuente y estructura antes de publicarla como verificada |
| AV-01 | Registrar estado actual de cada curso | Cada curso tiene un único estado actual: pendiente, cursando, aprobado o convalidado; una reprobación se conserva como intento histórico |
| AV-02 | Mantener intentos por período | Reprobar y volver a cursar no borra notas ni intentos anteriores |
| AV-03 | Mostrar avance | Asignaturas y créditos completados se calculan por separado; créditos desconocidos no se tratan como cero confirmado |
| AV-04 | Explicar disponibilidad de un curso | Se muestran reglas satisfechas, faltantes o desconocidas, sin etiquetar como disponible un curso con reglas críticas sin resolver |
| AV-05 | Registrar excepciones personales | La excepción tiene motivo y alcance; no transforma automáticamente el ramo en aprobado ni modifica el catálogo |
| AV-06 | Cambios masivos con revisión y recuperación | Antes de aprobar varios cursos se muestra la cantidad; el usuario puede deshacer la operación |
| NO-01 | Registrar evaluaciones, notas y ponderaciones por intento | El resultado coincide con casos de referencia y avisa si las ponderaciones no suman el total requerido |
| NO-02 | Configurar escala y calcular nota necesaria | Usa escala, umbral y ponderaciones declarados; muestra cuando una meta es imposible o falta información |
| NO-03 | Separar cálculo y aprobación | Una nota calculada no marca automáticamente un curso como aprobado |
| NO-04 **NUEVO** | Compartir la configuración de un ramo mediante enlace o código | Lo compartido contiene solo nombres de evaluaciones, ponderaciones, escala y reglas de eximición; nunca notas ni datos del autor más allá de un alias opcional |
| NO-05 **NUEVO** | Importar una configuración compartida | Se muestra carrera, período y fecha; la copia importada es editable (por ejemplo, renombrar evaluaciones) y no modifica el original. Importar está disponible en el nivel básico |
| HO-01 | Crear horario con asignaturas, secciones y bloques | Se admiten varias sesiones por asignatura y horarios definidos por el usuario |
| HO-02 | Detectar topes | Dos bloques que se superponen generan aviso; bloques contiguos no generan un falso tope |
| HO-03 | Guardar y exportar horario | La versión exportada contiene los mismos cursos, días y horas que el horario guardado |
| HO-04 | Diferenciar planificación e inscripción | Guardar un horario no se presenta como matrícula o inscripción oficial en una universidad |
| PL-01 | Seleccionar ramos para el próximo período | Se muestra carga y disponibilidad académica; permite guardar un plan básico |
| AD-01 | Administrar catálogo y revisión | Solo curadores y superadministrador pueden publicar versiones, retirar una malla del catálogo o cambiar su estado de revisión |
| AD-02 | Recibir y gestionar reportes | Cada incidencia tiene categoría, estado y contexto mínimo; nunca publica notas o datos privados |
| AD-03 **NUEVO** | Gestionar roles del equipo | Solo el superadministrador asigna o revoca el rol de curador; cada cambio de rol queda en el registro de auditoría (NF-11) |
| AN-01 | Medir uso del producto | Registra acciones exitosas según el contrato de eventos y distingue fallos de operaciones completadas |

### 5.1. Prueba gratuita y suscripción ACTUALIZADO

**Decisión confirmada (v1.2):** cada cuenta nueva tiene **2 meses de
prueba con la herramienta completa**, sin tarjeta ni cobro automático.
Luego puede suscribirse por **\$3.490 al mes** (precio de referencia por
validar). Quien no se suscribe mantiene el **nivel básico gratuito**.
Reemplaza la prueba limitada por asignatura de la v1.1. Dos meses
alcanzan a cubrir la toma de ramos y las primeras evaluaciones del
semestre, que es cuando el estudiante percibe el valor.

| **ID** | **Requerimiento** | **Criterio de aceptación** |
|---|---|---|
| PR-01 **ACTUALIZADO** | Activar la prueba completa de 2 meses | Toda cuenta nueva accede a todas las funciones de suscripción durante 2 meses; nunca se solicita tarjeta ni se genera un cobro para activarla |
| PR-02 **ACTUALIZADO** | Mostrar el estado de la prueba | Se ven los días restantes en todo momento y se avisa 7 días y 1 día antes del término |
| PR-03 | Mostrar condiciones antes de empezar | Se identifica qué incluye la prueba, cuánto dura y qué ocurre al terminar |
| PR-04 | Mantener derechos y límites por cuenta | Cambiar de malla, período o dispositivo, o borrar datos, no reinicia la prueba ni concede nuevos derechos |
| PR-05 | Convertir sin pérdida de datos | Al suscribirse se reutiliza todo lo registrado durante la prueba sin volver a ingresarlo |
| PR-06 **ACTUALIZADO** | Mantener acceso al volver al nivel básico | Se puede consultar y exportar todo lo registrado; se bloquean solo las operaciones que requieren suscripción |
| PR-07 **RETIRADO** | Prueba alternativa de siete días (v1.1) | Reemplazada por PR-01. Se conserva el ID para trazabilidad |

### 5.2. Directorio de tutores – incluido en V2.0

Un tutor publica qué enseña y cómo contactarlo. El estudiante explora el
catálogo y conversa directamente por WhatsApp; las condiciones de la
clase se acuerdan entre ellos. Es un **espacio de libre acceso y
gratuito**: una eventual forma de cobro se evaluará más adelante.

| **ID** | **Requerimiento**                    | **Criterio de aceptación**                                                                                                                                                                 |
|--------|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TU-01  | Crear perfil de tutor con cuenta     | Incluye nombre público, presentación, experiencia declarada, modalidad, ubicación si es presencial, disponibilidad general y número de WhatsApp                                            |
| TU-02  | Publicar servicios y tarifas         | Cada servicio detalla materia, descripción, precio y unidad (hora o sesión) o indica a convenir; puede vincularse a cursos, carreras e instituciones del catálogo                          |
| TU-03  | Vincular tutores a asignaturas       | Buscar un ramo devuelve servicios vinculados a ese curso; una materia genérica se distingue de una equivalencia curricular confirmada y no une cursos solo por nombre                      |
| TU-04  | Buscar y filtrar catálogo            | Admite texto, materia o asignatura, carrera, institución, modalidad y rango de precio; sin resultados se informa y permite ampliar filtros; precios a convenir se identifican por separado |
| TU-05  | Mostrar ficha y abrir WhatsApp       | La ficha muestra servicios, tarifas, modalidad y contacto; el botón abre el número publicado con un mensaje editable referido al servicio, sin enviar mensajes automáticamente             |
| TU-06  | Consentir y validar contacto público | Antes de publicar se informa que el número será público y se obtiene aceptación; se valida formato internacional y no se etiqueta como verificado sin comprobarlo                          |
| TU-07  | Editar, pausar o retirar oferta      | El tutor solo gestiona sus propios perfiles y servicios; una publicación pausada o retirada deja de aparecer y no expone el contacto en fichas públicas                                    |
| TU-08  | Revisar publicaciones y reportes     | Perfiles pasan por borrador, pendiente, publicado, rechazado o suspendido; el equipo puede revisar, indicar motivo y retirar publicaciones indebidas                                       |
| TU-09  | Reportar un tutor o servicio         | El estudiante puede reportar contacto incorrecto, spam o información engañosa; el reporte es privado y permite seguimiento                                                                 |
| TU-10  | Mantener transparencia en fichas     | Experiencia y disponibilidad declaradas se identifican como tales; la revisión de publicación no se presenta como certificación docente ni garantía de calidad                             |

Búsqueda, consulta y contacto no requieren suscripción. Publicación
inicial gratuita con revisión. Orden por relevancia a la asignatura y
actualización; no hay posiciones pagadas. Cada servicio muestra su
última actualización y puede marcarse no disponible.

No se incluyen reservas, chat interno, pago de clases ni reseñas en esta
entrega. El directorio no tiene acceso al avance ni a las notas del
estudiante.

## 6. Reglas académicas y modelo de mallas

Estos requisitos son obligatorios antes de habilitar planificación sobre
cualquier malla, sea verificada, comunitaria, importada o personal.

- **Identidad:** institución, carrera, sede o modalidad cuando
  corresponda, versión del plan, régimen de períodos y procedencia. Los
  cursos tendrán identificadores estables dentro de una versión; el
  nombre no será su identidad.

- **Créditos:** registrar el sistema de créditos y valores disponibles.
  No asumir que todos los créditos son SCT ni mezclar unidades
  distintas.

- **Dependencias:** representar todos los prerrequisitos (Y),
  alternativas (O), correquisitos y umbrales de créditos aprobados.
  Conservar el texto original de condiciones no estructuradas.

- **Datos incompletos:** distinguir «no tiene prerrequisitos» de
  «prerrequisitos desconocidos». Una imagen sin flechas no prueba que no
  existan requisitos.

- **Validación:** detectar referencias inexistentes, códigos duplicados
  que requieran revisión, dependencias imposibles, ciclos de
  prerrequisitos y conflictos entre reglas. Los correquisitos se validan
  según su semántica, no como ciclos.

- **Restricciones no soportadas:** mostrarlas como pendientes de
  evaluación y bloquear conclusiones que dependan de ellas. Se puede
  consultar la malla aunque no esté apta para planificar.

- **Oferta:** separar la ubicación curricular de un ramo de su
  disponibilidad real por período. Sin oferta conocida, una proyección
  debe declarar el supuesto utilizado.

- **Electivos:** modelar requisitos por grupo o cupo, evitando contar
  cada alternativa como obligatoria. Prácticas y titulación pueden tener
  reglas propias.

- **Convalidaciones:** registrar la decisión declarada por el estudiante
  y el curso al que aplica; no deducir equivalencias oficiales por
  nombres parecidos.

- **Versiones:** el progreso pertenece al perfil y a su versión de
  malla. Cambiar versión requiere revisar correspondencias y mostrar
  cursos sin equivalencia.

Ejemplos de aceptación: A y B exige ambos; A o B admite cualquiera; un
mínimo de 100 créditos compara créditos completados de la unidad
correcta; un curso sin reglas confirmadas se muestra con disponibilidad
desconocida.

## 7. Importación y comunidad – V2.1

### 7.1. Importación de mallas desde PDF o imagen

Cubre la propuesta del armador de mallas con IA.

| **ID** | **Requerimiento**                               | **Criterio de aceptación**                                                                                                          |
|--------|-------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| IA-01  | Admitir PDF, JPG y PNG con límites configurados | Antes de enviar se informan formatos, tamaño, páginas y cupo; un archivo rechazado no consume una importación exitosa               |
| IA-02  | Extraer estructura a un borrador privado        | Detecta los campos presentes y deja desconocidos los ausentes; conserva documento y página de origen durante la revisión            |
| IA-03  | Revisar y corregir extracción                   | El usuario puede comparar documento y campos, editar cursos y dependencias y revisar incidencias antes de activar                   |
| IA-04  | Validar antes de activar planificación          | Referencias rotas o reglas críticas desconocidas impiden conclusiones de disponibilidad; se admite guardar el borrador              |
| IA-05  | Procesamiento recuperable                       | Se distinguen pendiente, procesando, requiere revisión, completado y fallido; reintentar no duplica mallas ni consumo contabilizado |
| IA-06  | Controlar costo y abuso                         | Se limita consumo por cuenta y total del servicio; al alcanzar un límite se informa y permanece disponible la creación manual       |
| IA-07  | Definir tratamiento del documento               | Se informa finalidad y retención; notas y progreso no se envían al procesamiento de mallas                                          |

Flujo: subir → procesar → revisar → validar → activar como personal →
(opcional) publicar como comunitaria (7.3).

### 7.2. Importación de oferta de secciones NUEVO

Permite subir el PDF o una captura de la oferta de ramos del período
(secciones, días y horas) para usarla en el horario y en el generador de
V2.2. La IA solo extrae datos; nunca decide qué ramos tomar.

| **ID** | **Requerimiento**                       | **Criterio de aceptación**                                                                                       |
|--------|-----------------------------------------|------------------------------------------------------------------------------------------------------------------|
| OF-01  | Importar oferta desde PDF o imagen      | Extrae asignatura, código, sección, días, horas y, si existen, docente y sala, a un borrador privado del período |
| OF-02  | Revisar antes de usar                   | El usuario compara documento y datos, corrige horas y secciones; una oferta sin revisar no alimenta el generador |
| OF-03  | Vincular secciones a cursos de la malla | El vínculo se hace por código o selección del usuario, nunca solo por nombre parecido                            |
| OF-04  | Vigencia por período                    | La oferta queda asociada a un período; al terminar se marca como histórica                                       |
| OF-05  | Compartir oferta revisada (opcional)    | Una oferta revisada puede compartirse con la misma carrera y período, identificada como comunitaria y con fecha  |

### 7.3. Mallas comunitarias NUEVO

Base colaborativa: cuando un estudiante deja una malla completa y
validada, puede publicarla para que otros la usen. Se guarda como una
versión estructurada (por ejemplo, JSON) en la base de datos y se
muestra como **comunitaria**. Las mallas curadas por el equipo se
muestran como **verificadas por MallaPro**. Ninguna se presenta como
oficial de la universidad.

| **ID** | **Requerimiento**                   | **Criterio de aceptación**                                                                                                                                                                                                |
|--------|-------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| MC-01  | Publicar una malla como comunitaria | Es una acción explícita del autor, con aceptación de condiciones; solo se permite si pasa la validación completa de la sección 6 (períodos, cursos, créditos con unidad y prerrequisitos sin ciclos ni referencias rotas) |
| MC-02  | Etiquetar el origen                 | La ficha indica «Comunitaria» o «Verificada por MallaPro», fuente, alias del autor, fecha, versión y cantidad de usuarios                                                                                                 |
| MC-03  | Versionar la malla publicada        | Cada edición genera una nueva versión; quienes la usan no ven cambios silenciosos (CA-03)                                                                                                                                 |
| MC-04  | Detectar duplicados                 | Si ya existe la misma institución, carrera y versión, se ofrece usar la existente o proponer una corrección, mostrando las diferencias                                                                                    |
| MC-05  | Reportar errores                    | Cualquier usuario puede reportar; al superar un umbral configurable de reportes, la malla pasa a revisión                                                                                                                 |
| MC-06  | Promover a verificada               | Un curador revisa, corrige y promueve; se conserva la atribución al autor y se ofrece a los usuarios migrar con revisión de correspondencias                                                                              |

### 7.4. Panel del equipo: comparación y curaduría NUEVO

| **ID** | **Requerimiento**               | **Criterio de aceptación**                                                                                                |
|--------|---------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| AD-04  | Listar y filtrar mallas         | Muestra verificadas, comunitarias y propuestas, filtrables por institución, carrera, uso y reportes                       |
| AD-05  | Comparar dos mallas o versiones | Resalta diferencias de cursos, créditos, períodos y prerrequisitos                                                        |
| AD-06  | Editar, refinar y promover      | Una comunitaria se puede tomar, corregir y publicar como verificada en una nueva versión, con registro de quién la cambió |

## 8. Planificación avanzada – V2.2

| **ID** | **Requerimiento** | **Criterio de aceptación** |
|---|---|---|
| PA-01 | Crear escenarios independientes | Modificar un escenario no altera avance real, notas ni otros escenarios |
| PA-02 | Configurar restricciones | Admite máximo de ramos o créditos, cursos prioritarios, períodos y disponibilidad declarada |
| PA-03 | Generar planes con reglas deterministas | Ningún plan considera aprobado un curso solo por incluirlo en el mismo período si exige aprobación previa |
| PA-04 | Comparar alternativas | Muestra carga, cursos desbloqueados, períodos estimados, restricciones e hipótesis diferentes |
| PA-05 | Explicar recomendaciones | Cada sugerencia identifica reglas y datos utilizados; una explicación con IA no puede modificar el resultado del motor |
| PA-06 | Simular reprobación o convalidación | Cambia exclusivamente el escenario y recalcula dependencias y proyección |
| PA-07 | Declarar límites de las proyecciones | Sin oferta o información de cupos no promete fecha exacta de egreso; si no hay solución factible explica las restricciones incompatibles |
| PA-08 **NUEVO** | Generar combinaciones de horario sin topes | A partir de la oferta revisada (OF-02) y de los ramos disponibles según el avance, genera combinaciones sin topes con filtros: días libres, jornada, máximo de ramos o créditos y ramos prioritarios. El motor es determinista |
| PA-09 **NUEVO** | Explicar exclusiones | Para cada ramo que no entra se indica el motivo: prerrequisito pendiente, tope, sin oferta o restricción del usuario |

Con la oferta importada (7.2), una preferencia como «no quiero clases
los lunes» sí puede resolverse. Sin oferta, se planifica carga y
dependencias, pero no días de asistencia.

### 8.1. Sugerencias de configuración por coincidencia – posterior NUEVO

Las notas son privadas, pero el sistema puede detectar cuándo muchos
estudiantes configuraron igual una asignatura (mismas evaluaciones y
porcentajes, misma carrera e institución) y ofrecer esa estructura como
borrador para aplicarla sin repetir el trabajo. Complementa el compartir
explícito (NO-04).

| **ID** | **Requerimiento**                             | **Criterio de aceptación**                                                                                                                   |
|--------|-----------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| SC-01  | Detectar coincidencias solo con la estructura | Se comparan cantidad de evaluaciones, ponderaciones y escala; nunca notas, nombres de usuarios ni texto libre                                |
| SC-02  | Umbral mínimo configurable                    | La sugerencia aparece al superar un mínimo de configuraciones idénticas en la misma asignatura, carrera, institución y período (ver Anexo A) |
| SC-03  | Aplicar como borrador editable                | El estudiante la aplica con un clic, puede renombrar evaluaciones y nada se sobrescribe sin confirmación                                     |
| SC-04  | Mostrar alternativas                          | Si hay varias configuraciones frecuentes (por sección o docente), se muestran las alternativas con su frecuencia aproximada                  |
| SC-05  | Permitir excluirse                            | El estudiante puede excluir sus configuraciones del cálculo agregado                                                                         |

## 9. Monetización ACTUALIZADO

**Modelo:** freemium con prueba gratuita. Cada cuenta nueva tiene 2
meses con todo incluido; luego, suscripción mensual de **\$3.490**
(referencia por validar), cancelable en cualquier momento, o nivel
básico gratuito. **Sin publicidad.** Buscar y contactar tutores es
gratuito; publicar un perfil básico de tutor también.

| **Función**                                    | **Nivel básico (gratis)**       | **Prueba de 2 meses / suscripción** |
|------------------------------------------------|---------------------------------|-------------------------------------|
| Catálogo, malla y progreso                     | Incluido                        | Incluido                            |
| Cuenta y sincronización                        | Incluido                        | Incluido                            |
| Compartir e importar configuraciones de ramos  | Incluido                        | Incluido                            |
| Usar mallas comunitarias y verificadas         | Incluido                        | Incluido                            |
| Crear malla personal manual                    | Ver decisión pendiente          | Incluido                            |
| Notas, calculadora y eximición                 | Consulta de lo registrado       | Incluido                            |
| Registro histórico                             | Consulta y exportación          | Incluido                            |
| Horario y toma de ramos                        | Plan básico del próximo período | Incluido                            |
| Importación con IA (mallas y oferta)           | —                               | Cupo configurable                   |
| Escenarios, simulación y generador de horarios | Vista de demostración           | Incluido                            |
| Directorio de tutores                          | Incluido                        | Incluido                            |
| Exportación de datos personales                | Incluido                        | Incluido                            |

| **ID** | **Requerimiento**                             | **Criterio de aceptación**                                                                                                                     |
|--------|-----------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| CO-01  | Mostrar planes y condiciones                  | Indica precio final, moneda, duración, renovación si existe, cupos y funciones antes de pagar                                                  |
| CO-02  | Confirmar pagos desde el servidor             | La página de retorno no activa la suscripción por sí sola; se verifica el evento del proveedor                                                 |
| CO-03  | Procesar eventos de pago de forma idempotente | Eventos duplicados o fuera de orden no duplican beneficios ni extienden períodos incorrectamente                                               |
| CO-04  | Controlar permisos y cupos en servidor        | Cambiar el navegador no desbloquea funciones ni reinicia consumo                                                                               |
| CO-05  | Gestionar vencimiento, cancelación y fallos   | Se muestran estado y fecha de acceso; el usuario puede cancelar la renovación mensual en cualquier momento                                     |
| CO-06  | Conservar datos al volver al nivel básico     | Expirar la suscripción no elimina notas, progreso ni escenarios; permite consultar y exportar, y restringe solo las operaciones de suscripción |
| CO-07  | Gestionar soporte de pagos                    | Existe registro de transacciones e incidencias y procedimiento para devoluciones según condiciones definidas                                   |

Los cupos de IA se fijan tras medir costos; no habrá IA ilimitada.
Proveedor de pagos y obligaciones comerciales deben resolverse antes de
habilitar cobros.

## 10. Requerimientos no funcionales

| **ID** | **Requerimiento** | **Criterio de aceptación** |
|---|---|---|
| NF-01 | Privacidad y aislamiento | Pruebas con dos cuentas impiden leer o modificar mallas privadas, archivos, notas y horarios ajenos |
| NF-02 | Secretos y privilegios en servidor | No se incluyen credenciales privilegiadas ni claves de IA en el frontend; el equipo tiene permisos independientes |
| NF-03 | Integridad y conflictos de edición | Reintentos no duplican operaciones; ante cambios concurrentes se detecta conflicto y se ofrece recargar o resolver sin sobrescritura silenciosa |
| NF-04 | Rendimiento | Objetivo provisional: malla de 100 cursos utilizable en hasta 3 s en perfil móvil documentado; cambios visuales locales en hasta 200 ms. Importación asíncrona |
| NF-05 | Accesibilidad y móvil | Flujos principales funcionan desde 360 px y con teclado; estados no dependen solo del color; acciones disponibles sin Ctrl+clic |
| NF-06 | Respaldo y recuperación | Objetivo provisional: pérdida máxima de 24 h y recuperación en 24 h; restauración probada antes del lanzamiento comercial |
| NF-07 | Errores observables | Cada fallo tiene estado útil para el usuario y diagnóstico sin exponer notas, documentos o secretos en registros |
| NF-08 | Configuración operativa | Cupos, planes y límites pueden ajustarse sin alterar el cálculo académico; existe aviso al acercarse al presupuesto de procesamiento |
| NF-09 | Calidad | Casos de prueba cubren dependencias, cálculos de notas, topes, aislamiento, importaciones y ciclo de pago |
| NF-10 **NUEVO** | Privacidad en datos agregados | Las sugerencias (SC) y métricas del panel solo muestran agregados que superan un mínimo de anonimato; no permiten identificar a un estudiante ni deducir sus notas |
| NF-11 **NUEVO** | Registro de auditoría del equipo | Toda acción de curadores y superadministrador sobre mallas, roles, tutores o datos de soporte queda registrada con fecha y autor |
| NF-12 **NUEVO** | Infraestructura escalable | Arquitectura inicial en un VPS; el diseño permite separar la base de datos y migrar a servicios independientes si la demanda lo justifica, sin cambiar el modelo de datos |

### 10.1. Stack tecnológico (actualizado al repositorio)

**Criterios:** reutilizar lo que ya existe (frontend React y mallas en JSON), ajustarse al costo fijo de un VPS (US$120–150 al año) y preferir herramientas de código abierto. La arquitectura es un **monolito modular**: un solo backend dividido en módulos (cuentas, catálogo, avance, notas, horario, tutores, equipo y, después, importación y pagos) que pueden separarse si la demanda lo justifica (NF-12).

| Capa | Tecnología | Por qué | Cubre |
|---|---|---|---|
| Frontend | React 19 + Vite + Tailwind + React Router (JavaScript) | Es el frontend de la versión pública; funciona también sin backend con las mallas estáticas | CU-03, NF-04, NF-05 |
| Reglas académicas en la interfaz | Módulos JS puros con pruebas en Vitest (disponibilidad, notas, topes) | Deterministas y separados de la IA; los casos de referencia se comparten con el backend como datos | NO-01 a NO-03, HO-02, AV-04 |
| Backend / API | Python 3.12 + FastAPI, API REST en `/api/v1` | Ya implementado (base, auth y catálogo); tipado con Pydantic v2 | NF-02, CO-04 |
| Validación | Pydantic v2 en el backend; el árbol de prerrequisitos tiene esquema propio (`app/schemas/prereq.py`) | Un solo esquema valida mallas legadas, manuales, importadas y comunitarias | Sección 6, IA-04, MC-01 |
| Base de datos | PostgreSQL 16 con SQLAlchemy 2 (async, asyncpg) y Alembic; JSONB para árboles de prerrequisitos y atributos | Relacional para cuentas, permisos y pagos; JSONB conserva lo que el modelo no representa | CA-03, MC-03, NF-03 |
| Autenticación | Firebase Authentication (Google) en el frontend; el backend verifica el ID token con firebase-admin y guarda el usuario en Postgres | Firebase solo identifica; todos los datos viven en Postgres | CU-01, NF-01, NF-02 |
| Roles y auditoría | Roles en Postgres (estudiante, curador, superadministrador) verificados en el backend, y tabla de auditoría | Los permisos nunca dependen del navegador | AD-01 a AD-08, NF-11 |
| Tareas en segundo plano | Cola en PostgreSQL (sin Redis por ahora) | Una pieza menos que operar; suficiente para avisos, limpieza e importaciones | IA-05, PR-02, NF-04 |
| Archivos | Disco del VPS al inicio; almacenamiento compatible con S3 si crece | PDF e imágenes de mallas y ofertas, con política de retención | IA-01, IA-07, OF-01 |
| Importación con IA | Modelo con visión llamado solo desde el backend, salida validada con Pydantic; parser para formatos conocidos (Banner UNAB) | El parser es barato pero frágil; la IA cubre formatos nuevos | IA-01 a IA-06, OF-01 |
| Pagos | Mercado Pago o Flow / Transbank Webpay (a evaluar); webhooks idempotentes | Medios locales y cobro mensual en pesos | CO-01 a CO-07 |
| Correo transaccional | Resend o Amazon SES (a evaluar) | Avisos de la prueba y del sistema | PR-02 |
| Analítica | Google Analytics 4 más tabla de eventos propia en PostgreSQL | Eventos de la sección 13 sin datos personales | AN-01, AD-07, AD-08 |
| Contacto con tutores | Enlaces wa.me con mensaje prellenado | Sin costo y sin envío automático | TU-05 |
| Infraestructura | VPS Linux con Docker Compose y Caddy (HTTPS); el frontend puede seguir en Netlify, Vercel o cPanel | Dentro del costo fijo | NF-12 |
| Respaldo y monitoreo | Copia diaria cifrada de la base, restauración probada, Uptime Kuma y Sentry | Objetivos de recuperación y errores observables | NF-06, NF-07 |
| Calidad y despliegue | GitHub Actions; pytest y ruff en el backend; Vitest y ESLint en el frontend; Playwright para flujos completos | Cada cambio pasa por pruebas antes de publicarse | NF-09 |

**Migración desde la versión pública (CU-05):** el frontend ya guarda el avance por carrera (`career_key`) e id de curso; al crear la cuenta, lee esos datos, los muestra y los envía a la API. Las mallas de `frontend/public/mallas/` se importan como primeras versiones del catálogo (`import_legacy_mallas`).

**Costos:** las herramientas son de código abierto o tienen planes gratuitos suficientes para el piloto. Los costos variables nuevos son la IA (por malla procesada), la comisión de pagos, el correo sobre su plan gratuito y el almacenamiento de respaldos.

## 11. Datos y límites de responsabilidad

A las entidades de la v1.1 se agregan: **configuración compartida de
ramo, malla comunitaria, reporte de malla, oferta de secciones, sección
importada, sugerencia de configuración, rol del equipo y registro de
auditoría.**

Separaciones obligatorias adicionales: configuración compartida frente a
notas del estudiante; malla comunitaria frente a malla verificada;
oferta importada frente a oferta oficial de la universidad. El sistema
organiza información y realiza simulaciones; no se integra con matrícula
ni certifica aprobaciones.

## 12. Experiencia y pantallas

Se mantienen las 12 pantallas de la v1.1 y se agregan:

- **Comunidad de mallas:** búsqueda con etiqueta comunitaria o
  verificada, publicar mi malla y reportar errores (V2.1).

- **Compartir ramo:** botón para generar enlace o código desde cada
  asignatura, e importar desde un enlace recibido (V2.0).

- **Oferta y generador:** importar oferta, revisarla y generar
  combinaciones de horario (V2.1–V2.2).

- **Panel del equipo:** mallas, comparación, promoción, reportes,
  tutores, roles, métricas de uso y, para el superadministrador,
  métricas comerciales.

- **Estado de la prueba:** días restantes visibles en el panel y aviso
  antes del término.

## 13. Analíticas y validación de negocio

A los eventos de la v1.1 se agregan: configuracion_compartida,
configuracion_importada, malla_comunitaria_publicada, malla_reportada,
malla_promovida_verificada, oferta_importada, horarios_generados,
sugerencia_configuracion_aplicada, prueba_iniciada, prueba_finalizada,
suscripcion_iniciada, suscripcion_cancelada y datos_locales_importados.

### Métricas del panel del equipo **NUEVO**

| **ID** | **Requerimiento**                              | **Criterio de aceptación**                                                                                                                                                       |
|--------|------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| AD-07  | Métricas de uso                                | Usuarios activos diarios y mensuales, registros, mallas más usadas, búsquedas sin resultado, configuraciones compartidas e importadas, recurrencia entre períodos; todo agregado |
| AD-08  | Métricas comerciales (solo superadministrador) | Pruebas activas, conversión de prueba a suscripción, suscriptores activos, ingresos mensuales, cancelaciones y costo de IA por usuario                                           |

**Indicadores adicionales:** crecimiento por compartir (usuarios nuevos
que llegan por un enlace de configuración) y cobertura (universidades y
carreras con al menos una malla comunitaria o verificada).

**Metas de referencia** del informe de modelo de negocios: 300 usuarios
activos el próximo semestre, 800 en un año y 3% de conversión a
suscripción. Se ajustarán con la línea base del piloto; la línea base
actual es de 42 usuarios activos en 28 días (Google Analytics, 10 de
septiembre al 7 de octubre de 2026).

**Validación previa al cobro:** antes de habilitar pagos, mostrar
durante una toma de ramos un acceso «Plan completo (próximamente)» y
medir cuántos usuarios muestran interés, junto con una encuesta breve de
disposición a pagar.

## 14. Migración y liberación

La versión actual no tiene cuentas y guarda los datos solo en el
navegador. La migración (CU-05) debe detectar esos datos al crear la
cuenta, mostrar qué se importará, conservar el origen hasta confirmar y
no duplicar al repetir. Además: permitir respaldar datos anteriores,
detectar cursos sin equivalencia y no fusionar carreras por IDs
coincidentes. V2 se liberará con un grupo piloto antes de reemplazar la
versión pública, con opción de desactivar importación o cobros ante
incidencias.

## 15. Fuera del primer alcance

- Chat general de IA o tutor académico para cualquier materia.

- Inscripción directa de ramos, extracción automática desde portales
  universitarios y sincronización institucional.

- Reservas, cobro de tutorías, comisiones, pagos a tutores y reseñas.

- Aplicaciones móviles nativas, red social y mensajería entre
  estudiantes.

- **ACTUALIZADO** **Verificación automática por coincidencia de
  cargas.** La publicación comunitaria explícita y validada sí entra
  (7.3), pero coincidir con otras cargas no convierte una malla en
  verificada.

- Importación por enlaces o Excel.

- **NUEVO** **Publicidad dentro de MallaPro.**

- Planes institucionales y venta de datos académicos.

## 16. Orden del trabajo

1.  Cerrar reglas académicas, estados y modelo de datos (incluidas
    configuraciones compartidas y mallas comunitarias); inventariar la
    versión real y su almacenamiento local.

2.  Diseñar incorporación, malla, progreso, compartir ramos y límites de
    permisos.

3.  Implementar cuentas, persistencia, migración de datos locales,
    catálogo y editor personal.

4.  Integrar notas y horario, compartir configuraciones, plan básico,
    directorio de tutores, panel básico y métricas de uso.

5.  Probar V2.0 con estudiantes y resolver fallos de datos y usabilidad.

6.  Implementar importación de mallas y de oferta, mallas comunitarias y
    curaduría; medir costos de IA (V2.1).

7.  Probar planificación avanzada, generador de horarios y disposición a
    pagar (prueba de interés y encuesta).

8.  Integrar prueba de 2 meses, suscripción, cobros y métricas
    comerciales; liberar V2.2.

La definición de terminado de la v1.1 se mantiene: criterios de
aceptación aprobados, flujo funcionando en móvil y escritorio, sin
pérdida de datos ni acceso entre cuentas, errores recuperables y eventos
que permitan medir el resultado.

## 17. Decisiones pendientes ACTUALIZADO

| **Decisión**                       | **Propuesta de trabajo**                                                                                                               | **Debe cerrarse antes de**   |
|------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|------------------------------|
| Mercado inicial                    | Chile, partiendo por la UNAB; expansión mediante mallas personales, importadas y comunitarias                                          | Diseño de catálogo           |
| Crear malla manual en nivel básico | Recomendación: gratis, porque alimenta la base comunitaria y la expansión a otras universidades (ver Anexo A)                          | Implementar permisos         |
| Precio y prueba                    | 2 meses gratis y \$3.490 al mes como referencia; validar con prueba de interés y encuesta                                              | Habilitar cobros             |
| Inicio de la prueba                | Evaluar que los 2 meses comiencen con la primera acción de suscripción y no al registrarse, para que no se agoten en vacaciones        | Lanzamiento comercial        |
| Beneficio para usuarios actuales   | Evaluar un beneficio de «usuario fundador» (por ejemplo, prueba extendida) para quienes ya usan MallaPro                               | Migración pública            |
| Umbral de sugerencias (SC-02)      | Configurable; propuesta inicial de 15 a 20 coincidencias en lugar de 100                                                               | Habilitar sugerencias        |
| Etiquetas de origen de mallas      | «Verificada por MallaPro» y «Comunitaria»; evitar «oficial»                                                                            | Publicar mallas comunitarias |
| Límites de importación             | Configurables según costo y calidad medidos                                                                                            | Abrir importación pública    |
| Proveedores e infraestructura | Stack de 10.1 (Python/FastAPI, Firebase). Por decidir: proveedor de pagos, de IA y de correo | Implementación técnica |
| Retención de documentos            | Política explícita con plazos definidos                                                                                                | Procesar archivos reales     |

## 18. Cambios de la versión 1.2

- La monetización adopta el modelo del informe de negocios: 2 meses de
  prueba completa, suscripción de \$3.490 al mes como referencia y nivel
  básico gratuito; sin publicidad. La prueba limitada por asignatura
  (PR-07) queda retirada.

- Nuevos requisitos: compartir e importar configuraciones de ramos
  (NO-04, NO-05) y migración de datos locales (CU-05) en V2.0.

- Nuevos módulos: importación de oferta de secciones (OF), mallas
  comunitarias (MC), generador de horarios (PA-08, PA-09) y sugerencias
  por coincidencia (SC).

- Panel del equipo con roles de curador y superadministrador,
  comparación y promoción de mallas, métricas de uso y comerciales
  (AD-04 a AD-08), auditoría (NF-11) e infraestructura escalable
  (NF-12).

- Se agrega el stack tecnológico propuesto (10.1), ligado a los
  requisitos que cubre, y se actualiza el punto de partida con el MVP
  real (React, Netlify y mallas en JSON).

- Se agrega el Anexo A con la evaluación de cada propuesta.

## Anexo A. Evaluación de las propuestas

Valor: impacto para el estudiante o para el negocio. Esfuerzo:
complejidad técnica y de operación. Escala: alto, medio, bajo.

| **Propuesta**                                                                    | **Valor**      | **Esfuerzo** | **Evaluación**                                                                                                                                                                                                                                  | **Recomendación**                                                                                                                                                                                        |
|----------------------------------------------------------------------------------|----------------|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1\. Armador de mallas con IA desde PDF o imagen                                  | Alto           | Medio-alto   | Clave para salir de la UNAB sin cargar cada malla a mano. Ya estaba contemplado en V2.1 (IA-01 a IA-07). El riesgo principal son errores de extracción en prerrequisitos.                                                                       | Mantener en V2.1 con revisión obligatoria y cupos. Medir costo por malla activada.                                                                                                                       |
| 2\. Horarios y secciones con IA desde PDF o imagen, considerando ramos aprobados | Muy alto       | Alto         | Ataca directo el dolor central (la toma de ramos a ciegas). Los formatos de oferta varían mucho entre universidades y un error de horas genera topes falsos.                                                                                    | Separar en dos: extracción con IA y revisión (OF, V2.1) y generador determinista (PA-08, V2.2). Partir solo con el formato de la UNAB.                                                                   |
| 3\. Base de mallas colaborativa (no oficial / oficial)                           | Alto           | Medio        | Es la forma más barata de ganar cobertura frente a competidores con muchas universidades. El riesgo es la calidad: una malla mal cargada se propaga.                                                                                            | Sí, en V2.1, con validación completa antes de publicar, reportes y versiones. Usar «Comunitaria» y «Verificada por MallaPro» en vez de «oficial», que podría entenderse como respaldo de la universidad. |
| 4\. Notas privadas con detección de configuraciones repetidas                    | Medio-alto     | Medio        | Ahorra trabajo sin pedirle nada al estudiante. Con 100 coincidencias como umbral y una meta de 800 usuarios en total, casi nunca se activaría en una asignatura de una carrera. Además, las ponderaciones pueden cambiar por sección o docente. | Dejar para después de V2.2 con umbral configurable (15–20) y mínimo de anonimato. Priorizar antes el compartir explícito (NO-04), que da el mismo beneficio desde el día uno.                            |
| 5\. Panel superadmin para el equipo                                              | Alto (interno) | Medio        | Necesario para curar mallas comunitarias y decidir con datos. Mezcla datos sensibles (ventas) con operación diaria.                                                                                                                             | Separar roles: curador (mallas, reportes, uso) y superadministrador (roles, precios, ventas). Básico en V2.0, comparación en V2.1, ventas en V2.2. Auditoría de acciones.                                |
| Compartir configuración de ramo (discutida en el informe)                        | Alto           | Bajo         | Bajo costo, alto impacto y principal motor de crecimiento entre compañeros. No estaba en la v1.1.                                                                                                                                               | Incluir en V2.0 y en el nivel básico gratuito.                                                                                                                                                           |
| Prueba de 2 meses y \$3.490 al mes (informe)                                     | Alto (negocio) | Medio        | Coherente con el informe y simple de comunicar. Riesgo: si la prueba parte en vacaciones, se agota sin uso.                                                                                                                                     | Adoptado en v1.2. Evaluar que la prueba comience con la primera acción de suscripción.                                                                                                                   |
