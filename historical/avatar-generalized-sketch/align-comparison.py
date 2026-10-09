from pathlib import Path
import json,urllib.request,uuid,re,difflib,concurrent.futures
ROOT=Path(__file__).resolve().parent;OUT=Path('/path/to/local-assets');config=json.loads((ROOT/'comparison.json').read_text());key=__import__('os').environ['OPENAI_API_KEY']
def norm(text):
 text=text.lower()
 for a,b in [('three','3'),('two','2'),('one','1')]:text=re.sub(r'\b'+a+r'\b',b,text)
 return re.sub(r'[^a-z0-9]','',text)
def align(r):
 audio=ROOT/r['audioUrl'][2:];boundary='----'+uuid.uuid4().hex;parts=[]
 for n,v in [('model','whisper-1'),('response_format','verbose_json'),('language','en'),('timestamp_granularities[]','word')]:parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{n}"\r\n\r\n{v}\r\n'.encode())
 parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="audio.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n'.encode()+audio.read_bytes()+b'\r\n');parts.append(f'--{boundary}--\r\n'.encode());req=urllib.request.Request('https://api.openai.com/v1/audio/transcriptions',data=b''.join(parts),headers={'Authorization':'Bearer '+key,'Content-Type':'multipart/form-data; boundary='+boundary});asr=json.loads(urllib.request.urlopen(req,timeout=120).read());(OUT/f"{r['id']}-comparison-asr.json").write_text(json.dumps(asr,indent=2))
 sentences=re.split(r'(?<=[.!?])\s+',r['answer']);words=asr['words'];orig=''.join(map(norm,sentences));aw=''.join(norm(w['word'])for w in words);ops=difflib.SequenceMatcher(None,orig,aw).get_opcodes();ends=[];q=0
 for w in words:q+=len(norm(w['word']));ends.append(q)
 cursor=0;last=0;cues=[]
 for sentence in sentences:
  cursor+=len(norm(sentence));mapped=len(aw)
  for tag,i1,i2,j1,j2 in ops:
   if i1<=cursor<=i2:mapped=j1+(cursor-i1)/(i2-i1 or 1)*(j2-j1);break
  end=next((i for i,e in enumerate(ends)if e>=mapped),len(ends)-1);chunk=words[last:end+1];last=end+1
  if chunk:cues.append({'start':chunk[0]['start'],'end':chunk[-1]['end'],'text':sentence})
 r['captionCues']=cues;r['audioQA']={'normalizedScriptSimilarity':difflib.SequenceMatcher(None,orig,norm(asr['text'])).ratio(),'alignment':'Original authoritative sentences mapped to ASR word times, not ASR wording','lastWordIncluded':last==len(words)};return r
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:config['segments']=list(pool.map(align,config['segments']))
(ROOT/'comparison.json').write_text(json.dumps(config,indent=2));del key;print([{k:r[k]for k in ['id','audioQA']}for r in config['segments']])
