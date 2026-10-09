from pathlib import Path
import json,zipfile,hashlib,html
p=Path('/path/to/local-assets');a=json.load(open(p/'assessment.json'));files=[]
for c in a['cases']:
 for ext in ['mp4','png','srt','vtt','json','video-qa.json']:
  files.append((p/f"{c['prefix']}.{ext}",f"{c['prefix']}.{ext}"))
for name in ['assessment.json','final-media-audit.json','caption-qa.json','audio-gate.json','ryo-primer-montage.mp4','montage.srt','montage.vtt','montage-transcript.txt','montage-qa.json']:
 files.append((p/name,name))
for name in ['live-interaction.mp4','live-interaction.srt','live-interaction.vtt','receipt.json','live-interaction-qa.json']:
 files.append((p/'walkthrough'/name,'walkthrough/'+name))
text='''30 real live-generated test recordings, corrected final pass. Open index.html after extracting. Each full clip includes real waiting time, synthetic voice, and parameter preview. Live private app: http://127.0.0.1:8822/ ; gallery: http://127.0.0.1:8822/gallery.html . Requires Ryo tailnet access; not public.
Measured warm-browser labeled response p50 2125ms / p95 3217ms; ink continues ~4s. Audio ready p50 7230ms / p95 10849ms. Original160k Gaussian Ryo; manually fitted drawing rig/projected pointer, not captured hand/voiceclone. OpenAI gpt-4.1-mini selects local20-family validated catalog inspired by Jev architecture; Jev API not used. No microphone/STT/speech interruption. 30/30 corrected final scientific/mechanical checks, not first-pass perfection. Every request JSON preserves raw modelAnswer for audit; displayed/spoken numerical facts are locally calculated canonical text. Warm MacStudio tailnet browser timings, not remoteQuest benchmark. Native H264 High limited420/AAC48k captions; captions approximate sentence alignment. Audio computationally reviewed, no human headphones review.
''';(p/'delivery-readme.txt').write_text(text)
body='<meta charset="utf-8"><title>30 live sketch tests</title><style>body{font:16px system-ui;background:#102431;color:white;max-width:1100px;margin:30px auto}video{width:100%}section{margin:40px 0}a{color:aquamarine}</style><h1>30 live sketch tests</h1><pre style="white-space:pre-wrap">'+html.escape(text)+'</pre><h2>Overview</h2><video controls src="ryo-primer-montage.mp4"><track kind="captions" src="montage.vtt" srclang="ja" default></video><h2>Actual live UI</h2><video controls src="walkthrough/live-interaction.mp4"><track kind="captions" src="walkthrough/live-interaction.vtt" srclang="en" default></video>'
for c in a['cases']:
 body+=f'<section><h2>{c["id"]:02} / {html.escape(c["slug"])}</h2><p>{html.escape(c["question"])}</p><video controls preload="none" poster="{c["prefix"]}.png" src="{c["prefix"]}.mp4"><track kind="captions" src="{c["prefix"]}.vtt" srclang="en" default></video></section>'
(p/'index.html').write_text(body);files.extend([(p/'delivery-readme.txt','README.txt'),(p/'index.html','index.html')]);z=p/'ryo-primer-30-demos.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=3)as f:
 for src,dst in files:f.write(src,dst)
with zipfile.ZipFile(z)as f:
 assert f.testzip()is None
 assert len([x for x in f.namelist()if x.endswith('.mp4')])==32
r={'file':str(z),'bytes':z.stat().st_size,'sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'entries':len(files),'caseVideos':30,'totalVideos':32,'crcPassed':True};(p/'package-receipt.json').write_text(json.dumps(r,indent=2));print(r)
