from pathlib import Path
import json,hashlib,numpy as np,trimesh
R=Path(__file__).parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
chain=json.loads((R/'source-chain-verification.json').read_text());passed=[]
for c in chain:
 n=c['name'];d=json.loads((R/'data'/(n+'.json')).read_text());a=R/'source'
 for f,key in [('stroke.svg','sourceSVGHash'),('stroke.png','sourceRasterHash'),('conditioned-full.png','richImageHash'),('conditioned.png','meshInputHash'),('original.glb','originalGLBHash')]:assert sha(a/(n+'-'+f))==c[key]
 m=trimesh.load(a/(n+'-display.glb'),force='mesh',process=False);m.apply_transform(np.array(c['registration']['modelTransform']));vs=(m.vertices-m.bounds.mean(0))/np.ptp(m.vertices,axis=0).max()*c['registration']['worldMaxDimension'];assert np.max(np.abs(vs-np.array(d['vertices'])))<1e-9;assert np.array_equal(m.faces,d['faces']);assert len(d['sourceStrokePaths'])==c['sourcePaths'];assert sum(map(len,d['sourceStrokePaths']))==c['sourceSamples'];assert not c['registration']['exactContourCorrespondence'];assert all(np.array(p).shape[1]==3 and np.all(np.array(p)[:,2]==0) for p in d['sourceStrokePaths'])
 passed.append(n+' frozen source chain, actual mesh registration, separate original source strokes')
expected={'ryo_tpose.ply':'','ipad-room.ply':''}
manifest=R/'gaussian-hashes.json'
if manifest.exists():
 for n,h in json.loads(manifest.read_text()).items():assert sha(R/'assets'/n)==h
 passed.append('original Gaussian assets byte-identical')
f=json.loads((R/'data/fallback.json').read_text());mesh=trimesh.Trimesh(vertices=f['vertices'],faces=f['faces'],process=False);assert mesh.is_watertight and mesh.volume>0;assert len(f['sourceStrokePaths'])==1;passed.append('unseen closed polygon fallback watertight positive volume')
# Frontend has neither credential text nor backend credential-path use.
for n in ['app.js','body.js','prefix.js','index.html']:
 s=(R/n).read_text();assert 'secrets.json' not in s and 'sk-proj-' not in s and 'api.openai.com' not in s
passed.append('frontend credential-free')
print(json.dumps({'passed':passed,'count':len(passed)},indent=2))
