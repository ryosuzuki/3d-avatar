"""Mock-provider conformance for rejection/repair; not live latency evidence."""
import server,json,tempfile,threading,urllib.request
from pathlib import Path

def response(plan):return json.dumps({'model':'mock-fixture-not-live','choices':[{'message':{'content':json.dumps(plan)}}]}).encode()
def check(plans,expected_attempts,expected_action):
 queue=list(plans);server.sessions.clear();server.jobs.clear();server.total_calls=0
 server.provider=lambda path,payload:response(queue.pop(0));server.speech=lambda *a:None
 with tempfile.TemporaryDirectory() as out:
  server.OUT=Path(out);http=server.ThreadingHTTPServer(('127.0.0.1',0),server.Handler);th=threading.Thread(target=http.serve_forever,daemon=True);th.start()
  try:
   q=urllib.request.Request(f'http://127.0.0.1:{http.server_port}/api/ask',data=json.dumps({'question':'Explain Ohms law for 9 volts across a 100 ohm ideal resistor.'}).encode(),headers={'Content-Type':'application/json'});x=json.loads(urllib.request.urlopen(q).read());assert x['sketch']['scene']['primitives'][0]['kind']=='circuit';assert x['sketch']['semanticEvidence'][0]['currentA']==.09;assert x['selectionAttempts']==expected_attempts;assert x['validationRepair']['action']==expected_action;assert len(x['sketch']['scene']['primitives'])==1;assert not queue
  finally:http.shutdown();http.server_close()
base={'answer':'An ideal resistor follows Ohms law.','scene':{'primitives':[{'kind':'circuit','voltage':9,'resistance':100}]}}
invalid_aux={'answer':'An ideal resistor follows Ohms law.','scene':{'primitives':[{'kind':'circuit','voltage':9,'resistance':100},{'kind':'triangle','a':9,'b':100}]}}
check([invalid_aux],1,'Dropped invalid optional beats')
invalid_primary={'answer':'Wrong family','scene':{'primitives':[{'kind':'triangle','a':9,'b':100}]}}
check([invalid_primary,base],2,'Provider repair using full supported catalog ranges')
print('Mock conformance passed: valid primary survives invalid auxiliary; invalid primary invokes bounded repair; 90mA preserved')
