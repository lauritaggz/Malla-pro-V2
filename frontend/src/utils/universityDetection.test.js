import { afterEach, describe, expect, it, vi } from "vitest";
import { inferUniversidadFromUrl } from "./analytics.js";
import {
  isUniversidadDeChile,
  listarMallas,
  resetCatalogCache,
  supportsTomaDeRamos,
} from "./mallasLoader.js";
import { normalizeInstitution, validateCourseCompatibility } from "./shareCourseConfig.js";

const UCH_URLS = [
  "/mallas/BioquimicaUCH.json",
  "/mallas/IngenieriaAlimentosUCH.json",
  "/mallas/QuimicaUCH.json",
  "/mallas/QuimicaFarmaciaUCH.json",
];
const UNAB_URLS = ["/mallas/CInf.json", "/mallas/TM.json", "/mallas/Med.json"];

describe("universidad de cada malla (T-007)", () => {
  it.each(UCH_URLS)("%s es de la U. de Chile y no ofrece toma de ramos", (url) => {
    const malla = { url };
    expect(isUniversidadDeChile(malla)).toBe(true);
    expect(supportsTomaDeRamos(malla)).toBe(false);
    expect(inferUniversidadFromUrl(url)).toBe("Universidad de Chile");
    expect(normalizeInstitution({ url, universidad: "Universidad de Chile" })).toBe("UCH");
  });

  it.each(UNAB_URLS)("%s es UNAB y ofrece toma de ramos", (url) => {
    expect(isUniversidadDeChile({ url })).toBe(false);
    expect(supportsTomaDeRamos({ url })).toBe(true);
    expect(inferUniversidadFromUrl(url)).toBe("Universidad Andrés Bello");
    expect(normalizeInstitution({ url })).toBe("UNAB");
  });

  it("la universidad declarada manda aunque la URL sea de la API", () => {
    const malla = { url: "/api/v1/programs/0e4c/curriculum", universidad: "Universidad de Chile" };
    expect(isUniversidadDeChile(malla)).toBe(true);
    expect(supportsTomaDeRamos(malla)).toBe(false);
  });

  it("sin malla no se ofrece toma de ramos", () => {
    expect(supportsTomaDeRamos(null)).toBe(false);
  });

  it("una configuración UNAB no se acepta en un ramo de la U. de Chile ni al revés", () => {
    const unab = { institution: "UNAB", courseCode: "QUI001" };
    const uch = { institution: "UCH", courseCode: "QUI001" };
    expect(validateCourseCompatibility(unab, uch).compatible).toBe(false);
    expect(validateCourseCompatibility(uch, unab).compatible).toBe(false);
    expect(validateCourseCompatibility(uch, uch).compatible).toBe(true);
  });
});

describe("selector con la API: mismas áreas y semestres que sin API", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.unstubAllEnvs();
    resetCatalogCache();
  });

  it("completa área y semestres de las mallas legadas por su URL", async () => {
    vi.stubEnv("VITE_API_URL", "");
    const staticUnis = await listarMallas();
    const byUrl = new Map(staticUnis.flatMap((u) => u.mallas).map((m) => [m.url, m]));

    vi.stubEnv("VITE_API_URL", "http://api.test");
    const json = (body) => ({ ok: true, status: 200, json: async () => body });
    vi.stubGlobal(
      "fetch",
      vi.fn(async (url) => {
        if (url.endsWith("/api/v1/universities"))
          return json([
            { slug: "unab", name: "Universidad Andrés Bello" },
            { slug: "uch", name: "Universidad de Chile" },
          ]);
        if (url.endsWith("/universities/unab/programs"))
          return json([{ id: "a", name: "Medicina", career_key: "unab-med", legacy_url: "/mallas/Med.json" }]);
        if (url.endsWith("/universities/uch/programs"))
          return json([
            { id: "b", name: "Química", career_key: "unab-quimicauch", legacy_url: "/mallas/QuimicaUCH.json" },
            { id: "c", name: "Nueva", career_key: "uch-nueva", legacy_url: null },
          ]);
        throw new Error(`unexpected ${url}`);
      })
    );
    const unis = await listarMallas();
    const med = unis[0].mallas[0];
    expect(med).toMatchObject({ area: byUrl.get("/mallas/Med.json").area, semestres: 12 });
    const [quimica, nueva] = unis[1].mallas;
    expect(quimica).toMatchObject({ area: "Ciencias", semestres: 11, careerKey: "unab-quimicauch" });
    // Una malla que solo existe en la API no inventa área ni semestres.
    expect(nueva.area).toBeUndefined();
    expect(nueva.semestres).toBeUndefined();
  });
});
