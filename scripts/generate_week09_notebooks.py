"""Notebooks S9 reproductibles; Markdown = source de vérité."""
from pathlib import Path
import hashlib
import json
import re
ROOT=Path(__file__).resolve().parents[1]
SLUGS=['chunking','embeddings','vector_store','hybrid_search','reranking','memoire_agents','projet_rag']


def cell(kind,text):
    result={'cell_type':kind,'metadata':{},'source':text}
    if kind=='code':result.update(execution_count=None,outputs=[])
    return result


def markdown(path,executable=False):
    text=path.read_text(encoding='utf-8')
    if not executable:return [cell('markdown',text)]
    result=[];position=0
    for match in re.finditer(r'^```python\n(.*?)^```\s*$',text,re.MULTILINE|re.DOTALL):
        before=text[position:match.start()].strip()
        if before:result.append(cell('markdown',before))
        result.append(cell('code',match.group(1).strip()));position=match.end()
    if text[position:].strip():result.append(cell('markdown',text[position:].strip()))
    return result


def build(day,teacher):
    base=ROOT/f'book/week09/day{day:02d}'
    cells=[]
    for name in ('README.md','learning_objectives.md','chapter.md'):cells+=markdown(base/name)
    cells.append(cell('markdown','## Diagramme du jour\n\n```mermaid\n'+(base/'diagrams/knowledge.mmd').read_text()+'```\n\nLe rendu Mermaid dépend du lecteur; la source .mmd reste disponible.'))
    cells+=markdown(base/'assets/notebook_lab.md',True)
    cells+=markdown(base/'labs/README.md')
    for name in ('exercises.md','interview.md','challenge.md'):cells+=markdown(base/name)
    if teacher:
        for name in ('exercises_solution.md','interview_solution.md','challenge_solution.md','review.md'):
            cells+=markdown(base/'corriges'/name,name=='challenge_solution.md')
    cells+=markdown(base/'references.md')
    for index,c in enumerate(cells):
        c['id']=hashlib.sha256(f'{index}:{c["source"]}'.encode()).hexdigest()[:16]
        c['source']=c['source'].splitlines(keepends=True)
    return {'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
                                     'language_info':{'name':'python'},'source_of_truth':f'book/week09/day{day:02d}',
                                     'variant':'teacher' if teacher else 'student'},'nbformat':4,'nbformat_minor':5}


def main():
    for day,slug in enumerate(SLUGS,1):
        for teacher in (False,True):
            path=ROOT/'notebooks/week09'/('teacher' if teacher else '')/f'S9_J{day}_{slug}{"_teacher" if teacher else ""}.ipynb'
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(json.dumps(build(day,teacher),ensure_ascii=False,indent=1,sort_keys=True)+'\n')
    print('14 notebooks S9 générés depuis les sources Markdown')

if __name__=='__main__':main()
