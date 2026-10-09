from pathlib import Path
import json,subprocess,hashlib,re,textwrap
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent;OUT=Path('/path/to/local-assets');ids=['e39766449057','38a2a34b89d2','89ce7746c953']
ass='''[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 900
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Arial,23,&H00FFFFFF,&H00FFFFFF,&H001A2F3E,&H001A2F3E,0,0,0,0,100,100,0,0,1,1,0,2,45,45,67,1
Style: Limit,Arial,15,&H00BECED6,&H00BECED6,&H001A2F3E,&H001A2F3E,0,0,0,0,100,100,0,0,1,0,0,2,45,45,22,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
def stamp(t,ass=False):
 h=int(t//3600);m=int(t%3600//60);s=t%60
 return f'{h}:{m:02d}:{s:05.2f}'if ass else f'{h:02d}:{m:02d}:{int(s):02d},{round((s%1)*1000):03d}'
offset=0;cues=[];manifest=[]
for ident in ids:
 r=json.loads((ROOT/'generated'/f'{ident}.json').read_text());duration=float(json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_format','-of','json',str(OUT/f'{ident}-narrated.mp4')]))['format']['duration'])
 for c in r['captionCues']:
  a=offset+c['start'];b=offset+c['end'];cues.append({'start':a,'end':b,'text':c['text']});ass+=f"Dialogue: 0,{stamp(a,True)},{stamp(b,True)},Caption,,0,0,0,,{c['text']}\n"
 label='OpenAI-generated scene schema · procedural illustration · same projected strokes unfold into volume · schematic movement'
 ass+=f'Dialogue: 1,{stamp(offset,True)},{stamp(offset+duration,True)},Limit,,0,0,0,,{label}\n';manifest.append({'id':ident,'start':offset,'duration':duration,'question':r['question'],'title':r['scene']['title'],'audioQA':r['audioQA']});offset+=duration
cues[-1]['end']=offset
(OUT/'narration.ass').write_text(ass);(OUT/'narration.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}"for i,c in enumerate(cues))+'\n');(OUT/'narration.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f"{stamp(c['start']).replace(',', '.')} --> {stamp(c['end']).replace(',', '.')}\n{c['text']}"for c in cues)+'\n');(OUT/'narration.txt').write_text('\n\n'.join(json.loads((ROOT/'generated'/f'{ident}.json').read_text())['scene']['answer']for ident in ids)+'\n')
master=OUT/'generated-schema-proof-film.mp4';final=OUT/'generated-schema-verified-film.mp4'
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',23);small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',15);captionFiles=[]
for i,cue in enumerate(cues):
 img=Image.new('RGB',(1280,170),(16,39,55));draw=ImageDraw.Draw(img);lines=[];line=''
 for word in cue['text'].split():
  candidate=(line+' '+word).strip()
  if draw.textlength(candidate,font=font)>1180 and line:lines.append(line);line=word
  else:line=candidate
 if line:lines.append(line)
 y=42-(len(lines)-1)*14
 for line in lines:draw.text((640,y),line,font=font,fill=(240,255,250),anchor='mt');y+=29
 draw.text((640,142),'Generated scene schema · procedural illustration · same strokes unfold into volume · schematic movement',font=small,fill=(184,204,214),anchor='mt');f=OUT/f'caption-{i:02d}.png';img.save(f);captionFiles.append(f)
args=['ffmpeg','-y','-v','error','-i',str(master)]
for f in captionFiles:args+=['-i',str(f)]
args+=['-i',str(OUT/'narration.srt')];filters=['[0:v]drawbox=x=0:y=730:w=iw:h=170:color=0x102737:t=fill[v0]']
for i,cue in enumerate(cues):
 start=0 if i==0 else cue['start'];end=cues[i+1]['start'] if i+1<len(cues) else offset
 filters.append(f"[v{i}][{i+1}:v]overlay=0:730:enable='between(t,{start},{end})'[v{i+1}]")
args+=['-filter_complex',';'.join(filters),'-map',f'[v{len(cues)}]','-map','0:a','-map',f'{len(captionFiles)+1}:0','-c:v','libx264','-preset','fast','-crf','19','-af','loudnorm=I=-16:TP=-2.2:LRA=11','-c:a','aac','-ar','48000','-b:a','192k','-c:s','mov_text','-metadata:s:s:0','language=eng','-movflags','+faststart',str(final)];subprocess.run(args,check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(final),'-f','null','-'],check=True);probe=json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_streams','-show_format','-of','json',str(final)]));(OUT/'film-ffprobe.json').write_text(json.dumps(probe,indent=2));(OUT/'film-manifest.json').write_text(json.dumps({'segments':manifest,'file':str(final),'bytes':final.stat().st_size,'sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'duration':offset,'subtitleCues':len(cues),'captionAlignment':'Authoritative narration text aligned to complete Whisper word timestamps; exact spoken last words included','visualReview':'Source scene screenshots and actual fish film frame inspected; final transition probes pending','perceptualAudioReview':'Not yet performed','mechanicalDecode':'pass'},indent=2));print(final)
