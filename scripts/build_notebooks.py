"""Generate notebooks from the bootcamp Markdown structure.

The source of truth is now:

book/
└── weekXX/
    └── dayYY/
        ├── README.md
        ├── learning_objectives.md
        ├── chapter.md
        ├── exercises.md
        ├── interview.md
        ├── challenge.md
        ├── references.md
        ├── corriges/
        │   ├── exercises_solution.md
        │   ├── interview_solution.md
        │   ├── challenge_solution.md
        │   └── review.md
        ├── diagrams/
        ├── assets/
        └── labs/

By default, generated notebooks are "student notebooks" and do not include corrections.

Usage:

    python scripts/build_notebooks.py
    python scripts/build_notebooks.py --week week01 --day day02
    python scripts/build_notebooks.py --teacher
    python scripts/build_notebooks.py --week week01 --day day02 --teacher

Outputs:

    notebooks/week01/S1_J2_<slug>.ipynb
    notebooks/week01/teacher/S1_J2_<slug>_teacher.ipynb
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"
NOTEBOOKS = ROOT / "notebooks"


MAIN_SECTIONS = [
    "README.md",
    "learning_objectives.md",
    "chapter.md",
    "exercises.md",
    "interview.md",
    "challenge.md",
    "references.md",
]

TEACHER_SECTIONS = [
    "corriges/exercises_solution.md",
    "corriges/interview_solution.md",
    "corriges/challenge_solution.md",
    "corriges/review.md",
]


def week_number(week_name: str) -> int:
    match = re.search(r"(\\d+)", week_name)
    if not match:
        raise ValueError(f"Invalid week name: {week_name}")
    return int(match.group(1))


def day_number(day_name: str) -> int:
    match = re.search(r"(\\d+)", day_name)
    if not match:
        raise ValueError(f"Invalid day name: {day_name}")
    return int(match.group(1))


def title_from_chapter(day_dir: Path) -> str:
    chapter = day_dir / "chapter.md"
    if not chapter.exists():
        return day_dir.name

    for line in chapter.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()

    return day_dir.name


def slugify(text: str) -> str:
    text = text.lower()
    text = (
        text.replace("é", "e")
        .replace("è", "e")
        .replace("ê", "e")
        .replace("à", "a")
        .replace("ù", "u")
        .replace("ç", "c")
        .replace("'", "")
    )
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")[:60] or "notebook"


def read_section(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8").strip()


def collect_diagrams(day_dir: Path) -> list[str]:
    diagrams_dir = day_dir / "diagrams"
    if not diagrams_dir.exists():
        return []

    cells = []
    for diagram in sorted(diagrams_dir.glob("*.mmd")):
        content = diagram.read_text(encoding="utf-8").strip()
        cells.append(
            f"## Diagramme — {diagram.name}\\n\\n```mermaid\\n{content}\\n```"
        )
    return cells


def collect_labs(day_dir: Path) -> list[str]:
    labs_dir = day_dir / "labs"
    if not labs_dir.exists():
        return []

    lab_files = sorted(
        [
            p
            for p in labs_dir.iterdir()
            if p.is_file() and p.name.lower() not in {"readme.md"}
        ]
    )

    if not lab_files:
        readme = labs_dir / "README.md"
        if readme.exists():
            return [readme.read_text(encoding="utf-8").strip()]
        return []

    lines = ["## Labs associés", ""]
    for lab in lab_files:
        lines.append(f"- `{lab.relative_to(ROOT)}`")
    return ["\\n".join(lines)]


def build_day_notebook(week_name: str, day_name: str, teacher: bool = False) -> Path:
    week_dir = BOOK / week_name
    day_dir = week_dir / day_name

    if not day_dir.exists():
        raise FileNotFoundError(f"Day directory not found: {day_dir}")

    cells = []

    # Main student content
    for section in MAIN_SECTIONS:
        content = read_section(day_dir / section)
        if content:
            cells.append(new_markdown_cell(content))

    # Diagrams and labs are included in student mode too.
    for content in collect_diagrams(day_dir):
        cells.append(new_markdown_cell(content))

    for content in collect_labs(day_dir):
        cells.append(new_markdown_cell(content))

    # Teacher/correction mode
    if teacher:
        cells.append(
            new_markdown_cell(
                "# Corrigés\\n\\n"
                "Cette section est générée uniquement en mode formateur."
            )
        )

        for section in TEACHER_SECTIONS:
            content = read_section(day_dir / section)
            if content:
                cells.append(new_markdown_cell(content))

    nb = new_notebook(cells=cells)

    w_num = week_number(week_name)
    d_num = day_number(day_name)
    title = title_from_chapter(day_dir)
    slug = slugify(title)

    if teacher:
        out_dir = NOTEBOOKS / week_name / "teacher"
        filename = f"S{w_num}_J{d_num}_{slug}_teacher.ipynb"
    else:
        out_dir = NOTEBOOKS / week_name
        filename = f"S{w_num}_J{d_num}_{slug}.ipynb"

    out_dir.mkdir(parents=True, exist_ok=True)
    output = out_dir / filename

    with output.open("w", encoding="utf-8") as f:
        nbformat.write(nb, f)

    return output


def iter_days(week: str | None = None, day: str | None = None):
    weeks = [BOOK / week] if week else sorted(BOOK.glob("week*"))

    for week_dir in weeks:
        if not week_dir.exists():
            continue

        if day:
            day_dirs = [week_dir / day]
        else:
            day_dirs = sorted(week_dir.glob("day*"))

        for day_dir in day_dirs:
            if day_dir.exists() and day_dir.is_dir():
                yield week_dir.name, day_dir.name


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", help="Week directory name, e.g. week01")
    parser.add_argument("--day", help="Day directory name, e.g. day02")
    parser.add_argument(
        "--teacher",
        action="store_true",
        help="Include corrections from dayXX/corriges/",
    )

    args = parser.parse_args()

    generated = []
    for week_name, day_name in iter_days(args.week, args.day):
        generated.append(build_day_notebook(week_name, day_name, teacher=args.teacher))

    if not generated:
        raise SystemExit("No notebooks generated.")

    print("Generated notebooks:")
    for path in generated:
        print(f"- {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
