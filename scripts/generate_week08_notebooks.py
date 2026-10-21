"""14 notebooks dérivés du Markdown; format compatible avec le générateur J1."""
from pathlib import Path
import hashlib
import json
import re
ROOT=Path(__file__).resolve().parents[1]
SLUGS=['evaluation','benchmarks','observabilite','couts','gouvernance','securite','supervision']


def cell(kind,text):
    result={'cell_type':kind,'metadata':{},'source':text}
    if kind=='code':
        result.update(execution_count=None,outputs=[])
    return result


def read_cells(path,executable=False):
    text=path.read_text(encoding='utf-8')
    if not executable:
        return [cell('markdown',text)]
    result=[];position=0
    for match in re.finditer(r'^```python\n(.*?)^```\s*$',text,re.MULTILINE|re.DOTALL):
        before=text[position:match.start()].strip()
        if before: result.append(cell('markdown',before))
        result.append(cell('code',match.group(1).strip()))
        position=match.end()
    if text[position:].strip(): result.append(cell('markdown',text[position:].strip()))
    return result


def build(day,teacher=False):
    base=ROOT/f'book/week08/day{day:02d}'
    cells=[]
    for name in ('README.md','learning_objectives.md','chapter.md'):
        cells+=read_cells(base/name)
    cells+=read_cells(base/'assets/notebook_lab.md',True)
    for name in ('exercises.md','interview.md','challenge.md'):
        cells+=read_cells(base/name)
    if teacher:
        for name in ('exercises_solution.md','interview_solution.md','challenge_solution.md','review.md'):
            cells+=read_cells(base/'corriges'/name,name=='challenge_solution.md')
    cells+=read_cells(base/'references.md')
    for index,c in enumerate(cells):
        c['id']=hashlib.sha256(f'{index}:{c["source"]}'.encode()).hexdigest()[:16]
        c['source']=c['source'].splitlines(keepends=True)
    return {'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
                                    'language_info':{'name':'python'}},'nbformat':4,'nbformat_minor':5}


def main():
    for day,slug in enumerate(SLUGS,1):
        for teacher in (False,True):
            target=ROOT/'notebooks/week08'/('teacher' if teacher else '')/f'S8_J{day}_{slug}{"_teacher" if teacher else ""}.ipynb'
            target.parent.mkdir(parents=True,exist_ok=True)
            content=build(day,teacher)
            # indent=1, clés triées : même sérialisation que nbformat.write de J1.
            target.write_text(json.dumps(content,ensure_ascii=False,indent=1,sort_keys=True)+'\n',encoding='utf-8')
    print('14 notebooks générés depuis les sources Markdown')

if __name__=='__main__':
    main()
