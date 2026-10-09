from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import json,urllib.request,urllib.parse,uuid,time,threading,os,re
from catalog import compile_scene,KINDS
ROOT=Path(__file__).resolve().parent;OUT=Path(__import__('os').environ.get('OUTPUT_DIR', str(ROOT/'runtime-output')));OUT.mkdir(parents=True,exist_ok=True)
sessions={};jobs={};lock=threading.Lock();total_calls=0
SYSTEM='''You teach using a closed catalog of tested sketches, inspired by Primer/Jev composition. Select, order and parameterize one or at most two beats. Never generate executable code. Return JSON with title, answer (accurate, <=95 words, actual user language), limits, scene:{primitives:[{kind,...parameters}]}. The first beat must directly answer the question. Prefer exactly one numerical beat; do not add auxiliary triangles/vectors unless the user specifically asks for them. Choose the dedicated numeric family when it matches the question. Never replace a supported circuit or other numerical family with flow/bars merely because the user requests arithmetic; the backend computes it. For unrelated concepts use flow with meaningful short nodes, not arbitrary numerical plots. Available kinds: triangle(a,b): right triangle Pythagoras; unitcircle(angle degrees): sin/cos; exponential(rate): annual compound growth (1+r)^t; damped(damping,frequency): decaying cosine; attention(query 3 numbers,keys exactly3 vectors each3 numbers,scale MULTIPLIES dot scores, never divides); wave/pendulum/spring(amplitude,frequency,phase): illustrative sine motion, spring/pendulum small oscillations only; projectile(speed m/s,angle degrees): ideal no drag; orbit(eccentricity): ellipse not scaled solar system; growth(rate): logistic not exponential; decay(rate): exponential; normal(mean,sigma): probability density; bayes(prior,sensitivity,falsePositive); circuit(voltage,resistance): ideal resistor; lens(focalLength .5–2,objectDistance >2.1): thin converging lens; vector(x,y); molecule(formula H2O or CO2 only): USE THIS supported beat when asked to draw water or carbon dioxide, including CO2 double bonds and 180-degree geometry; flow: for genuinely sequential steps, nodes2–4 short labels. For resources/reactants forming products, use inputs (1–3 labels), process (short label), outputs (1–3 labels); this draws a merging-input/branching-output graph. Never chain independent resources as though one transforms into the next. Photosynthesis must include light, water and carbon dioxide inputs and glucose/sugar AND oxygen outputs; bars(values0–1,names,label): illustrative not empirical. Use values supplied by user. The backend supplies ALL calculated numeric results. NEVER calculate or state numerical weights, probabilities, distances, trigonometric values, currents or other arithmetic in the answer. Give a qualitative conceptual explanation only; exact computed facts will be appended locally. Followups retain prior parameters except explicitly requested edits. Unsupported exact scientific geometry is a concept flow with honest limitation. No real measurements fabricated. Include units and assumptions. Explain differences accurately. Molecular H2O angle104.5 is explanatory; topology drawn not atom scale. Attention uses dot/sqrt3 and stable softmax; teaching vectors not trained embeddings. No diagnosis. Numeric supported ranges: triangle a,b0.1–6; unitcircle angle0–360; wave/pendulum/spring amplitude0.1–1.5, frequency0.2–3, phase0–6.28; projectile speed3–22, angle10–80; orbit eccentricity0–0.85; growth/decay rate0.05–2; normal mean-2–2, sigma0.3–2; bayes prior0.01–0.9, sensitivity0.1–0.99, falsePositive0.01–0.5; circuit voltage1–24, resistance10–1000; lens focalLength0.5–2, objectDistance2.1–6; vector x,y-2–2; exponential rate0.02–0.3; damped damping0.05–1,frequency0.2–2; attention scale0.1–4, vector entries-5–5. The numeric ranges of ONE kind do not limit other kinds: resistor values belong to circuit, NEVER triangle. An invalid optional triangle is not proof that a valid circuit request is unsupported.'''
def provider(path,payload):
 key=__import__('os').environ['OPENAI_API_KEY']
 req=urllib.request.Request('https://api.openai.com/v1/'+path,data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=90) as r:return r.read()
def speech(jid,text):
 start=time.perf_counter()
 try:
  b=provider('audio/speech',{'model':'gpt-4o-mini-tts','voice':'shimmer','input':text,'response_format':'mp3','instructions':'Friendly clear explanatory delivery, input language. This is a synthetic presenter voice, not a cloned voice.'});jobs[jid].update(status='ready',bytes=b,audioMs=round((time.perf_counter()-start)*1000))
 except Exception:jobs[jid]['status']='unavailable'
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def log_message(self,*a):pass
 def end_headers(self):
  self.send_header('Cache-Control','no-store');self.send_header('Cross-Origin-Opener-Policy','same-origin');self.send_header('Cross-Origin-Embedder-Policy','require-corp');super().end_headers()
 def pathclean(self):
  self.path=urllib.parse.urlsplit(self.path).path
  if self.path.startswith('/primer-live'):self.path=self.path[12:] or '/'
 def reply(self,obj,status=200,sid=None):
  b=json.dumps(obj,ensure_ascii=False).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(b)))
  if sid:self.send_header('Set-Cookie',f'ryo_primer={sid}; HttpOnly; SameSite=Strict; Path=/')
  self.end_headers();self.wfile.write(b)
 def sid(self):
  from http.cookies import SimpleCookie
  ck=SimpleCookie(self.headers.get('Cookie',''));return ck['ryo_primer'].value if 'ryo_primer' in ck else str(uuid.uuid4())
 def do_GET(self):
  self.pathclean()
  if self.path.startswith('/api/audio/'):
   jid=self.path.rsplit('/',1)[1];j=jobs.get(jid)
   if not j or j['sid']!=self.sid():self.reply({'error':'not found'},404);return
   if self.headers.get('Accept')!='audio/mpeg':self.reply({'status':j['status'],'audioMs':j.get('audioMs'),'url':'./api/audio/'+jid});return
   if j['status']!='ready':self.reply({'status':j['status']},202);return
   b=j['bytes'];self.send_response(200);self.send_header('Content-Type','audio/mpeg');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b);return
  p=self.path
  if p not in ['/','/index.html','/app.js','/avatar.js','/rig.js','/room.js','/story.json','/gallery.html','/gallery.js','/cases.json'] and not p.startswith(('/assets/','/vendor/','/media/')):self.send_error(404);return
  if '..' in urllib.parse.unquote(p):self.send_error(404);return
  super().do_GET()
 def do_POST(self):
  global total_calls
  self.pathclean()
  origin=self.headers.get('Origin','')
  if origin and origin not in ['http://127.0.0.1:8821','http://localhost:8821','http://127.0.0.1:8822','http://localhost:8822','https://localhost']:self.reply({'error':'origin rejected'},403);return
  try:
   n=int(self.headers.get('Content-Length',0))
   if not 0<n<20000:raise ValueError('Request size')
   inp=json.loads(self.rfile.read(n))
   if self.path=='/api/parameter':
    sketch=compile_scene(inp['sketch']);state=sessions.get(self.sid())
    if state and state[-1]['role']=='assistant':state[-1]['content']=json.dumps({k:sketch[k] for k in ['title','answer','scene','limits']})
    self.reply({'sketch':sketch,'generated':False,'provider':'Local validated numerical update','contextUpdated':bool(state)});return
   if self.path=='/api/context':
    sid=self.sid();sketch=compile_scene(inp['sketch']);sessions[sid]=[{'role':'user','content':str(inp['question'])[:1200]},{'role':'assistant','content':json.dumps({k:sketch[k] for k in ['title','answer','scene','limits']})}]
    self.reply({'restored':True,'generated':False,'source':'Recorded prior test context; no model call'},sid=sid);return
   if self.path!='/api/ask':self.reply({'error':'not found'},404);return
   q=str(inp.get('question','')).strip()
   if not 1<=len(q)<=1200:raise ValueError('Question size')
   sid=self.sid();state=sessions.setdefault(sid,[])
   if inp.get('contextScene') and state:
    previous=compile_scene(inp['contextScene'])
    if state[-1]['role']=='assistant':state[-1]['content']=json.dumps({k:previous[k] for k in ['title','answer','scene','limits']})
   with lock:
    if total_calls>=250 or len(state)//2>=80:raise ValueError('Session usage limit reached; no automatic topup')
    total_calls+=1
   t=time.perf_counter()
   raw=json.loads(provider('chat/completions',{'model':'gpt-4.1-mini','messages':[{'role':'system','content':SYSTEM}]+state[-8:]+[{'role':'user','content':q}],'response_format':{'type':'json_object'},'max_tokens':1300}))
   attempts=1;repair_receipt=None
   try:v=json.loads(raw['choices'][0]['message']['content']);v['language']='ja' if re.search('[ぁ-んァ-ン一-龯]',q) else 'en';sketch=compile_scene(v)
   except (ValueError,TypeError,KeyError) as validation:
    rejected=raw['choices'][0]['message']['content'];primary=None
    try:
     initial=json.loads(rejected);initial['language']='ja' if re.search('[ぁ-んァ-ン一-龯]',q) else 'en'
     if len(initial.get('scene',{}).get('primitives',[]))>1 and initial['scene']['primitives'][0].get('kind')!='flow':
      primary={**initial,'scene':{'primitives':[initial['scene']['primitives'][0]]}};sketch=compile_scene(primary)
    except (ValueError,TypeError,KeyError,IndexError):primary=None
    repair_receipt={'validationError':str(validation),'rejectedPlan':rejected,'action':'Dropped invalid optional beats' if primary else 'Provider repair using full supported catalog ranges'}
    if primary:raw['choices'][0]['message']['content']=json.dumps(primary)
    else:attempts=2
    if not primary:
     repair='The prior plan failed local validation: '+str(validation)+'. Return corrected JSON for the SAME user request. Keep a valid primary beat; drop invalid optional auxiliary beats. Do not silently change requested numbers. If the request exceeds a numeric catalog range, use an honest concept flow instead.'
     raw=json.loads(provider('chat/completions',{'model':'gpt-4.1-mini','messages':[{'role':'system','content':SYSTEM}]+state[-8:]+[{'role':'user','content':q},{'role':'assistant','content':raw['choices'][0]['message']['content']},{'role':'user','content':repair}],'response_format':{'type':'json_object'},'max_tokens':1300}))
     v=json.loads(raw['choices'][0]['message']['content']);v['language']='ja' if re.search('[ぁ-んァ-ン一-龯]',q) else 'en';sketch=compile_scene(v)
   ms=round((time.perf_counter()-t)*1000);jid=str(uuid.uuid4());jobs[jid]={'sid':sid,'status':'pending'}
   state.extend([{'role':'user','content':q},{'role':'assistant','content':json.dumps({k:sketch[k] for k in ['title','answer','scene','limits']})}]);threading.Thread(target=speech,args=(jid,sketch['answer']),daemon=True).start()
   result={'sketch':sketch,'generated':True,'provider':'OpenAI catalog selection (not Jev API)','model':raw['model'],'selectionMs':ms,'audioJob':jid,'contextTurns':len(state)//2,'selectionAttempts':attempts,'validationRepair':repair_receipt,'usage':raw.get('usage')}
   with lock:
    with (OUT/'generation-log.jsonl').open('a') as f:f.write(json.dumps({'question':q,**result},ensure_ascii=False)+'\n')
   self.reply(result,sid=sid)
  except Exception as e:self.reply({'error':str(e) if isinstance(e,ValueError) else type(e).__name__+' service unavailable'},502)
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',8821),Handler).serve_forever()
