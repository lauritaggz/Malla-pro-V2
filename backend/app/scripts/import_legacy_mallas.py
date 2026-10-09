"""Usage: uv run python -m app.scripts.import_legacy_mallas <folder> [--report PATH]"""

import argparse
import asyncio
from pathlib import Path

from app.db.session import get_engine, get_sessionmaker
from app.services.legacy_import import (
    KIND_TITLES,
    import_legacy_folder,
    render_report_markdown,
)

BACKEND_DIR = Path(__file__).resolve().parents[2]
DEFAULT_REPORT = BACKEND_DIR / "reports" / "legacy_inconsistencies.md"


async def run(folder: Path, report_path: Path) -> None:
    async with get_sessionmaker()() as session:
        report = await import_legacy_folder(session, folder)
    await get_engine().dispose()

    print(f"{'malla':45} {'cursos':>6} {'menciones':>9} {'nuevos':>6}  career_key")
    for r in report.results:
        print(
            f"{r.program_name:45} {r.courses:>6} {r.tracks:>9} "
            f"{r.created_courses:>6}  {r.career_key}"
        )
    print(f"{'TOTAL':45} {sum(r.courses for r in report.results):>6}")

    print("\nInconsistencias:")
    for r in report.results:
        mine = [i for i in report.inconsistencies if i.malla == r.program_name]
        counts = {k: sum(1 for i in mine if i.kind == k) for k in KIND_TITLES}
        summary = ", ".join(f"{k}={n}" for k, n in counts.items() if n) or "ninguna"
        print(f"  {r.program_name}: {summary}")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(render_report_markdown(report))
    print(f"\nReporte: {report_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Import legacy mallas JSON into Postgres.")
    parser.add_argument("folder", type=Path)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    asyncio.run(run(args.folder.resolve(), args.report.resolve()))


if __name__ == "__main__":
    main()
