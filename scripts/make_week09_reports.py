"""Rapports recalculés depuis le corpus S9 et les qrels locaux."""
from pathlib import Path
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from examples.week09.demo import populated,evaluate_retrieval
from examples.week09.knowledge import answer
OUT=ROOT/'docs/week09/reports'


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    store=populated()
    try:
        evaluation=evaluate_retrieval(store)
        response=answer(store,'Comment rejouer un paiement avec Kafka ?','team-a')
        abstention=answer(store,'Quelle météo demain à Oslo ?','team-a')
        paraphrase=answer(store,'Retenter un encaissement depuis le journal distribué','team-a')
        state={'documents':store.db.execute('SELECT COUNT(*) FROM documents').fetchone()[0],
               'chunks':store.db.execute('SELECT COUNT(*) FROM chunks').fetchone()[0],
               'embedding':store.embedding.fingerprint,'storage':'SQLite + exact scan Python'}
    finally:store.close()
    for name,value in [('retrieval.json',evaluation),('answer.json',response),('abstention.json',abstention),('index_summary.json',state),('paraphrase_answer.json',paraphrase)]:
        (OUT/name).write_text(json.dumps(value,ensure_ascii=False,allow_nan=False,indent=2)+'\n')
    md='# Rapport de retrieval — Semaine 9\n\n'
    md+='Corpus fictif, calculs réellement exécutés; aucun modèle neuronal ou génératif interrogé.\n\n'
    md+='| Mode | Recall@3 | MRR@3 | nDCG@3 |\n|---|---|---|---|\n'
    for mode,values in evaluation['summaries'].items():
        md+=f'| {mode} | {values["recall_at_k"]:.4f} | {values["mrr_at_k"]:.4f} | {values["ndcg_at_k"]:.4f} |\n'
    md+='\n## Cas de paraphrase q8\n\n'
    for case in evaluation['cases']:
        if case['query_id']=='q8':
            md+=f'- {case["mode"]} : documents {case["ranked_docs"]}, Recall@3={case["recall_at_k"]}.\n'
    md+='\nSur q8, hashbow retrouve le document pertinent au rang 3 grâce à des similarités de projection accidentelles, mais le premier résultat est un autre sujet. La réponse extractive s’abstient : aucun passage ne satisfait la couverture lexicale. Ce gain de Recall@3 ne prouve donc aucune compréhension des synonymes. Ne pas supprimer ce cas pour améliorer la moyenne. Les deux questions hors corpus sont conservées dans retrieval.json avec leur statut d’abstention.\n'
    md+='\n## Provenance\n\n'
    md+=f'Corpus : `{evaluation["corpus_hash"]}`.\n\nQrels : `{evaluation["qrels_hash"]}`.\n\nEncodeur : `{evaluation["embedding"]}`.\n'
    md+='\nLe jeu contient huit questions positives et deux questions hors corpus. Il est réservé à la démonstration et au développement, sans validation indépendante de production. Une citation vérifiée n’est pas une preuve de vérité générale.\n'
    (OUT/'comparison.md').write_text(md)
    print('6 rapports S9 recalculés')

if __name__=='__main__':main()
