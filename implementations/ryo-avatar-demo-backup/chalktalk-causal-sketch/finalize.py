from pathlib import Path
import subprocess,json,re,hashlib,zipfile
p=Path(__file__).resolve().parent;o=Path('/path/to/local-assets');lines=json.loads((o/'narration.json').read_text())
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
srt='\n'.join(f'{i+1}\n{stamp(i*11)} --> {stamp((i+1)*11)}\n{s}\n' for i,s in enumerate(lines));(o/'narration.srt').write_text(srt);(o/'narration.txt').write_text('\n\n'.join(lines))
subprocess.run(['ffmpeg','-y','-v','error','-i',str(o/'visual-master.mp4'),'-i',str(o/'narration.wav'),'-i',str(o/'narration.srt'),'-map','0:v','-map','1:a','-map','2:s','-c:v','copy','-c:a','aac','-b:a','160k','-af','volume=-0.5dB','-ar','48000','-c:s','mov_text','-metadata:s:s:0','language=eng','-t','77','-movflags','+faststart',str(o/'chalktalk-causal-demo.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(o/'chalktalk-causal-demo.mp4'),'-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(o/'chalktalk-causal-demo.mp4')]))
(o/'ffprobe.json').write_text(json.dumps(probe,indent=2))
with (o/'loudness.txt').open('w')as f:subprocess.run(['ffmpeg','-i',str(o/'chalktalk-causal-demo.mp4'),'-af','ebur128=peak=true','-f','null','-'],stderr=f,stdout=f,check=True)
with zipfile.ZipFile(o/'chalktalk-causal-sketch.zip','w',zipfile.ZIP_DEFLATED)as z:
 for name in ['index.html','app.js','server.mjs','README.md','package.json','package-lock.json']:z.write(p/name,'chalktalk-causal-sketch/'+name)
 for name in ['chalktalk-causal-demo.mp4','narration.srt','narration.txt','ui-verification.json']:z.write(o/name,'chalktalk-causal-sketch/evidence/'+name)
manifest={'duration':77,'video':'chalktalk-causal-demo.mp4','fullDecode':'passed','voice':'OpenAI gpt-4o-mini-tts / shimmer; 1.15x tempo to fit segments without truncation','proof':'ui-verification.json','limitations':['No avatar or room rendering in this focused causal prototype.','Screen-space projection, not tracked AR.','Explicit ports; no generic shape recognition.','Operation screenshots at 15fps, delivery 30fps; narration-paced holds.','Full perceptual audio listen not performed.'],'files':{}}
for name in ['chalktalk-causal-demo.mp4','chalktalk-causal-sketch.zip','narration.srt','ui-verification.json']:
 f=o/name;manifest['files'][name]={'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
(o/'delivery-manifest.json').write_text(json.dumps(manifest,indent=2));print('FULL_DECODE_OK',probe['format']['duration'])
