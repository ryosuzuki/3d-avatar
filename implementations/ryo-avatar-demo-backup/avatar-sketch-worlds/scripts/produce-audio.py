from pathlib import Path
import json,urllib.request,concurrent.futures,subprocess
p=Path(__file__).resolve().parents[1];out=Path('/path/to/local-assets');story=json.loads((p/'story.json').read_text());key=__import__('os').environ['OPENAI_API_KEY']
def make(s):
 i=s['id'];dst=out/f'voice-{i}.wav'
 if not dst.exists():
  payload=json.dumps(dict(model='gpt-4o-mini-tts',voice='shimmer',input=s['narration'],response_format='wav',instructions='Natural English demonstration. Warm, clear, conversational, brisk but unhurried. Use expressive sentence phrasing, not a lecture monotone.')).encode()
  req=urllib.request.Request('https://api.openai.com/v1/audio/speech',data=payload,headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
  with urllib.request.urlopen(req,timeout=100)as r:dst.write_bytes(r.read())
 dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(dst)]));target=s['duration'];speed=dur/(target-.4)
 # Preserve a natural pace, never force a segment to be slower than the speaker; pad only final hold.
 speed=max(1,min(1.35,speed));subprocess.run(['ffmpeg','-y','-v','error','-i',str(dst),'-af',f'atempo={speed},apad','-t',str(target),'-ar','48000','-ac','1','-c:a','pcm_s16le',str(out/f'segment-{i}.wav')],check=True)
 print('VOICE_READY',i,'source_seconds',round(dur,2),'target',target,'speed',round(speed,3),flush=True);return {'id':i,'sourceDuration':dur,'target':target,'speed':speed}
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:receipts=list(ex.map(make,story['segments']))
key=None
(out/'voice-segments.json').write_text(json.dumps(receipts,indent=2));(out/'audio-list.txt').write_text(''.join(f"file '{out}/segment-{s['id']}.wav'\n"for s in story['segments']))
subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(out/'audio-list.txt'),'-af','loudnorm=I=-16:TP=-2:LRA=11','-ar','48000','-ac','1','-c:a','pcm_s16le',str(p/'assets/narration.wav')],check=True)
