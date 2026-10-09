from pathlib import Path
from schema import validate
import json,hashlib
ROOT=Path(__file__).resolve().parent
records=[]
for p in (ROOT/'generated').glob('*.json'):
 d=json.loads(p.read_text());validate(d['scene']);records.append({'id':d['id'],'question':d['question'],'parts':len(d['scene']['parts']),'hash':hashlib.sha256(p.read_bytes()).hexdigest()})
for p in ['ryo_tpose.ply','ipad-room.ply']:
 source=Path('/path/to/local-assets')/p
 destination=ROOT/'assets'/p
 if destination.exists():assert destination.read_bytes()==source.read_bytes()
 else:
  manifest=json.loads((ROOT/'source-manifest.json').read_text());receipt=next(x for x in manifest['assets']if x['source']==str(source));assert hashlib.sha256(source.read_bytes()).hexdigest()==receipt['sha256']
for bad in [{'parts':[{'kind':'script'}]},{'parts':[{'kind':'mesh','vertices':[[0,0,0],[1,0,0],[0,1,0]],'triangles':[[0,1,99]]}]}]:
 try:validate(bad);raise AssertionError('Unsafe schema accepted')
 except ValueError:pass
print(json.dumps({'validatedRecords':records,'originalAssetsByteIdentical':True,'unsupportedCodeAndIndicesRejected':True},indent=2))
