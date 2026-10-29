# Trazabilidad requisito → tarea → prueba

Generado con `python3 tools/docs/traceability.py` desde los requerimientos y el backlog. La columna **Pruebas** la completa el implementador al cerrar cada tarea (ruta del archivo y nombre del caso) y se conserva al regenerar.

| ID | Requisito | Entrega | Tareas | Pruebas |
|---|---|---|---|---|
| AD-01 | Administrar catálogo y revisión | V2.0 | T-002, T-031, T-050 |  |
| AD-02 | Recibir y gestionar reportes | V2.0 | T-034, T-050 |  |
| AD-03 | Gestionar roles del equipo | V2.0 | T-002, T-050 |  |
| AD-04 | Listar y filtrar mallas | V2.1 | épica V2.1 · Mallas comunitarias y curaduría |  |
| AD-05 | Comparar dos mallas o versiones | V2.1 | épica V2.1 · Mallas comunitarias y curaduría |  |
| AD-06 | Editar, refinar y promover | V2.1 | épica V2.1 · Mallas comunitarias y curaduría |  |
| AD-07 | Métricas de uso | V2.0 | T-052 |  |
| AD-08 | Métricas comerciales (solo superadministrador) | V2.2 | épica V2.2 · Prueba de 2 meses y suscripción |  |
| AN-01 | Medir uso del producto | V2.0 | T-051 |  |
| AV-01 | Registrar estado actual de cada curso | V2.0 | T-021 |  |
| AV-02 | Mantener intentos por período | V2.0 | T-021 |  |
| AV-03 | Mostrar avance | V2.0 | T-016 |  |
| AV-04 | Explicar disponibilidad de un curso | V2.0 | T-012 |  |
| AV-05 | Registrar excepciones personales | V2.0 | T-024 |  |
| AV-06 | Cambios masivos con revisión y recuperación | V2.0 | T-026 |  |
| CA-01 | Buscar catálogo por institución y carrera | V2.0 | T-010, T-030, s03 (parcial) | `backend/tests/test_catalog.py::test_universities_endpoint`, `::test_programs_endpoint_lists_uch_in_order`, `::test_uch_programs_belong_to_their_own_university`; `frontend/src/utils/verifiedMallas.test.js` › "lista UNAB y U. de Chile por separado" (T-010) |
| CA-02 | Separar mallas de catálogo y mallas personales | V2.0 | T-030, T-032 |  |
| CA-03 | Versionar el catálogo | V2.0 | T-031, s03 (parcial) |  |
| CO-01 | Mostrar planes y condiciones | V2.2 | épica V2.2 · Prueba de 2 meses y suscripción |  |
| CO-02 | Confirmar pagos desde el servidor | V2.2 | épica V2.2 · Prueba de 2 meses y suscripción |  |
| CO-03 | Procesar eventos de pago de forma idempotente | V2.2 | épica V2.2 · Prueba de 2 meses y suscripción |  |
| CO-04 | Controlar permisos y cupos en servidor | V2.2 | T-002, épica V2.2 · Prueba de 2 meses y suscripción |  |
| CO-05 | Gestionar vencimiento, cancelación y fallos | V2.2 | épica V2.2 · Prueba de 2 meses y suscripción |  |
| CO-06 | Conservar datos al volver al nivel básico | V2.2 | épica V2.2 · Prueba de 2 meses y suscripción |  |
| CO-07 | Gestionar soporte de pagos | V2.2 | épica V2.2 · Prueba de 2 meses y suscripción |  |
| CU-01 | Registro, inicio y cierre de sesión; al menos un método de autenticación | V2.0 | s02 |  |
| CU-02 | Perfil académico con institución, carrera, versión de malla y régimen de períodos | V2.0 | T-020 |  |
| CU-03 | Sincronización y estado de guardado | V2.0 | T-005, T-022 |  |
| CU-04 | Exportar datos y solicitar eliminación de cuenta | V2.0 | T-053 |  |
| CU-05 | Importar datos guardados en el navegador por la versión actual | V2.0 | T-023 |  |
| HO-01 | Crear horario con asignaturas, secciones y bloques | V2.0 | T-027 |  |
| HO-02 | Detectar topes | V2.0 | T-014 |  |
| HO-03 | Guardar y exportar horario | V2.0 | T-027 |  |
| HO-04 | Diferenciar planificación e inscripción | V2.0 | T-027 |  |
| IA-01 | Admitir PDF, JPG y PNG con límites configurados | V2.1 | épica V2.1 · Importación con IA de mallas |  |
| IA-02 | Extraer estructura a un borrador privado | V2.1 | épica V2.1 · Importación con IA de mallas |  |
| IA-03 | Revisar y corregir extracción | V2.1 | épica V2.1 · Importación con IA de mallas |  |
| IA-04 | Validar antes de activar planificación | V2.1 | T-015, épica V2.1 · Importación con IA de mallas |  |
| IA-05 | Procesamiento recuperable | V2.1 | épica V2.1 · Importación con IA de mallas |  |
| IA-06 | Controlar costo y abuso | V2.1 | épica V2.1 · Importación con IA de mallas |  |
| IA-07 | Definir tratamiento del documento | V2.1 | épica V2.1 · Importación con IA de mallas |  |
| MC-01 | Publicar una malla como comunitaria | V2.1 | T-015, épica V2.1 · Mallas comunitarias y curaduría |  |
| MC-02 | Etiquetar el origen | V2.1 | épica V2.1 · Mallas comunitarias y curaduría |  |
| MC-03 | Versionar la malla publicada | V2.1 | épica V2.1 · Mallas comunitarias y curaduría |  |
| MC-04 | Detectar duplicados | V2.1 | épica V2.1 · Mallas comunitarias y curaduría |  |
| MC-05 | Reportar errores | V2.1 | épica V2.1 · Mallas comunitarias y curaduría |  |
| MC-06 | Promover a verificada | V2.1 | épica V2.1 · Mallas comunitarias y curaduría |  |
| MP-01 | Crear y editar una malla personal manualmente | V2.0 | T-032 |  |
| MP-02 | Mostrar malla y conexiones | V2.0 | T-033 |  |
| MP-03 | Reportar un error o proponer una malla para revisión | V2.0 | T-034 |  |
| NF-01 | Privacidad y aislamiento | Transversal | T-004, T-029 |  |
| NF-02 | Secretos y privilegios en servidor | Transversal | T-060 |  |
| NF-03 | Integridad y conflictos de edición | Transversal | T-005, T-022 |  |
| NF-04 | Rendimiento | Transversal | T-033 |  |
| NF-05 | Accesibilidad y móvil | Transversal | T-033 |  |
| NF-06 | Respaldo y recuperación | Transversal | T-061 |  |
| NF-07 | Errores observables | Transversal | T-003, T-062 |  |
| NF-08 | Configuración operativa | Transversal | épica V2.1 · Importación con IA de mallas |  |
| NF-09 | Calidad | Transversal | T-006, T-063 |  |
| NF-10 | Privacidad en datos agregados | Transversal | T-052, épica Posterior · Sugerencias por coincidencia |  |
| NF-11 | Registro de auditoría del equipo | Transversal | T-002, T-031, T-042 |  |
| NF-12 | Infraestructura escalable | Transversal | T-060 |  |
| NO-01 | Registrar evaluaciones, notas y ponderaciones por intento | V2.0 | T-013, T-025 |  |
| NO-02 | Configurar escala y calcular nota necesaria | V2.0 | T-013, T-025 |  |
| NO-03 | Separar cálculo y aprobación | V2.0 | T-013, T-025 |  |
| NO-04 | Compartir la configuración de un ramo mediante enlace o código | V2.0 | T-029 |  |
| NO-05 | Importar una configuración compartida | V2.0 | T-029 |  |
| OF-01 | Importar oferta desde PDF o imagen | V2.1 | épica V2.1 · Importación de oferta |  |
| OF-02 | Revisar antes de usar | V2.1 | épica V2.1 · Importación de oferta |  |
| OF-03 | Vincular secciones a cursos de la malla | V2.1 | épica V2.1 · Importación de oferta |  |
| OF-04 | Vigencia por período | V2.1 | épica V2.1 · Importación de oferta |  |
| OF-05 | Compartir oferta revisada (opcional) | V2.1 | épica V2.1 · Importación de oferta |  |
| PA-01 | Crear escenarios independientes | V2.2 | épica V2.2 · Planificación avanzada y generador de horarios |  |
| PA-02 | Configurar restricciones | V2.2 | épica V2.2 · Planificación avanzada y generador de horarios |  |
| PA-03 | Generar planes con reglas deterministas | V2.2 | épica V2.2 · Planificación avanzada y generador de horarios |  |
| PA-04 | Comparar alternativas | V2.2 | épica V2.2 · Planificación avanzada y generador de horarios |  |
| PA-05 | Explicar recomendaciones | V2.2 | épica V2.2 · Planificación avanzada y generador de horarios |  |
| PA-06 | Simular reprobación o convalidación | V2.2 | épica V2.2 · Planificación avanzada y generador de horarios |  |
| PA-07 | Declarar límites de las proyecciones | V2.2 | épica V2.2 · Planificación avanzada y generador de horarios |  |
| PA-08 | Generar combinaciones de horario sin topes | V2.2 | épica V2.2 · Planificación avanzada y generador de horarios |  |
| PA-09 | Explicar exclusiones | V2.2 | épica V2.2 · Planificación avanzada y generador de horarios |  |
| PL-01 | Seleccionar ramos para el próximo período | V2.0 | T-028 |  |
| PR-01 | Activar la prueba completa de 2 meses | V2.2 | épica V2.2 · Prueba de 2 meses y suscripción |  |
| PR-02 | Mostrar el estado de la prueba | V2.2 | épica V2.2 · Prueba de 2 meses y suscripción |  |
| PR-03 | Mostrar condiciones antes de empezar | V2.2 | épica V2.2 · Prueba de 2 meses y suscripción |  |
| PR-04 | Mantener derechos y límites por cuenta | V2.2 | épica V2.2 · Prueba de 2 meses y suscripción |  |
| PR-05 | Convertir sin pérdida de datos | V2.2 | épica V2.2 · Prueba de 2 meses y suscripción |  |
| PR-06 | Mantener acceso al volver al nivel básico | V2.2 | épica V2.2 · Prueba de 2 meses y suscripción |  |
| SC-01 | Detectar coincidencias solo con la estructura | Posterior | épica Posterior · Sugerencias por coincidencia |  |
| SC-02 | Umbral mínimo configurable | Posterior | épica Posterior · Sugerencias por coincidencia |  |
| SC-03 | Aplicar como borrador editable | Posterior | épica Posterior · Sugerencias por coincidencia |  |
| SC-04 | Mostrar alternativas | Posterior | épica Posterior · Sugerencias por coincidencia |  |
| SC-05 | Permitir excluirse | Posterior | épica Posterior · Sugerencias por coincidencia |  |
| TU-01 | Crear perfil de tutor con cuenta | V2.0 | T-040 |  |
| TU-02 | Publicar servicios y tarifas | V2.0 | T-040 |  |
| TU-03 | Vincular tutores a asignaturas | V2.0 | T-041 |  |
| TU-04 | Buscar y filtrar catálogo | V2.0 | T-041 |  |
| TU-05 | Mostrar ficha y abrir WhatsApp | V2.0 | T-041 |  |
| TU-06 | Consentir y validar contacto público | V2.0 | T-040 |  |
| TU-07 | Editar, pausar o retirar oferta | V2.0 | T-040 |  |
| TU-08 | Revisar publicaciones y reportes | V2.0 | T-042 |  |
| TU-09 | Reportar un tutor o servicio | V2.0 | T-042 |  |
| TU-10 | Mantener transparencia en fichas | V2.0 | T-040, T-041 |  |

Requisitos sin tarea asignada: ninguno.
PR-07 está retirado y no se implementa.
