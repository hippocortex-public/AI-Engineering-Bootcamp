"""Validate the mandatory day structure for the bootcamp."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"

MANDATORY_FILES = [
    "README.md",
    "learning_objectives.md",
    "chapter.md",
    "exercises.md",
    "interview.md",
    "challenge.md",
    "references.md",
]

MANDATORY_DIRS = [
    "corriges",
    "diagrams",
    "assets",
    "labs",
]

MANDATORY_CORRIGES = [
    "exercises_solution.md",
    "interview_solution.md",
    "challenge_solution.md",
    "review.md",
]


def validate_day(day_dir: Path) -> list[str]:
    errors: list[str] = []

    for file_name in MANDATORY_FILES:
        if not (day_dir / file_name).exists():
            errors.append(f"{day_dir.relative_to(ROOT)} missing file: {file_name}")

    for dir_name in MANDATORY_DIRS:
        if not (day_dir / dir_name).is_dir():
            errors.append(f"{day_dir.relative_to(ROOT)} missing directory: {dir_name}")

    corriges = day_dir / "corriges"
    if corriges.exists():
        for file_name in MANDATORY_CORRIGES:
            if not (corriges / file_name).exists():
                errors.append(
                    f"{day_dir.relative_to(ROOT)} missing correction file: corriges/{file_name}"
                )

    labs = day_dir / "labs"
    if labs.exists() and not any(p.is_file() for p in labs.iterdir()):
        errors.append(f"{day_dir.relative_to(ROOT)} labs/ must contain at least README.md")

    return errors


def main() -> None:
    if not BOOK.exists():
        raise SystemExit("book/ directory not found")

    day_dirs = sorted(d for d in BOOK.glob("week*/day*") if d.is_dir())

    errors: list[str] = []
    for day_dir in day_dirs:
        errors.extend(validate_day(day_dir))

    if errors:
        print("Day structure validation failed:\n")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(f"Validated {len(day_dirs)} day directories.")


if __name__ == "__main__":
    main()
