"""Notebooks reproductibles : les sources Markdown restent autoritaires."""
import hashlib
import re
from pathlib import Path

import nbformat


def markdown_cells(path: Path, execute_python: bool = False) -> list:
    text = path.read_text(encoding="utf-8")
    if not execute_python:
        return [nbformat.v4.new_markdown_cell(text)]
    cells = []
    position = 0
    for match in re.finditer(r"^```python\n(.*?)^```\s*$", text, re.MULTILINE | re.DOTALL):
        before = text[position:match.start()].strip()
        if before:
            cells.append(nbformat.v4.new_markdown_cell(before))
        cells.append(nbformat.v4.new_code_cell(match.group(1).strip()))
        position = match.end()
    if text[position:].strip():
        cells.append(nbformat.v4.new_markdown_cell(text[position:].strip()))
    return cells


def generate() -> None:
    root = Path(__file__).resolve().parents[4]
    day = root / "book/week05/day06"
    for teacher in (False, True):
        cells = []
        for name in ("README.md", "learning_objectives.md", "chapter.md"):
            cells += markdown_cells(day / name)
        cells += markdown_cells(day / "assets/notebook_lab.md", execute_python=True)
        for name in ("exercises.md", "interview.md", "challenge.md"):
            cells += markdown_cells(day / name)
        if teacher:
            for name in ("exercises_solution.md", "interview_solution.md", "challenge_solution.md", "review.md"):
                cells += markdown_cells(day / "corriges" / name, execute_python=(name == "challenge_solution.md"))
        cells += markdown_cells(day / "references.md")
        notebook = nbformat.v4.new_notebook(cells=cells)
        notebook.metadata = {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        }
        for index, cell in enumerate(notebook.cells):
            cell.id = hashlib.sha256(f"{index}:{cell.source}".encode()).hexdigest()[:16]
        nbformat.validate(notebook)
        relative = "teacher/S5_J6_security_teacher.ipynb" if teacher else "S5_J6_security.ipynb"
        output = root / "notebooks/week05" / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        nbformat.write(notebook, output)
        print(output.name)


if __name__ == "__main__":
    generate()
