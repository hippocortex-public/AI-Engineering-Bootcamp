from __future__ import annotations
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
from .ops import EvidenceError, assess, benchmark, comparable, cost_report, telemetry, govern, run_security, read_json, Budget
ROOT=Path(__file__).resolve().parents[2]
FIXTURES=Path(__file__).resolve().parent/'fixtures'
LAB=ROOT/'book/week08/day01/labs'
sys.path.insert(0,str(LAB))
from evaluation_lab.core import read_rows, evaluate, compare


def load(version):
    if version not in ('baseline','candidate'):
        raise EvidenceError('Version inconnue')
    assets=ROOT/'book/week08/day01/assets'
    evaluation=evaluate(read_rows(assets/'dataset.jsonl'),read_rows(assets/(version+'.jsonl')))
    return {'evaluation':evaluation,'runs':read_json(FIXTURES/(version+'_runs.json')),
            'prices':read_json(FIXTURES/'prices.json'),'manifest':read_json(FIXTURES/(version+'_release.json')),
            'policy':read_json(FIXTURES/'policy.json'),'security_cases':read_json(FIXTURES/'security_cases.json')}


def scenario(day,version='baseline',as_of='2026-10-20'):
    data=load(version)
    report=data['evaluation']
    ids=[c['id'] for c in report['cases']]
    if day==1:
        other=load('candidate')['evaluation']
        base=load('baseline')['evaluation']
        return {'baseline_rate':base['rate'],'candidate_rate':other['rate'],'comparison':compare(base,other)}
    if day==2:
        base=load('baseline'); candidate=load('candidate')
        left=benchmark(base['runs'],ids); right=benchmark(candidate['runs'],ids)
        return {'baseline':left,'candidate':right,'comparison':comparable(left,right)}
    if day==3:
        return telemetry(data['runs'])
    if day==4:
        result=cost_report(data['runs'],data['prices'],{c['id'] for c in report['cases'] if c['passed']})
        budget=Budget('0.01')
        first=budget.reserve('call-1','0.008')
        second=budget.reserve('call-2','0.008')
        budget.settle('call-1','0.003')
        result['admission_demo']={'first':first,'parallel_second':second,'spent_usd':str(budget.spent)}
        return result
    if day==5:
        config=data['runs'][0]['config_hash']
        accepted=govern(data['manifest'],config,data['policy'],as_of)
        stale=deepcopy(data['manifest']);stale['config_hash']='changed'
        return {'current':accepted,'stale':govern(stale,config,data['policy'],as_of)}
    if day==6:
        return run_security(data['security_cases'])
    if day==7:
        return assess(**data,day=as_of)
    raise EvidenceError('Jour attendu entre 1 et 7')


def main():
    parser=argparse.ArgumentParser(description='AI Ops sur fixtures synthétiques, sans appel LLM')
    parser.add_argument('--day',type=int,choices=range(1,8),default=7)
    parser.add_argument('--version',choices=['baseline','candidate'],default='baseline')
    parser.add_argument('--as-of',default='2026-10-20',help='date de décision explicite pour le replay')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    try:
        result=scenario(args.day,args.version,args.as_of)
        text=json.dumps(result,ensure_ascii=False,allow_nan=False,indent=2)+'\n'
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=True)
            args.output.write_text(text)
        print(text,end='')
        return 1 if args.day==7 and not result['accepted'] else 0
    except (EvidenceError,ValueError,KeyError,OSError) as exc:
        print('Preuve invalide : '+str(exc),file=sys.stderr)
        return 2

if __name__=='__main__':
    raise SystemExit(main())
