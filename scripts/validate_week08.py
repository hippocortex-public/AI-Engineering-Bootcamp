"""Contrôles reproductibles : structure, génération, cellules, labs et tests."""
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
          'corriges/exercises_solution.md','corriges/interview_solution.md','corriges/challenge_solution.md','corriges/review.md']


def run(args,cwd=ROOT):
    result=subprocess.run([sys.executable,*args],cwd=cwd,capture_output=True,text=True)
    if result.returncode:
        raise RuntimeError(result.stdout+result.stderr)
    return result.stdout+result.stderr


def main():
    os.chdir(ROOT)
    days=sorted((ROOT/'book/week08').glob('day*'))
    assert len(days)==7
    for day in days:
        for name in REQUIRED:assert (day/name).is_file() and (day/name).stat().st_size
        for name in ('corriges','diagrams','assets','labs'):
            assert (day/name).is_dir() and any((day/name).iterdir())
    notebooks=sorted((ROOT/'notebooks/week08').rglob('*.ipynb'))
    assert len(notebooks)==14
    original={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in notebooks}
    run(['scripts/generate_week08_notebooks.py'])
    assert all(hashlib.sha256(p.read_bytes()).hexdigest()==digest for p,digest in original.items())
    cells=0
    for path in notebooks:
        document=json.loads(path.read_text())
        assert document['nbformat']==4 and document['nbformat_minor']==5
        assert len({c['id'] for c in document['cells']})==len(document['cells'])
        namespace={'__name__':'__main__'}
        for cell in document['cells']:
            assert cell['cell_type'] in ('markdown','code') and isinstance(cell['source'],list)
            if cell['cell_type']=='code':
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(compile(''.join(cell['source']),str(path),'exec'),namespace)
                cells+=1
        texts=''.join(''.join(c['source']) for c in document['cells'])
        if path.parent.name!='teacher':assert '# Solution du challenge' not in texts
        else:assert '# Solution du challenge' in texts
    for file in (ROOT/'book/week08').rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',file.read_text()):
            if not target.startswith(('https:','http:','#')):
                assert (file.parent/target).exists(),(file,target)
    for day in range(2,8):run([f'book/week08/day{day:02d}/labs/run.py'])
    tests_j1=run(['-m','unittest','discover','-s','evaluation_lab/tests','-v'],ROOT/'book/week08/day01/labs')
    tests_ops=run(['-m','unittest','discover','-s','tests/week08','-v'])
    # Les codes CLI 0/1/2 sont vérifiés par les tests métier.
    print(json.dumps({'days':len(days),'notebooks':len(notebooks),'executed_code_cells':cells,
                      'markdown_regeneration':'identical','relative_links':'ok','labs_j2_j7':'ok',
                      'tests_j1':int(re.search(r'Ran (\d+) tests',tests_j1).group(1)),
                      'tests_ops':int(re.search(r'Ran (\d+) tests',tests_ops).group(1))},indent=2))

if __name__=='__main__':main()
