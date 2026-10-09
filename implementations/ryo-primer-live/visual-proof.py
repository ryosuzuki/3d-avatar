from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
p=Path('/path/to/local-assets');o=p/'montage-visual-proof';o.mkdir(exist_ok=True)
for page in range(5):
 sheet=Image.new('RGB',(1440,900),(10,20,28));d=ImageDraw.Draw(sheet)
 for i in range(6):
  n=page*6+i+1
  for j,t in enumerate([.2,2,3.7]):
   f=o/f'{n:02}-{j}.jpg';subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(p/f'montage-part-{n:02}.mp4'),'-frames:v','1','-y',str(f)],check=True)
   im=Image.open(f);im.thumbnail((480,135));x=j*480;y=i*150;sheet.paste(im,(x,y));d.text((x+5,y+135),f'Case {n:02} / {t}s',fill='white')
 sheet.save(o/f'sheet-{page+1}.jpg')
