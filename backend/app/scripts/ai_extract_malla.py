"""PROTOTYPE: extract a draft malla from a PDF or photo with Claude and measure it.

Usage (from backend/, with ANTHROPIC_API_KEY in backend/.env):
  uv run python -m app.scripts.ai_extract_malla <documento.pdf|foto.jpg> \\
      [--compare ../frontend/public/mallas/QuimicaUCH.json] [--out borrador.json] [--model ...]

Writes the draft (never imported), prints warnings, consistency problems, tokens used and, with
--compare, how close it is to a verified malla. The document's content is not printed.
"""

import argparse
import json
import sys
from pathlib import Path

from app.core.config import get_settings
from app.services.ai_malla import compare, extract, media_type_for, to_draft, validate


def main() -> int:
    parser = argparse.ArgumentParser(description="Prototipo: malla desde PDF o foto con IA.")
    parser.add_argument("documento", type=Path, help="PDF o imagen de la malla")
    parser.add_argument("--compare", type=Path, help="malla verificada para medir el acierto")
    parser.add_argument("--out", type=Path, help="dónde guardar el borrador (JSON)")
    parser.add_argument("--model", help="modelo de Claude (por defecto AI_MODEL)")
    args = parser.parse_args()

    settings = get_settings()
    if not settings.anthropic_api_key:
        print("Falta ANTHROPIC_API_KEY en backend/.env", file=sys.stderr)
        return 1
    try:
        media_type = media_type_for(args.documento.name)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    import anthropic  # imported here so the rest of the app never needs it

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    model = args.model or settings.ai_model
    print(f"Extrayendo con {model}…")
    try:
        result = extract(args.documento.read_bytes(), media_type, client=client, model=model)
    except anthropic.APIError as exc:
        print(f"Error de la API de Claude: {type(exc).__name__}", file=sys.stderr)
        return 2

    draft = to_draft(result.raw)
    draft.malla["borrador_ia"] = {
        "modelo": result.model,
        "documento": args.documento.name,
        "advertencias": draft.warnings,
    }
    out = args.out or args.documento.with_suffix(".borrador.json")
    out.write_text(json.dumps(draft.malla, ensure_ascii=False, indent=2), encoding="utf-8")

    courses = sum(len(s["cursos"]) for s in draft.malla["semestres"])
    print(f"Borrador: {out}")
    print(f"Ramos: {courses} en {draft.malla['totalSemestres']} semestres")
    print(f"Requisitos desconocidos: {draft.unknown_courses}")
    print(f"Tokens: {result.input_tokens} de entrada, {result.output_tokens} de salida")
    if result.stop_reason == "max_tokens":
        print("AVISO: la respuesta se cortó por largo (max_tokens); el borrador está incompleto")
    for w in draft.warnings:
        print(f"  advertencia: {w}")
    issues = validate(draft.malla)
    print(f"Problemas de consistencia: {len(issues)}")
    for i in issues[:20]:
        print(f"  {i}")

    if args.compare:
        verified = json.loads(args.compare.read_text(encoding="utf-8"))
        metrics = compare(draft.malla, verified)
        print("Comparación con la malla verificada:")
        for k, v in metrics.items():
            print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
