from pathlib import Path
import json, numpy as np, hashlib
from PIL import Image
src=Path('/path/to/local-assets')
p=Path('/path/to/local-assets')
a=p/'assets';s=json.loads((src/'session.json').read_text());room=json.loads((a/'quest-room-geometry.json').read_text());mesh=room['parts'][0]
v=np.asarray(mesh['vertices']).reshape(-1,3);tri=np.asarray(mesh['triangles']).reshape(-1,3);cent=v[tri].mean(1);norm=np.cross(v[tri[:,1]]-v[tri[:,0]],v[tri[:,2]]-v[tri[:,0]]);area=np.linalg.norm(norm,axis=1);norm/=np.maximum(area[:,None],1e-9)
# Ceiling is opened only for the derived viewer. Original capture remains unmodified.
mask=cent[:,1]<1.10;tri=tri[mask];cent=cent[mask];norm=norm[mask];area=area[mask]
ins=s['intrinsics'];W,H=ins['width'],ins['height'];fx,fy,cx,cy=[ins[x] for x in ['fx','fy','cx','cy']]
def rot(q):
 x,y,z,w=q;return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
frames=[(i,s['frames'][i]) for i in range(0,len(s['frames']),9)]
scores=[]
for i,f in frames:
 pos=np.array(f['position']);R=rot(f['quaternion']);c=(cent-pos)@R;dep=-c[:,2];u=fx*c[:,0]/np.maximum(dep,.01)+cx;vv=cy-fy*c[:,1]/np.maximum(dep,.01)
 edge=np.minimum(np.minimum(u/W,1-u/W),np.minimum(vv/H,1-vv/H));valid=(dep>.05)&(edge>.025);direction=pos-cent;direction/=np.maximum(np.linalg.norm(direction,axis=1)[:,None],1e-7);facing=np.abs(np.sum(norm*direction,axis=1));score=np.where(valid,np.minimum(edge*4,1)*(facing*.7+.3),0);scores.append(score)
scores=np.asarray(scores);current=np.zeros(len(tri));chosen=[]
for j in range(16):
 improvements=((np.maximum(scores-current,0))*area).sum(1);improvements[chosen]=-1;ix=int(np.argmax(improvements));chosen.append(ix);current=np.maximum(current,scores[ix])
selected=scores[chosen];assignment=selected.argmax(0);unseen=selected.max(0)<.04
# A face is projected from a single calibrated view; perspective division happens per fragment.
result={'schema':'captured-room-texture-projection.v1','capture':'20261002_215403','derived_from':'Quest calibrated RGB frames and exact GLOBAL_MESH0','image_origin':s['imageOrigin'],'intrinsics':ins,'views':[],'vertices':v.flatten().tolist(),'triangles':tri.flatten().tolist(),'triangle_view':assignment.tolist(),'unseen':unseen.tolist(),'transform':[-3.5,1.222106,1.7],'ceiling_cutaway_original_y_max':1.10,'limits':'View-projected authentic RGB on measured coarse geometry; no generative fill, not a full photogrammetric reconstruction. Unseen surfaces use a neutral material.'}
for j,ix in enumerate(chosen):
 i,f=frames[ix];filename=f'room-view-{j:02}.jpg';Image.open(src/f['image']).convert('RGB').resize((1024,1024),Image.Resampling.LANCZOS).save(a/filename,quality=92)
 result['views'].append({'frame_index':i,'source_image':f['image'],'source_sha256':hashlib.sha256((src/f['image']).read_bytes()).hexdigest(),'image':filename,'position':f['position'],'quaternion':f['quaternion'],'timestamp':f['t'],'assigned_triangles':int(np.sum((assignment==j)&~unseen))})
(a/'room-texture-projection.json').write_text(json.dumps(result,separators=(',',':')))
print('Textured triangles:',int(np.sum(~unseen)),'/',len(tri),'views',len(chosen))
print('Source frames:',[frames[i][0] for i in chosen])
