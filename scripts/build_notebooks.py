"""Generate notebooks from Markdown chapters."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"
NOTEBOOKS = ROOT / "notebooks"


def build_day_notebook(week: str, day: str, output_name: str) -> None:
    day_dir = BOOK / week / day
    sections = [
        "chapter.md",
        "notes_architect.md",
        "exercises.md",
        "interview.md",
        "references.md",
    ]

    cells = []
    for section in sections:
        path = day_dir / section
        if path.exists():
            cells.append(new_markdown_cell(path.read_text(encoding="utf-8")))

    nb = new_notebook(cells=cells)
    NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    with (NOTEBOOKS / output_name).open("w", encoding="utf-8") as f:
        nbformat.write(nb, f)


def main() -> None:
    build_day_notebook("week01", "day01", "S1_J1_History_of_Language_Models.ipynb")


if __name__ == "__main__":
    main()
