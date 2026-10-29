import { describe, expect, it } from "vitest";
import {
  COURSE_COLOR_HUES,
  assignCourseColorIndexes,
  getCourseColorByIndex,
} from "../services/scheduleService";

describe("Colores por asignatura", () => {
  it("no repite color entre asignaturas del mismo horario", () => {
    const codes = Array.from({ length: 12 }, (_, i) => `RAMO${100 + i}`);
    const idx = assignCourseColorIndexes(codes, {});
    const values = Object.values(idx);
    expect(new Set(values).size).toBe(codes.length);
  });

  it("mantiene el color de las que ya estaban cuando entra una nueva", () => {
    const before = assignCourseColorIndexes(["FMMP112", "CFIS310", "TDFI103"], {});
    const after = assignCourseColorIndexes(["FMMP112", "CFIS310", "TDFI103", "NUEVO200"], before);
    expect(after.FMMP112).toBe(before.FMMP112);
    expect(after.CFIS310).toBe(before.CFIS310);
    expect(after.TDFI103).toBe(before.TDFI103);
    expect(Object.values(before)).not.toContain(after.NUEVO200);
  });

  it("la asignatura nueva no hereda el color de una que sigue en el horario", () => {
    const stored = { A1: 0, B2: 1, C3: 2 };
    const after = assignCourseColorIndexes(["A1", "B2", "C3", "D4"], stored);
    expect(after.D4).toBe(3);
  });

  it("si dos asignaturas guardadas chocan, la primera conserva el color y la otra se reasigna", () => {
    const after = assignCourseColorIndexes(["A1", "B2"], { A1: 4, B2: 4 });
    expect(after.A1).toBe(4);
    expect(after.B2).not.toBe(4);
  });

  it("normaliza los códigos (mayúsculas, espacios y guiones)", () => {
    const idx = assignCourseColorIndexes(["tdfi 103", "TDFI-103"], {});
    expect(Object.keys(idx)).toEqual(["TDFI103"]);
  });

  it("sigue dando colores distintos pasada la primera vuelta de la paleta", () => {
    const n = COURSE_COLOR_HUES.length;
    const a = getCourseColorByIndex(0);
    const b = getCourseColorByIndex(n);
    expect(a.bgLight).not.toBe(b.bgLight);
  });
});
