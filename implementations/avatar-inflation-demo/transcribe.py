from pathlib import Path
import urllib.request,json,uuid
root=Path(__file__).parent;out=Path('/path/to/local-assets');key=__import__('os').environ['OPENAI_API_KEY'];results=[]
for name in ['fish','octopus','leaf','unseen']:
 boundary=uuid.uuid4().hex;blob=(root/'meshes'/f'{name}.mp3').read_bytes();body=(f'--{boundary}\r\nContent-Disposition: form-data; name="model"\r\n\r\nwhisper-1\r\n--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="audio.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n').encode()+blob+f'\r\n--{boundary}--\r\n'.encode()
 req=urllib.request.Request('https://api.openai.com/v1/audio/transcriptions',data=body,headers={'Authorization':'Bearer '+key,'Content-Type':f'multipart/form-data; boundary={boundary}'})
 with urllib.request.urlopen(req,timeout=120) as r:result=json.loads(r.read());result['shape']=name;results.append(result)
(out/'audio-asr.json').write_text(json.dumps(results,indent=2));del key
