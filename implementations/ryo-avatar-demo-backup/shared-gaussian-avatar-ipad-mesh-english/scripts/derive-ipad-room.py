from pathlib import Path
import numpy as np,shutil,json
p=Path('/path/to/local-assets');o=Path('/path/to/local-assets');v=[];uv=[];f=[]
for line in (p/'textured_output.obj').open():
 a=line.split()
 if not a:continue
 if a[0]=='v':v.append(list(map(float,a[1:4])))
 if a[0]=='vt':uv.append(list(map(float,a[1:3])))
 if a[0]=='f':f.extend([list(map(int,x.split('/')[:2])) for x in a[1:]])
f=np.array(f)-1;v=np.array(v,dtype='<f4')[f[:,0]];uv=np.array(uv,dtype='<f4')[f[:,1]];np.column_stack([v,uv]).astype('<f4').tofile(o/'ipad-mesh.bin');shutil.copy(p/'textured_output.jpg',o/'ipad-mesh.jpg');print('vertices',len(v))
