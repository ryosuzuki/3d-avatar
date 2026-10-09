from pathlib import Path
import urllib.request,json,uuid,subprocess,base64
R=Path(__file__).parent;O=Path('/path/to/local-assets');key=__import__('os').environ['OPENAI_API_KEY']
result={}
for name in ['fish','owl']:
 f=R/'audio'/f'{name}.wav';b='boundary'+uuid.uuid4().hex
 body=(f'--{b}\r\nContent-Disposition: form-data; name="model"\r\n\r\ngpt-4o-mini-transcribe\r\n--{b}\r\nContent-Disposition: form-data; name="file"; filename="{name}.wav"\r\nContent-Type: audio/wav\r\n\r\n').encode()+f.read_bytes()+f'\r\n--{b}--\r\n'.encode()
 req=urllib.request.Request('https://api.openai.com/v1/audio/transcriptions',data=body,headers={'Authorization':'Bearer '+key,'Content-Type':'multipart/form-data; boundary='+b})
 with urllib.request.urlopen(req,timeout=120) as resp:result[name]=json.load(resp)
(O/'audio-asr.json').write_text(json.dumps(result,indent=2));del key;print(json.dumps(result))
