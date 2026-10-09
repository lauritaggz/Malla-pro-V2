/**
 * Adaptador entre la API de catálogo (/api/v1/programs/{id}/curriculum) y el formato JSON
 * legado de public/mallas/*.json, para que mapMallaData y la UI no cambien.
 */

export class UnsupportedPrereqError extends Error {
  constructor(message = "Árbol de prerrequisitos no soportado por la UI actual") {
    super(message);
    this.name = "UnsupportedPrereqError";
  }
}

/**
 * Hoy la UI solo aplica "todos los prerrequisitos aprobados" (AND de ids).
 * Si la API entrega OR o créditos mínimos, no se puede representar sin cambiar la
 * semántica: se lanza para que el cargador use los JSON estáticos.
 */
function idsFromTree(tree, legacyIdOf) {
  if (!tree) return [];
  if (tree.course) return [legacyIdOf(tree.course)];
  if (tree.op === "and" && Array.isArray(tree.items)) {
    return tree.items.flatMap((item) => idsFromTree(item, legacyIdOf));
  }
  throw new UnsupportedPrereqError();
}

/**
 * @param {object} api Respuesta de GET /programs/{id}/curriculum
 * @returns {object} Mismo shape que public/mallas/*.json
 */
export function apiCurriculumToLegacyJson(api) {
  const byId = new Map(api.courses.map((c) => [c.id, c]));

  const legacyIdOf = (uuid) => {
    const course = byId.get(uuid);
    if (!course || course.legacy_id == null) {
      throw new Error(`Curso sin id legado en la respuesta de la API: ${uuid}`);
    }
    return course.legacy_id;
  };

  const toLegacyCourse = (c) => {
    const out = {
      id: c.legacy_id,
      codigo: c.code,
      nombre: c.name,
      sct: c.credits,
      prerrequisitos: idsFromTree(c.prereq_expr, legacyIdOf),
    };
    if (c.prereq_raw !== null && c.prereq_raw !== undefined) out.prereq_expr = c.prereq_raw;
    const hasCoreq = c.coreq_expr != null || c.coreq_raw != null;
    if (hasCoreq) out.correquisitos = idsFromTree(c.coreq_expr, legacyIdOf);
    if (c.coreq_raw != null) out.correq_expr = c.coreq_raw;
    return { ...out, ...(c.attrs || {}) };
  };

  const periodsFor = (trackCode) =>
    api.periods
      .filter((p) => (p.track_code ?? null) === trackCode)
      .map((p) => ({
        numero: p.number,
        cursos: p.course_ids.map((id) => toLegacyCourse(byId.get(id))),
      }));

  const hasTracks = api.tracks.length > 0;
  const data = {
    carrera: api.program.official_name || api.program.name,
    totalSemestres: api.version.total_periods,
    semestres: hasTracks ? [] : periodsFor(null),
  };
  if (api.program.official_code) data.codigo_programa = api.program.official_code;
  if (api.version.total_credits) data.total_creditos = api.version.total_credits;

  if (hasTracks) {
    data.semestres_comunes = periodsFor(null);
    data.menciones_disponibles = api.tracks.map((t) => ({ codigo: t.code, nombre: t.name }));
    data.menciones = Object.fromEntries(
      api.tracks.map((t) => [
        t.code,
        { codigo: t.code, nombre: t.name, semestres: periodsFor(t.code) },
      ])
    );
    data.total_creditos_por_mencion = Object.fromEntries(
      api.tracks.filter((t) => t.total_credits != null).map((t) => [t.code, t.total_credits])
    );
  }
  if (api.aliases && Object.keys(api.aliases).length > 0) {
    data.courseCodeAliases = api.aliases;
  }
  return data;
}
