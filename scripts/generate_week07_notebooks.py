"""Génération déterministe des notebooks depuis les fichiers Markdown S7."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SPECS = [
    ('n8n_fondations',1),('orchestration_etat',2),('evenements_contrats',3),
    ('fiabilite_reprises',4),('workflows_hybrides',5),('human_in_loop',6),
    ('projet_integration',7),
]


def markdown(text):
    return {'cell_type':'markdown','metadata':{},'source':text.splitlines(keepends=True)}


def code(text):
    return {'cell_type':'code','metadata':{},'source':text.splitlines(keepends=True),
            'execution_count':None,'outputs':[]}


def parse_lab(text):
    cells=[]
    position=0
    for match in re.finditer(r'^```python\n(.*?)^```\s*$',text,flags=re.MULTILINE|re.DOTALL):
        if text[position:match.start()].strip():
            cells.append(markdown(text[position:match.start()]))
        cells.append(code(match.group(1)))
        position=match.end()
    if text[position:].strip():
        cells.append(markdown(text[position:]))
    return cells


def build(day, slug, teacher=False):
    base=ROOT/f'book/week07/day{day:02d}'
    cells=[]
    for name in ['README.md','learning_objectives.md','chapter.md']:
        cells.append(markdown((base/name).read_text()))
    cells.append(markdown('## Diagramme du jour\n\n```mermaid\n'+(base/'diagrams/workflow.mmd').read_text()+'```\n\nSi votre lecteur Jupyter ne rend pas Mermaid, ouvrir le fichier .mmd avec un lecteur compatible.'))
    cells.extend(parse_lab((base/'assets/notebook_lab.md').read_text()))
    cells.append(markdown((base/'labs/README.md').read_text()))
    for name in ['exercises.md','interview.md','challenge.md','references.md']:
        cells.append(markdown((base/name).read_text()))
    if teacher:
        for name in ['exercises_solution.md','interview_solution.md','challenge_solution.md','review.md']:
            cells.append(markdown((base/'corriges'/name).read_text()))
        cells.extend(parse_lab((base/'corriges/lab_solution.md').read_text()))
    # Identifiants déterministes compatibles nbformat 4.5.
    for index,cell in enumerate(cells):
        cell['id']=f'w7d{day}-{index:03d}'
    return {'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
                                     'language_info':{'name':'python','version':'3.12'},
                                     'source_of_truth':f'book/week07/day{day:02d}',
                                     'variant':'teacher' if teacher else 'student'},
            'nbformat':4,'nbformat_minor':5}


def main():
    for slug,day in SPECS:
        for teacher in [False,True]:
            stem=f'S7_J{day}_{slug}'+('_teacher' if teacher else '')
            folder=ROOT/'notebooks/week07'/('teacher' if teacher else '')
            folder.mkdir(parents=True,exist_ok=True)
            (folder/(stem+'.ipynb')).write_text(json.dumps(build(day,slug,teacher),ensure_ascii=False,indent=2)+'\n')
    print('14 notebooks générés depuis le Markdown')


if __name__ == '__main__':
    main()
