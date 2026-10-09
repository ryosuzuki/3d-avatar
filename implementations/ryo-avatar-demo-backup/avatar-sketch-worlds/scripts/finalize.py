from pathlib import Path
import json,re,hashlib,subprocess,shutil,sys
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
f=o/'avatar-sketch-worlds.mp4'
subprocess.run(['ffmpeg','-y','-v','error','-i',str(o/(sys.argv[1] if len(sys.argv)>1 else 'visual-master.mp4')),'-i',str(p/'assets/narration.wav'),'-i',str(o/'narration.srt'),'-map','0:v','-map','1:a','-map','2:s','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t',str(story['duration']),'-c:s','mov_text','-metadata:s:s:0','language=eng','-movflags','+faststart',str(f)],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(f),'-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]));(o/'ffprobe.json').write_text(json.dumps(probe,indent=2));v=probe['streams'][0];a=probe['streams'][1];assert v['width']==1920 and v['height']==1080 and v['nb_frames']=='3840' and v['r_frame_rate']=='30/1' and v['pix_fmt']=='yuv420p';assert abs(float(v['duration'])-float(a['duration']))<.1
raw=f.read_bytes();assert raw.index(b'moov')<raw.index(b'mdat')
for st,n in [(18,'pendulum'),(49,'fish'),(86,'terrain'),(117,'water')]:subprocess.run(['ffmpeg','-y','-v','error','-ss',str(st),'-i',str(f),'-frames:v','1',str(o/f'screenshot-{n}.png')],check=True)
loud=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-vn','-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True);(o/'audio-loudness.txt').write_text(loud.stderr[-1600:]);silence=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-vn','-af','silencedetect=n=-45dB:d=1','-f','null','-'],capture_output=True,text=True);(o/'audio-silence.txt').write_text('\n'.join(x for x in silence.stderr.splitlines()if 'silence_'in x))
assets=[];base=Path('/path/to/local-assets')
for n in ['ryo_tpose.ply','ipad-room.ply','original-room.spz','source-provenance.json','narration.wav']:
 assets.append({'file':n,'size':(p/'assets'/n).stat().st_size,'sha256':h(p/'assets'/n),'identicalToApprovedBaseline':h(p/'assets'/n)==h(base/n)})
(p/'asset-receipt.json').write_text(json.dumps(assets,indent=2));(p/'provenance.json').write_text(json.dumps({'base':'/path/to/local-assets','taskDate':'2026-10-08','originalAssets':assets,'authoredGeometry':['pendulum','fish','terrain/river/cloud','schematic water'],'source':'references/source-ledger.md','noReplacementMeshes':True,'credentialsStored':False},indent=2))
cap=json.loads((o/'visual-master-capture.json').read_text());assert cap['completed'] and cap['frames']==3840 and not cap['errors'];assert cap['cleanup']['status']=='verified'
patchfile=o/'hand-reach-patch-capture.json'
if patchfile.exists():
 patch=json.loads(patchfile.read_text());assert patch['completed'] and patch['frames']==3000 and not patch['errors'];assert max(max(s['state']['armErrors'])for s in patch['samples'])<.01

manifest={'title':'Avatar Sketch Worlds: four sketches become living explanations','duration':128,'segments':8,'chapters':['pendulum waveform','fish unfold/swim','terrain river cloud orbit','schematic H2O'],'video':{'path':str(f),'sha256':h(f),'bytes':f.stat().st_size,'width':1920,'height':1080,'fps':30,'frames':3840,'codec':v['codec_name'],'pixelFormat':v['pix_fmt'],'audio':'AAC48kHz','faststart':True},'voice':story['voice'],'assets':assets,'sourceInspection':{'googleSlides':'actual target109/174 and bounded nearby source text read; embedded clips not played','baseline':'original code/receipts/manifests read, original avatar and room retained'},'qa':{'fullDecode':'passed exact final file','captureFrames':3840,'browserErrors':cap['errors'],'geometry':'14 checks passed; independent reviewer findings repaired before master','subtitles':'burned English + embedded English mov_text + SRT/VTT; sentence timings proportional approximation','ASR':'complete local Whisper turbo reviewed against source; orthographic/number changes only','perceptualAudio':'independent gpt-audio listener; see audio-perceptual-review.json and corroboration notes','fullMediaPlayback':'pending actual ended verification'},'limitations':['Authored procedural geometry and choreography, not arbitrary sketch recognition or live AI','Approximate Gaussian skinning/hand IK, no supplied finger rig or lip sync','Layered avatar/room visibility, not tracked AR registration or physical room occlusion','Cursive labels are typography, not captured handwriting','Schematic water radii/bonds, no atom-scale forces or molecular dynamics'],'pendingScope':['additional dinosaur/attention/gas/body demos','private remote live-Q&A sketch app'],'backup':{'repository':'https://github.com/ryosuzuki/ryo-avatar-demo-backup','visibility':'private','ownedPaths':['avatar-sketch-worlds/'],'integrationState':'pending','releaseTag':'avatar-sketch-worlds-2026-10-08'}}
for d in [p,o]:(d/'delivery-manifest.json').write_text(json.dumps(manifest,indent=2))
print('FINAL_DECODE_PASS',f.stat().st_size)
