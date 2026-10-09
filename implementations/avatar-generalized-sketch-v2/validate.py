from pathlib import Path
import json,hashlib,numpy as np
from adapter import inflate_source,to_renderer,AdapterError
R=Path(__file__).parent
b=inflate_source([{'sourceId':'validator-unseen','closed':True,'points':[[0,0],[.6,0],[.35,.3],[.6,.8],[.1,.65],[-.25,.2]]}]);assert b['diagnostics']['watertight'];d=to_renderer(b);assert d['sourceStrokePaths'] and b['registration']['exactBoundaryXY']
try:inflate_source([{'closed':True,'points':[[0,0],[1,1],[0,1],[1,0]]}]);raise AssertionError('Invalid shape accepted')
except AdapterError as e:assert e.code=='SELF_INTERSECTION'
for f in ['server.py','app.js','adapter.py','geometry.js','index.html']:
 assert (R/f).is_file()
for name in ['fish','owl']:
 b=json.loads((R/'data'/f'{name}-asset.json').read_text());assert b['provenance']['precomputed'];p=R/'source'/f'{name}-display.glb'
 if p.exists():assert hashlib.sha256(p.read_bytes()).hexdigest()==b['mesh']['originalAsset']['sha256']
print('Validated source-preserving common adapter, rejected self-intersection, imported asset descriptors')
