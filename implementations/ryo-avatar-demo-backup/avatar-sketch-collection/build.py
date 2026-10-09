from pathlib import Path
import json,hashlib,re,subprocess
p=Path(__file__).parent;o=Path('/path/to/local-assets');a=Path('/path/to/local-assets');b=Path('/path/to/local-assets');ha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();run=lambda args:subprocess.run(args,check=True)
inputs=[a/'avatar-sketch-worlds.mp4',b/'avatar-sketch-frontiers.mp4',a/'avatar-sketch-worlds-slack.mp4',b/'avatar-sketch-frontiers-slack.mp4'];sourceHashes={str(f):ha(f)for f in inputs}
def parse_stamp(s):
 h,m,t=s.split(':');return int(h)*3600000+int(m)*60000+round(float(t.replace(',','.'))*1000)
def stamp(n):return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
cues=[]
for folder,off in [(a,0),(b,128000)]:
 for block in (folder/'narration.srt').read_text().strip().split('\n\n'):
  rows=block.splitlines();times=rows[1].split(' --> ');start,end=[parse_stamp(t)+off for t in times];cues.append({'start':start,'end':end,'text':'\n'.join(rows[2:])})
assert all(0<=c['start']<c['end']<=272000 for c in cues);assert all(cues[i]['end']<=cues[i+1]['start']for i in range(len(cues)-1));assert cues[-1]['end']==272000
srt='\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}"for i,c in enumerate(cues))+'\n'
(o/'narration.srt').write_text(srt);(o/'narration.vtt').write_text('WEBVTT\n\n'+re.sub(r'(\d{2}:\d{2}:\d{2}),(\d{3})',r'\1.\2',srt));(o/'narration.txt').write_text('\n\n'.join(c['text']for c in cues));(p/'subtitle-cues.json').write_text(json.dumps(cues,indent=2))
chapters=[(0,28,'Pendulum / motion becomes waveform'),(28,62,'Fish / outline unfolds and swims'),(62,98,'Landscape / ridge, river and clouds'),(98,128,'Water / circles become H2O'),(128,164,'Dinosaur / outline becomes walking creature'),(164,200,'Attention / spatial heads and weights'),(200,236,'Gas / volume, temperature and pressure'),(236,272,'Body / schematic lungs and heart')]
(p/'chapters.json').write_text(json.dumps([{'start':s,'end':e,'title':t}for s,e,t in chapters],indent=2));(p/'chapters.ffmetadata').write_text(';FFMETADATA1\ntitle=Living Sketch Collection\n'+''.join(f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={s*1000}\nEND={e*1000}\ntitle={t}\n'for s,e,t in chapters))
voiceA=Path('/path/to/local-assets');voiceB=Path('/path/to/local-assets')
run(['ffmpeg','-y','-v','error','-i',str(voiceA),'-i',str(voiceB),'-filter_complex','[0:a][1:a]concat=n=2:v=0:a=1[a]','-map','[a]','-ar','48000','-ac','1','-c:a','pcm_s16le',str(o/'narration.wav')])
for suffix,ins,bitrate in [('master',inputs[:2],'192k'),('slack',inputs[2:],'128k')]:
 fl=p/f'concat-{suffix}.txt';fl.write_text(''.join(f"file '{f}'\nduration {dur}\n"for f,dur in zip(ins,[128,144])));dest=o/f'avatar-sketch-collection-{suffix}.mp4'
 run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(fl),'-i',str(o/'narration.wav'),'-i',str(o/'narration.srt'),'-i',str(p/'chapters.ffmetadata'),'-map','0:v:0','-map','1:a:0','-map','2:s:0','-map_metadata','3','-map_chapters','3','-c:v','copy','-c:a','aac','-b:a',bitrate,'-ar','48000','-c:s','mov_text','-metadata:s:s:0','language=eng','-t','272','-movflags','+faststart',str(dest)])
 run(['ffmpeg','-v','error','-i',str(dest),'-f','null','-']);probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-show_chapters','-of','json',str(dest)]));(o/f'ffprobe-{suffix}.json').write_text(json.dumps(probe,indent=2));vs=next(s for s in probe['streams']if s['codec_type']=='video');avs=next(s for s in probe['streams']if s['codec_type']=='audio');sub=next(s for s in probe['streams']if s['codec_type']=='subtitle');assert vs['nb_frames']=='8160'and vs['r_frame_rate']=='30/1'and float(vs['duration'])==272;assert max(float(s['duration'])for s in [vs,avs,sub])-min(float(s['duration'])for s in [vs,avs,sub])<=.1;assert len(probe['chapters'])==8
 dumped=subprocess.check_output(['ffmpeg','-v','error','-i',str(dest),'-map','0:s:0','-f','srt','-']).decode();clean=lambda s:re.sub(r'\s+',' ',s.strip());assert clean(dumped)==clean(srt)
 assert dest.read_bytes().index(b'moov')<dest.read_bytes().index(b'mdat')
 print('VERIFIED',suffix,dest.stat().st_size,flush=True)
assert (o/'avatar-sketch-collection-slack.mp4').stat().st_size<=16000000
for f,h in sourceHashes.items():assert ha(Path(f))==h
manifest={'duration':272,'fps':30,'frameCount':8160,'chapters':json.loads((p/'chapters.json').read_text()),'sourceHashes':sourceHashes,'sourcesPreserved':True,'video':'stream copied original scenes; no regenerated footage','voice':'existing neural speech PCM concatenated exactly128+144s; encoded AAC once; no API calls','subtitles':{'offsetSecondMs':128000,'count':len(cues),'embeddedParity':True,'endMs':272000},'qa':{'fullDecode':'both final files passed','streamDurationDriftMs':0,'chaptersEmbedded':8,'sourceFramesIdentity':'pending decoded frame comparison','joinVisualReview':'pending'},'files':{f.name:{'path':str(f),'bytes':f.stat().st_size,'sha256':ha(f)}for f in [o/'avatar-sketch-collection-master.mp4',o/'avatar-sketch-collection-slack.mp4']},'boundaries':['Eight authored sketch transformations, not Chalktalk full parity or arbitrary recognition','Illustrative attention, ideal gas and body symbols retain source disclaimers','Avatar hand/rig/occlusion limits inherited','Live AI Q&A is a separate delivered application, not this compilation']}
(o/'delivery-manifest.json').write_text(json.dumps(manifest,indent=2));(p/'delivery-manifest.json').write_text(json.dumps(manifest,indent=2))
