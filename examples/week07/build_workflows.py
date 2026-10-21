"""Exports n8n sans credentials incorporés; configuration requise après import."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent/'workflows'
ROOT.mkdir(exist_ok=True)


def node(name,kind,parameters,x,version=1):
    return {'id':name.lower().replace(' ','-'),'name':name,'type':f'n8n-nodes-base.{kind}',
            'typeVersion':version,'position':[x,300],'parameters':parameters}


def webhook(name,path):
    return node(name,'webhook',{'httpMethod':'POST','path':path,'authentication':'headerAuth',
                              'responseMode':'responseNode','options':{}},200,2)


def request(name,url,body):
    return node(name,'httpRequest',{'method':'POST','url':url,'authentication':'genericCredentialType',
          'genericAuthType':'httpHeaderAuth','sendBody':True,'specifyBody':'json','jsonBody':body,
          'options':{'timeout':5000,'response':{'response':{'fullResponse':True,'neverError':True,'responseFormat':'json'}}}},460,4.2)


def respond():
    return node('Respond','respondToWebhook',{'respondWith':'json','responseBody':'={{ $json.body }}',
          'options':{'responseCode':'={{ $json.statusCode }}'}},720,1.4)


def save(name,nodes,edges):
    connections={}
    for left,right in edges:
        connections.setdefault(left,{'main':[[]]})['main'][0].append({'node':right,'type':'main','index':0})
    content={'name':name,'nodes':nodes,'connections':connections,'active':False,
             'settings':{'executionOrder':'v1'},'pinData':{},'tags':[]}
    (ROOT/(name.split(' ')[0]+'.json')).write_text(json.dumps(content,ensure_ascii=False,indent=2)+'\n')


save('01_ingress Support request',
     [webhook('Ingress','week07-request'),request('Persist event','http://backend:8080/events','={{ JSON.stringify($json.body) }}'),respond()],
     [('Ingress','Persist event'),('Persist event','Respond')])
save('02_worker Scheduled processing',
     [node('Schedule','scheduleTrigger',{'rule':{'interval':[{'field':'seconds','secondsInterval':10}]}},200,1.2),
      node('Manual','manualTrigger',{},200),request('Tick','http://backend:8080/tick','{}')],
     [('Schedule','Tick'),('Manual','Tick')])
save('03_decision Human review',
     [webhook('Review','week07-decision'),
      request('Decide',"={{ 'http://backend:8080/jobs/' + encodeURIComponent($json.body.event_id) + '/decision' }}",
              '={{ JSON.stringify({decision: $json.body.decision, proposal_hash: $json.body.proposal_hash}) }}'),respond()],
     [('Review','Decide'),('Decide','Respond')])
print('3 exports n8n créés; aucun credential ni secret')
