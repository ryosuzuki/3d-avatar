from pathlib import Path
import numpy as np,trimesh,json,itertools
from PIL import Image,ImageDraw
R=Path(__file__).parent
for d in (R/'generated/jobs').iterdir():
 if not(d/'state.json').exists():continue
 j=json.loads((d/'state.json').read_text())
 if j['status']!='success' or not j.get('resultId'):continue
 review=json.loads((d/'quality-review.json').read_text()) if (d/'quality-review.json').exists() else{}
 if review.get('recognizableSubject') is False:continue
 raw=d/json.loads(next(d.glob('triposr-*-receipt.json')).read_text())['items'][0]['glb'];m=trimesh.load(raw,force='mesh',process=False);v=np.asarray(m.vertices);colors=np.asarray(m.visual.vertex_colors)[:,:3];target=Image.open(d/'shape-input.png').convert('RGBA');a=np.asarray(target);ys,xs=np.where(a[:,:,3]>64);crop=target.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1));side=max(crop.size);canvas=Image.new('RGBA',(side,side),(255,255,255,255));canvas.alpha_composite(crop,((side-crop.width)//2,(side-crop.height)//2));target=np.asarray(canvas.convert('RGB').resize((256,256)))/255;mask=np.min(target,axis=2)<.94
 candidates=[];previews=[]
 for perm in itertools.permutations(range(3)):
  for signs in itertools.product([-1,1],repeat=3):
   rot=np.diag(signs)@np.eye(3)[list(perm)]
   if np.linalg.det(rot)<.5:continue
   p=v@rot.T;xy=p[:,:2];span=np.ptp(xy,axis=0).max();xy=(xy-(xy.min(0)+xy.max(0))/2)/span*252+128;xy[:,1]=256-xy[:,1];im=Image.new('RGB',(256,256),'white');draw=ImageDraw.Draw(im);depth=p[m.faces,2].mean(1);fc=colors[m.faces].mean(1).astype('uint8')
   for f in np.argsort(depth):draw.polygon([tuple(x)for x in xy[m.faces[f]]],fill=tuple(fc[f]))
   arr=np.asarray(im)/255;pred=np.min(arr,axis=2)<.94;union=(mask|pred).sum();iou=float((mask&pred).sum()/max(union,1));err=float(np.abs(target-arr)[mask|pred].mean());score=err+(1-iou)*.2;candidates.append({'score':score,'rgbMAE':err,'silhouetteIoU':iou,'rotation':rot.tolist()});previews.append(im)
 best=int(np.argmin([x['score']for x in candidates]));rot=np.asarray(candidates[best]['rotation']);p=v@rot.T;factor=.95/np.ptp(p,axis=0).max();mat=np.eye(4);mat[:3,:3]=rot*factor;mat[:3,3]=-(p.min(0)+p.max(0))/2*factor
 resultpath=R/'generated'/f"{j['resultId']}.json";r=json.loads(resultpath.read_text());reg=r['asset']['registration'];old=np.asarray(reg['meshToDisplay']);reg['meshToDisplay']=mat.tolist();reg['method']='24 proper axis orientations scored against actual conditioned foreground with coarse color + silhouette correspondence; not exact fidelity';r['renderer']['registration']=reg;r['renderer']['vertices']=(np.c_[v,np.ones(len(v))]@mat.T)[:,:3].tolist();r['asset']['provenance']['frontRegistration']={'candidates':24,'selected':candidates[best],'rawGeometryChanged':False,'limits':'coarse correspondence, approximate software painter; symmetric/front ambiguity remains'};r['renderer']['provenance']=r['asset']['provenance'];resultpath.write_text(json.dumps(r));(d/'front-registration.json').write_text(json.dumps({'selected':candidates[best],'candidates':candidates,'oldTransform':old.tolist(),'newTransform':mat.tolist()},indent=2));sheet=Image.new('RGB',(256*6,280*4),'white')
 for i,im in enumerate(previews):sheet.paste(im,((i%6)*256,(i//6)*280));ImageDraw.Draw(sheet).text(((i%6)*256+3,(i//6)*280+258),f"{i} score {candidates[i]['score']:.3f}"+(' BEST'if i==best else''),fill='black')
 sheet.save(d/'orientation-contact-sheet.png');previews[best].save(d/'best-registration.png');print(j['id'],best,candidates[best])
