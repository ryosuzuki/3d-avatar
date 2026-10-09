import subprocess,json,urllib.request,uuid
from pathlib import Path
O=Path('/path/to/local-assets');R=Path(__file__).parent
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(O/'generalized-v2-real-operations.mp4'),'-vn','-ar','16000','-ac','1',str(O/'actual-answer-audio.wav')],check=True)
key=__import__('os').environ['OPENAI_API_KEY'];boundary='v2-'+uuid.uuid4().hex
body=(f'--{boundary}\r\nContent-Disposition: form-data; name="model"\r\n\r\ngpt-4o-mini-transcribe\r\n--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="answer.wav"\r\nContent-Type: audio/wav\r\n\r\n').encode()+(O/'actual-answer-audio.wav').read_bytes()+f'\r\n--{boundary}--\r\n'.encode()
req=urllib.request.Request('https://api.openai.com/v1/audio/transcriptions',data=body,headers={'Authorization':'Bearer '+key,'Content-Type':'multipart/form-data; boundary='+boundary});data=json.load(urllib.request.urlopen(req,timeout=90));(O/'actual-audio-asr.json').write_text(json.dumps(data,indent=2));print(data.get('text',''))
