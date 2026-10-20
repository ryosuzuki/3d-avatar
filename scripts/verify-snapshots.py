"""Verify original sanitized snapshots and explicitly reviewed English derivatives."""
import pathlib,json,hashlib
root=pathlib.Path(__file__).resolve().parents[1]
derivatives=json.loads((root/'ENGLISH-DERIVATIVES.json').read_text())['files']
by_path={f['path']:f for f in derivatives}
assert len(by_path)==len(derivatives),'Duplicate derivative paths'
seen=set();n=0
for m in root.rglob('CATEGORY-SNAPSHOT.json'):
 data=json.loads(m.read_text())
 for f in data['files']:
  p=m.parent/f['path'];rel=str(p.relative_to(root))
  assert p.is_file(),str(p)
  actual=hashlib.sha256(p.read_bytes()).hexdigest()
  if rel in by_path:
   d=by_path[rel]
   assert d['snapshot']==str(m.relative_to(root)),rel
   assert d['originalSanitizedSha256']==f['sha256'],rel
   assert d['reason'].strip(),rel
   assert actual==d['currentSha256'],rel
   seen.add(rel)
  else:
   assert actual==f['sha256'],str(p)
  n+=1
assert seen==set(by_path),'Derivative not bound to an original snapshot'
print('PASS snapshot files:',n,'including reviewed English derivatives:',len(seen))
