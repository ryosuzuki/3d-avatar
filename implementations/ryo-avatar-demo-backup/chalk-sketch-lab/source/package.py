import pathlib,json,hashlib,zipfile,subprocess
p=pathlib.Path('/path/to/local-assets');o=pathlib.Path('/path/to/local-assets')
with zipfile.ZipFile(o/'chalk-sketch-lab.zip','w',zipfile.ZIP_DEFLATED) as z:
 for name in ['index.html','app.js','README.md','capture.mjs','package.py','playback.mjs']:
  z.write(p/name,'chalk-sketch-lab/'+name)
files=['chalk-sketch-demo-tv.mp4','chalk-sketch-lab.zip','screenshot.png','interaction-proof.json']
manifest={'project':str(p),'output':str(o),'local_url':'http://127.0.0.1:8766','video':{'duration':60,'language':'English captions','audio':'none, caption-led demo','method':'actual managed-browser pointer input capture, 30fps'},'scope':'arbitrary captured stroke, explicit semantic confirmation, shape+angle ports, Y rotation matrix, vertex propagation, disconnect holds geometry, undo/reset','limitations':['screen-space orthographic 3D, not tracked AR','pre-existing view and control nodes; arbitrary glyph recognition not implemented','no live AI','room/avatar omitted to keep sketch computation legible; original assets retained untouched'],'references':['https://github.com/kenperlin/chalktalk','https://www.youtube.com/watch?v=ZZi3I_NCiUk&t=322','https://x.com/HCI_Research/status/1251898938967207937'],'files':{}}
for name in files:
 b=(o/name).read_bytes();manifest['files'][name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(o/'manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(manifest['files'],indent=2))
