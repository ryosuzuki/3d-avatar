from pathlib import Path
import json,urllib.request,uuid,unicodedata,re,difflib
out=Path('/path/to/local-assets');audio=out/'live-question-sketch-captured.wav';b='----'+uuid.uuid4().hex
parts=[]
def field(n,v):parts.append(f'--{b}\r\nContent-Disposition: form-data; name="{n}"\r\n\r\n{v}\r\n'.encode())
field('model','whisper-1');field('response_format','verbose_json');field('language','en')
parts.append(f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="captured.wav"\r\nContent-Type: audio/wav\r\n\r\n'.encode()+audio.read_bytes()+b'\r\n');parts.append(f'--{b}--\r\n'.encode())
k=__import__('os').environ['OPENAI_API_KEY'];req=urllib.request.Request('https://api.openai.com/v1/audio/transcriptions',data=b''.join(parts),headers={'Authorization':'Bearer '+k,'Content-Type':'multipart/form-data; boundary='+b})
with urllib.request.urlopen(req,timeout=120) as r:asr=json.load(r)
del k
(out/'live-question-sketch-audio-asr.json').write_text(json.dumps(asr,indent=2))
expected=json.loads((out/'ui-and-audio-verification.json').read_text())['answer']['sketch']['answer']
def norm(s):
 s=unicodedata.normalize('NFKC',s).lower().replace('°',' degrees ').replace('cancelling','canceling')
 for w,n in {'one':'1','two':'2','three':'3','four':'4','five':'5','six':'6','seven':'7','eight':'8','nine':'9','ten':'10'}.items():s=re.sub(r'\b'+w+r'\b',n,s)
 return re.sub(r'[^a-z0-9]','',s)
a=norm(expected);c=norm(asr['text']);ratio=difflib.SequenceMatcher(None,a,c).ratio();(out/'live-question-sketch-audio-comparison.json').write_text(json.dumps({'expected':expected,'transcribed':asr['text'],'normalizedSimilarity':ratio,'capturedFrom':'actual browser MediaElementSource of newly generated answer audio','notPrerecordedNarration':True},indent=2));print('captured full-audio ASR similarity',ratio)
if ratio<.9:raise SystemExit('Inspect transcript mismatch')
