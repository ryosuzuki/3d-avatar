from pathlib import Path
import os,json,subprocess,hashlib
R=Path(os.environ['PRIMER_OUT']);paths=sorted(R.glob('[0-9][0-9]-*.mp4'))+[R/'ryo-primer-montage.mp4',R/'walkthrough/live-interaction.mp4'];rows=[]
for p in paths:
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio');sub=next(s for s in probe['streams'] if s['codec_type']=='subtitle');av=abs(float(v['duration'])-float(a['duration']));sv=abs(float(v['duration'])-float(sub['duration']));assert v['codec_name']=='h264' and v['profile']=='High' and v['pix_fmt']=='yuv420p' and v['color_range']=='tv' and v['r_frame_rate']=='30/1' and v['avg_frame_rate']=='30/1';assert a['codec_name']=='aac' and a['sample_rate']=='48000' and sub['codec_name']=='mov_text' and av<=.1 and sv<=.1
 atoms=[]
 with p.open('rb') as f:
  while b:=f.read(8):
   if len(b)<8:break
   size=int.from_bytes(b[:4],'big');atoms.append(b[4:].decode('ascii','replace'))
   if size==1:size=int.from_bytes(f.read(8),'big');f.seek(size-16,1)
   elif size>=8:f.seek(size-8,1)
   else:break
 assert atoms.index('moov')<atoms.index('mdat');rows.append({'file':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'duration':float(v['duration']),'avEndDriftSeconds':av,'subtitleEndDriftSeconds':sv,'profile':v['profile'],'pixelFormat':v['pix_fmt'],'colorRange':v['color_range'],'frameRate':v['r_frame_rate'],'audioSampleRate':a['sample_rate'],'moovBeforeMdat':True})
(R/'final-media-audit.json').write_text(json.dumps({'verifiedCount':len(rows),'expectedCount':32,'files':rows},indent=2));print('final media compatibility audit',len(rows),'passed')
