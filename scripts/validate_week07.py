"""Complétude, cellules exécutables et cohérence des exports S7."""
from pathlib import Path
import contextlib
import hashlib
import io
import json
import os
import re
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
REQUIRED=['README.md','learning_objectives.md','chapter.md','exercises.md','interview.md','challenge.md','references.md',
          'corriges/exercises_solution.md','corriges/interview_solution.md','corriges/challenge_solution.md','corriges/review.md',
          'diagrams/workflow.mmd','assets/event.json','assets/notebook_lab.md','labs/README.md','labs/run.py']


def main():
    os.chdir(ROOT)
    days=sorted((ROOT/'book/week07').glob('day*'))
    assert len(days)==7
    for day in days:
        for name in REQUIRED:
            path=day/name
            assert path.is_file() and path.stat().st_size, path
        for directory in ['corriges','diagrams','assets','labs']:
            assert (day/directory).is_dir()
    notebooks=sorted((ROOT/'notebooks/week07').rglob('*.ipynb'))
    assert len(notebooks)==14
    before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in notebooks}
    subprocess.run([sys.executable,'scripts/generate_week07_notebooks.py'],check=True,stdout=subprocess.DEVNULL)
    assert all(hashlib.sha256(p.read_bytes()).hexdigest()==digest for p,digest in before.items())
    cell_count=0
    for path in notebooks:
        notebook=json.loads(path.read_text())
        assert notebook['nbformat']==4 and notebook['nbformat_minor']==5
        assert len({cell['id'] for cell in notebook['cells']})==len(notebook['cells'])
        namespace={'__name__':'__main__'}
        for cell in notebook['cells']:
            assert cell['cell_type'] in {'code','markdown'} and isinstance(cell['source'],list)
            if cell['cell_type']=='code':
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(compile(''.join(cell['source']),str(path),'exec'),namespace)
                cell_count+=1
        text=''.join(''.join(c['source']) for c in notebook['cells'])
        if notebook['metadata']['variant']=='student':
            assert '# Corrigé des exercices' not in text and '# Réponses d’entretien' not in text
        else:
            assert '# Corrigé des exercices' in text and '# Revue pédagogique' in text
    workflows=sorted((ROOT/'examples/week07/workflows').glob('*.json'))
    assert len(workflows)==3
    for path in workflows:
        workflow=json.loads(path.read_text())
        assert workflow['active'] is False
        names={node['name'] for node in workflow['nodes']}
        for node in workflow['nodes']:
            assert 'credentials' not in node
        for source,links in workflow['connections'].items():
            assert source in names
            for branch in links['main']:
                for target in branch:
                    assert target['node'] in names
    for file in (ROOT/'book/week07').rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',file.read_text()):
            if not target.startswith(('http:','https:','#')):
                assert (file.parent/target).exists(), (file,target)
    print(json.dumps({'days':len(days),'notebooks':len(notebooks),'executed_code_cells':cell_count,
                      'n8n_exports_static':len(workflows),'regeneration':'identical','relative_links':'ok'},indent=2))


if __name__=='__main__':
    main()
