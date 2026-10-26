import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { readAcademicProgress, writeAcademicProgress } from "./academicProgressStorage.js";
import { listarMallas, mapMallaData } from "./mallasLoader.js";
import { academicProgressKey, getCareerId, LEGACY_KEYS } from "./storageKeys.js";

const here = dirname(fileURLToPath(import.meta.url));
const MALLAS = join(here, "..", "..", "public", "mallas");
const BEFORE = JSON.parse(
  readFileSync(join(here, "__fixtures__", "curriculum", "_legacy_ids_before_t010.json"), "utf8")
).mallas;

const readMalla = (url) => JSON.parse(readFileSync(join(MALLAS, url.replace(/^\/mallas\//, "")), "utf8"));

/** id -> código de todos los cursos de una malla (comunes y de cada mención). */
function coursesById(data) {
  const m = mapMallaData(data);
  const sems = [
    ...m.semestres,
    ...m.semestresComunes,
    ...Object.values(m.menciones).flatMap((x) => x.semestres),
  ];
  return new Map(sems.flatMap((s) => s.cursos.map((c) => [c.id, c.codigo])));
}

/** localStorage en memoria, como el del navegador. */
function memoryStorage() {
  const map = new Map();
  return {
    get length() {
      return map.size;
    },
    key: (i) => [...map.keys()][i] ?? null,
    getItem: (k) => (map.has(k) ? map.get(k) : null),
    setItem: (k, v) => map.set(k, String(v)),
    removeItem: (k) => map.delete(k),
    clear: () => map.clear(),
  };
}

describe("mallas verificadas (T-010): los ids no cambian", () => {
  it.each(Object.keys(BEFORE))("%s conserva exactamente los mismos ids", (stem) => {
    const now = coursesById(readMalla(`/mallas/${stem}.json`));
    expect([...now.keys()].sort((a, b) => a - b)).toEqual(
      Object.keys(BEFORE[stem])
        .map(Number)
        .sort((a, b) => a - b)
    );
  });

  it("Civil Informática: los códigos nuevos (CINF) quedan en el mismo id que los antiguos", () => {
    const now = coursesById(readMalla("/mallas/CInf.json"));
    const renamed = Object.entries(BEFORE.CInf)
      .filter(([id, code]) => now.get(Number(id)) !== code)
      .map(([id, code]) => [Number(id), code, now.get(Number(id))]);
    expect(renamed).toHaveLength(16);
    expect(renamed).toContainEqual([22, "ICF201", "CINF102"]);
    expect(renamed).toContainEqual([17, "INSW220", "CINF100"]);
    expect(renamed.every(([, , code]) => /^CINF\d{3}$/.test(code))).toBe(true);
  });
});

describe("avance guardado en el navegador (localStorage simulado)", () => {
  beforeEach(() => {
    vi.stubGlobal("localStorage", memoryStorage());
  });
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it.each(["CInf", "TM"])(
    "%s: el avance guardado con la malla anterior se lee completo con la nueva",
    async (stem) => {
      const url = `/mallas/${stem}.json`;
      const oldIds = Object.keys(BEFORE[stem]).map(Number);
      // Lo que la versión pública guardó antes de este cambio (misma URL => mismo careerId).
      const saved = {
        aprobados: oldIds.filter((id) => id % 2 === 0),
        cursando: oldIds.filter((id) => id % 5 === 1),
        excepciones: oldIds.slice(-2),
      };
      expect(writeAcademicProgress({ url, nombre: stem }, saved).ok).toBe(true);
      const notas = { [oldIds[0]]: [{ nombre: "Certamen 1", peso: 30, nota: 5.5 }] };
      localStorage.setItem(LEGACY_KEYS.notas, JSON.stringify(notas));

      // La malla tal como la lista hoy el selector.
      const unis = await listarMallas();
      const malla = unis.flatMap((u) => u.mallas).find((m) => m.url === url);
      expect(getCareerId(malla)).toBe(`unab-${stem.toLowerCase()}`);

      const progress = readAcademicProgress(malla);
      expect(progress.aprobados).toEqual(saved.aprobados);
      expect(progress.cursando).toEqual(saved.cursando);
      expect(progress.excepciones).toEqual(saved.excepciones);

      const now = coursesById(readMalla(url));
      for (const id of [...progress.aprobados, ...progress.cursando, ...progress.excepciones]) {
        expect(now.has(id)).toBe(true);
      }
      const storedNotas = JSON.parse(localStorage.getItem(LEGACY_KEYS.notas));
      expect(now.has(Number(Object.keys(storedNotas)[0]))).toBe(true);
    }
  );
});

describe("selector de carreras agrupado por universidad", () => {
  const UCH = {
    "/mallas/BioquimicaUCH.json": "unab-bioquimicauch",
    "/mallas/IngenieriaAlimentosUCH.json": "unab-ingenieriaalimentosuch",
    "/mallas/QuimicaUCH.json": "unab-quimicauch",
    "/mallas/QuimicaFarmaciaUCH.json": "unab-quimicafarmaciauch",
  };

  it("lista UNAB y U. de Chile por separado", async () => {
    vi.stubEnv("VITE_API_URL", "");
    const unis = await listarMallas();
    vi.unstubAllEnvs();
    expect(unis.map((u) => [u.universidad, u.mallas.length])).toEqual([
      ["Universidad Andrés Bello", 9],
      ["Universidad de Chile", 4],
    ]);
    expect(unis[1].mallas.map((m) => m.nombre)).toEqual([
      "Bioquímica",
      "Ingeniería en Alimentos",
      "Química",
      "Química y Farmacia",
    ]);
  });

  it("cada malla listada existe y declara la universidad de su grupo", async () => {
    const unis = await listarMallas();
    for (const uni of unis) {
      for (const m of uni.mallas) {
        const data = readMalla(m.url);
        expect(coursesById(data).size).toBeGreaterThan(0);
        if (data.universidad) expect(data.universidad).toBe(uni.universidad);
      }
    }
  });

  it("las mallas de la U. de Chile mantienen el careerId de la versión pública", async () => {
    vi.stubGlobal("localStorage", memoryStorage());
    const unis = await listarMallas();
    const uch = unis.find((u) => u.universidad === "Universidad de Chile").mallas;
    expect(Object.fromEntries(uch.map((m) => [m.url, getCareerId(m)]))).toEqual(UCH);

    const malla = uch[0];
    localStorage.setItem(
      academicProgressKey(UCH[malla.url]),
      JSON.stringify({ schemaVersion: 1, aprobados: [1, 2], excepciones: [], cursando: [3] })
    );
    expect(readAcademicProgress(malla)).toMatchObject({ aprobados: [1, 2], cursando: [3] });
    vi.unstubAllGlobals();
  });
});
