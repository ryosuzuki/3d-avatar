from pathlib import Path
import json,urllib.request,uuid,concurrent.futures,re,difflib
ROOT=Path(__file__).resolve().parent;OUT=Path('/path/to/local-assets')
key=__import__('os').environ['OPENAI_API_KEY']
def align(ident):
 d=json.loads((ROOT/'generated'/f'{ident}.json').read_text());boundary='----'+uuid.uuid4().hex;parts=[]
 for name,value in [('model','whisper-1'),('response_format','verbose_json'),('language','en'),('timestamp_granularities[]','word')]:parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode())
 parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="audio.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n'.encode()+(ROOT/'generated'/f'{ident}.mp3').read_bytes()+b'\r\n');parts.append(f'--{boundary}--\r\n'.encode())
 req=urllib.request.Request('https://api.openai.com/v1/audio/transcriptions',data=b''.join(parts),headers={'Authorization':'Bearer '+key,'Content-Type':'multipart/form-data; boundary='+boundary})
 asr=json.loads(urllib.request.urlopen(req,timeout=120).read());(OUT/f'{ident}-asr.json').write_text(json.dumps(asr,indent=2));sentences=re.split(r'(?<=[.!?])\s+',d['scene']['answer']);words=asr['words'];norm=lambda text:re.sub(r'[^a-z0-9]','',text.lower());orig=''.join(map(norm,sentences));aw=''.join(norm(w['word'])for w in words);ops=difflib.SequenceMatcher(None,orig,aw).get_opcodes();ends=[];q=0
 for w in words:q+=len(norm(w['word']));ends.append(q)
 cursor=0;last=0;cues=[]
 for sentence in sentences:
  cursor+=len(norm(sentence));mapped=len(aw)
  for tag,i1,i2,j1,j2 in ops:
   if i1<=cursor<=i2:mapped=j1+(cursor-i1)/(i2-i1 or 1)*(j2-j1);break
  end=next((i for i,e in enumerate(ends)if e>=mapped),len(ends)-1);chunk=words[last:end+1];last=end+1
  if chunk:cues.append({'start':chunk[0]['start'],'end':chunk[-1]['end'],'text':sentence.strip()})
 ratio=difflib.SequenceMatcher(None,re.sub(r'[^a-z0-9]','',d['scene']['answer'].lower()),re.sub(r'[^a-z0-9]','',asr['text'].lower())).ratio();d['captionCues']=cues;d['audioQA']={'normalizedTranscriptSimilarity':ratio,'alignment':'Authoritative sentence boundaries mapped by normalized-character ASR word alignment; decimals retained; last spoken word included'};(ROOT/'generated'/f'{ident}.json').write_text(json.dumps(d,indent=2));return {'id':ident,'ratio':ratio,'cues':len(cues),'lastEnd':cues[-1]['end']}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 results=list(pool.map(align,['e39766449057','38a2a34b89d2','89ce7746c953']))
(OUT/'audio-asr-comparison.json').write_text(json.dumps(results,indent=2));print(json.dumps(results));del key
