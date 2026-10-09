from pathlib import Path
import json
import numpy as np
import scipy.sparse as sp
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
r=Path(__file__).parent;o=Path('/path/to/local-assets')
m=trimesh.load(r/'meshes/unseen.glb',force='mesh');v=m.vertices.copy();z=v[:,2];boundary=np.abs(z)<1e-9;edges=m.edges_unique
rows=np.r_[edges[:,0],edges[:,1]];cols=np.r_[edges[:,1],edges[:,0]];a=sp.coo_matrix((np.ones(len(rows)),(rows,cols)),shape=(len(v),len(v))).tocsr();a=sp.diags(1/np.asarray(a.sum(axis=1)).ravel())@a
h=np.abs(z).copy()
for _ in range(30):h=.65*h+.35*(a@h);h[boundary]=0
v[:,2]=np.sign(z)*h;sm=trimesh.Trimesh(vertices=v,faces=m.faces.copy(),process=False);factor=m.volume/sm.volume;v[:,2]*=factor;sm=trimesh.Trimesh(vertices=v,faces=m.faces.copy(),process=False)
assert sm.is_watertight and sm.is_winding_consistent and sm.volume>0 and np.allclose(v[:,:2],m.vertices[:,:2],atol=0,rtol=0) and np.all(v[boundary,2]==0)
sm.export(r/'meshes/unseen-smoothed.glb');sm.export(o/'unseen-smoothed.glb')
light=np.array([.3,-.5,.8]);light/=np.linalg.norm(light);fig=plt.figure(figsize=(12,5),facecolor='#eef5f7')
for i,(mesh,title) in enumerate([(m,'Original distance-field height'),(sm,'30 boundary-locked smoothing steps')]):
 ax=fig.add_subplot(1,2,i+1,projection='3d');shade=.35+.65*np.maximum(0,mesh.face_normals@light);pc=Poly3DCollection(mesh.triangles,linewidth=0);pc.set_facecolor(np.c_[.38*shade,.75*shade,.84*shade,np.ones(len(shade))]);ax.add_collection3d(pc);ax.set_xlim(-.6,.6);ax.set_ylim(-.6,.6);ax.set_zlim(-.3,.3);ax.set_box_aspect((1,1,.5));ax.view_init(24,-65);ax.axis('off');ax.set_title(title,fontsize=15)
fig.suptitle('Same unseen outline and triangle topology; XY and zero-depth boundary unchanged',fontsize=13);fig.tight_layout();fig.savefig(o/'inflation-smoothing-before-after.png',dpi=160);plt.close(fig)
def roughness(mesh):
 normals=mesh.face_normals;d=1-np.einsum('ij,ij->i',normals[mesh.face_adjacency[:,0]],normals[mesh.face_adjacency[:,1]]);return {'meanNormalDisagreement':float(d.mean()),'p95NormalDisagreement':float(np.percentile(d,95))}
result={'input':'meshes/unseen.glb','output':'meshes/unseen-smoothed.glb','method':'30 graph-laplacian height-only steps; lambda .35; boundary zero locked; positive/negative symmetry; global Z scale restores original volume','originalPreserved':True,'XYMaxError':float(np.abs(v[:,:2]-m.vertices[:,:2]).max()),'boundaryZMaxError':float(np.abs(v[boundary,2]).max()),'volumeRelativeError':float(abs(sm.volume-m.volume)/m.volume),'volumeRestorationScale':factor,'watertight':bool(sm.is_watertight),'sameTopology':bool(np.array_equal(sm.faces,m.faces)),'before':roughness(m),'after':roughness(sm),'limits':['Not learned hidden shape or anatomical articulation','Smoothing trades local curvature accuracy for softer appearance','Only this single unseen silhouette checked; not production-wide acceptance']}
(o/'inflation-smoothing-receipt.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
