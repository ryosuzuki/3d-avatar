from pathlib import Path
import sys,json,hashlib
from PIL import Image
import numpy as np
from rembg import remove,new_session
src=Path(sys.argv[1]);dst=Path(sys.argv[2]);weight=Path.home()/'.rembg/models/u2netp/u2netp.onnx'
assert weight.exists(),'Existing U2NetP weight required; no downloads allowed'
im=Image.open(src).convert('RGB');out=remove(im,session=new_session('u2netp'));a=np.asarray(out.getchannel('A'));yy,xx=np.where(a>16)
assert len(xx)>100,'Empty learned foreground'
bbox=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)];crop=out.crop(bbox);side=int(max(crop.size)*1.3);canvas=Image.new('RGBA',(side,side));canvas.paste(crop,((side-crop.width)//2,(side-crop.height)//2));canvas.resize((512,512),Image.Resampling.LANCZOS).save(dst)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
dst.with_suffix('.receipt.json').write_text(json.dumps({'method':'cached U2NetP foreground alpha, crop and 15percent square padding','checkpointSHA256':sha(weight),'sourceSHA256':sha(src),'outputSHA256':sha(dst),'bbox':bbox},indent=2))
