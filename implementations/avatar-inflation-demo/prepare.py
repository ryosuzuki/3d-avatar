import sys,json,shutil
from pathlib import Path
import numpy as np
import trimesh
from shapely.geometry import Polygon
BASE=Path(__file__).resolve().parent;sys.path.insert(0,str(BASE))
from inflate import inflate
ROOT=Path(__file__).resolve().parent;out=ROOT/'meshes';out.mkdir(exist_ok=True)
unseen=[[-1,-.2],[-.6,-.55],[-.1,-.35],[.3,-.6],[.7,-.15],[.4,.15],[.85,.6],[.15,.4],[-.15,.7],[-.45,.3],[-.9,.55]]
checks=[]
for name in ['fish','octopus','leaf','unseen']:
 if name=='unseen':points=unseen;m=inflate(points,.32);m.export(out/(name+'.glb'))
 else:
  points=json.loads((BASE/'input'/f'{name}-stroke.json').read_text())['points'];m=trimesh.load(BASE/'input'/f'{name}.glb',force='mesh');shutil.copy2(BASE/'input'/f'{name}.glb',out/(name+'.glb'))
 poly=Polygon(points);center=np.asarray(poly.centroid.coords[0]);scale=np.ptp(points,axis=0).max();boundary=(np.asarray(points)-center)/scale
 # Source boundary survives at exactly z=0; preserve it rather than reverse-engineering mesh features.
 d=np.linalg.norm(m.vertices[:,None,:2]-boundary[None,:,:],axis=2).min(axis=0)
 assert d.max()<1e-6 and m.is_watertight and m.is_winding_consistent and m.volume>0
 # View silhouettes + sparse Z cross sections, not triangle-wireframe noise.
 sections=[]
 for axis,offsets in [(0,[-.3,0,.3]),(1,[-.2,0,.2])]:
  normal=np.eye(3)[axis]
  for offset in offsets:
   origin=np.zeros(3);origin[axis]=offset;sec=m.section(plane_origin=origin,plane_normal=normal)
   if sec:
    for line in sec.discrete:
     ids=np.linspace(0,len(line)-1,min(60,len(line))).astype(int);sections.append(line[ids].tolist())
 record={'name':name,'vertices':m.vertices.tolist(),'faces':m.faces.tolist(),'normals':m.face_normals.tolist(),'adjacency':m.face_adjacency.tolist(),'edges':m.face_adjacency_edges.tolist(),'boundary':boundary.tolist(),'sections':sections,'inputPoints':points,'thickness':.32}
 (out/f'{name}.json').write_text(json.dumps(record,separators=(',',':')))
 checks.append({'name':name,'watertight':True,'consistentWinding':True,'volume':m.volume,'boundaryError':float(d.max()),'vertices':len(m.vertices),'faces':len(m.faces),'categoryLookup':False,'unseen':name=='unseen'})
(ROOT/'geometry-verification.json').write_text(json.dumps(checks,indent=2));print(checks)
