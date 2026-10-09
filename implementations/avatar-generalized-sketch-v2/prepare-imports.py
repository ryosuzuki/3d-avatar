from pathlib import Path
import json,numpy as np,trimesh,hashlib
from adapter import import_asset,to_renderer,sha
R=Path(__file__).parent
proof=[]
for name,model in [('fish','Hunyuan'),('owl','TripoSR')]:
 source=json.loads((R/'data'/f'{name}.json').read_text());paths=[{'sourceId':'actual-svg-'+str(i),'points':q,'closed':bool(np.linalg.norm(np.array(q[0])-q[-1])<1e-7)}for i,q in enumerate(source['originalSVGPaths'])]
 bb=np.array(source['registration']['sourceBBox']);center=bb.mean(0);factor=.95/np.ptp(bb,axis=0).max();sm=np.eye(4);sm[0,0]=factor;sm[1,1]=-factor;sm[0,3]=-center[0]*factor;sm[1,3]=center[1]*factor
 path=R/'source'/f'{name}-display.glb';rotation=np.array(source['registration']['modelTransform']);raw=trimesh.load(path,force='mesh',process=False);rv=trimesh.transform_points(raw.vertices,rotation);mf=.95/np.ptp(rv,axis=0).max();mm=np.eye(4);mm[:3,:3]=rotation[:3,:3]*mf;mm[:3,3]=-rv.min(0).add(rv.max(0)) if False else -((rv.min(0)+rv.max(0))/2)*mf
 b=import_asset(path,paths,{'sourceToDisplay':sm.tolist(),'meshToDisplay':mm.tolist(),'exactCorrespondence':False,'method':'separate uniform source and learned mesh registration'}, {'method':'precomputed learned image-to-3D import','model':model,'fresh':False,'precomputed':True,'expectedAssetSHA256':sha(path),'sourceAssetSHA256':sha(R/'source'/f'{name}-stroke.svg'),'sourceAuthorship':'actual supplied fixture SVG; not human input','originalFullAssetSHA256':sha(R/'source'/f'{name}-original.glb'),'displayDerivativeDeclared':name=='fish'},motion={'kind':'authored-rigid'})
 d=to_renderer(b);d.update(name=name,title=f'{name.upper()} / PRECOMPUTED {model} IMPORT',answer='This is an existing learned mesh with the actual source sketch. Registration aligns the two independently; exact contour fidelity and anatomical rigs are not claimed.',limits='Precomputed inference artifact, not a new GPU request. Same source contract and rendering backend.');(R/'data'/f'{name}.json').write_text(json.dumps(d));(R/'data'/f'{name}-asset.json').write_text(json.dumps(b));proof.append({'name':name,'sourceSHA':b['provenance']['sourceAssetSHA256'],'assetSHA':b['mesh']['originalAsset']['sha256'],'diagnostics':b['diagnostics'],'routeStatus':b['routeStatus']})
(R/'import-verification.json').write_text(json.dumps(proof,indent=2))
