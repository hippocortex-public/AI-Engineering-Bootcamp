"""Rapports JSON, Markdown et HTML statique calculés depuis les preuves S8."""
from pathlib import Path
from html import escape
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from examples.week08.demo import scenario
OUT=ROOT/'docs/week08/reports'


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    reports={name:scenario(7,name) for name in ('baseline','candidate')}
    for name,report in reports.items():
        (OUT/(name+'_release.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (OUT/'candidate_telemetry.json').write_text(json.dumps(scenario(3,'candidate'),ensure_ascii=False,indent=2)+'\n')
    a,b=reports['baseline'],reports['candidate']
    rows=[('Décision locale','ACCEPTÉE' if a['accepted'] else 'REFUSÉE','ACCEPTÉE' if b['accepted'] else 'REFUSÉE'),
          ('Qualité J1',f'{a["quality"]["rate"]:.2%}',f'{b["quality"]["rate"]:.2%}'),
          ('Cas critiques',str(a['quality']['critical_ok']),str(b['quality']['critical_ok'])),
          ('p95 automatisé (ms)',str(a['benchmark']['p95_ms']),str(b['benchmark']['p95_ms'])),
          ('Maximum (ms)',str(a['benchmark']['max_ms']),str(b['benchmark']['max_ms'])),
          ('Erreurs techniques',f'{a["benchmark"]["technical_error_rate"]:.2%}',f'{b["benchmark"]["technical_error_rate"]:.2%}'),
          ('Coût utile USD synthétique',a['cost']['usd_per_success'],b['cost']['usd_per_success']),
          ('Contrôles refusés',', '.join(a['failed_checks']) or 'aucun',', '.join(b['failed_checks']) or 'aucun')]
    md='# Rapport de supervision synthétique — 20 octobre 2026\n\n'
    md+='Données fabriquées; aucun fournisseur, outil externe ou déploiement exécuté.\n\n| Indicateur | Baseline | Candidat |\n|---|---|---|\n'
    md+=''.join(f'| {label} | {left} | {right} |\n' for label,left,right in rows)
    md+='\nLe candidat est plus rapide et moins cher, mais la régression critique c09 bloque quality. Les 36 tentatives par version réutilisent les 12 résultats de qualité de J1; ce ne sont pas 36 générations indépendantes.\n'
    (OUT/'comparison.md').write_text(md)
    table=''.join('<tr>'+''.join('<td>'+escape(str(value))+'</td>' for value in row)+'</tr>' for row in rows)
    checks=''.join('<tr><th>'+escape(key)+'</th>'+''.join('<td class="'+('pass' if reports[name]['checks'][key] else 'fail')+'">'+('Conforme' if reports[name]['checks'][key] else 'Refusé')+'</td>' for name in ('baseline','candidate'))+'</tr>' for key in a['checks'])
    html='''<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Supervision AI Ops — S8</title>
<style>body{margin:0;background:#0b1422;color:#e8eef9;font:16px/1.6 system-ui,sans-serif}main{max-width:1080px;margin:0 auto;padding:48px 24px}h1{font-size:38px;line-height:1.2;margin:14px 0}h2{margin-top:36px}p{max-width:880px;color:#bbc9dc}.tag{font-size:13px;letter-spacing:.1em;color:#8ed9d0}.cards{display:flex;gap:20px;flex-wrap:wrap;margin:30px 0}.card{padding:22px 26px;background:#152238;border:1px solid #30435f;border-radius:12px;flex:1;min-width:240px}.pass{color:#8de3bb}.fail{color:#ffa6ac}table{width:100%;border-collapse:collapse;background:#121f32}td,th{text-align:left;padding:13px 16px;border-bottom:1px solid #2b3a50}thead{background:#1b2e49}.scroll{overflow:auto}.note{padding:18px;border-left:4px solid #e7b76a;background:#1f2633}footer{margin-top:40px;font-size:14px;color:#9badc3}</style><main>
<div class="tag">AI ENGINEERING BOOTCAMP · SEMAINE 8 · REPLAY AU 20/10/2026</div><h1>Une meilleure moyenne ne suffit pas.</h1><p>Le candidat gagne en vitesse et en coût utile. Une régression critique maintient le refus de livraison selon la politique pédagogique.</p>
<div class="cards"><div class="card"><b>Baseline</b><h2 class="pass">Acceptation locale</h2><p>Cinq contrôles conformes sur les fixtures.</p></div><div class="card"><b>Candidat</b><h2 class="fail">Refus : qualité</h2><p>Le cas critique c09 reste bloquant.</p></div></div>
<p class="note"><b>Rapport synthétique.</b> Aucun fournisseur mesuré, aucune action métier exécutée et aucun déploiement autorisé. Les prix, durées, identités et approbations sont fictifs.</p>
<h2>Comparaison</h2><div class="scroll"><table><thead><tr><th>Indicateur</th><th>Baseline</th><th>Candidat</th></tr></thead><tbody>'''+table+'''</tbody></table></div>
<h2>Contrôles indépendants</h2><div class="scroll"><table><thead><tr><th>Contrôle</th><th>Baseline</th><th>Candidat</th></tr></thead><tbody>'''+checks+'''</tbody></table></div>
<footer>36 tentatives synthétiques par version. Qualité issue de 12 cas J1, réutilisée pour les répétitions. Le p95 est un nearest-rank incluant les erreurs. Les preuves détaillées figurent dans les rapports JSON et le runbook.</footer></main></html>'''
    (OUT/'supervision.html').write_text(html)
    print('5 rapports de référence régénérés')

if __name__=='__main__':main()
