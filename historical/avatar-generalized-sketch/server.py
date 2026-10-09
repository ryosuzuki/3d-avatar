from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import json,urllib.request,urllib.parse,time,uuid,argparse,threading
from schema import validate
ROOT=Path(__file__).resolve().parent
CALLS=0
CALL_LOCK=threading.Lock()
SYSTEM='''You generate original rich 3D object geometry for an embodied sketch explainer. Answer the actual question in English, 60–100 words. Return JSON only with title, answer, limits, motion (swim/flap/sway/spin/idle), parts. Compose 5–20 meaningful anatomically recognizable mesh parts; never reduce objects to disconnected primitive spheres/boxes. Build connected organic swept bodies with many varying cross sections, extruded irregular fins/wings/leaves, stems, curved legs. Coordinate X horizontal, Y up, Z depth. Fit whole object in x[-1,1],y[-.65,.65],z[-.4,.4], centered about origin. Fish should have long X body, head right, fins, eyes, mouth, forked tail; bird has head, neck, beak, feet, wings, feathers; requested variants change actual geometry. Each part is {kind,name,color:'#rrggbb',position:[x,y,z],rotation:[EulerX,EulerY,EulerZ] in RADIANS, never degrees,scale:[x,y,z],animate:'body'/'tail'/'wing-left'/'wing-right'/'leaf'/'static', ...}. IMPORTANT: use ONLY absolute coordinates for path, vertices and outline. Do not combine absolute geometry coordinates with position offsets; omit position, rotation and scale entirely unless a lathe requires positioning. Never shrink radii with scale. Fish body radii should reach .25 in Y and .15 in Z, and fins and head must meet the body rather than float disconnected. Bird wings must touch shoulders and plant leaves must meet stems. All transforms optional. Allowed general geometry operations, not fixed object catalog: sweep with path:[[x,y,z],...] of 3–30 points and radii:[[horizontalRadius,verticalRadius],...] (one pair per point), segments:12–24; path is central spine, cross sections perpendicular to tangent. lathe with profile:[[radius,y],...] and segments:24; extrude with outline:[[x,y],...] ordered closed polygon (do not duplicate first point), depth:.02–.2,bevel:.005–.03; mesh with vertices and triangles index arrays for custom geometry. No code, scripts, URLs, or other operations. Different requests produce newly designed complete geometry, not a preset. For organic animal bodies never use a constant-radius two-point cylinder. Use at least six varying cross-sections with tapered rounded ends, or a lathe profile with at least nine meaningful varying radii. Curved necks and coiled tails need at least six centerline control points. Avoid floating disconnected anatomy. All organic parts should visibly meet their adjacent parts. Add educational answer and honest limits (procedural illustration, not reconstruction/rigged anatomy). Use moderate topology and bounded numbers.'''
class H(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def log_message(self,*a):pass
 def end_headers(self):
  self.send_header('Cross-Origin-Opener-Policy','same-origin');self.send_header('Cross-Origin-Embedder-Policy','require-corp');self.send_header('Cache-Control','no-store');super().end_headers()
 def reply(self,d,status=200):
  b=json.dumps(d).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
 def do_GET(self):
  p=urllib.parse.unquote(self.path.split('?')[0])
  if p=='/api/assets':self.reply({'assets':[x.name for x in (ROOT/'generated').glob('*.json')]});return
  if '..' in p or any(x.startswith('.')for x in p.split('/')if x) or (p not in ['/','/index.html','/app.js','/geometry.js','/avatar.js','/rig.js','/room.js','/imports.json','/comparison.json','/review.html'] and not p.startswith(('/assets/','/vendor/','/generated/'))):self.send_error(404);return
  super().do_GET()
 def do_POST(self):
  global CALLS
  if self.path!='/api/generate':self.reply({'error':'Not found'},404);return
  try:
   n=int(self.headers.get('Content-Length',0));assert 0<n<12000
   data=json.loads(self.rfile.read(n));q=str(data['question'])[:1400]
   if not q.strip():raise ValueError('Question required')
   with CALL_LOCK:
    if CALLS>=30:raise ValueError('Run usage cap reached; no automatic topup')
    CALLS+=1
   key=__import__('os').environ['OPENAI_API_KEY'];t=time.time()
   payload={'model':'gpt-4.1' if data.get('quality') else 'gpt-4.1-mini','messages':[{'role':'system','content':SYSTEM},{'role':'user','content':q}],'response_format':{'type':'json_object'},'max_tokens':12000}
   req=urllib.request.Request('https://api.openai.com/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
   with urllib.request.urlopen(req,timeout=150) as r:result=json.loads(r.read())
   raw=json.loads(result['choices'][0]['message']['content']);ident=uuid.uuid4().hex[:12]
   try:scene=validate(raw)
   except ValueError as err:
    (ROOT/'generated').mkdir(exist_ok=True);(ROOT/'generated'/f'{ident}-rejected.txt').write_text(json.dumps(raw,indent=2))
    payload['messages'] += [{'role':'assistant','content':json.dumps(raw)},{'role':'user','content':'Repair this scene schema without changing the requested object. Validator error: '+str(err)+'. Only sweep, lathe, extrude, mesh. Use nested index triples. All numeric values finite and bounded. Omit unsupported geometry operations. Return complete corrected JSON.'}]
    req=urllib.request.Request('https://api.openai.com/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=150) as r:result=json.loads(r.read())
    scene=validate(json.loads(result['choices'][0]['message']['content']))
   record={'id':ident,'question':q,'backend':'llm-scene-schema','model':result['model'],'usage':result.get('usage'),'seconds':round(time.time()-t,2),'scene':scene,'generated':True,'notPreset':True}
   (ROOT/'generated').mkdir(exist_ok=True);(ROOT/'generated'/f'{ident}.json').write_text(json.dumps(record,indent=2))
   if data.get('voice',True):
    speech={'model':'gpt-4o-mini-tts','voice':'shimmer','input':scene['answer'],'response_format':'mp3','instructions':'Natural clear educational English narration, conversational with intentional pauses.'}
    req=urllib.request.Request('https://api.openai.com/v1/audio/speech',data=json.dumps(speech).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=90) as r:mp3=r.read()
    (ROOT/'generated'/f'{ident}.mp3').write_bytes(mp3);record['audioUrl']=f'./generated/{ident}.mp3';(ROOT/'generated'/f'{ident}.json').write_text(json.dumps(record,indent=2))
   del key;self.reply(record)
  except Exception as e:self.reply({'error':str(e) if isinstance(e,(ValueError,AssertionError)) else type(e).__name__},502)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8824);a=p.parse_args();print(f'Generalized sketch http://127.0.0.1:{a.port}',flush=True);ThreadingHTTPServer(('127.0.0.1',a.port),H).serve_forever()
