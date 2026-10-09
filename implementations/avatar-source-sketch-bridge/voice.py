from pathlib import Path
import urllib.request,json,subprocess,math
R=Path(__file__).parent;A=R/'audio';A.mkdir(exist_ok=True)
S={'fish':[
'These are the actual supplied vector strokes. The presenter traces their outline and details, instead of reconstructing lines from a mesh.',
'This actual diffusion image is the next intermediate.',
'Hunyuan predicts the volume from that image, including unobserved surfaces. The inference output is preserved; a declared lighter mesh supports this display.',
'The original drawing remains as a faint reference while the volume turns. Registration is uniform and approximate: the learned contour can differ. This shape has real depth, but its gentle swimming is authored, not an anatomical rig.'],
'owl':[
'The same renderer now traces the actual supplied owl paths, including the eyes, wings, and feathers. These strokes existed before neural image or shape generation.',
'Again, the conditioned image is a real intermediate.',
'Tripo S R is a different learned model. Its predicted mesh includes a rounded body and unobserved surfaces, not just a symmetric inflation of the drawing.',
'The camera reveals that volume, while a few silhouette contours keep it readable. We do not draw every triangle. Neither model guarantees anatomy or exact sketch fidelity. The common pipeline preserves the source drawing, inference provenance, and separate display registration.']}
key=__import__('os').environ['OPENAI_API_KEY'];all=[]
for name,parts in S.items():
 durations=[]
 for i,text in enumerate(parts):
  req=urllib.request.Request('https://api.openai.com/v1/audio/speech',data=json.dumps({'model':'gpt-4o-mini-tts','voice':'shimmer','input':text,'response_format':'mp3','instructions':'Natural conversational educational English. Clear moderately brisk pacing; avoid dramatic long pauses. Pronounce Tripo S R as Try-po ess arr.'}).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
  with urllib.request.urlopen(req,timeout=120) as resp:(A/f'{name}-{i}.mp3').write_bytes(resp.read())
  subprocess.run(['ffmpeg','-y','-v','error','-i',str(A/f'{name}-{i}.mp3'),'-ar','48000','-c:a','pcm_s16le',str(A/f'{name}-{i}.wav')],check=True)
  duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(A/f'{name}-{i}.wav')]));durations.append(duration)
 (A/f'{name}-concat.txt').write_text('\n'.join(f"file '{A}/{name}-{i}.wav'" for i in range(4)));subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(A/f'{name}-concat.txt'),'-c:a','pcm_s16le',str(A/f'{name}.wav')],check=True)
 data=json.loads((R/'data'/f'{name}.json').read_text());ends=[];c=0
 for duration in durations:c+=duration;ends.append(c)
 data['cueTimes']={'drawEnd':ends[0],'imageEnd':ends[1],'morphEnd':ends[1]+min(5,durations[2]),'turnStart':ends[2],'duration':ends[3]};data['captions']=parts;(R/'data'/f'{name}.json').write_text(json.dumps(data,separators=(',',':')));all.append({'name':name,'parts':parts,'durations':durations,'cueTimes':data['cueTimes']})
(R/'narration.json').write_text(json.dumps(all,indent=2));del key;print(all)
