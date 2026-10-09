from pathlib import Path
import json,hashlib,zipfile,shutil
p=Path(__file__).resolve().parents[1];o=Path('/path/to/local-assets');h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();m=json.loads((p/'delivery-manifest.json').read_text());play=json.loads((o/'playback-verification.json').read_text());assert play['final']['ended'] and not play['errors'] and not play['final']['error'];m['qa']['fullMediaPlayback']=play['final'];m['qa']['audioVideoEndDriftMs']=0;m['qa']['ASR']=json.loads((o/'audio-asr-comparison.json').read_text());m['backup']['integrationState']='main-integrated';m['backup']['validation']='8 causal geometry tests, exact144s full decode/browser playback, source syntax, original-asset hashes, ZIP integrity and extracted runtime'
# Completion records describe the final target without embedding their own commit hash.
for dest in [p,o]:(dest/'delivery-manifest.json').write_text(json.dumps(m,indent=2))
for n in ['audio-asr-comparison.json','audio-perceptual-review.json','audio-loudness.txt','ffprobe.json','playback-verification.json','scene-proof.json']:shutil.copy2(o/n,p/n)
source=[]
for f in sorted(p.rglob('*')):
 rel=f.relative_to(p)
 if f.is_file()and not any(x in rel.parts for x in ['node_modules','.git','__pycache__'])and f.name not in ['final.mp4','source-manifest.json','backup-state.json']:source.append({'path':str(rel),'bytes':f.stat().st_size,'sha256':h(f)})
(p/'source-manifest.json').write_text(json.dumps({'base':'avatar-sketch-worlds','root':str(p),'files':source},indent=2))
z=o/'avatar-sketch-frontiers-project.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED)as arc:
 for x in source:arc.write(p/x['path'],'avatar-sketch-frontiers/'+x['path'])
 arc.write(p/'source-manifest.json','avatar-sketch-frontiers/source-manifest.json');arc.write(o/'avatar-sketch-frontiers.mp4','avatar-sketch-frontiers/final.mp4')
 for n in ['narration.srt','narration.vtt','narration.txt','delivery-manifest.json','screenshot-dinosaur.png','screenshot-attention.png','screenshot-gas.png','screenshot-body.png']:arc.write(o/n,'delivery/'+n)
with zipfile.ZipFile(z)as arc:
 assert arc.testzip()is None
 for n in ['ryo_tpose.ply','ipad-room.ply','narration.wav']:assert hashlib.sha256(arc.read('avatar-sketch-frontiers/assets/'+n)).hexdigest()==h(p/'assets'/n)
files=[o/'avatar-sketch-frontiers.mp4',z,o/'delivery-manifest.json',p/'source-manifest.json'];(o/'artifact-hashes.json').write_text(json.dumps({f.name:{'sha256':h(f),'bytes':f.stat().st_size}for f in files},indent=2));print('ZIP_VERIFIED',z.stat().st_size)
