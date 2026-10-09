from pathlib import Path
import json,re,hashlib,subprocess,zipfile,sys
p=Path('/path/to/local-assets');o=Path('/path/to/local-assets');story=json.loads((p/'story.json').read_text())
def stamp(t):
 n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
cues=[]
for s in story['segments']:
 ss=re.findall(r'[^.!?]+[.!?]+',s['narration']);total=sum(len(x) for x in ss);t=s['start']
 for x in ss:
  end=t+s['duration']*len(x)/total;cues.append(f'{len(cues)+1}\n{stamp(t)} --> {stamp(end)}\n{x.strip()}\n');t=end
(o/'narration.srt').write_text('\n'.join(cues));(o/'narration.vtt').write_text('WEBVTT\n\n'+re.sub(r'(\d{2}:\d{2}:\d{2}),(\d{3})',r'\1.\2','\n'.join(cues)));(o/'narration.txt').write_text('\n\n'.join(s['narration'] for s in story['segments']))
f=o/'avatar-chalktalk-expanded.mp4'
subprocess.run(['ffmpeg','-y','-v','error','-i',str(o/(sys.argv[1] if len(sys.argv)>1 else 'visual-master.mp4')),'-i',str(p/'assets/narration.wav'),'-i',str(o/'narration.srt'),'-map','0:v','-map','1:a','-map','2:s','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-af','loudnorm=I=-16:TP=-2.0:LRA=11,apad','-t',str(story['duration']),'-c:s','mov_text','-metadata:s:s:0','language=eng','-movflags','+faststart',str(f)],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(f),'-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]));(o/'ffprobe.json').write_text(json.dumps(probe,indent=2))
for st,n in [(23,'pendulum'),(53,'vase'),(78,'matrix')]:subprocess.run(['ffmpeg','-y','-v','error','-ss',str(st),'-i',str(f),'-frames:v','1',str(o/f'screenshot-{n}.png')],check=True)
loud=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-vn','-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True);(o/'audio-loudness.txt').write_text(loud.stderr[-1800:])
raw=f.read_bytes();manifest={'duration':story['duration'],'video':{'path':str(f),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)},'mechanical':{'fullDecode':'passed','faststart':raw.find(b'moov')<raw.find(b'mdat'),'streams':[{k:s.get(k)for k in ['codec_name','width','height','pix_fmt','r_frame_rate','sample_rate','duration','nb_frames']}for s in probe['streams']]},'voice':story['voice'],'project':str(p),'assets':{n:hashlib.sha256((p/'assets'/n).read_bytes()).hexdigest()for n in ['ryo_tpose.ply','ipad-room.ply','original-room.spz']},'limitations':['Authored choreography; no freehand semantic recognition or general Chalktalk parity','Manual Gaussian placement in captured room; no tracked AR','No realtime AI, lip sync, or gesture understanding','Natural labels are cursive typography, not genuine captured handwriting'],'review':{'visual':'beginning/middle/end of each example inspected; causal controls verified','perceptualAudio':'not independently listened; full Whisper ASR reviewed against script, no substantive omission','fullMotionPlayback':'pending parent review'}}
(o/'delivery-manifest.json').write_text(json.dumps(manifest,indent=2));(p/'delivery-manifest.json').write_text(json.dumps(manifest,indent=2));print('FINAL_MP4_DECODED',probe['format']['duration'])
