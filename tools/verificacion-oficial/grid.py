"""Extrae filas de las tablas 'MALLA CURRICULAR' (Banner UNAB) desde PDF.

- Las filas se delimitan con las líneas horizontales de la tabla (imagen renderizada).
- Las columnas salen de las líneas verticales de cada fila; si una fila no las tiene
  completas (corte de página), se usan las del último encabezado.
- El texto viene de la capa de texto del PDF si existe; si no, de OCR por celda.
- Las filas partidas entre páginas se marcan (borde sup/inf) para unirlas después.
"""
import subprocess, sys, json, os, re, tempfile, html
import numpy as np
from PIL import Image
import pytesseract

DPI = 300
SCALE = DPI / 72
RUIDO = re.compile(r"(https?://|\d\d-\d\d-\d\d, \d|^\d+/\d+$|a\.\s?m\.|p\.\s?m\.)")

def render(pdf, page, outdir):
    base = os.path.join(outdir, f"p{page}")
    subprocess.run(["pdftoppm", "-r", str(DPI), "-png", "-f", str(page), "-l", str(page), pdf, base], check=True)
    path = [os.path.join(outdir, f) for f in os.listdir(outdir) if f.startswith(f"p{page}-")][0]
    im = Image.open(path).convert("L")
    os.remove(path)
    return im

def runs(mask):
    out, start = [], None
    for i, v in enumerate(mask):
        if v and start is None: start = i
        if not v and start is not None: out.append((start, i - 1)); start = None
    if start is not None: out.append((start, len(mask) - 1))
    return out

def h_lines(dark, min_frac=0.45):
    rows = dark.sum(axis=1) > min_frac * dark.shape[1]
    return [(a + b) // 2 for a, b in runs(rows)]

def v_lines(dark, y0, y1, min_frac=0.85):
    band = dark[y0:y1]
    if band.shape[0] < 4: return []
    cols = band.sum(axis=0) > min_frac * band.shape[0]
    out = []
    for a, b in runs(cols):
        x = (a + b) // 2
        if not out or x - out[-1] >= 20: out.append(x)
    return out

def text_words(pdf, page):
    out = subprocess.run(["pdftotext", "-bbox", "-f", str(page), "-l", str(page), pdf, "-"], capture_output=True, text=True).stdout
    ws = []
    for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', out):
        x0, y0, x1, y1 = (float(v) * SCALE for v in m.groups()[:4])
        ws.append((x0, y0, x1, y1, html.unescape(m.group(5))))
    lines = {}
    for w in ws: lines.setdefault(round(w[1] / 8), []).append(w)
    bad = set()
    for k, l in lines.items():
        txt = " ".join(w[4] for w in l)
        if RUIDO.search(txt) and len(l) <= 8: bad.add(k)
    return [w for w in ws if round(w[1] / 8) not in bad]

def words_in(words, box):
    x0, y0, x1, y1 = box
    sel = [w for w in words if x0 <= (w[0] + w[2]) / 2 <= x1 and y0 <= (w[1] + w[3]) / 2 <= y1]
    sel.sort(key=lambda w: ((w[1] + w[3]) / 2, w[0]))
    lines, cur, cury = [], [], None
    for w in sel:
        yc = (w[1] + w[3]) / 2
        if cury is None or abs(yc - cury) > 10:
            if cur: lines.append(" ".join(x[4] for x in sorted(cur)))
            cur, cury = [w], yc
        else:
            cur.append(w)
    if cur: lines.append(" ".join(x[4] for x in sorted(cur)))
    return lines

def ocr(im, box, psm=6, whitelist=None):
    x0, y0, x1, y1 = (int(v) for v in box)
    if x1 - x0 < 8 or y1 - y0 < 8: return []
    crop = im.crop((x0 + 3, y0 + 3, x1 - 2, y1 - 2))
    if (np.array(crop) < 128).sum() < 15: return []
    crop = crop.resize((crop.width * 2, crop.height * 2), Image.LANCZOS)
    cfg = f"--psm {psm}" + (f" -c tessedit_char_whitelist={whitelist}" if whitelist else "")
    return [l.strip() for l in pytesseract.image_to_string(crop, config=cfg).splitlines() if l.strip()]

def page_count(pdf):
    return int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))

TITULO = re.compile(r"\d{3,5}\s*[-_]\s*\d{1,2}\s*S|ESPECIALIDADES|MENCIONES", re.I)

def extract(pdf, use_text):
    tmp = tempfile.mkdtemp()
    filas, cabecera, cols = [], "", None
    for p in range(1, page_count(pdf) + 1):
        im = render(pdf, p, tmp)
        dark = np.array(im) < 140
        W = dark.shape[1]
        words = text_words(pdf, p) if use_text else None
        T = (lambda box, **kw: words_in(words, box)) if use_text else (lambda box, **kw: ocr(im, box, **kw))
        hs = h_lines(dark)
        if use_text and words:
            top, bot = int(min(w[1] for w in words)) - 4, int(max(w[3] for w in words)) + 4
        else:
            ys = np.where(dark.sum(axis=1) > 0)[0]; top, bot = int(ys[0]), int(ys[-1])
        if p == 1 and hs:
            cabecera = " ".join(T((0, 0, W, hs[0] - 2)))
            if not use_text: hs = hs  # la cabecera queda fuera de las bandas
        edges = list(hs)
        abre = bool(hs) and hs[0] - top > 25 and p > 1
        cierra = bool(hs) and bot - hs[-1] > 25
        if abre: edges = [top] + edges
        if cierra: edges = edges + [bot]
        bandas = [(a, b) for a, b in zip(edges, edges[1:]) if b - a >= 12]
        for i, (y0, y1) in enumerate(bandas):
            vs = v_lines(dark, y0 + 3, y1 - 2)
            borde = "sup" if (i == 0 and abre) else "inf" if (i == len(bandas) - 1 and cierra) else None
            if len(vs) >= 5:
                cajas = [(a, y0, b, y1) for a, b in zip(vs, vs[1:])]
            elif cols:
                cajas = [(a, y0, b, y1) for a, b in cols]
            else:
                cajas = None
            if not cajas or len(vs) < 5:
                txt = " ".join(T((0, y0, W, y1)))
                if TITULO.search(txt) and len(txt) < 120:
                    filas.append({"tipo": "titulo", "texto": txt, "pagina": p}); continue
                if not cajas:
                    if txt.strip(): filas.append({"tipo": "otro", "texto": txt, "pagina": p})
                    continue
            n = len(cajas)
            c0 = " ".join(T(cajas[0], psm=7))
            c1 = " ".join(T(cajas[1], psm=7)) if n > 1 else ""
            if re.search(r"Asignatura", c0 + " " + c1, re.I):
                if len(vs) >= 5: cols = list(zip(vs, vs[1:]))
                continue
            filas.append({
                "tipo": "fila", "pagina": p, "borde": borde, "caja": [int(cajas[0][0]), int(y0), int(cajas[-1][2]), int(y1)],
                "codigo": c0, "nombre": c1,
                "creditos": " ".join(T(cajas[n - 3], psm=7, whitelist="0123456789")) if n >= 5 else "",
                "req": T(cajas[n - 2]) if n >= 5 else [],
                "coreq": T(cajas[n - 1]) if n >= 5 else [],
            })
    return {"cabecera": cabecera, "filas": filas}

if __name__ == "__main__":
    pdf, out, mode = sys.argv[1], sys.argv[2], sys.argv[3]
    data = extract(pdf, mode == "text")
    json.dump(data, open(out, "w"), ensure_ascii=False, indent=1)
    print(out, sum(1 for f in data["filas"] if f["tipo"] == "fila"), "filas")
