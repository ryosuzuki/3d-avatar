from pathlib import Path
import json,hashlib,shutil,math
import numpy as np
import trimesh
from svgpathtools import svg2paths2
from PIL import Image
R=Path(__file__).parent;GPU=Path('/path/to/local-assets');O=Path('/path/to/local-assets');A=R/'source';D=R/'data';A.mkdir(exist_ok=True);D.mkdir(exist_ok=True)
h=json.loads((O/'hunyuan-mps-s30-r256-seed42-sdxl-rich-bridge-receipt.json').read_text());t=json.loads((O/'triposr-mps-r128-sdxl-bridge-receipt.json').read_text());b=json.loads((O/'sdxl-bridge-preprocess-scale0.65-seed4242-receipt.json').read_text());cn=json.loads((O/'controlnet-sdxl-s28-size768-scale0.65-seed4242-receipt.json').read_text());mobile=json.loads((O/'shape-mobile-derivative-receipt.json').read_text())
records=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for name,model,receipt in [('fish','Hunyuan3D-2mini',h),('owl','TripoSR',t)]:
 id=name+'-stroke-sdxl-bridge';item=next(x for x in receipt['items'] if x['id']==id);bridge=next(x for x in b['items'] if x['id']==id);image=next(x for x in cn['items'] if x['id']==name+'-stroke')
 assert sha(O/item['glb'])==item['glb_sha256'] and sha(O/(id+'-input.png'))==item['input_sha256'];assert sha(O/bridge['source_image'])==bridge['source_image_sha256'];assert sha(O/bridge['source_sketch'])==bridge['source_sketch_sha256'];assert sha(O/image['source_input'])==image['source_input_sha256']
 svg=GPU/(name+'-stroke-fixture.svg');original=A/(name+'-original.glb');shutil.copy2(O/item['glb'],original);shutil.copy2(svg,A/(name+'-stroke.svg'));shutil.copy2(O/bridge['source_sketch'],A/(name+'-stroke.png'));shutil.copy2(O/(id+'-input.png'),A/(name+'-conditioned.png'));shutil.copy2(O/bridge['source_image'],A/(name+'-conditioned-full.png'))
 if name=='fish':
  mr=next(x for x in mobile['items'] if x['source']==item['glb']);display=O/mr['mobile'];assert sha(display)==mr['mobile_sha256'];derivative={'method':mr['method'],'originalFaces':mr['original_faces'],'displayFaces':mr['mobile_faces'],'sha256':sha(display)}
 else:display=original;derivative=None
 shutil.copy2(display,A/(name+'-display.glb'));m=trimesh.load(display,force='mesh',process=False)
 transform=np.eye(4)
 if name=='owl':transform=trimesh.transformations.rotation_matrix(-math.pi/2,[1,0,0])@trimesh.transformations.rotation_matrix(math.pi/2,[0,0,1]);m.apply_transform(transform)
 center=m.bounds.mean(axis=0);extent=np.ptp(m.vertices,axis=0).max();worldsize=1.05 if name=='fish' else .85;verts=(m.vertices-center)/extent*worldsize
 paths,attrs,_=svg2paths2(svg);samples=[]
 for path,attr in zip(paths,attrs):
  if attr.get('fill','').lower() in ['white','#fff','#ffffff']:continue # paper rectangle is not an ink stroke
  for sub in path.continuous_subpaths():
   points=[]
   for seg in sub:
    n=max(2,min(160,math.ceil(seg.length(error=1e-4)/3)));points.extend([[seg.point(k/n).real,seg.point(k/n).imag] for k in range(n)])
   q=sub[-1].end;points.append([q.real,q.imag]);samples.append(points)
 pts=np.concatenate([np.array(p) for p in samples]);lo=pts.min(0);hi=pts.max(0);c=(lo+hi)/2;span=(hi-lo).max();strokes=[np.c_[(np.array(p)[:,0]-c[0])/span*worldsize,(c[1]-np.array(p)[:,1])/span*worldsize,np.zeros(len(p))].tolist() for p in samples]
 rgba=np.array(Image.open(A/(name+'-conditioned.png')).convert('RGBA'));yy,xx=np.where(rgba[:,:,3]>128);maxdim=max(xx.max()-xx.min(),yy.max()-yy.min());plane={'width':rgba.shape[1]/maxdim*worldsize,'height':rgba.shape[0]/maxdim*worldsize,'offset':[(rgba.shape[1]/2-(xx.max()+xx.min())/2)/maxdim*worldsize,((yy.max()+yy.min())/2-rgba.shape[0]/2)/maxdim*worldsize]}
 # Deliberately retain all original mesh geometry; viewing transform only, fish display derivative declared separately.
 rec={'name':name,'model':model,'vertices':verts.tolist(),'faces':m.faces.tolist(),'adjacency':m.face_adjacency.tolist(),'edges':m.face_adjacency_edges.tolist(),'sourceStrokePaths':strokes,'originalSVGPaths':samples,'imagePlane':plane,'conditionedImage':'./source/'+name+'-conditioned.png','registration':{'method':'Independent uniform bbox centering/scaling; SVG Y-down -> Y-up; model coords explicitly transformed','sourceBBox':np.vstack([lo,hi]).tolist(),'meshBBoxDisplay':np.vstack([verts.min(0),verts.max(0)]).tolist(),'modelTransform':transform.tolist(),'worldMaxDimension':worldsize,'exactContourCorrespondence':False},'sourceStrokeIdentity':'Experiment-authored SVG centerlines, not a human sketch and not projected from final 3D'}
 (D/(name+'.json')).write_text(json.dumps(rec,separators=(',',':')));records.append({'name':name,'model':model,'actualDevice':receipt['device'],'sourceSVGHash':sha(svg),'sourceRasterHash':bridge['source_sketch_sha256'],'richImageHash':bridge['source_image_sha256'],'meshInputHash':item['input_sha256'],'originalGLBHash':item['glb_sha256'],'sourcePaths':len(strokes),'sourceSamples':sum(len(x) for x in strokes),'originalFaces':item['faces'],'displayFaces':len(m.faces),'source3DUnchanged':sha(original)==item['glb_sha256'],'derivative':derivative,'inputChainVerified':True,'registration':rec['registration'],'inferenceCompleteEarlier':True})
(R/'source-chain-verification.json').write_text(json.dumps(records,indent=2));print(records)
