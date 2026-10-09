from pathlib import Path
import json,numpy as np,trimesh
R=Path(__file__).parent
for d in (R/'generated/jobs').iterdir():
 if not(d/'state.json').exists():continue
 j=json.loads((d/'state.json').read_text())
 if j['status']!='success':continue
 p=R/'generated'/f"{j['resultId']}.json";r=json.loads(p.read_text());tr=json.loads(next(d.glob('triposr-*-receipt.json')).read_text());raw=d/tr['items'][0]['glb'];m=trimesh.load(raw,force='mesh',process=False)
 if r['asset']['provenance'].get('displayDerivative'):m=trimesh.load(d/'declared-mobile.glb',force='mesh',process=False)
 assert np.array_equal(m.faces,np.asarray(r['asset']['mesh']['faces'])) and np.allclose(m.vertices,r['asset']['mesh']['vertices'])
 if m.visual.kind=='vertex':r['asset']['mesh']['vertexColors']=m.visual.vertex_colors.tolist();r['renderer']['vertexColors']=m.visual.vertex_colors.tolist();r['renderer']['provenance']['vertexColorInterpretation']='Faint official inferred vertex colors; sRGB-to-linear display hint, not appearance ground truth'
 r['renderer']['cueTimes']={'drawEnd':3,'imageEnd':6,'morphEnd':9,'turnStart':9,'duration':24};r['renderer']['imagePlane']={'width':.95,'height':.95,'offset':[0,0]}
 p.write_text(json.dumps(r));print(j['id'],p.name,m.visual.kind,len(m.faces))
