import gzip,struct,numpy as np,pathlib,json,shutil
root=pathlib.Path('/path/to/local-assets');src=pathlib.Path('/path/to/local-assets');d=gzip.open(src,'rb').read();magic,ver,n,deg,bits,flags,_=struct.unpack('<III4B',d[:16]);offset=16
def take(count):
 global offset
 a=np.frombuffer(d,dtype=np.uint8,count=count,offset=offset).copy();offset+=count;return a
p=take(n*9).reshape(n,3,3).astype(np.int32);p=p[:,:,0]+(p[:,:,1]<<8)+(p[:,:,2]<<16);p=np.where(p&0x800000,p-0x1000000,p)/2**bits
alpha=np.clip(take(n)/255.,1e-6,1-1e-6);dc=(take(n*3).reshape(n,3)/255.-.5)/.15;scale=take(n*3).reshape(n,3)/16.-10
r=take(n*4).copy().view('<u4');big=r>>30;q=np.zeros((n,4));
for i in range(3,-1,-1):
 m=big!=i;c=r[m];q[m,i]=(c&511)/511*np.sqrt(.5)*np.where((c>>9)&1,-1,1);r[m]>>=10
q[np.arange(n),big]=np.sqrt(np.maximum(0,1-(q*q).sum(1)))
sh=(take(n*45).reshape(n,15,3).astype(float)-128)/128
print('percentiles',np.percentile(p,[1,5,25,50,75,95,99],axis=0))
# RY90 and translate source into presentation scene, original all splats preserved.
p=np.stack([p[:,2],p[:,1]+.80,-p[:,0]],axis=1)
# quaternion product [0,s,0,s] * [x,y,z,w]
s=np.sqrt(.5);x,y,z,w=q.T;q=np.stack([s*(x+z),s*(y+w),s*(z-x),s*(w-y)],1)
# DC-only presentation derivative, original SH3 SPZ retained. No geometry decimation.
a=np.column_stack([p,np.zeros((n,3)),dc,np.log(alpha/(1-alpha)),scale,q[:,[3,0,1,2]]]).astype('<f4')
names=['x','y','z','nx','ny','nz','f_dc_0','f_dc_1','f_dc_2','opacity','scale_0','scale_1','scale_2','rot_0','rot_1','rot_2','rot_3']
h=('ply\nformat binary_little_endian 1.0\nelement vertex '+str(n)+'\n'+''.join('property float '+k+'\n' for k in names)+'end_header\n').encode();(root/'assets/ipad-room.ply').write_bytes(h+a.tobytes());shutil.copy(src,root/'assets/original-room.spz')
