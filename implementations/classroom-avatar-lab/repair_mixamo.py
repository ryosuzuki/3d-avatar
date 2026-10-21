"""Weld OBJ geometry without welding its independently indexed UV coordinates."""
from pathlib import Path
from collections import Counter
import argparse, zipfile

def weld_obj(text):
    lines=text.splitlines();vertices=[];unique={};remap=[]
    for line in lines:
        if line.startswith('v '):
            point=tuple(map(float,line.split()[1:]))
            if point not in unique: unique[point]=len(vertices)+1;vertices.append(line)
            remap.append(unique[point])
    output=['# Welded geometry; independent UV seam indices retained']+vertices
    faces=[]
    for line in lines:
        if line.startswith('v '):continue
        if line.startswith('f '):
            parts=[part.split('/') for part in line.split()[1:]]
            for part in parts:part[0]=str(remap[int(part[0])-1])
            faces.append([int(part[0]) for part in parts])
            line='f '+' '.join('/'.join(part) for part in parts)
        output.append(line)
    edges=Counter(tuple(sorted((face[i],face[(i+1)%len(face)]))) for face in faces for i in range(len(face)))
    if any(n!=2 for n in edges.values()):raise ValueError('Mesh has open or non-manifold edges')
    if any(len(set(face))!=len(face) for face in faces):raise ValueError('Degenerate face')
    return '\n'.join(output)+'\n',{'vertices':len(vertices),'faces':len(faces),'boundary_edges':0}

def repair(folder):
    obj=folder/'avatar-textured.obj';text,report=weld_obj(obj.read_text())
    temp=obj.with_suffix('.obj.tmp');temp.write_text(text);temp.replace(obj)
    archive=folder/'mixamo-avatar.zip';temp=archive.with_suffix('.zip.tmp')
    with zipfile.ZipFile(temp,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for name in ('avatar-textured.obj','avatar-textured.mtl','avatar-texture.png'):z.write(folder/name,name)
    with zipfile.ZipFile(temp) as z:assert z.testzip() is None
    temp.replace(archive)
    return report
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path);args=parser.parse_args();print(repair(args.folder))
