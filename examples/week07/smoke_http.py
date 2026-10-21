"""Scénario HTTP nominal et doublon; --n8n vérifie aussi les exports importés."""
import argparse
import json
import os
import time
import uuid
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def call(url, token, body=None):
    request=Request(url,data=json.dumps(body).encode() if body is not None else None,
                    headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'})
    try:
        with urlopen(request,timeout=10) as response:
            return response.status,json.load(response)
    except HTTPError as response:
        return response.code,json.load(response)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--n8n',action='store_true')
    args=parser.parse_args()
    service=os.environ['SERVICE_TOKEN']
    review=os.environ['REVIEW_TOKEN']
    api=os.environ.get('API_URL','http://127.0.0.1:8080')
    n8n=os.environ.get('N8N_URL','http://127.0.0.1:5678')
    eid='smoke-'+uuid.uuid4().hex
    event={'event_id':eid,'schema_version':1,'type':'support.requested','ticket_id':'T-SMOKE','text':'Question facture'}
    ingress=n8n+'/webhook/week07-request' if args.n8n else api+'/events'
    assert call(ingress,service,event)[0]==202
    assert call(ingress,service,event)[0]==200
    assert call(ingress,service,{**event,'text':'Collision'})[0]==409
    if args.n8n:
        # Laisser le scheduler importé déclencher le traitement, pas un tick manuel.
        deadline=time.monotonic()+30
        while time.monotonic()<deadline:
            job=call(api+'/jobs/'+eid,service)[1]
            if job['status']=='awaiting_review':
                break
            time.sleep(1)
        else:
            raise AssertionError('Le scheduler n8n ne traite pas le job')
    else:
        assert call(api+'/tick',service,{})[0]==200
        job=call(api+'/jobs/'+eid,service)[1]
    body={'decision':'approve','proposal_hash':job['proposal_hash']}
    assert call(api+'/jobs/'+eid+'/decision',service,body)[0]==401
    if args.n8n:
        destination=n8n+'/webhook/week07-decision'
        body['event_id']=eid
    else:
        destination=api+'/jobs/'+eid+'/decision'
    for _ in range(2):
        status,result=call(destination,review,body)
        assert status==200 and result['status']=='published'
    assert call(destination,review,{**body,'decision':'reject'})[0]==409
    print(json.dumps({'mode':'n8n' if args.n8n else 'backend','event_id':eid,
                      'status':'published','checks':'202, duplicate, collision, scheduler, roles, idempotent decision, conflicting decision'},indent=2))


if __name__=='__main__':
    main()
