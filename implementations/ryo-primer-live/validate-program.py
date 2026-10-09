from pathlib import Path
import os,json,subprocess,hashlib,re
R=Path(os.environ['PRIMER_OUT']);p=R/'ryo-primer-montage.mp4';m=json.loads((R/'montage-manifest.json').read_text());s=m['probe']['streams'];v=next(x for x in s if x['codec_type']=='video');a=next(x for x in s if x['codec_type']=='audio');sub=next(x for x in s if x['codec_type']=='subtitle');duration=float(v['duration']);drift=abs(duration-float(a['duration']));assert drift<=.1 and v['r_frame_rate']=='30/1' and a['sample_rate']=='48000' and v['pix_fmt']=='yuv420p'
def secs(st):
 h,mi,s=st.replace(',','.').split(':');return int(h)*3600+int(mi)*60+float(s)
cues=re.findall(r'(\d\d:\d\d:\d\d,\d{3}) --> (\d\d:\d\d:\d\d,\d{3})\n(.+)',(R/'montage.srt').read_text());last=0
for start,end,text in cues:
 start,end=secs(start),secs(end);assert last<=start<=end<=duration+.1;last=end
embedded=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:s:0','-f','srt','-']).decode();et=re.findall(r'--> [^\n]+\n(.+)',embedded);assert [x[2] for x in cues]==et
meter=subprocess.run(['ffmpeg','-hide_banner','-i',str(p),'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True,check=True).stderr;summary=meter[meter.rfind('Summary:'):];lufs=float(re.search(r'I:\s*(-?[\d.]+) LUFS',summary)[1]);peak=float(re.search(r'Peak:\s*(-?[\d.]+) dBFS',summary)[1]);assert -17<=lufs<=-15 and peak<=-1.5;assert abs(duration-last)<=.1
(R/'montage-loudness.txt').write_text(summary);atoms=[]
with p.open('rb') as f:
 while b:=f.read(8):
  if len(b)<8:break
  size=int.from_bytes(b[:4],'big');name=b[4:].decode('ascii','replace');atoms.append(name)
  if size==1:size=int.from_bytes(f.read(8),'big');f.seek(size-16,1)
  elif size>=8:f.seek(size-8,1)
  else:break
assert atoms.index('moov')<atoms.index('mdat');receipts={'fullDecodePassed':m['fullDecodePassed'],'avDriftSeconds':drift,'subtitleEndDriftSeconds':duration-last,'subtitleCueCount':len(cues),'subtitleTextParity':True,'subtitleNonOverlapAndBounds':True,'moovBeforeMdat':True,'profile':v['profile'],'loudnessSummary':meter[meter.rfind('Summary:'):],'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};(R/'montage-qa.json').write_text(json.dumps(receipts,indent=2));print(json.dumps(receipts,indent=2))
