from pathlib import Path
import json,urllib.request
root=Path(__file__).parent
scripts={
'fish':'Start with one rough closed fish outline. The same boundary stays in place as its interior gains depth. This is a real mesh, not a flat cutout. Swimming is only an illustrative deformation.',
'octopus':'Now use the same operation on a many armed silhouette. There is no octopus category or model lookup. Distance from the boundary controls the surface thickness. Concave outlines also become a closed volume.',
'leaf':'A leaf follows exactly the same pipeline. Its outline becomes a softly inflated surface. Sparse contour bands and camera movement reveal the depth, without hiding the shape under every triangle edge.',
'unseen':'Finally, try a new asymmetric shape with no category name. The original corners remain, and the interior inflates. This works for simple closed silhouettes, but does not infer hidden anatomy or articulated parts.'}
key=__import__('os').environ['OPENAI_API_KEY']
for name,text in scripts.items():
 req=urllib.request.Request('https://api.openai.com/v1/audio/speech',data=json.dumps({'model':'gpt-4o-mini-tts','voice':'shimmer','input':text,'response_format':'mp3','instructions':'Warm conversational English, moderately brisk educational narration.'}).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=120) as r:(root/'meshes'/f'{name}.mp3').write_bytes(r.read())
(root/'narration.json').write_text(json.dumps(scripts,indent=2));del key
