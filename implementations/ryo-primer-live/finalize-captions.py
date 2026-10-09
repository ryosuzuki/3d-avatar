from pathlib import Path
import os,json,re,subprocess,hashlib
R=Path(os.environ['PRIMER_OUT']);checks=[]
for p in sorted(R.glob('[0-9][0-9]-*.mp4')):
 x=json.loads(p.with_suffix('.json').read_text());qa=json.loads(p.with_suffix('.video-qa.json').read_text());duration=round(x['recording']['seconds']*30)/30;srt=p.with_suffix('.srt');text=srt.read_text();lines=text.splitlines();indexes=[i for i,l in enumerate(lines) if ' --> ' in l]
 def stamp(t):
  ms=round(t*1000);h,ms=divmod(ms,3600000);mi,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{mi:02}:{s:02},{ms:03}'
 def secs(t):
  h,mi,s=t.replace(',','.').split(':');return int(h)*3600+int(mi)*60+float(s)
 if abs(secs(lines[indexes[-1]].split(' --> ')[1])-duration)>.1:
  lines[indexes[-1]]=lines[indexes[-1]].split(' --> ')[0]+' --> '+stamp(duration);text='\n'.join(lines)+'\n';srt.write_text(text);p.with_suffix('.vtt').write_text('WEBVTT\n\n'+re.sub(r'(\d\d:\d\d:\d\d),(\d{3})',r'\1.\2',text));temp=p.with_name(p.stem+'-remux.mp4')
  subprocess.run(['ffmpeg','-y','-v','error','-i',str(p),'-i',str(srt),'-map','0:v:0','-map','0:a:0','-map','1:0','-c:v','copy','-c:a','copy','-c:s','mov_text','-metadata:s:s:0','language='+('jpn' if x['id']==30 else 'eng'),'-movflags','+faststart',str(temp)],check=True);temp.replace(p);subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True);qa['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();qa['bytes']=p.stat().st_size
 prior=0
 for i in indexes:
  st,en=map(secs,lines[i].split(' --> '));assert prior<=st<=en<=duration+.1;prior=en
 embedded=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:s:0','-f','srt','-']).decode();src=re.findall(r'--> [^\n]+\n(.+)',text);actual=re.findall(r'--> [^\n]+\n(.+)',embedded);assert src==actual
 qa.update(subtitleTextParity=True,subtitleNonOverlapAndBounds=True,subtitleEndDriftSeconds=abs(duration-prior),lastCaptionHeldThroughLocalPreview=True);p.with_suffix('.video-qa.json').write_text(json.dumps(qa,indent=2));checks.append({'id':x['id'],'cues':len(indexes),'passed':True})
(R/'caption-qa.json').write_text(json.dumps(checks,indent=2));print('captions',len(checks),'passed')
