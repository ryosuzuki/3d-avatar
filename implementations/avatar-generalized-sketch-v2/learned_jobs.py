"""Bounded local learned producer. No shell, paid provisioning, or fixture fallback."""
from pathlib import Path
import json,hashlib,time,uuid,threading,queue,subprocess,os,re
import numpy as np,trimesh
from PIL import Image,ImageDraw
from adapter import source_paths,import_asset
from learned_registration import select_front
ROOT=Path(__file__).parent;GPU=Path('/path/to/local-assets');PY=GPU/'.venv/bin/python'
SHA=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
class Jobs:
 def __init__(self,save,review=None):
  self.save=save;self.review=review;self.q=queue.Queue(2);self.jobs={};self.lock=threading.Lock();self.submitted=0
  for state in (ROOT/'generated/jobs').glob('*/state.json'):
   old=json.loads(state.read_text())
   if old.get('status') in ['queued','running']:
    old.update(status='failure',stage='service restarted before job completion',error='Interrupted producer; no fixture substituted',previousPreviewPreserved=True,fixtureSubstituted=False);state.write_text(json.dumps(old,indent=2))
  threading.Thread(target=self.worker,daemon=True).start()
 def public(self,j):
  o={k:v for k,v in j.items() if k not in ['source','preview']};review=ROOT/'generated/jobs'/j['id']/'quality-review.json'
  if review.exists():
   o['semanticReview']=json.loads(review.read_text())
   if not o['semanticReview'].get('recognizableSubject') and j['status']=='success':o.update(status='failure',stage='mesh generated but subject-recognition review rejected it',geometryInferenceComplete=True,error=o['semanticReview']['reason'],previousPreviewPreserved=True,fixtureSubstituted=False)
  return o
 def store(self,j):
  j['elapsedSeconds']=round(j.get('completedAt',time.time())-j['queuedAt'],2);d=ROOT/'generated/jobs'/j['id'];d.mkdir(parents=True,exist_ok=True);tmp=d/('.state-'+uuid.uuid4().hex+'.tmp');tmp.write_text(json.dumps(self.public(j),indent=2));tmp.replace(d/'state.json')
 def enqueue(self,preview):
  paths=source_paths(preview['asset']['sourceStrokePaths'],True)
  if len(paths)!=1 or len(paths[0]['points'])>256:raise ValueError('One closed boundary at most256vertices required')
  if not preview.get('fresh') or preview.get('precomputed'):raise ValueError('Fresh source required; fixtures cannot be fresh learned jobs')
  with self.lock:
   if self.submitted>=3 or self.q.full():raise ValueError('Learned job limit: max3 per service run, max2 waiting')
   self.submitted+=1;j={'id':uuid.uuid4().hex,'status':'queued','stage':'waiting for local resource','queuedAt':time.time(),'previewId':preview['id'],'question':str(preview.get('question') or preview['renderer']['title'])[:1400],'source':paths,'preview':preview,'fresh':True,'precomputed':False,'device':'AppleM2Ultra MPS','events':[]};self.jobs[j['id']]=j;self.store(j);self.q.put(j);return self.public(j)
 def get(self,i):
  if not re.fullmatch('[0-9a-f]{32}',i):raise ValueError('Invalid job identifier')
  if i in self.jobs:self.store(self.jobs[i]);return self.public(self.jobs[i])
  p=ROOT/'generated/jobs'/i/'state.json'
  if p.exists():return self.public(json.loads(p.read_text()))
  raise ValueError('Unknown job')
 def phase(self,j,status,stage,**kw):
  j.update(status=status,stage=stage,**kw);j['events'].append({'at':time.time(),'status':status,'stage':stage});self.store(j)
 def busy(self):
  rows=[]
  for line in subprocess.check_output(['ps','-axo','pid=,comm=,args='],text=True).splitlines():
   a=line.strip().split(None,2)
   if len(a)==3 and 'python' in a[1].lower() and any(x in a[2] for x in ['run-shape.py','run-triposr.py','run-controlnet-bridge.py']):rows.append({'pid':int(a[0]),'producer':next(x for x in ['run-shape.py','run-triposr.py','run-controlnet-bridge.py'] if x in a[2])})
  return rows
 def wait(self,j):
  while True:
   busy=self.busy()
   if not busy:return
   self.phase(j,'queued','waiting for existing local inference',blockingProducers=busy)
   if time.time()-j['queuedAt']>2400:raise TimeoutError('Existing local GPU producers did not become free within40minutes; no fixture substituted')
   time.sleep(5)
 def run(self,j,script,args):
  if script not in ['run-controlnet-bridge.py','run-triposr.py']:raise ValueError('Producer command is not allowlisted')
  self.wait(j);self.phase(j,'running',script,blockingProducers=[]);env=os.environ.copy();env.update(PYTORCH_ENABLE_MPS_FALLBACK='1',PYTHONDONTWRITEBYTECODE='1',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1')
  d=ROOT/'generated/jobs'/j['id']
  with (d/'.execution.log').open('ab') as out:
   p=subprocess.Popen([str(PY),str(ROOT/'neural-producer'/script),*args],stdout=out,stderr=out,env=env)
   try:code=p.wait(timeout=900)
   except subprocess.TimeoutExpired:p.kill();p.wait();raise TimeoutError('Owned neural stage exceeded15minutes; only this job process stopped')
   if code:raise RuntimeError(f'{script} failed with exit{code}; no precomputed fallback')
 def execute(self,j):
  d=ROOT/'generated/jobs'/j['id'];source=d/'source-strokes.json';source.write_text(json.dumps(j['source'],indent=2));p=np.asarray(j['source'][0]['points'])[:,:2];span=np.ptp(p,axis=0).max();xy=(p-(p.min(0)+p.max(0))/2)*(.8*768/span)+384;xy[:,1]=768-xy[:,1];im=Image.new('RGB',(768,768),'white');ImageDraw.Draw(im).line([tuple(x)for x in np.vstack([xy,xy[0]])],fill='black',width=5,joint='curve');inp=d/'live-input.png';im.save(inp)
  subject=re.sub(r'^(draw|sketch|create|show|make)\s+','',j['question'].split('.')[0],flags=re.I)[:350];prompt='Single isolated three-dimensional sculpture on clean white background. '+subject+'. Rounded thick detailed body, preserve supplied silhouette, no lettering or base.';(d/'prompt.json').write_text(json.dumps({'live':prompt}));j['sourceSHA256']=SHA(source);j['rasterSHA256']=SHA(inp);self.store(j)
  self.run(j,'run-controlnet-bridge.py',['--output',str(d),'--ids','live','--prompt-file',str(d/'prompt.json'),'--steps','28','--size','768','--scale','0.65','--seed','20261009','--run-name','fresh'])
  sd=json.loads(next(d.glob('controlnet-*-receipt.json')).read_text());row=sd['items'][0]
  if row['status']!='actual-neural-sketch-to-rich-image-complete':raise ValueError('Conditioned image generation failed')
  img=d/row['output'];j['conditionedImageUrl']='/generated/jobs/'+j['id']+'/'+img.name
  if self.review:
   self.phase(j,'running','conditioned-image semantic review');quality=self.review(j['question'],img);(d/'quality-review.json').write_text(json.dumps(quality,indent=2));j['semanticReview']=quality
   if not quality.get('recognizableSubject'):raise ValueError('Conditioned image failed subject review: '+quality.get('reason','unrecognized subject'))
  self.phase(j,'running','learned foreground separation');env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';subprocess.run([str(PY),str(ROOT/'neural-producer/prepare-foreground.py'),str(img),str(d/'shape-input.png')],check=True,timeout=120,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  self.run(j,'run-triposr.py',['--output',str(d),'--ids','shape','--run-name','fresh','--device','mps','--resolution','128'])
  tr=json.loads(next(d.glob('triposr-*-receipt.json')).read_text());row=tr['items'][0]
  if row['status']!='actual-neural-inference-complete':raise ValueError('Learned mesh failed')
  raw=d/row['glb'];display=raw;m=trimesh.load(raw,force='mesh',process=False)
  derivative=None
  if len(m.faces)>30000:
   m=m.simplify_quadric_decimation(face_count=18000);display=d/'declared-mobile.glb';m.export(display);derivative={'method':'quadric18000 separate display derivative','originalSHA256':SHA(raw),'displaySHA256':SHA(display)}
  # Generic source/mesh centering plus explicit TripoSR front-axis registration; not exact fidelity.
  self.phase(j,'running','generic front registration against actual foreground');mm,front=select_front(m,d/'shape-input.png');(d/'front-registration.json').write_text(json.dumps(front,indent=2))
  reg={'sourceToDisplay':j['preview']['asset']['registration']['sourceToDisplay'],'meshToDisplay':mm.tolist(),'exactBoundaryXY':False,'method':'independent uniform registration; source and learned contour can differ','hiddenShapeInferred':True}
  prov={'method':'fresh source raster→SDXL ControlNet→U2NetP→TripoSR','model':'stabilityai/TripoSR','fresh':True,'precomputed':False,'expectedAssetSHA256':SHA(display),'sourceSHA256':SHA(source),'rasterSHA256':SHA(inp),'conditionedImageSHA256':SHA(img),'rawLearnedMeshSHA256':SHA(raw),'meshCheckpointSHA256':tr['checkpoint_sha256'],'SDXLRevision':sd['model_revision'],'ControlNetRevision':sd['controlnet_revision'],'TripoSRRevision':tr['revision'],'device':'AppleM2Ultra MPS','question':j['question'],'displayDerivative':derivative,'frontRegistration':front,'semanticReview':j.get('semanticReview'),'morphologyStatus':'reviewed image identity, not guaranteed mesh anatomy or exact contour preservation'}
  bundle=import_asset(display,j['source'],reg,prov,motion={'kind':'authored-rigid'});answer=(j.get('semanticReview') or {}).get('answer') or j['preview']['renderer']['answer']+' Hidden surfaces are inferred; this is an illustrative prediction, not exact sketch fidelity.'
  result=self.save(bundle,'Fresh learned shape / '+j['preview']['renderer']['title'],answer,'fresh learned MPS',j['question'],True);result['externalLearnedProducer']={'connected':True,'jobId':j['id'],'device':'AppleM2Ultra MPS','fresh':True};result['renderer']['conditionedImage']='/generated/jobs/'+j['id']+'/'+img.name;result['renderer']['limits']='FRESH local SDXL + TripoSR inference · source retained · inferred hidden shape, no exact fidelity or anatomical rig';
  if j.get('semanticReview') and not j['semanticReview'].get('requirementsSatisfied'):result['renderer']['limits']+=' · Details differ: '+j['semanticReview'].get('reason','')[:220];
  (ROOT/'generated'/f"{result['id']}.json").write_text(json.dumps(result));j.update(resultUrl='/generated/'+result['id']+'.json',resultId=result['id'],provenance=prov,conditionedImageUrl=result['renderer']['conditionedImage'],rawMeshUrl='/generated/jobs/'+j['id']+'/'+raw.name,completedAt=time.time());self.phase(j,'success','new learned mesh validated and ready')
 def worker(self):
  while True:
   j=self.q.get()
   try:self.execute(j)
   except Exception as e:self.phase(j,'failure','learned inference failed',error=str(e)[:400],previousPreviewPreserved=True,fixtureSubstituted=False)
   finally:self.q.task_done()
