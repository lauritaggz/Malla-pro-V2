/**
 * Lleva un elemento a la vista moviendo solo su contenedor con scroll, nunca la página.
 * (`scrollIntoView` desplaza también todos los ancestros, incluida la ventana.)
 *
 * - Si el elemento es más alto que el contenedor, alinea su borde superior arriba.
 * - Si cabe, lo muestra completo con el mínimo desplazamiento.
 *
 * @param {Element | null} el
 * @param {{ scroller?: Element | null, margin?: number, behavior?: "auto" | "smooth" }} [options]
 */
export function revealInScroller(el, { scroller, margin = 8, behavior } = {}) {
  if (!el) return;
  const container = scroller || el.closest(".overflow-y-auto");
  if (!container) return;

  const reduce =
    typeof window !== "undefined" &&
    window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
  const mode = behavior || (reduce ? "auto" : "smooth");

  const c = container.getBoundingClientRect();
  const r = el.getBoundingClientRect();

  let delta = 0;
  if (r.height > c.height - margin * 2 || r.top < c.top + margin) {
    delta = r.top - c.top - margin;
  } else if (r.bottom > c.bottom - margin) {
    delta = r.bottom - c.bottom + margin;
  }
  if (Math.abs(delta) > 1) container.scrollBy({ top: delta, behavior: mode });
}
