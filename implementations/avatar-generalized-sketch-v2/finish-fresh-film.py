from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess,json
O=Path('/path/to/local-assets');font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',16)
for kind,text in [('queue','Request began before capture; actual job states and elapsed time are retained.'),('ready','Same new GLB; front adjusted after display review. No additional neural generation.')]:
 im=Image.new('RGBA',(1280,720));d=ImageDraw.Draw(im);box=d.textbbox((35,100),text,font=font);d.rectangle((29,96,box[2]+6,box[3]+5),fill=(16,37,54,235));d.text((35,100),text,font=font,fill='white');im.save(O/f'fresh-{kind}-caption.png')
for kind,stem,seconds in [('queue','fresh-queued-cb427f',17),('ready','fresh-ready-cb427f',43)]:
 subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(O/(stem+'.webm')),'-loop','1','-i',str(O/f'fresh-{kind}-caption.png'),'-t',str(seconds),'-filter_complex','[0:v]fps=30[v];[v][1:v]overlay=0:0:shortest=1[out]','-map','[out]','-map','0:a','-af',('volume=0,'if kind=='queue'else'')+'aresample=48000','-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k',f'/tmp/openclaw/v2-fresh-{kind}.mp4'],check=True)
Path('/tmp/openclaw/v2-fresh-concat.txt').write_text("file '/tmp/openclaw/v2-fresh-queue.mp4'\nfile '/tmp/openclaw/v2-fresh-ready.mp4'\n")
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i','/tmp/openclaw/v2-fresh-concat.txt','-c','copy','/tmp/openclaw/v2-fresh-joined.mp4'],check=True)
srt='''1
00:00:00,000 --> 00:00:17,000
[Request began before capture. Actual original sketch and job status are shown.]

2
00:00:17,000 --> 00:00:24,800
The visible spiral chambers suggest a coiled, gradually expanding form
with inferred depth from center to edge.

3
00:00:24,800 --> 00:00:32,700
The original outline alone does not uniquely determine the hidden internal surfaces;
this is illustrative, not anatomically exact.

4
00:00:32,700 --> 00:00:35,360
The shown opening is for demonstration.

5
00:00:35,360 --> 00:01:00,000
[Silent mesh orbit. Same actual learned output; no new neural inference.]
''';(O/'fresh-learned-runtime.srt').write_text(srt)
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i','/tmp/openclaw/v2-fresh-joined.mp4','-i',str(O/'fresh-learned-runtime.srt'),'-map','0:v','-map','0:a','-map','1:0','-c:v','copy','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000','-c:a','aac','-b:a','128k','-c:s','mov_text','-metadata:s:s:0','language=eng','-movflags','+faststart',str(O/'fresh-learned-runtime.mp4')],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(O/'fresh-learned-runtime.mp4'),'-f','null','-'],check=True)
print(json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size','-of','json',str(O/'fresh-learned-runtime.mp4')],text=True)))
