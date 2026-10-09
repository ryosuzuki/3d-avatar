from pathlib import Path
import zipfile,json,hashlib
R=Path(__file__).parent;O=Path('/path/to/local-assets');files=[]
for p in R.rglob('*'):
 rel=p.relative_to(R)
 if any(x in rel.parts for x in ['.git','node_modules','__pycache__','.venv']) or p.is_symlink() or not p.is_file() or p.suffix=='.mp4' or p.name=='.execution.log' or p.name.startswith('.state-'):continue
 files.append((p,rel))
with zipfile.ZipFile(O/'avatar-generalized-sketch-v2-project.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p,rel in files:z.write(p,'avatar-generalized-sketch-v2/'+str(rel))
manifest={'files':[{ 'path':str(rel),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p,rel in files],'requiredBinaryBackupIncluded':True,'includedOriginalGaussianAssets':True,'includedRawGLBs':True,'dependenciesExcluded':True,'secretStoreExcluded':True}
(O/'portable-project-hashes.json').write_text(json.dumps(manifest,indent=2));print(len(files), 'files', (O/'avatar-generalized-sketch-v2-project.zip').stat().st_size,'bytes')
