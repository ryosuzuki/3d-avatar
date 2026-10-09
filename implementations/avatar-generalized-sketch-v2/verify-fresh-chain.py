from pathlib import Path
import json,hashlib
R=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
proof=[]
for d in (R/'generated/jobs').iterdir():
 if not(d/'state.json').exists():continue
 j=json.loads((d/'state.json').read_text())
 if j['status']!='success':continue
 result=json.loads((R/'generated'/f"{j['resultId']}.json").read_text());preview=json.loads((R/'generated'/f"{j['previewId']}.json").read_text());source=json.loads((d/'source-strokes.json').read_text());assert source==preview['asset']['sourceStrokePaths']==result['asset']['sourceStrokePaths'];assert result['fresh'] and not result['precomputed'];pr=result['asset']['provenance'];assert sha(d/'source-strokes.json')==pr['sourceSHA256'];assert sha(d/'live-input.png')==pr['rasterSHA256'];sd=json.loads(next(d.glob('controlnet-*-receipt.json')).read_text());tr=json.loads(next(d.glob('triposr-*-receipt.json')).read_text());assert sd['items'][0]['status']=='actual-neural-sketch-to-rich-image-complete';assert tr['items'][0]['status']=='actual-neural-inference-complete';assert sha(d/sd['items'][0]['output'])==pr['conditionedImageSHA256'];assert sha(d/tr['items'][0]['glb'])==pr['rawLearnedMeshSHA256'];assert tr['checkpoint_sha256']==pr['meshCheckpointSHA256'];assert result['asset']['mesh']['originalGeometryChanged']==False;proof.append({'jobId':j['id'],'question':j['question'],'seconds':j['completedAt']-j['queuedAt'],'sourceIdentityPreserved':True,'rawMeshSHA256':pr['rawLearnedMeshSHA256'],'checkpointSHA256':pr['meshCheckpointSHA256'],'actualModelReceiptsPassed':True,'diagnostics':result['asset']['diagnostics'],'rendererImageIntermediate':bool(result['renderer']['conditionedImage'])})
assert proof,'No successful learned job to verify'
(R/'fresh-chain-verification.json').write_text(json.dumps(proof,indent=2));print(json.dumps(proof))
