from pathlib import Path
import json,re,subprocess,math
p=Path(__file__).resolve().parent;o=Path('/path/to/local-assets');s=json.loads((p/'story.json').read_text());duration=math.ceil(s['duration']*30)/30
# Replace only the repaired first 750 frames, retaining the exact remaining master frames.
subprocess.run(['ffmpeg','-y','-v','error','-i',str(o/'opening-patch.mp4'),'-i',str(o/'visual-master.mp4'),'-i',str(o/'manipulation-patch.mp4'),'-filter_complex','[0:v]setpts=PTS-STARTPTS[a];[1:v]split=2[x][y];[x]trim=start_frame=750:end_frame=1320,setpts=PTS-STARTPTS[b];[2:v]setpts=PTS-STARTPTS[c];[y]trim=start_frame=1660,setpts=PTS-STARTPTS[d];[a][b][c][d]concat=n=4:v=1:a=0[v]','-map','[v]','-c:v','libx264','-crf','17','-preset','medium','-pix_fmt','yuv420p','-r','30','-movflags','+faststart',str(o/'corrected-visual-master.mp4')],check=True)
def stamp(t):
 n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
cues=[]
for seg in s['segments']:
 ss=re.findall(r'[^.!?]+[.!?]+',seg['narration']);total=sum(len(x) for x in ss);t=seg['start']
 for x in ss:
  end=t+seg['duration']*len(x)/total;cues.append(f'{len(cues)+1}\n{stamp(t)} --> {stamp(end)}\n{x.strip()}\n');t=end
cues[-1]=re.sub(r'( --> )[^\n]+',r'\g<1>'+stamp(duration),cues[-1])
(o/'narration.srt').write_text('\n'.join(cues));(o/'narration.vtt').write_text('WEBVTT\n\n'+re.sub(r'(?m)^\d+\n','', '\n'.join(cues)).replace(',','.'));(o/'narration.txt').write_text('\n\n'.join(x['narration'] for x in s['segments']))
subprocess.run(['ffmpeg','-y','-v','error','-i',str(o/'corrected-visual-master.mp4'),'-i',str(p/'assets/narration.wav'),'-i',str(o/'narration.srt'),'-map','0:v','-map','1:a','-map','2:s','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-af','apad','-t',str(duration),'-c:s','mov_text','-metadata:s:s:0','language=eng','-movflags','+faststart',str(o/'orbit-sketch-lab.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(o/'orbit-sketch-lab.mp4'),'-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(o/'orbit-sketch-lab.mp4')]))
(o/'ffprobe.json').write_text(json.dumps(probe,indent=2));print('FULL_DECODE_OK',probe['format']['duration'])
with open(o/'loudness.txt','w') as f:subprocess.run(['ffmpeg','-i',str(o/'orbit-sketch-lab.mp4'),'-af','ebur128=peak=true','-f','null','-'],stderr=f,stdout=f,check=True)
subprocess.run(['ffmpeg','-y','-v','error','-ss','52','-i',str(o/'orbit-sketch-lab.mp4'),'-frames:v','1',str(o/'final-screenshot.png')],check=True)
