"""Complétude S10, notebooks exécutables, liens, labs et tests."""
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
          'assets/notebook_lab.md','labs/README.md','labs/run.py','diagrams/nlp.mmd']


def run(args):
    process=subprocess.run([sys.executable,*args],cwd=ROOT,capture_output=True,text=True)
    if process.returncode:raise RuntimeError(process.stdout+process.stderr)
    return process.stdout+process.stderr


def main():
    os.chdir(ROOT)
    days=sorted((ROOT/'book/week10').glob('day*'))
    assert len(days)==7
    for day in days:
        for name in REQUIRED:assert (day/name).is_file() and (day/name).stat().st_size
        for folder in ('corriges','diagrams','assets','labs'):assert (day/folder).is_dir()
    notebooks=sorted((ROOT/'notebooks/week10').rglob('*.ipynb'))
    assert len(notebooks)==14
    before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in notebooks}
    run(['scripts/generate_week10_notebooks.py'])
    assert all(hashlib.sha256(p.read_bytes()).hexdigest()==digest for p,digest in before.items())
    executed=0
    for path in notebooks:
        notebook=json.loads(path.read_text())
        assert notebook['nbformat']==4 and notebook['nbformat_minor']==5
        assert len({c['id'] for c in notebook['cells']})==len(notebook['cells'])
        namespace={'__name__':'__main__'}
        for cell in notebook['cells']:
            assert cell['cell_type'] in ('markdown','code') and isinstance(cell['source'],list)
            if cell['cell_type']=='code':
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(compile(''.join(cell['source']),str(path),'exec'),namespace)
                executed+=1
        full=''.join(''.join(c['source']) for c in notebook['cells'])
        if notebook['metadata']['variant']=='student':assert '# Solution du challenge' not in full
        else:assert '# Solution du challenge' in full and '# Revue pédagogique' in full
    for file in (ROOT/'book/week10').rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',file.read_text()):
            if not target.startswith(('https:','http:','#')):
                assert (file.parent/target).exists(),(file,target)
    # Compiler aussi les adaptateurs optionnels sans importer leurs dépendances.
    for file in (ROOT/'examples/week10').rglob('*.py'):compile(file.read_text(),str(file),'exec')
    for day in range(1,8):run([f'book/week10/day{day:02d}/labs/run.py'])
    tests=run(['-m','unittest','discover','-s','tests/week10','-v'])
    print(json.dumps({'days':len(days),'notebooks':len(notebooks),'executed_code_cells':executed,
                     'markdown_regeneration':'identical','relative_links':'ok','labs':7,
                     'tests':int(re.search(r'Ran (\d+) tests',tests).group(1)),
                     'optional_adapters':'syntax only, not executed'},indent=2))

if __name__=='__main__':main()
