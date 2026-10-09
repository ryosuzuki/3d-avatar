from pathlib import Path
import subprocess,json
p=Path(__file__).parent;o=Path('/path/to/local-assets');a=Path('/path/to/local-assets');b=Path('/path/to/local-assets')
def hashes(f):
 s=subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-map','0:v','-f','framemd5','-']).decode();return [r.split(',')[-1].strip()for r in s.splitlines()if r and not r.startswith('#')]
checks=[]
for suffix,names in [('master',['avatar-sketch-worlds.mp4','avatar-sketch-frontiers.mp4']),('slack',['avatar-sketch-worlds-slack.mp4','avatar-sketch-frontiers-slack.mp4'])]:
 expected=hashes(a/names[0])+hashes(b/names[1]);actual=hashes(o/f'avatar-sketch-collection-{suffix}.mp4');assert len(actual)==8160 and actual==expected;checks.append({'file':f'avatar-sketch-collection-{suffix}.mp4','decodedFrames':len(actual),'everyFrameIdenticalToOrderedInputs':True});print('FRAMES_IDENTICAL',suffix,len(actual),flush=True)
for t in [127.8,127.9666667,128,128.2]:subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(o/'avatar-sketch-collection-master.mp4'),'-frames:v','1',str(o/('join-'+str(t).replace('.','-')+'.png'))],check=True)
# Authoritative PCM ordering preserves every original voice sample before AAC encoding.
audio=lambda f:subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-map','0:a','-f','s16le','-'])
a1=audio(Path('/path/to/local-assets'));a2=audio(Path('/path/to/local-assets'));both=audio(o/'narration.wav');assert both==a1+a2
(o/'frame-identity-verification.json').write_text(json.dumps({'checks':checks,'PCMVoiceSamplesIdenticalToOrderedInputs':True,'combinedPCMSamples':len(both)//2,'sourceFootageRegenerated':False},indent=2));print('PCM_IDENTICAL',len(both)//2)
