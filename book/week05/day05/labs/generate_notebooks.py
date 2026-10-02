"""Génère les notebooks depuis les sources Markdown du jour."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[4]
day = root / "book/week05/day05"
output = root / "notebooks/week05"

def markdown(path):
    return {"cell_type": "markdown", "metadata": {}, "source": path.read_text().splitlines(keepends=True)}

for teacher in (False, True):
    cells = [markdown(day / name) for name in ("README.md", "learning_objectives.md", "chapter.md", "exercises.md", "interview.md", "challenge.md")]
    if teacher:
        cells += [markdown(day / "corriges" / name) for name in ("exercises_solution.md", "interview_solution.md", "challenge_solution.md")]
    cells.append(markdown(day / "labs/README.md"))
    code = """from pathlib import Path
import sys
roots = [Path.cwd(), *Path.cwd().parents]
lab = next((r / 'book/week05/day05/labs' for r in roots if (r / 'book/week05/day05/labs').is_dir()), None)
if lab is None:
    raise RuntimeError('Ouvrir ce notebook depuis le dépôt ai-engineering-bootcamp.')
sys.path.insert(0, str(lab))
from fastapi.testclient import TestClient
from monitoring_ai_service.app import app, metrics_store
metrics_store.reset()
client = TestClient(app)
assert client.post('/chat', json={'message': 'Bonjour'}).status_code == 200
assert client.get('/metrics').json()['request_count'] == 1
client.get('/metrics').json()
"""
    cells.append({"cell_type": "code", "metadata": {}, "source": code.splitlines(keepends=True), "outputs": [], "execution_count": None})
    notebook = {"cells": cells, "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}, "language_info": {"name": "python", "version": "3.12"}}, "nbformat": 4, "nbformat_minor": 5}
    for index, cell in enumerate(cells):
        cell['id'] = f'cell-{index:03d}'
    path = output / ("teacher/S5_J5_monitoring_teacher.ipynb" if teacher else "S5_J5_monitoring.ipynb")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=2) + '\n')
