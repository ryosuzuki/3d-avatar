import json, pathlib, urllib.request, concurrent.futures, subprocess
out=pathlib.Path('/path/to/local-assets')
lines=[
'This is a working, Chalktalk inspired sketch experiment. We start with an empty canvas. Every shape comes from pointer input, not a preset model.',
'I draw an irregular arrow. Now I connect its output to the three dimensional view. The wireframe preserves the actual vertices of my stroke.',
'A number becomes a control when I connect it to rotation. The connection carries a value. Without that connection, the number cannot rotate the shape.',
'As I scrub the number, the rotation matrix and the three dimensional geometry update together. This is a live coordinate transformation, not a prerecorded orbit.',
'Now I edit the source itself. Moving this vertex immediately changes the transformed wireframe. The drawing remains the source of truth, even after rotation.',
'I disconnect rotation, then change the number again. The shape holds its last orientation. Reconnecting resumes the relationship using the current value.',
'Finally, I draw a different shape. The same connections still work. This prototype demonstrates causal sketch computation, with explicit ports rather than automatic sketch recognition.'
]
(out/'narration.json').write_text(json.dumps(lines,indent=2))
key=__import__('os').environ['OPENAI_API_KEY']
def make(i):
 data=json.dumps(dict(model='gpt-4o-mini-tts',voice='shimmer',input=lines[i],response_format='wav',instructions='Clear, natural English product demonstration. Calm and conversational, moderately brisk.')).encode()
 req=urllib.request.Request('https://api.openai.com/v1/audio/speech',data=data,headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=100) as r:(out/f'voice-{i}.wav').write_bytes(r.read())
 subprocess.run(['ffmpeg','-y','-v','error','-i',str(out/f'voice-{i}.wav'),'-af','atempo=1.15,apad','-t','11','-ar','48000',str(out/f'segment-{i}.wav')],check=True)
 print('voice ready',i,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:list(ex.map(make,range(7)))
(out/'audio-list.txt').write_text(''.join(f"file 'segment-{i}.wav'\n" for i in range(7)))
subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(out/'audio-list.txt'),'-af','loudnorm=I=-16:TP=-1.5:LRA=9','-ar','48000',str(out/'narration.wav')],check=True)
