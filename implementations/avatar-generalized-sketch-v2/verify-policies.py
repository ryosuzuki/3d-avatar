from pathlib import Path
import json,urllib.request,urllib.error
R=Path(__file__).parent;proof=[]
for case,payload in [('open-stroke',{'closed':False,'points':[[0,0],[1,0],[1,1]]}),('unspecified-closure',{'points':[[0,0],[1,0],[1,1]]}),('hole',{'sourceStrokePaths':[{'closed':True,'points':[[0,0],[1,0],[1,1]],'holes':[[[.1,.1],[.2,.1],[.2,.2]]]}]})]:
 req=urllib.request.Request('http://127.0.0.1:8846/api/inflate',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
 try:urllib.request.urlopen(req);raise AssertionError('Unsupported source accepted')
 except urllib.error.HTTPError as e:d=json.load(e);assert e.code==400 and d['previousScenePreserved'];proof.append({'case':case,'code':d['code'],'error':d['error']})
(R/'policy-verification.json').write_text(json.dumps(proof,indent=2));print(json.dumps(proof))
