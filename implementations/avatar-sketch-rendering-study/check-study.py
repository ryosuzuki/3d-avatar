from pathlib import Path
import json,math
R=Path(__file__).parent;O=Path('/path/to/local-assets');rec=json.loads((O/'capture-receipt.json').read_text());assert not rec['errors'];assert len(rec['checks'])==3
checks=[]
for c in rec['checks']:
 es=c['styles'];assert len(es)==3 and {e['style'] for e in es}=={'section','ink','hatch'};assert len({e['displayGeometryChecksum'] for e in es})==1;assert all(math.isfinite(e['displayGeometryChecksum']) for e in es);assert len({e['sourceStrokePaths'] for e in es})==1;assert len({e['meshTriangles'] for e in es})==1
 for e in es:
  assert e['contourSegments']<=640;assert e['sectionSegments']<=({'section':240,'ink':0,'hatch':400}[e['style']]);assert e['originalAvatarAndRoom'];assert e['sourceStrokeProgress']==1
 checks.append({'name':c['name'],'styleGeometryUnchanged':True,'originalSourcePathsRetained':True,'states':[{k:e[k] for k in ['style','contourPaths','contourSegments','sectionPaths','sectionSegments','surfaceOpacity','meshTriangles','sourceStrokePaths']} for e in es]})
(O/'renderer-style-verification.json').write_text(json.dumps({'shapes':checks,'styleStates':9,'boundedGeometryIndependentStyles':True,'actualScope':'2 learned meshes plus one unseen inflated boundary; not universal neural-generation evaluation','newInferenceOrAPICalls':0},indent=2));print('9 style states verified')
