from pathlib import Path
import json,urllib.request,base64,subprocess,concurrent.futures
p=Path(__file__).resolve().parents[1];o=Path('/path/to/local-assets');tmp=Path('/tmp/openclaw/avatar-sketch-worlds');story=json.loads((p/'story.json').read_text());key=__import__('os').environ['OPENAI_API_KEY']
def review(s):
 f=tmp/f"review-segment-{s['id']}.wav";subprocess.run(['ffmpeg','-y','-v','error','-i',str(o/f"segment-{s['id']}.wav"),'-ar','16000',str(f)],check=True)
 data=json.dumps({'model':'gpt-audio','messages':[{'role':'system','content':'You are an audio quality listener. Listen directly to supplied audio; no tools exist. Return completed observations, not intent. Do not invent timestamps.'},{'role':'user','content':[{'type':'text','text':f"This English narration segment is {s['duration']} seconds. The audio is attached in this same message. First transcribe its first and last complete spoken sentences, proving the file was heard. Then briefly assess clipped final words, abrupt voice cuts, intelligibility, unnatural speed or pronunciation. Do not ask for another file."},{'type':'input_audio','input_audio':{'data':base64.b64encode(f.read_bytes()).decode(),'format':'wav'}}]}],'modalities':['text'],'temperature':0,'max_tokens':500}).encode();req=urllib.request.Request('https://api.openai.com/v1/chat/completions',data=data,headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=90)as r:res=json.loads(r.read())
 return {'id':s['id'],'duration':s['duration'],'model':res['model'],'review':res['choices'][0]['message']['content']}
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:results=list(ex.map(review,story['segments']))
key=None;(o/'audio-segment-listening.json').write_text(json.dumps(results,indent=2));print('SEGMENT_LISTENING_READY')
