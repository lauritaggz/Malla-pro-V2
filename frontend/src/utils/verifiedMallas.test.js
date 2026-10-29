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

/** id -> { codigo, nombre } de todos los cursos de una malla (comunes y de cada mención). */
function coursesById(data) {
  const m = mapMallaData(data);
  const sems = [
    ...m.semestres,
    ...m.semestresComunes,
    ...Object.values(m.menciones).flatMap((x) => x.semestres),
  ];
  return new Map(
    sems.flatMap((s) => s.cursos.map((c) => [c.id, { codigo: c.codigo, nombre: c.nombre }]))
  );
}

/**
 * Únicos cambios permitidos en T-010 sobre un id existente: los códigos de Civil Informática
 * pasan a los oficiales (ICF/INSW -> CINF) y un nombre se corrige. Todo lo demás debe quedar
 * igual, para que el avance guardado por id siga apuntando al mismo ramo.
 */
const ALLOWED_CHANGES = {
  CInf: {
    17: { codigo: ["INSW220", "CINF100"] },
    22: { codigo: ["ICF201", "CINF102"] },
    23: { codigo: ["ICF202", "CINF101"] },
    28: { codigo: ["ICF203", "CINF103"] },
    31: { codigo: ["ICF204", "CINF104"] },
    32: { codigo: ["ICF205", "CINF105"] },
    38: { codigo: ["INSW411", "CINF107"] },
    39: {
      codigo: ["INSW421", "CINF200"],
      nombre: [
        "Seminario de Licenciatura en Ingeniería",
        "Integrador II: Seminario de Licenciatura en Ciencias de la Ingeniería",
      ],
    },
    41: { codigo: ["INSW410", "CINF108"] },
    42: { codigo: ["ICF206", "CINF109"] },
    43: { codigo: ["ICF207", "CINF110"] },
    44: { codigo: ["INSW412", "CINF111"] },
    45: { codigo: ["INSW413", "CINF112"] },
    46: { codigo: ["INSW422", "CINF400"] },
    47: { codigo: ["ICF208", "CINF113"] },
    48: { codigo: ["INSW420", "CINF300"] },
  },
};

/** Lo que debería tener hoy cada id: el valor anterior más los cambios permitidos. */
function expectedNow(stem) {
  const allowed = ALLOWED_CHANGES[stem] || {};
  return new Map(
    Object.entries(BEFORE[stem]).map(([id, before]) => {
      const change = allowed[id] || {};
      const pick = (field) => {
        if (!change[field]) return before[field];
        expect(before[field]).toBe(change[field][0]); // la lista de cambios refleja el antes real
        return change[field][1];
      };
      return [Number(id), { codigo: pick("codigo"), nombre: pick("nombre") }];
    })
  );
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

describe("mallas verificadas (T-010): cada id sigue siendo el mismo ramo", () => {
  it.each(Object.keys(BEFORE))("%s: mismo conjunto de ids y mismo código y nombre por id", (stem) => {
    const now = coursesById(readMalla(`/mallas/${stem}.json`));
    // Map -> objeto ordenado para un diff legible si algo cambia o se intercambia.
    const asObject = (m) => Object.fromEntries([...m].sort(([a], [b]) => a - b));
    expect(asObject(now)).toEqual(asObject(expectedNow(stem)));
  });

  it("Civil Informática: los 16 códigos nuevos son CINF y no se repiten", () => {
    const changes = Object.values(ALLOWED_CHANGES.CInf).map((c) => c.codigo[1]);
    expect(changes).toHaveLength(16);
    expect(new Set(changes).size).toBe(16);
    expect(changes.every((code) => /^CINF\d{3}$/.test(code))).toBe(true);
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
      expect(oldIds.length).toBeGreaterThan(40);
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

      // Cada id guardado sigue siendo el mismo ramo (mismo nombre; en CInf, código nuevo).
      const now = coursesById(readMalla(url));
      const expected = expectedNow(stem);
      for (const id of [...progress.aprobados, ...progress.cursando, ...progress.excepciones]) {
        expect(now.get(id)).toEqual(expected.get(id));
      }
      const storedNotas = JSON.parse(localStorage.getItem(LEGACY_KEYS.notas));
      expect(now.get(Number(Object.keys(storedNotas)[0]))).toEqual(expected.get(oldIds[0]));
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
