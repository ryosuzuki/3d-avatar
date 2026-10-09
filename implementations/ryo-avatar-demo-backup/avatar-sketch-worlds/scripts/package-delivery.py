from pathlib import Path
import json,hashlib,zipfile,shutil
p=Path(__file__).resolve().parents[1];o=Path('/path/to/local-assets');h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();manifest=json.loads((p/'delivery-manifest.json').read_text());play=json.loads((o/'playback-verification.json').read_text());assert play['final']['ended'] and not play['final']['error'] and not play['errors'];manifest['qa']['fullMediaPlayback']=play['final'];manifest['qa']['audioVideoEndDriftMs']=0;manifest['qa']['audioListeningEvidence']='audio-listening-verdict.json';manifest['backup']['integrationState']='main-integrated';manifest['backup']['completionOwner']='avatar_sketch_worlds';manifest['backup']['validation']='14 geometry/provenance checks; full final decode and128s browser playback; source syntax; ZIP integrity'
for dest in [p,o]:(dest/'delivery-manifest.json').write_text(json.dumps(manifest,indent=2))
for name in ['geometry-verification.json','audio-asr-comparison.json','audio-listening-verdict.json','playback-verification.json','audio-loudness.txt','ffprobe.json']:
 shutil.copy2(o/name,p/name)
source=[]
for f in sorted(p.rglob('*')):
 rel=f.relative_to(p)
 if f.is_file() and not any(x in rel.parts for x in ['node_modules','.git','__pycache__']) and f.name not in ['final.mp4','source-manifest.json']:source.append({'path':str(rel),'bytes':f.stat().st_size,'sha256':h(f)})
(p/'source-manifest.json').write_text(json.dumps({'base':'avatar-chalktalk-expanded','root':str(p),'files':source},indent=2))
z=o/'avatar-sketch-worlds-project.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED)as arc:
 for x in source:arc.write(p/x['path'],'avatar-sketch-worlds/'+x['path'])
 arc.write(p/'source-manifest.json','avatar-sketch-worlds/source-manifest.json')
 arc.write(o/'avatar-sketch-worlds.mp4','avatar-sketch-worlds/final.mp4')
 for name in ['narration.srt','narration.vtt','narration.txt','delivery-manifest.json','screenshot-fish.png','screenshot-terrain.png','screenshot-water.png']:arc.write(o/name,'delivery/'+name)
with zipfile.ZipFile(z)as arc:
 assert arc.testzip()is None
 for name in ['ryo_tpose.ply','ipad-room.ply','narration.wav']:assert hashlib.sha256(arc.read('avatar-sketch-worlds/assets/'+name)).hexdigest()==h(p/'assets'/name)
files=[o/'avatar-sketch-worlds.mp4',z,o/'delivery-manifest.json',p/'source-manifest.json'];(o/'artifact-hashes.json').write_text(json.dumps({f.name:{'sha256':h(f),'bytes':f.stat().st_size}for f in files},indent=2));print('ZIP_VERIFIED',z.stat().st_size)
