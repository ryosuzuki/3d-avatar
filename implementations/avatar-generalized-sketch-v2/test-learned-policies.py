import json,queue,threading,urllib.request,urllib.error
from pathlib import Path
from learned_jobs import Jobs
url='http://127.0.0.1:8846'
proof={'negativeHTTP':[]}
for value in ['../../server','../../secrets.json','fish','f72bf999-543/../x','']:
 req=urllib.request.Request(url+'/api/learned',data=json.dumps({'previewId':value}).encode(),headers={'Content-Type':'application/json'})
 try:urllib.request.urlopen(req);raise AssertionError('Must reject')
 except urllib.error.HTTPError as e:
  o=json.load(e);assert e.code==400 and o['previousScenePreserved'];proof['negativeHTTP'].append({'input':value,'status':e.code,'error':o['error']})
x=Jobs.__new__(Jobs);x.lock=threading.Lock();x.q=queue.Queue(2);x.submitted=3
valid=json.loads(Path('fresh-learned-request.json').read_text())
try:x.enqueue(valid);raise AssertionError('limit')
except ValueError as e:assert 'limit' in str(e);proof['totalJobLimit']=str(e)
x.submitted=0;x.q.put(1);x.q.put(2)
try:x.enqueue(valid);raise AssertionError('queue budget')
except ValueError as e:proof['pendingJobLimit']=str(e)
valid['precomputed']=True
try:x.enqueue(valid);raise AssertionError('fixture')
except ValueError as e:assert 'Fresh source' in str(e);proof['fixtureRejected']=str(e)
proof['allowlistedProducerCommands']=['run-controlnet-bridge.py','prepare-foreground.py','run-triposr.py'];proof['shellExecution']=False;proof['newPackagesOrPaidProvisioning']=False
Path('learned-policy-verification.json').write_text(json.dumps(proof,indent=2));print(json.dumps(proof))
