"""Generic coarse front registration using actual inferred vertex colors and foreground. Never edits mesh."""
import itertools,numpy as np
from PIL import Image,ImageDraw
def select_front(mesh,foreground):
 v=np.asarray(mesh.vertices);colors=np.asarray(mesh.visual.vertex_colors)[:,:3];im=Image.open(foreground).convert('RGBA');a=np.asarray(im);ys,xs=np.where(a[:,:,3]>64)
 if len(xs)<100:raise ValueError('Foreground missing for registration')
 crop=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1));side=max(crop.size);canvas=Image.new('RGBA',(side,side),(255,255,255,255));canvas.alpha_composite(crop,((side-crop.width)//2,(side-crop.height)//2));target=np.asarray(canvas.convert('RGB').resize((128,128)))/255;mask=np.min(target,axis=2)<.94;rows=[]
 for perm in itertools.permutations(range(3)):
  for signs in itertools.product([-1,1],repeat=3):
   rot=np.diag(signs)@np.eye(3)[list(perm)]
   if np.linalg.det(rot)<.5:continue
   p=v@rot.T;xy=p[:,:2];span=np.ptp(xy,axis=0).max();xy=(xy-(xy.min(0)+xy.max(0))/2)/span*126+64;xy[:,1]=128-xy[:,1];render=Image.new('RGB',(128,128),'white');draw=ImageDraw.Draw(render);depth=p[mesh.faces,2].mean(1);fc=colors[mesh.faces].mean(1).astype('uint8')
   for f in np.argsort(depth):draw.polygon([tuple(x)for x in xy[mesh.faces[f]]],fill=tuple(fc[f]))
   arr=np.asarray(render)/255;pred=np.min(arr,axis=2)<.94;both=mask|pred;iou=float((mask&pred).sum()/max(both.sum(),1));mae=float(np.abs(target-arr)[both].mean());rows.append({'score':mae+.2*(1-iou),'rgbMAE':mae,'silhouetteIoU':iou,'rotation':rot.tolist()})
 best=min(rows,key=lambda x:x['score']);rot=np.asarray(best['rotation']);p=v@rot.T;f=.95/np.ptp(p,axis=0).max();mm=np.eye(4);mm[:3,:3]=rot*f;mm[:3,3]=-(p.min(0)+p.max(0))/2*f;return mm,{'candidates':24,'selected':best,'rawGeometryChanged':False,'limits':'coarse color/silhouette registration; approximate painter; front ambiguity remains'}
