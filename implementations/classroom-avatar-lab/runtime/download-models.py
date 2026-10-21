from pathlib import Path
import urllib.request,json,concurrent.futures,hashlib,time
root=Path(__file__).resolve().parent/'source/pretrained_models';root.mkdir(exist_ok=True)
def download(job):
 repo,item,base=job;name=item['path'];target=base/name;target.parent.mkdir(parents=True,exist_ok=True);expected=item.get('lfs',{}).get('oid');size=item.get('size');
 if target.exists() and target.stat().st_size==size and (not expected or hashlib.sha256(target.read_bytes()).hexdigest()==expected):return str(target)
 for attempt in range(3):
  try:
   url=f'https://huggingface.co/{repo}/resolve/main/{name}?download=true&task=video2mr-{attempt}'
   with urllib.request.urlopen(url,timeout=120) as response,open(str(target)+'.part','wb') as output:
    while block:=response.read(4*1024*1024):output.write(block)
   p=Path(str(target)+'.part');assert p.stat().st_size==size,(name,'size mismatch')
   if expected:assert hashlib.sha256(p.read_bytes()).hexdigest()==expected,(name,'digest mismatch')
   p.replace(target);print('READY',repo,name,size,flush=True);return str(target)
  except Exception as e:
   print('RETRY',name,type(e).__name__,flush=True)
   if attempt==2:raise
jobs=[]
manifest=json.loads((Path(__file__).parent/'model-files.json').read_text())
for item in manifest['files']:
 repo=item['repository'];base=root if repo.endswith('Prior') else root/'lhmpp-700m'
 jobs.append((repo,{'path':item['path'],'size':item['bytes'],'lfs':{'oid':item.get('sha256')}},base))
print('DOWNLOAD_COUNT',len(jobs),'bytes',sum(x[1]['size'] for x in jobs),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(download,jobs))
(root/'video2mr-models-ready.json').write_text(json.dumps({'files':[{'repository':r,'path':j['path'],'bytes':j['size'],'sha256':j.get('lfs',{}).get('oid')} for r,j,b in jobs]},indent=2))
print('CURATED_WEIGHTS_READY',flush=True)
