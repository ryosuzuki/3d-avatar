"""Bake neural colors onto original Gaussians; export a clearly labeled static mesh proxy."""
from pathlib import Path
import json,struct
import numpy as np
from PIL import Image
from scipy.ndimage import minimum_filter,gaussian_filter,binary_fill_holes,binary_closing,label
from scipy.spatial import cKDTree
from skimage.measure import marching_cubes
import trimesh
def export(r):
    blob=(r/'avatar-raw.ply').read_bytes();end=blob.index(b'end_header\n')+11;header=blob[:end];props=[x.split()[-1] for x in header.decode().splitlines() if x.startswith('property')];v=np.frombuffer(blob[end:],dtype=[(x,'<f4') for x in props]).copy();n=len(v)
    meta=json.loads((r/'posed/projection.json').read_text());oh,ow=meta['ori_size'];sums=np.zeros((n,3));weights=np.zeros(n)
    for i in range(6):
        d=np.load(r/f'posed/frame-{i:05}.npz');xyz=d['xyz'];intr=d['intrinsic'];h,w=int(d['height']),int(d['width']);sx,sy,ox,oy=meta['offsets'][i];im=np.array(Image.open(r/f'view-{i+1:02}.png').convert('RGB'));ih,iw=im.shape[:2];z=xyz[:,2];u=intr[0,0]*xyz[:,0]/z+intr[0,2];vv=intr[1,1]*xyz[:,1]/z+intr[1,2];ui=np.rint(u).astype(int);vi=np.rint(vv).astype(int);valid=(z>.01)&(ui>=0)&(ui<w)&(vi>=0)&(vi<h);depth=np.full((h,w),np.inf);np.minimum.at(depth,(vi[valid],ui[valid]),z[valid]);depth=minimum_filter(depth,size=3);delta=np.full(n,np.inf);delta[valid]=z[valid]-depth[vi[valid],ui[valid]];weight=np.clip(1-np.maximum(delta,0)/.025,0,1);x=np.rint((u/sx+ox)*iw/ow).astype(int);y=np.rint((vv/sy+oy)*ih/oh).astype(int);good=valid&(weight>0)&(x>=0)&(x<iw)&(y>=0)&(y<ih);inside=np.where(good)[0];good[inside]&=(im[y[inside],x[inside]].min(1)<251);sums[good]+=im[y[good],x[good]]*weight[good,None];weights[good]+=weight[good]
    xyz=np.column_stack([v[x] for x in ['x','y','z']]);known=weights>0
    if not known.any():raise ValueError('Color projection did not cover the generated avatar')
    colors=sums/np.maximum(weights[:,None],1e-8);fill_distance=np.zeros(n)
    if (~known).any():
        fill_distance[~known],near=cKDTree(xyz[known]).query(xyz[~known]);colors[~known]=colors[known][near]
    colors=np.clip(colors/255,0,1)
    for i in range(3):v[f'f_dc_{i}']=(colors[:,i]-.5)/.28209479177387814
    # Filter unsupported background lobes after neural color projection.
    # Standard .splat, compatible with common Gaussian viewers (not a triangle mesh).
    scales=np.exp(np.column_stack([v[f'scale_{i}'] for i in range(3)]));q=np.column_stack([v[f'rot_{i}'] for i in range(4)]);q/=np.maximum(np.linalg.norm(q,axis=1)[:,None],1e-8);alpha=1/(1+np.exp(-np.clip(v['opacity'],-80,80)))
    out=np.empty(n,dtype=[('position','<f4',3),('scale','<f4',3),('rgba','u1',4),('rotation','u1',4)]);out['position']=xyz;out['scale']=scales;out['rgba']=(np.column_stack([colors,alpha])*255).astype('u1');out['rotation']=np.clip(q*128+128,0,255).astype('u1');export_keep=(alpha>.012)&(fill_distance<.045);export_header=header.replace(f'element vertex {n}'.encode(),f'element vertex {int(export_keep.sum())}'.encode());(r/'avatar.ply').write_bytes(export_header+v[export_keep].tobytes());(r/'avatar.splat').write_bytes(out[export_keep].tobytes())
    # Occupancy surface is deliberately a static approximation, not neural rigging.
    keep=export_keep&np.isfinite(xyz).all(1);points=xyz[keep];lo=np.percentile(points,0.1,axis=0)-.04;hi=np.percentile(points,99.9,axis=0)+.04;step=float(max(hi-lo)/144);grid_shape=np.ceil((hi-lo)/step).astype(int)+1;grid=np.zeros(grid_shape,dtype='float32');ix=np.rint((points-lo)/step).astype(int);ix=np.minimum(np.maximum(ix,0),grid_shape-1);np.maximum.at(grid,tuple(ix.T),1);grid=gaussian_filter(grid,1.25);grid=binary_fill_holes(binary_closing(grid>.025,iterations=2));components,count=label(grid);sizes=np.bincount(components.ravel());sizes[0]=0;grid=components==sizes.argmax();vertices,faces,_,_=marching_cubes(grid.astype('float32'),.5,spacing=(step,)*3);vertices+=lo
    _,near=cKDTree(xyz).query(vertices);vc=(colors[near]*255).astype('uint8');vertices[:,1]-=vertices[:,1].min();mesh=trimesh.Trimesh(vertices=vertices,faces=faces,vertex_colors=vc,process=False);mesh.fix_normals();trimesh.smoothing.filter_taubin(mesh,lamb=.45,nu=.5,iterations=12);assert mesh.is_watertight and mesh.volume>0, 'Static proxy must be a closed, outward-facing surface';mesh.export(r/'avatar-static.glb');mesh.export(r/'avatar-static.ply');(r/'avatar-static.obj').write_text(trimesh.exchange.obj.export_obj(mesh,include_color=True))
    # Real UV texture for OBJ/Mixamo (OBJ vertex colors are not portable there).
    import xatlas, zipfile
    from PIL import ImageDraw,ImageFilter
    mapping,indices,uv=xatlas.parametrize(np.asarray(mesh.vertices,dtype=np.float32),np.asarray(mesh.faces,dtype=np.uint32))
    textured_vertices=mesh.vertices[mapping];textured_colors=vc[mapping]
    texture=Image.new('RGB',(2048,2048),(180,180,180));draw=ImageDraw.Draw(texture)
    tex_uv=np.column_stack([uv[:,0]*2047,(1-uv[:,1])*2047])
    for tri in indices:
        xy=[tuple(p) for p in tex_uv[tri]];color=tuple(np.mean(textured_colors[tri],axis=0).astype(int))
        draw.polygon(xy,fill=color);draw.line(xy+[xy[0]],fill=color,width=2)
    texture.save(r/'avatar-texture.png')
    material=trimesh.visual.material.SimpleMaterial(image=texture,diffuse=[255,255,255,255])
    textured=trimesh.Trimesh(vertices=textured_vertices,faces=indices,visual=trimesh.visual.texture.TextureVisuals(uv=uv,material=material),process=False)
    textured.export(r/'avatar-static.glb')
    # Keep geometric vertices welded across UV seams. OBJ has independent v/vt indices.
    welded_vertices, uv_to_vertex=np.unique(textured_vertices,axis=0,return_inverse=True)
    with (r/'avatar-textured.obj').open('w') as f:
        f.write('mtllib avatar-textured.mtl\nusemtl AvatarTexture\n')
        for vtx in welded_vertices:f.write('v %.7f %.7f %.7f\n'%tuple(vtx))
        for coord in uv:f.write('vt %.7f %.7f\n'%tuple(coord))
        for tri in indices:f.write('f '+' '.join(f'{int(uv_to_vertex[i])+1}/{int(i)+1}' for i in tri)+'\n')
    (r/'avatar-textured.mtl').write_text('newmtl AvatarTexture\nKa 1 1 1\nKd 1 1 1\nKs 0 0 0\nd 1\nillum 1\nmap_Kd avatar-texture.png\n')
    with zipfile.ZipFile(r/'mixamo-avatar.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
        for name in ['avatar-textured.obj','avatar-textured.mtl','avatar-texture.png']:z.write(r/name,name)
    return dict(gaussians=int(export_keep.sum()),reconstructed_gaussians=n,color_coverage=int(known.sum()),mesh_vertices=len(vertices),mesh_faces=len(faces),mesh_height=float(np.ptp(vertices[:,1])),uv_texture=True,texture_size=2048,limits=['Unobserved regions are inferred from the provided reference images.','Gaussian colors are baked from six neural views; neural preview can look sharper.','GLB/OBJ are static occupancy-mesh proxies, not skinned characters.','Uploaded video supplies appearance only, not captured motion.'])
