import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it, vi } from "vitest";
import { apiCurriculumToLegacyJson, UnsupportedPrereqError } from "./curriculumApi.js";
import { fetchMallaJson, listarMallas, mapMallaData, resetCatalogCache } from "./mallasLoader.js";
import { getCareerId } from "./storageKeys.js";

const here = dirname(fileURLToPath(import.meta.url));
const FIXTURES = join(here, "__fixtures__", "curriculum");
const MALLAS = join(here, "..", "..", "public", "mallas");
const STEMS = [
  "Industrial",
  "Comp",
  "Geo",
  "MM",
  "CInf",
  "Minas",
  "Med",
  "TM",
  "Psicologia",
  "BioquimicaUCH",
  "IngenieriaAlimentosUCH",
  "QuimicaUCH",
  "QuimicaFarmaciaUCH",
];

const readJson = (dir, name) => JSON.parse(readFileSync(join(dir, `${name}.json`), "utf8"));

/** Los objetos de mención de MM no traen "codigo" en el JSON; la API siempre lo devuelve. */
function normalizeMenciones(mapped) {
  return {
    ...mapped,
    menciones: Object.fromEntries(
      Object.entries(mapped.menciones).map(([code, m]) => [code, { ...m, codigo: code }])
    ),
  };
}

describe.each(STEMS)("catálogo API vs JSON estático: %s", (stem) => {
  const fixture = readJson(FIXTURES, stem);
  const legacy = readJson(MALLAS, stem);

  it("el adaptador produce lo mismo que mapMallaData(JSON estático)", () => {
    const fromApi = mapMallaData(apiCurriculumToLegacyJson(fixture));
    const fromStatic = mapMallaData(legacy);
    expect(normalizeMenciones(fromApi)).toEqual(normalizeMenciones(fromStatic));
  });

  it("conserva ids, semestres y prerrequisitos por id legado", () => {
    const fromApi = mapMallaData(apiCurriculumToLegacyJson(fixture));
    const fromStatic = mapMallaData(legacy);
    const flat = (m) => [
      ...m.semestres,
      ...m.semestresComunes,
      ...Object.values(m.menciones).flatMap((x) => x.semestres),
    ].flatMap((s) => s.cursos.map((c) => [s.numero, c.id, c.codigo, c.prerrequisitos]));
    expect(flat(fromApi)).toEqual(flat(fromStatic));
    expect(fromApi.totalSemestres).toBe(fromStatic.totalSemestres);
    expect(fromApi.nombre).toBe(fromStatic.nombre);
  });

  it("career_key coincide con getCareerId de la malla legada", () => {
    const legacyMalla = { url: fixture.program.legacy_url, nombre: fixture.program.name };
    expect(fixture.program.career_key).toBe(getCareerId(legacyMalla));
    expect(getCareerId({ ...legacyMalla, careerKey: fixture.program.career_key })).toBe(
      getCareerId(legacyMalla)
    );
  });
});

describe("adaptador", () => {
  it("rechaza árboles OR / créditos mínimos que la UI no puede representar", () => {
    const fixture = structuredClone(readJson(FIXTURES, "Med"));
    const [a, b] = fixture.courses;
    fixture.courses[5].prereq_expr = {
      op: "or",
      items: [{ course: a.id }, { course: b.id }],
    };
    expect(() => apiCurriculumToLegacyJson(fixture)).toThrow(UnsupportedPrereqError);
  });
});

describe("mallasLoader con y sin API", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.unstubAllEnvs();
    resetCatalogCache();
  });

  const jsonResponse = (body, ok = true, status = 200) => ({
    ok,
    status,
    json: async () => body,
  });

  it("sin VITE_API_URL usa el catálogo y los JSON estáticos", async () => {
    vi.stubEnv("VITE_API_URL", "");
    const fetchMock = vi.fn(async () => jsonResponse(readJson(MALLAS, "Med")));
    vi.stubGlobal("fetch", fetchMock);

    const unis = await listarMallas();
    expect(unis[0].mallas.map((m) => m.url)).toContain("/mallas/Med.json");
    expect(unis[0].mallas).toHaveLength(9);

    const data = await fetchMallaJson("/mallas/Med.json");
    expect(data.carrera).toBe("Medicina (UNAB)");
    expect(fetchMock.mock.calls[0][0]).toMatch(/^\/mallas\/Med\.json\?t=/);
  });

  it("con VITE_API_URL lista desde la API y conserva url y careerKey legados", async () => {
    vi.stubEnv("VITE_API_URL", "http://api.test/");
    const programs = readJson(FIXTURES, "_programs");
    const med = programs.find((p) => p.legacy_url === "/mallas/Med.json");
    const fetchMock = vi.fn(async (url) => {
      if (url.endsWith("/api/v1/universities"))
        return jsonResponse([{ slug: "unab", name: "Universidad Andrés Bello" }]);
      if (url.endsWith("/universities/unab/programs")) return jsonResponse(programs);
      if (url.endsWith(`/programs/${med.id}/curriculum`))
        return jsonResponse(readJson(FIXTURES, "Med"));
      throw new Error(`unexpected ${url}`);
    });
    vi.stubGlobal("fetch", fetchMock);

    const unis = await listarMallas();
    const malla = unis[0].mallas.find((m) => m.nombre === "Medicina");
    expect(malla).toMatchObject({ url: "/mallas/Med.json", careerKey: "unab-med" });
    expect(getCareerId(malla)).toBe(getCareerId({ url: "/mallas/Med.json", nombre: "Medicina" }));

    const data = await fetchMallaJson("/mallas/Med.json");
    expect(mapMallaData(data)).toEqual(mapMallaData(readJson(MALLAS, "Med")));
  });

  it("si la API falla cae a los JSON estáticos", async () => {
    vi.stubEnv("VITE_API_URL", "http://api.test");
    const fetchMock = vi.fn(async (url) => {
      if (url.startsWith("http://api.test")) throw new TypeError("Failed to fetch");
      return jsonResponse(readJson(MALLAS, "TM"));
    });
    vi.stubGlobal("fetch", fetchMock);
    vi.spyOn(console, "warn").mockImplementation(() => {});

    const unis = await listarMallas();
    expect(unis[0].mallas).toHaveLength(9);
    expect(unis[0].mallas[0].careerKey).toBeUndefined();

    const data = await fetchMallaJson("/mallas/TM.json");
    expect(data.carrera).toMatch(/Tecnolog/);
  });
});
