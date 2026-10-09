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
(o/'narration.srt').write_text('\n'.join(cues));(o/'narration.txt').write_text('\n\n'.join(s['narration'] for s in story['segments']))
master=o/(sys.argv[1] if len(sys.argv)>1 else 'visual-master.mp4')
cmd=['ffmpeg','-y','-v','error','-i',str(master),'-i',str(p/'assets/narration.wav'),'-i',str(o/'narration.srt'),'-map','0:v','-map','1:a','-map','2:s','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-af','loudnorm=I=-16:TP=-1.5:LRA=11,apad','-t','86.733333','-c:s','mov_text','-metadata:s:s:0','language=eng','-movflags','+faststart',str(o/'transformer-pen-sketch.mp4')]
subprocess.run(cmd,check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(o/'transformer-pen-sketch.mp4'),'-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(o/'transformer-pen-sketch.mp4')]))
(o/'ffprobe.json').write_text(json.dumps(probe,indent=2))
subprocess.run(['ffmpeg','-v','error','-ss','53','-i',str(o/'transformer-pen-sketch.mp4'),'-frames:v','1',str(o/'final-screenshot.png')],check=True)
print('FINAL_MP4_DECODED',probe['format']['duration'])
