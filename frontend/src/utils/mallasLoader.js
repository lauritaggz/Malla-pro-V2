import { apiCurriculumToLegacyJson } from "./curriculumApi";

/**
 * Indica si la malla pertenece a la Universidad de Chile.
 * @param {{ universidad?: string, url?: string } | null | undefined} malla
 */
export function isUniversidadDeChile(malla) {
  if (!malla) return false;
  const uni = String(malla.universidad || "").toLowerCase();
  if (uni.includes("chile") || uni.includes("uch")) return true;
  const url = String(malla.url || "").toLowerCase();
  return /uch\.json|\/uch\//i.test(url) || url.includes("uch");
}

/**
 * Toma de ramos / programación académica solo está disponible para UNAB.
 * @param {{ universidad?: string, url?: string } | null | undefined} malla
 */
export function supportsTomaDeRamos(malla) {
  if (!malla) return false;
  return !isUniversidadDeChile(malla);
}

const API_TIMEOUT_MS = 5000;
const CURRICULUM_PATH_RE = /^\/api\/v1\/programs\/([0-9a-f-]{36})\/curriculum\/?$/i;

/** Catálogo estático: se usa cuando no hay VITE_API_URL o la API no responde. */
const STATIC_UNIVERSIDADES = [
  {
    universidad: "Universidad Andrés Bello",
    mallas: [
      {
        nombre: "Ingeniería Civil Industrial",
        url: "/mallas/Industrial.json",
        area: "Ingeniería",
        semestres: 10,
      },
      {
        nombre: "Ingeniería en Computación e Informática",
        url: "/mallas/Comp.json",
        area: "Ingeniería",
        semestres: 8,
      },
      {
        nombre: "Geología",
        url: "/mallas/Geo.json",
        area: "Ingeniería",
        semestres: 10,
      },
      {
        nombre: "Ingeniería en Marina Mercante",
        url: "/mallas/MM.json",
        area: "Ingeniería",
        semestres: 8,
      },
      {
        nombre: "Ingeniería Civil Informática",
        url: "/mallas/CInf.json",
        area: "Ingeniería",
        semestres: 10,
      },
      {
        nombre: "Ingeniería Civil en Minas",
        url: "/mallas/Minas.json",
        area: "Ingeniería",
        semestres: 10,
      },
      {
        nombre: "Medicina",
        url: "/mallas/Med.json",
        area: "Salud",
        semestres: 12,
      },
      {
        nombre: "Tecnología Médica",
        url: "/mallas/TM.json",
        area: "Salud",
        semestres: 10,
      },
      {
        nombre: "Psicología",
        url: "/mallas/Psicologia.json",
        area: "Ciencias sociales",
        semestres: 10,
      },
    ],
  },
  {
    // Misma URL que en la versión pública: de ella sale el careerId del avance guardado.
    universidad: "Universidad de Chile",
    mallas: [
      {
        nombre: "Bioquímica",
        url: "/mallas/BioquimicaUCH.json",
        area: "Ciencias",
        semestres: 11,
      },
      {
        nombre: "Ingeniería en Alimentos",
        url: "/mallas/IngenieriaAlimentosUCH.json",
        area: "Ingeniería",
        semestres: 11,
      },
      {
        nombre: "Química",
        url: "/mallas/QuimicaUCH.json",
        area: "Ciencias",
        semestres: 11,
      },
      {
        nombre: "Química y Farmacia",
        url: "/mallas/QuimicaFarmaciaUCH.json",
        area: "Ciencias",
        semestres: 11,
      },
    ],
  },
];

/** Área y semestres de las mallas legadas, para que el selector se vea igual con la API. */
const STATIC_META_BY_URL = new Map(
  STATIC_UNIVERSIDADES.flatMap((u) =>
    u.mallas.map((m) => [m.url, { area: m.area, semestres: m.semestres }])
  )
);

function getApiBase() {
  const raw = import.meta.env?.VITE_API_URL;
  return typeof raw === "string" && raw.trim() ? raw.trim().replace(/\/$/, "") : "";
}

async function fetchApiJson(path) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), API_TIMEOUT_MS);
  try {
    const res = await fetch(`${getApiBase()}${path}`, {
      headers: { Accept: "application/json" },
      signal: controller.signal,
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } finally {
    clearTimeout(timer);
  }
}

/** @type {Promise<{ universidades: object[], programIdByUrl: Map<string, string> }> | null} */
let catalogPromise = null;

async function loadApiCatalog() {
  const universities = await fetchApiJson("/api/v1/universities");
  const programIdByUrl = new Map();
  const universidades = [];
  for (const uni of universities) {
    const programs = await fetchApiJson(`/api/v1/universities/${uni.slug}/programs`);
    const mallas = programs.map((p) => {
      // Las mallas legadas conservan su URL de siempre (y con ella su careerId).
      const url = p.legacy_url || `/api/v1/programs/${p.id}/curriculum`;
      programIdByUrl.set(url, p.id);
      const meta = STATIC_META_BY_URL.get(url) || {};
      return { nombre: p.name, url, careerKey: p.career_key, programId: p.id, ...meta };
    });
    if (mallas.length > 0) universidades.push({ universidad: uni.name, mallas });
  }
  if (universidades.length === 0) throw new Error("Catálogo vacío");
  return { universidades, programIdByUrl };
}

function getApiCatalog() {
  if (!catalogPromise) {
    catalogPromise = loadApiCatalog().catch((err) => {
      catalogPromise = null;
      throw err;
    });
  }
  return catalogPromise;
}

/** Solo para tests. */
export function resetCatalogCache() {
  catalogPromise = null;
}

export async function listarMallas() {
  if (getApiBase()) {
    try {
      return (await getApiCatalog()).universidades;
    } catch (err) {
      console.warn("[mallas] API de catálogo no disponible; uso JSON estáticos", err);
    }
  }
  return STATIC_UNIVERSIDADES;
}

async function resolveProgramId(url) {
  const direct = CURRICULUM_PATH_RE.exec(url);
  if (direct) return direct[1];
  const { programIdByUrl } = await getApiCatalog();
  return programIdByUrl.get(url) || null;
}

/**
 * Carga un JSON de malla sin caché del navegador,
 * para que ediciones en public/mallas/*.json se reflejen al recargar.
 * Con VITE_API_URL intenta primero la API y, si falla, cae al JSON estático.
 * @param {string} url
 * @returns {Promise<object>}
 */
export async function fetchMallaJson(url) {
  if (!url) throw new Error("URL de malla vacía");

  if (getApiBase()) {
    try {
      const programId = await resolveProgramId(url);
      if (programId) {
        const api = await fetchApiJson(`/api/v1/programs/${programId}/curriculum`);
        return apiCurriculumToLegacyJson(api);
      }
    } catch (err) {
      console.warn("[mallas] API de catálogo falló; uso JSON estático", err);
    }
  }

  if (url.startsWith("/api/")) throw new Error("Malla de API no disponible");

  const separator = url.includes("?") ? "&" : "?";
  const bustUrl = `${url}${separator}t=${Date.now()}`;

  const res = await fetch(bustUrl, {
    cache: "no-store",
    headers: { Accept: "application/json" },
  });

  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const data = await res.json();
  if (!data || typeof data !== "object") {
    throw new Error("Invalid malla JSON");
  }
  return data;
}

/**
 * Normaliza el shape del JSON de malla al usado por la UI.
 * @param {object} data
 */
export function mapMallaData(data) {
  const isMencion = !!data.menciones;
  const mencionesDisponibles = data.menciones_disponibles || [];
  const totalSemestres = data.totalSemestres || data.semestres?.length || 0;

  return {
    nombre: data.carrera || "Malla sin nombre",
    semestres: data.semestres || [],
    semestresComunes: data.semestres_comunes || [],
    menciones: data.menciones || {},
    courseCodeAliases: data.courseCodeAliases || data.course_code_aliases || {},
    isMencion,
    mencionesDisponibles,
    totalSemestres,
  };
}
