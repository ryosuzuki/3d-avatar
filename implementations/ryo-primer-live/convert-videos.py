from pathlib import Path
import json,subprocess,re,hashlib,os
ROOT=Path(os.environ.get('PRIMER_OUT','/path/to/local-assets'))
def stamp(t):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
for p in sorted(ROOT.glob('[0-9][0-9]-*.webm')):
 if p.stem.endswith('-failed'):continue
 dest=p.with_suffix('.mp4')
 if dest.exists():continue
 if not p.with_suffix('.json').exists():continue
 x=json.loads(p.with_suffix('.json').read_text());audio=p.with_suffix('.mp3')
 duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(audio)])) if audio.exists() else 0
 sentences=re.split(r'(?<=[.!?。])\s+',x['sketch']['answer']);total=sum(len(s) for s in sentences);start=x.get('audioStartedMs',x.get('audioReadyMs',0))/1000;cursor=start;srt=[]
 for i,s in enumerate(sentences):
  end=round(x['recording']['seconds']*30)/30 if i==len(sentences)-1 else cursor+duration*len(s)/max(1,total);srt.append(f'{i+1}\n{stamp(cursor)} --> {stamp(end)}\n{s}\n');cursor=end
 p.with_suffix('.srt').write_text('\n'.join(srt));p.with_suffix('.vtt').write_text('WEBVTT\n\n'+re.sub(r'(\d\d:\d\d:\d\d),(\d{3})',r'\1.\2','\n'.join(srt)))
 cmd=['ffmpeg','-y','-v','error','-i',str(p),'-i',str(p.with_suffix('.srt')),'-map','0:v:0','-map','0:a:0','-map','1:0','-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p','-vf','scale=out_range=tv,format=yuv420p,tpad=stop_mode=clone:stop_duration=1','-color_range','tv','-r','30','-c:a','aac','-ar','48000','-b:a','128k','-af','apad','-t',str(round(x['recording']['seconds']*30)/30),'-c:s','mov_text','-metadata:s:s:0','language='+('jpn' if re.search('[ぁ-んァ-ン一-龯]',x['sketch']['answer']) else 'eng'),'-movflags','+faststart',str(dest)]
 subprocess.run(cmd,check=True)
 subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-f','null','-'],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(dest)]));stream=[s for s in probe['streams'] if s['codec_type'] in ['audio','video']];drift=abs(float(stream[0]['duration'])-float(stream[1]['duration']))
 atoms=[]
 with dest.open('rb') as f:
  while True:
   b=f.read(8)
   if len(b)<8:break
   size=int.from_bytes(b[:4],'big');name=b[4:].decode('ascii','replace');atoms.append(name)
   if size==1:size=int.from_bytes(f.read(8),'big');f.seek(size-16,1)
   elif size>=8:f.seek(size-8,1)
   else:break
 faststart='moov' in atoms and 'mdat' in atoms and atoms.index('moov')<atoms.index('mdat')
 receipt={'moovBeforeMdat':faststart,'path':str(dest),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'bytes':dest.stat().st_size,'duration':probe['format']['duration'],'avEndDriftSeconds':drift,'fullDecodePassed':True,'subtitleTiming':'Sentence durations proportional to authoritative text; approximate speech alignment','streams':[{k:s.get(k) for k in ['codec_type','codec_name','width','height','r_frame_rate','sample_rate','duration']} for s in probe['streams']]};dest.with_suffix('.video-qa.json').write_text(json.dumps(receipt,indent=2));print('converted',dest.name,'drift',round(drift,3),flush=True)
