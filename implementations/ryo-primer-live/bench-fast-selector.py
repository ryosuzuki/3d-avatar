from server import provider,SYSTEM
from catalog import compile_scene
from pathlib import Path
import json,time
cases=json.loads(Path(__file__).with_name('cases.json').read_text())
results=[]
for i in [0,3,12,21,27,29]:
 c=cases[i];t=time.perf_counter()
 try:
  raw=json.loads(provider('chat/completions',{'model':'gpt-4.1-nano','messages':[{'role':'system','content':SYSTEM},{'role':'user','content':c['question']}],'response_format':{'type':'json_object'},'max_tokens':1000}));sketch=compile_scene(json.loads(raw['choices'][0]['message']['content']));r={'id':c['id'],'question':c['question'],'elapsedMs':round((time.perf_counter()-t)*1000),'kindPass':sketch['scene']['primitives'][0]['kind']==c['expectedKind'],'sketch':sketch,'model':raw['model']}
 except Exception as e:r={'id':c['id'],'elapsedMs':round((time.perf_counter()-t)*1000),'error':type(e).__name__}
 results.append(r);print(r['id'],r['elapsedMs'],r.get('kindPass'),flush=True)
Path('/path/to/local-assets').write_text(json.dumps(results,ensure_ascii=False,indent=2))
