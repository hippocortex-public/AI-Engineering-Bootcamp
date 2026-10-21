"""Entraînement et rapports S10 : données fictives, calculs réellement exécutés."""
from pathlib import Path
import json
import platform
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from examples.week10.demo import scenario
from examples.week10.nlp import artifact,digest,read_data,specialized,trained
import numpy
import scipy
import sklearn
OUT=ROOT/'docs/week10/reports'


def write(name,value):
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,allow_nan=False,indent=2)+'\n')


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    bundle=trained()
    classification=scenario(5);extraction=scenario(2);summary=scenario(3);ner=scenario(4);embeddings=scenario(6);integrated=scenario(7)
    for name,value in [('classification.json',classification),('extraction.json',extraction),('summary.json',summary),
                       ('ner.json',ner),('embeddings.json',embeddings),('pipeline.json',integrated),
                       ('baseline_classifier.json',artifact(bundle,'baseline')),('adapted_classifier.json',artifact(bundle,'adapted'))]:
        write(name,value)
    projection,details=specialized()
    write('nca_projection.json',{'components':projection.components_.tolist(),'provenance':details,
                                'scope':'projection matrix; use the matching TF-IDF artifact and feature hash'})
    write('experiment.json',{'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__,
                            'scikit_learn':sklearn.__version__,'data_hash':digest(read_data('tickets.json')),
                            'examples_hash':digest(read_data('examples.json')),'provenance':bundle['provenance'],
                            'selected_epochs':bundle['selected_epochs'],'threshold_trials':bundle['threshold_trials'],
                            'nature':'real local learning; fictional corpus; LoRA not executed'})
    baseline=classification['baseline'];adapted=classification['adapted']
    md='# Rapport NLP — Semaine 10\n\nCorpus fictif; entraînements scikit-learn réellement exécutés. Aucun LLM ni LoRA exécuté.\n\n'
    md+='## Classification\n\n| Mesure test | Baseline | Tête adaptée |\n|---|---|---|\n'
    for name in ('count','accuracy_argmax','macro_f1_argmax','coverage','selective_accuracy','threshold'):
        md+=f'| {name} | {baseline[name]} | {adapted[name]} |\n'
    md+=f'\nEpochs retenus par validation : {classification["selected_epochs"]}. Vocabulaire inchangé : {classification["vocabulary_unchanged"]}. Poids modifiés : {classification["head_weights_changed"]}.\n'
    md+='\nL’adaptation change réellement les poids mais ne démontre pas de gain de F1 sur ce test facile. Aucun réglage n’a été choisi sur le test. Les résultats hors distribution sont inspectables avec la démo J1.\n'
    md+='\n## Extraction et NER\n\n'
    md+=f'{extraction["value_matches"]}/{extraction["field_count"]} valeurs et {extraction["status_matches"]}/{extraction["field_count"]} statuts corrects. Les champs ambigus restent null avec preuves conservées.\n\n'
    md+=f'NER : {ner["metrics"]["true_positive"]} spans exacts sur des noms connus, F1={ner["metrics"]["f1"]}. Ce résultat ne prouve pas le rappel sur de nouvelles entités ni un masquage exhaustif.\n'
    md+='\n## Projection spécialisée\n\n| Mode | Dimension | Precision@3 | Recall@3 | MRR@3 |\n|---|---|---|---|---|\n'
    for name,values in embeddings['retrieval']['modes'].items():
        md+=f'| {name} | {values["dimension"]} | {values["precision_at_3"]:.4f} | {values["recall_at_3"]:.4f} | {values["mrr_at_3"]:.4f} |\n'
    md+='\nLa pertinence est un proxy de même catégorie. Douze documents train sont pertinents par classe : le Recall@3 maximal vaut 0,25. Ce protocole ne mesure pas une pertinence sémantique humaine.\n'
    md+='\n## Limites\n\n72 tickets courts et fictifs, quatre exemples intégrés, labels simples. Le résumé est extractif et son proxy lexical n’évalue pas les omissions critiques. Le modèle reste non calibré pour le hors distribution. Les artefacts JSON gardent une empreinte locale, sans authentification d’auteur. Aucun service de production n’est déployé.\n'
    (OUT/'comparison.md').write_text(md)
    print('11 rapports et artefacts S10 régénérés')

if __name__=='__main__':main()
