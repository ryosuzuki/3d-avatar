from pathlib import Path
import json,re,hashlib,subprocess
p=Path(__file__).resolve().parents[1];o=Path('/path/to/local-assets');story=json.loads((p/'story.json').read_text());h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def stamp(t):
 n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
cues=[]
for s in story['segments']:
 ss=re.findall(r'[^.!?]+[.!?]+',s['narration']);total=sum(len(x)for x in ss);t=s['start']
 for x in ss:
  end=t+s['duration']*len(x)/total;cues.append(f'{len(cues)+1}\n{stamp(t)} --> {stamp(end)}\n{x.strip()}\n');t=end
for dest in [o,p]:
 (dest/'narration.srt').write_text('\n'.join(cues));(dest/'narration.vtt').write_text('WEBVTT\n\n'+re.sub(r'(\d{2}:\d{2}:\d{2}),(\d{3})',r'\1.\2','\n'.join(cues)));(dest/'narration.txt').write_text('\n\n'.join(s['narration']for s in story['segments']))
f=o/'avatar-sketch-frontiers.mp4'
subprocess.run(['ffmpeg','-y','-v','error','-i',str(o/'visual-master.mp4'),'-i',str(p/'assets/narration.wav'),'-i',str(o/'narration.srt'),'-map','0:v','-map','1:a','-map','2:s','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t',str(story['duration']),'-c:s','mov_text','-metadata:s:s:0','language=eng','-movflags','+faststart',str(f)],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(f),'-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]));(o/'ffprobe.json').write_text(json.dumps(probe,indent=2));v=probe['streams'][0];a=probe['streams'][1];assert v['width']==1920 and v['height']==1080 and v['nb_frames']=='4320' and v['r_frame_rate']=='30/1' and v['pix_fmt']=='yuv420p';assert abs(float(v['duration'])-float(a['duration']))<.1
raw=f.read_bytes();assert raw.index(b'moov')<raw.index(b'mdat')
for st,n in [(20,'dinosaur'),(59,'attention'),(100,'gas'),(128,'body')]:subprocess.run(['ffmpeg','-y','-v','error','-ss',str(st),'-i',str(f),'-frames:v','1',str(o/f'screenshot-{n}.png')],check=True)
loud=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-vn','-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True);(o/'audio-loudness.txt').write_text(loud.stderr[-1600:]);silence=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-vn','-af','silencedetect=n=-45dB:d=1','-f','null','-'],capture_output=True,text=True);(o/'audio-silence.txt').write_text('\n'.join(x for x in silence.stderr.splitlines()if 'silence_'in x))
assets=[];base=Path('/path/to/local-assets')
for n in ['ryo_tpose.ply','ipad-room.ply','original-room.spz','source-provenance.json']:
 assets.append({'file':n,'size':(p/'assets'/n).stat().st_size,'sha256':h(p/'assets'/n),'identicalToApprovedBaseline':h(p/'assets'/n)==h(base/n)})
assert all(a['identicalToApprovedBaseline']for a in assets)
cap=json.loads((o/'visual-master-capture.json').read_text());proof=json.loads((o/'scene-proof.json').read_text());assert cap['completed'] and cap['frames']==4320 and not cap['errors'];assert len(proof['causalTests'])==8 and all(t['passed']for t in proof['causalTests']);assert max(max(s['state']['armErrors'])for s in cap['samples'])<.01
manifest={'title':'Avatar Sketch Frontiers','duration':144,'segments':8,'chapters':['walking dinosaur','illustrative spatial attention','schematic ideal gas','schematic body'],'video':{'path':str(f),'sha256':h(f),'bytes':f.stat().st_size,'width':1920,'height':1080,'fps':30,'frames':4320,'codec':v['codec_name'],'pixelFormat':v['pix_fmt'],'audio':'AAC48kHz','faststart':True},'voice':story['voice'],'assets':assets,'sourceInspection':'First batch source ledger inherited; no new video-inspection claim. Procedural examples authored for requested topics.','qa':{'fullDecode':'passed exact final file','captureFrames':4320,'browserErrors':cap['errors'],'causalChecks':proof['causalTests'],'maxSampledIKError':max(max(s['state']['armErrors'])for s in cap['samples']),'subtitles':'burned English + embedded English mov_text + SRT/VTT; sentence timings proportional approximation','fullMediaPlayback':'pending actual ended verification','perceptualAudio':'AI listener returned partly inconsistent timestamp claims; independent full perceptual signoff not claimed. See review/comparison evidence.'},'limitations':['Authored procedural geometry and choreography, not arbitrary recognition or live AI','Approximate Gaussian skinning and pen grip, no finger rig or lip sync','Layered avatar/room visibility, not calibrated AR or physical occlusion','Cursive labels are typography','Attention weights illustrative, not actual model weights','Gas particle paths authored, pressure from ideal-gas relation not collision-derived; relative units','Body/lungs/heart schematic symbols, not anatomical reconstruction'],'backup':{'repository':'https://github.com/ryosuzuki/ryo-avatar-demo-backup','visibility':'private','ownedPaths':['avatar-sketch-frontiers/'],'integrationState':'pending','releaseTag':'avatar-sketch-frontiers-2026-10-08','completionOwner':'sketch_worlds_remaining'}}
for d in [p,o]:(d/'delivery-manifest.json').write_text(json.dumps(manifest,indent=2))
print('FINAL_DECODE_PASS',f.stat().st_size)
