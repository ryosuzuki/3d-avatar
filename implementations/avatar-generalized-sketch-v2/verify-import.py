from pathlib import Path
import json,base64,urllib.request
R=Path(__file__).parent;proof=[]
for name in ['fish','owl']:
 b=json.loads((R/'data'/f'{name}-asset.json').read_text());payload={'format':'glb','assetBase64':base64.b64encode((R/'source'/f'{name}-display.glb').read_bytes()).decode(),'sourceStrokePaths':b['sourceStrokePaths'],'registration':b['registration'],'provenance':b['provenance'],'style':b['style'],'motion':b['motion']};req=urllib.request.Request('http://127.0.0.1:8846/api/import',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'});r=json.load(urllib.request.urlopen(req,timeout=30));assert r['asset']['mesh']['originalAsset']['sha256']==b['mesh']['originalAsset']['sha256'];assert r['asset']['sourceStrokePaths']==b['sourceStrokePaths'];proof.append({'name':name,'id':r['id'],'assetSHA':r['asset']['mesh']['originalAsset']['sha256'],'sourceRetained':True,'warnings':r['asset']['routeStatus']['warnings']})
for p in ['server.py','/../server.py','/.git/config','/secrets.json','/adapter.py']:
 try:urllib.request.urlopen('http://127.0.0.1:8846/'+p.lstrip('/'));raise AssertionError('Backend file exposed')
 except urllib.error.HTTPError as e:assert e.code==404
(R/'runtime-import-verification.json').write_text(json.dumps(proof,indent=2));print(json.dumps(proof))
