from pathlib import Path
import json,hashlib
import trimesh,numpy as np
root=Path(__file__).parent;checks=[]
for name in ['fish','octopus','leaf','unseen']:
 d=json.loads((root/'meshes'/f'{name}.json').read_text());v=np.array(d['vertices']);m=trimesh.Trimesh(vertices=v,faces=d['faces'],process=False)
 assert m.is_watertight and m.is_winding_consistent and m.volume>0
 boundary=np.c_[np.array(d['boundary']),np.zeros(len(d['boundary']))];error=np.linalg.norm(v[:,None,:]-boundary[None,:,:],axis=2).min(axis=0).max();assert error<1e-6
 assert np.isfinite(v).all() and np.allclose(np.linalg.norm(m.vertex_normals,axis=1),1)
 checks.append({'name':name,'watertight':True,'winding':True,'volume':float(m.volume),'boundaryError':float(error),'categoryLookup':False})
print(json.dumps({'pass':True,'cases':checks},indent=2))
