"""Validate notebook files as well-formed Jupyter notebooks."""

from __future__ import annotations

from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIRS = [
    ROOT / "notebooks",
    ROOT / "book",
]


def iter_notebooks():
    for directory in NOTEBOOK_DIRS:
        if directory.exists():
            yield from directory.rglob("*.ipynb")


def main() -> None:
    notebooks = sorted(iter_notebooks())

    for notebook in notebooks:
        with notebook.open("r", encoding="utf-8") as f:
            nbformat.read(f, as_version=4)

    print(f"Validated {len(notebooks)} notebook files.")


if __name__ == "__main__":
    main()
