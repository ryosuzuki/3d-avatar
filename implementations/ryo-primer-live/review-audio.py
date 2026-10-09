from pathlib import Path
from server import provider
import base64,json,os,concurrent.futures,urllib.request,uuid,subprocess,re
ROOT=Path(os.environ.get('PRIMER_OUT','/path/to/local-assets'))
def transcribe(p):
 dest=p.with_suffix('.asr.json')
 if dest.exists():return
 try:
  key=__import__('os').environ['OPENAI_API_KEY'];boundary=uuid.uuid4().hex
  body=(f'--{boundary}\r\nContent-Disposition: form-data; name="model"\r\n\r\ngpt-4o-mini-transcribe\r\n--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="speech.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n'.encode()+p.read_bytes()+f'\r\n--{boundary}--\r\n'.encode())
  req=urllib.request.Request('https://api.openai.com/v1/audio/transcriptions',data=body,headers={'Authorization':'Bearer '+key,'Content-Type':'multipart/form-data; boundary='+boundary})
  with urllib.request.urlopen(req,timeout=120) as r:x=json.loads(r.read())
  dest.write_text(json.dumps(x,ensure_ascii=False,indent=2));print('ASR',p.name,flush=True)
 except Exception as e:dest.write_text(json.dumps({'error':type(e).__name__}));print('ASR failed',p.name,type(e).__name__,flush=True)
paths=sorted(ROOT.glob('[0-9][0-9]-*.mp3'))+sorted(ROOT.glob('montage-voice-*.mp3'))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(transcribe,paths))
reviews=[]
for p in paths:
 dest=p.with_suffix('.perceptual-review.json')
 if dest.exists():reviews.append(json.loads(dest.read_text()));continue
 try:
  wav=Path('/tmp/openclaw')/('primer-review-'+uuid.uuid4().hex+'.wav');subprocess.run(['ffmpeg','-y','-v','error','-i',str(p),'-ar','16000','-ac','1','-c:a','pcm_s16le',str(wav)],check=True)
  raw=json.loads(provider('chat/completions',{'model':'gpt-audio-1.5','modalities':['text'],'messages':[{'role':'user','content':[{'type':'text','text':'Listen to this English or Japanese synthetic explanatory narration. Review audible intelligibility, technical-term pronunciation, clipping/artifacts, unnatural long silences or abrupt endings. Return concise JSON: intelligible, clipping, issues (timestamped if present), summary, actualPhraseHeard. Cite an actual audible phrase to demonstrate you received the audio. Do not assume quality from the script; listen to the audio.'},{'type':'input_audio','input_audio':{'data':base64.b64encode(wav.read_bytes()).decode(),'format':'wav'}}]}],'max_tokens':700}));text=raw['choices'][0]['message']['content'];review={'file':p.name,'model':raw['model'],'review':text};dest.write_text(json.dumps(review,ensure_ascii=False,indent=2));wav.unlink(missing_ok=True);reviews.append(review);print('Perceptual',p.name,flush=True)
 except Exception as e:review={'file':p.name,'error':type(e).__name__};dest.write_text(json.dumps(review));reviews.append(review);print('Perceptual unavailable',type(e).__name__,flush=True)
(ROOT/'audio-review-summary.json').write_text(json.dumps({'asrFiles':len(paths),'perceptualReviews':reviews,'humanHeadphoneReview':'Not performed; audio-capable model review used'},ensure_ascii=False,indent=2))
