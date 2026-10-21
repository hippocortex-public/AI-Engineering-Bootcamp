"""AI Ops pédagogique : preuves synthétiques, aucun SDK LLM ni appel externe."""
from __future__ import annotations
import hashlib
import json
import math
import re
from decimal import Decimal
from pathlib import Path


class EvidenceError(ValueError):
    """Donnée ou configuration invalide : décision de livraison interdite."""


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,
                                    separators=(',', ':'),allow_nan=False).encode()).hexdigest()


def unique_pairs(pairs):
    result={}
    for key,value in pairs:
        if key in result:
            raise EvidenceError('Clé JSON dupliquée')
        result[key]=value
    return result


def read_json(path):
    def invalid(_):
        raise EvidenceError('Nombre JSON non fini')
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'),object_pairs_hook=unique_pairs,parse_constant=invalid)
    except (ValueError,TypeError) as exc:
        raise EvidenceError(str(exc)) from exc


def finite_number(value, name, minimum=0):
    if type(value) not in (int,float) or not math.isfinite(value) or value < minimum:
        raise EvidenceError('Nombre invalide : '+name)
    return value


def validate_runs(rows):
    if not isinstance(rows,list) or not rows:
        raise EvidenceError('Mesures absentes')
    required={'run_id','case_id','repeat','status','duration_ms','input_tokens','cached_input_tokens',
              'output_tokens','human_wait_ms','trace_id','span_id','parent_span_id',
              'version','dataset_hash','workload_hash','config_hash'}
    ids=set()
    attempts=set()
    for row in rows:
        if not isinstance(row,dict) or set(row)!=required:
            raise EvidenceError('Contrat de mesure invalide')
        for name in ('run_id','case_id','version','dataset_hash','workload_hash','config_hash'):
            if not isinstance(row[name],str) or not row[name].strip():
                raise EvidenceError('Métadonnée absente : '+name)
        if row['run_id'] in ids:
            raise EvidenceError('run_id dupliqué')
        ids.add(row['run_id'])
        if type(row['repeat']) is not int or row['repeat']<1:
            raise EvidenceError('Répétition invalide')
        key=(row['case_id'],row['repeat'])
        if key in attempts:
            raise EvidenceError('Essai dupliqué')
        attempts.add(key)
        if row['status'] not in ('ok','timeout','error'):
            raise EvidenceError('Statut inconnu')
        for name in ('duration_ms','human_wait_ms'):
            finite_number(row[name],name)
        for name in ('input_tokens','cached_input_tokens','output_tokens'):
            if type(row[name]) is not int or row[name]<0:
                raise EvidenceError('Compteur de tokens invalide')
        if row['cached_input_tokens']>row['input_tokens']:
            raise EvidenceError('Cache supérieur aux tokens entrants')
        for name,length in [('trace_id',32),('span_id',16)]:
            if not isinstance(row[name],str) or not re.fullmatch(r'[0-9a-f]{%d}'%length,row[name]) or set(row[name])=={'0'}:
                raise EvidenceError('Identifiant de trace invalide')
        parent=row['parent_span_id']
        if parent is not None and (not isinstance(parent,str) or not re.fullmatch(r'[0-9a-f]{16}',parent)):
            raise EvidenceError('Parent de span invalide')
    for name in ('version','dataset_hash','workload_hash','config_hash'):
        if len({r[name] for r in rows})!=1:
            raise EvidenceError('Mesures de protocoles mélangés : '+name)
    return rows


def percentile(values, p):
    """Quantile empirique nearest-rank, échantillon non vide."""
    if not values:
        raise EvidenceError('Quantile sans observations')
    if type(p) not in (int,float) or not math.isfinite(p) or not 0<p<=1:
        raise EvidenceError('Quantile invalide')
    ordered=sorted(finite_number(v,'duration') for v in values)
    return ordered[math.ceil(len(ordered)*p)-1]


def validate_grid(runs, case_ids, repeats):
    validate_runs(runs)
    if type(repeats) is not int or repeats<1 or not case_ids or len(case_ids)!=len(set(case_ids)):
        raise EvidenceError('Grille attendue invalide')
    expected={(c,r) for c in case_ids for r in range(1,repeats+1)}
    actual={(r['case_id'],r['repeat']) for r in runs}
    if actual!=expected:
        raise EvidenceError('Essais manquants ou inconnus')


def benchmark(runs,case_ids,repeats=3):
    validate_grid(runs,case_ids,repeats)
    durations=[r['duration_ms'] for r in runs]
    elapsed_ms=sum(durations)
    return {'count':len(runs),'p50_ms':percentile(durations,.5),'p95_ms':percentile(durations,.95),
            'max_ms':max(durations),'technical_error_rate':sum(r['status']!='ok' for r in runs)/len(runs),
            'sequential_throughput_rps':len(runs)/(elapsed_ms/1000) if elapsed_ms else None,
            'human_wait_p95_ms':percentile([r['human_wait_ms'] for r in runs],.95),
            'method':'synthetic sequential replay; nearest-rank; errors included',
            'dataset_hash':runs[0]['dataset_hash'],'workload_hash':runs[0]['workload_hash'],
            'config_hash':runs[0]['config_hash'],'runs_hash':canonical_hash(runs)}


def comparable(left,right):
    for key in ('dataset_hash','workload_hash'):
        if left[key]!=right[key]:
            raise EvidenceError('Benchmarks non comparables : '+key)
    return {'p95_delta_ms':right['p95_ms']-left['p95_ms'],
            'error_delta':right['technical_error_rate']-left['technical_error_rate']}


def decimal_value(value,name):
    if type(value) not in (str,int):
        raise EvidenceError('Décimal attendu : '+name)
    try:
        result=Decimal(value)
    except Exception as exc:
        raise EvidenceError('Décimal invalide') from exc
    if not result.is_finite() or result<0:
        raise EvidenceError('Montant négatif ou non fini')
    return result


def validate_prices(prices):
    if not isinstance(prices,dict) or set(prices)!={'currency','kind','input_per_million','cached_per_million','output_per_million'}:
        raise EvidenceError('Grille tarifaire invalide')
    if prices['currency']!='USD' or prices['kind']!='synthetic':
        raise EvidenceError('Le lab utilise exclusivement des prix USD synthétiques')
    for key in ('input_per_million','cached_per_million','output_per_million'):
        decimal_value(prices[key],key)


def attempt_cost(row,prices):
    validate_prices(prices)
    # Appelé après validation des runs pour leurs compteurs.
    uncached=row['input_tokens']-row['cached_input_tokens']
    return (Decimal(uncached)*Decimal(prices['input_per_million'])+
            Decimal(row['cached_input_tokens'])*Decimal(prices['cached_per_million'])+
            Decimal(row['output_tokens'])*Decimal(prices['output_per_million']))/Decimal(1000000)


def cost_report(runs,prices,passed_ids):
    validate_runs(runs)
    validate_prices(prices)
    total=sum((attempt_cost(r,prices) for r in runs),Decimal(0))
    successes=sum(r['status']=='ok' and r['case_id'] in passed_ids for r in runs)
    return {'currency':'USD','price_kind':'synthetic','total_usd':str(total),
            'successful_attempts':successes,
            'usd_per_success':str(total/successes) if successes else None,
            'attempt_count':len(runs),'prices_hash':canonical_hash(prices),'runs_hash':canonical_hash(runs)}


class Budget:
    """Admission locale par réservation; pas un ledger distribué."""
    def __init__(self,limit):
        self.limit=decimal_value(limit,'limit')
        self.spent=Decimal(0)
        self.reserved={}
        self.done={}

    def reserve(self,request_id,maximum):
        amount=decimal_value(maximum,'maximum')
        if not isinstance(request_id,str) or not request_id or request_id in self.reserved or request_id in self.done:
            raise EvidenceError('Identifiant de réservation invalide')
        if self.spent+sum(self.reserved.values(),Decimal(0))+amount>self.limit:
            return False
        self.reserved[request_id]=amount
        return True

    def settle(self,request_id,actual):
        cost=decimal_value(actual,'actual')
        if request_id in self.done:
            if self.done[request_id]!=cost:
                raise EvidenceError('Règlement contradictoire')
            return
        if request_id not in self.reserved:
            raise EvidenceError('Réservation inconnue')
        ceiling=self.reserved[request_id]
        if cost>ceiling:
            raise EvidenceError('Coût supérieur au plafond réservé')
        del self.reserved[request_id]
        self.spent+=cost
        self.done[request_id]=cost


def telemetry(runs):
    validate_runs(runs)
    logs=[{key:r[key] for key in ('trace_id','span_id','parent_span_id','version','status','duration_ms')}
          for r in runs]
    counters={status:sum(r['status']==status for r in runs) for status in ('ok','timeout','error')}
    return {'logs':logs,'metrics':{'requests_by_status':counters,'p95_ms':percentile([r['duration_ms'] for r in runs],.95)},
            'note':'JSON illustratif, pas un export OTLP ni une instrumentation SDK'}


def authorize(actor,tenant,tool,arguments,grant=None):
    """Contrôle d’action, sans exécution d’outil. Identité supposée authentifiée."""
    if not isinstance(actor,dict) or actor.get('tenant')!=tenant:
        return {'allowed':False,'reason':'tenant_mismatch'}
    if tool not in ('read_ticket','publish_draft'):
        return {'allowed':False,'reason':'unknown_tool'}
    if not isinstance(arguments,dict) or set(arguments)!={'ticket_id','tenant'} or arguments.get('tenant')!=tenant:
        return {'allowed':False,'reason':'invalid_arguments'}
    if not isinstance(arguments['ticket_id'],str) or not re.fullmatch(r'T-[0-9]{3}',arguments['ticket_id']):
        return {'allowed':False,'reason':'invalid_ticket'}
    if tool=='read_ticket' and actor.get('role') in ('reader','reviewer'):
        return {'allowed':True,'reason':'read_granted'}
    if tool=='publish_draft' and actor.get('role')=='reviewer' and grant is not None:
        expected=canonical_hash({'tenant':tenant,'tool':tool,'arguments':arguments})
        if isinstance(grant,dict) and grant.get('approved') is True and grant.get('action_hash')==expected:
            return {'allowed':True,'reason':'bound_approval'}
    return {'allowed':False,'reason':'insufficient_permission'}


def run_security(cases):
    if not isinstance(cases,list) or not cases:
        raise EvidenceError('Cas de sécurité absents')
    ids=[]
    results=[]
    for case in cases:
        if not isinstance(case,dict) or set(case)!={'id','actor','tenant','tool','arguments','grant','expected_allowed','untrusted_text'}:
            raise EvidenceError('Contrat de sécurité invalide')
        if not isinstance(case['id'],str) or not case['id'] or case['id'] in ids or type(case['expected_allowed']) is not bool:
            raise EvidenceError('Identité ou oracle du cas invalide')
        ids.append(case['id'])
        observed=authorize(case['actor'],case['tenant'],case['tool'],case['arguments'],case['grant'])
        results.append({'id':case['id'],'passed':observed['allowed']==case['expected_allowed'],**observed})
    return {'count':len(results),'passed':all(r['passed'] for r in results),'cases':results,
            'suite_hash':canonical_hash(cases),'note':'Tests du contrôleur de permissions, aucun modèle ni outil réel'}


def govern(manifest, expected_config, policy, day):
    required={'release_id','owner','reviewer','approved','config_hash','valid_until','risk_review','rollback_ref'}
    if not isinstance(manifest,dict) or set(manifest)!=required:
        raise EvidenceError('Manifeste de livraison invalide')
    from datetime import date
    try:
        expiry=date.fromisoformat(manifest['valid_until'])
        current=date.fromisoformat(day)
    except (ValueError,TypeError) as exc:
        raise EvidenceError('Date invalide') from exc
    text_fields=('release_id','owner','reviewer','config_hash','risk_review','rollback_ref')
    if any(not isinstance(manifest[x],str) or not manifest[x].strip() for x in text_fields) or type(manifest['approved']) is not bool:
        raise EvidenceError('Métadonnées de gouvernance invalides')
    reasons=[]
    if manifest['config_hash']!=expected_config: reasons.append('configuration_changed')
    if manifest['reviewer'] not in policy['reviewers']: reasons.append('reviewer_not_authorized')
    if manifest['owner']==manifest['reviewer']: reasons.append('separation_of_duties')
    if not manifest['approved']: reasons.append('approval_missing')
    if expiry<current: reasons.append('approval_expired')
    return {'accepted':not reasons,'reasons':reasons,'manifest_hash':canonical_hash(manifest)}


def validate_policy(policy):
    required={'minimum_quality','max_p95_ms','max_error_rate','max_usd_per_success','reviewers'}
    if not isinstance(policy,dict) or set(policy)!=required:
        raise EvidenceError('Politique invalide')
    for key in ('minimum_quality','max_p95_ms','max_error_rate'):
        finite_number(policy[key],key)
    if policy['minimum_quality']>1 or policy['max_error_rate']>1:
        raise EvidenceError('Taux hors intervalle')
    decimal_value(policy['max_usd_per_success'],'max_usd_per_success')
    if not isinstance(policy['reviewers'],list) or not policy['reviewers'] or any(not isinstance(x,str) or not x for x in policy['reviewers']):
        raise EvidenceError('Relecteurs requis')


def assess(evaluation,runs,prices,manifest,policy,security_cases,day):
    """Décision restrictive : preuve invalide => exception, jamais succès par défaut."""
    validate_policy(policy)
    ids=[c['id'] for c in evaluation['cases']]
    measured=benchmark(runs,ids)
    if evaluation['dataset_hash']!=measured['dataset_hash']:
        raise EvidenceError('Empreinte dataset différente')
    passed={c['id'] for c in evaluation['cases'] if c['passed']}
    costs=cost_report(runs,prices,passed)
    governance=govern(manifest,measured['config_hash'],policy,day)
    security=run_security(security_cases)
    if not security['count'] or not any(not c['expected_allowed'] for c in security_cases) or not any(c['expected_allowed'] for c in security_cases):
        raise EvidenceError('Suite sécurité sans cas positifs et négatifs')
    checks={'quality':evaluation['accepted'] is True and evaluation['critical_ok'] is True and evaluation['coverage']==1 and evaluation['rate']>=policy['minimum_quality'],
            'performance':measured['p95_ms']<=policy['max_p95_ms'] and measured['technical_error_rate']<=policy['max_error_rate'],
            'cost':costs['usd_per_success'] is not None and Decimal(costs['usd_per_success'])<=Decimal(policy['max_usd_per_success']),
            'governance':governance['accepted'],'security':security['passed']}
    return {'schema_version':1,'day':day,'release_id':manifest['release_id'],'checks':checks,
            'accepted':all(checks.values()),'failed_checks':[k for k,v in checks.items() if not v],
            'quality':{'rate':evaluation['rate'],'coverage':evaluation['coverage'],'critical_ok':evaluation['critical_ok']},
            'benchmark':measured,'cost':costs,'governance':governance,'security':security,
            'evidence_hash':canonical_hash({'evaluation':evaluation,'runs':runs,'prices':prices,'manifest':manifest,'policy':policy,'security_cases':security_cases}),
            'scope':'synthetic local evidence; no production authorization or deployment'}
