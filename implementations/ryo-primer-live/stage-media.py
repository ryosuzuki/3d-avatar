from pathlib import Path
import os,json,shutil,hashlib
R=Path(os.environ['PRIMER_OUT']);P=Path(__file__).parent;M=P/'media';M.mkdir(exist_ok=True);files=[]
for c in json.loads((R/'assessment.json').read_text())['cases']:
 for ext in ['.mp4','.png','.srt','.vtt']:
  files.append((R/(c['prefix']+ext),c['prefix']+ext))
for name in ['assessment.json','ryo-primer-montage.mp4','montage.srt','montage.vtt','montage-transcript.txt']:files.append((R/name,name))
for name in ['live-interaction.mp4','live-interaction.srt','live-interaction.vtt','live-interaction-transcript.txt']:files.append((R/'walkthrough'/name,name))
receipts=[]
for src,name in files:
 dst=M/name;shutil.copy2(src,dst);a=hashlib.sha256(src.read_bytes()).hexdigest();b=hashlib.sha256(dst.read_bytes()).hexdigest();assert a==b;receipts.append({'file':name,'sha256':a,'bytes':dst.stat().st_size})
(R/'gallery-media-receipt.json').write_text(json.dumps({'copiedAndHashVerified':len(receipts),'mediaDirectory':str(M),'files':receipts},indent=2));print('gallery files',len(receipts),'byte-exact')
