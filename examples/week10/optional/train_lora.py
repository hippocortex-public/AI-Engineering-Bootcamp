"""Lab optionnel non exécuté : LoRA SEQ_CLS sur un modèle BERT local.
Nécessite torch, transformers, peft et un tokenizer/base-model sur disque.
"""
from pathlib import Path
import argparse
import json
import random


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--base-model',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--epochs',type=int,default=3)
    args=parser.parse_args()
    if not args.base_model.is_dir() or args.epochs<1:raise SystemExit('Modèle local et epochs positifs requis')
    if args.output.exists() and any(args.output.iterdir()):raise SystemExit('Utiliser un répertoire de sortie vide')
    import numpy as np
    import torch
    from transformers import AutoConfig,AutoTokenizer,AutoModelForSequenceClassification
    from peft import LoraConfig,TaskType,get_peft_model
    from sklearn.metrics import f1_score
    torch.manual_seed(17);random.seed(17);np.random.seed(17)
    config=AutoConfig.from_pretrained(str(args.base_model),local_files_only=True,trust_remote_code=False)
    if config.model_type!='bert':raise SystemExit('Ce lab cible BERT : query/value et classifier; adapter explicitement une autre architecture')
    tokenizer=AutoTokenizer.from_pretrained(str(args.base_model),local_files_only=True,trust_remote_code=False)
    if tokenizer.pad_token_id is None:raise SystemExit('Tokenizer avec padding requis')
    labels=['acces','deploiement','performance'];label_to_id={label:i for i,label in enumerate(labels)}
    base=AutoModelForSequenceClassification.from_pretrained(str(args.base_model),local_files_only=True,
        trust_remote_code=False,num_labels=3,ignore_mismatched_sizes=True,
        id2label={i:label for i,label in enumerate(labels)},label2id=label_to_id)
    model=get_peft_model(base,LoraConfig(task_type=TaskType.SEQ_CLS,r=4,lora_alpha=8,lora_dropout=.05,
                                        target_modules=['query','value'],modules_to_save=['classifier']))
    # CPU pour rester explicite; ce script ne suppose pas de GPU disponible.
    model.to('cpu')
    from ..nlp import validate_dataset
    rows=validate_dataset(json.loads((Path(__file__).resolve().parents[1]/'data/tickets.json').read_text()))
    train=[r for r in rows if r['split']=='train'];validation=[r for r in rows if r['split']=='validation']
    optimizer=torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],lr=1e-4)
    best=-1.0;history=[]
    for epoch in range(1,args.epochs+1):
        order=list(range(len(train)));random.Random(17+epoch).shuffle(order)
        model.train()
        for position in range(0,len(order),8):
            batch=[train[i] for i in order[position:position+8]]
            encoded=tokenizer([r['text'] for r in batch],padding=True,truncation=True,max_length=128,return_tensors='pt')
            target=torch.tensor([label_to_id[r['label']] for r in batch])
            optimizer.zero_grad();loss=model(**encoded,labels=target).loss
            loss.backward();optimizer.step()
        model.eval()
        with torch.no_grad():
            encoded=tokenizer([r['text'] for r in validation],padding=True,truncation=True,max_length=128,return_tensors='pt')
            predicted=model(**encoded).logits.argmax(dim=-1).tolist()
        score=float(f1_score([label_to_id[r['label']] for r in validation],predicted,labels=[0,1,2],average='macro',zero_division=0))
        history.append({'epoch':epoch,'validation_macro_f1':score})
        if score>best:
            best=score;args.output.mkdir(parents=True,exist_ok=True)
            model.save_pretrained(str(args.output));tokenizer.save_pretrained(str(args.output))
    import hashlib
    data_hash=hashlib.sha256(json.dumps(train,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    (args.output/'experiment.json').write_text(json.dumps({'base_model_path':str(args.base_model.resolve()),
      'base_revision':getattr(config,'_commit_hash',None),'training_data_hash':data_hash,'seed':17,
      'history':history,'selection':'validation only; test not evaluated by this script',
      'trainable_parameters':sum(p.numel() for p in model.parameters() if p.requires_grad),
      'total_parameters':sum(p.numel() for p in model.parameters())},ensure_ascii=False,indent=2)+'\n')
    print('Adaptateur local enregistré; évaluer le test une seule fois après sélection verrouillée.')

if __name__=='__main__':main()
