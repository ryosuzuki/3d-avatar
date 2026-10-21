"""Bounded, isolated classroom LHM++ inference. Never changes the shared model source."""
import os, sys, json, math, runpy, time, argparse, shutil, subprocess
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('job',type=Path); p.add_argument('--frame',type=float,default=0); p.add_argument('--views',type=int,choices=[1,8],default=1); p.add_argument('--end',type=float,default=8); a=p.parse_args()
os.umask(0o077)
r=a.job.resolve(); runtime=Path(os.environ.get('AVATAR_RUNTIME',str(Path.home()/'gpu-lab/video2mr-person-20261015')))
os.environ.update(CUDA_HOME=os.environ.get('CUDA_HOME',str(runtime/'compiler')),TORCH_CUDA_ARCH_LIST=os.environ.get('TORCH_CUDA_ARCH_LIST','8.9'),OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='4',PYTORCH_CUDA_ALLOC_CONF='max_split_size_mb:128',VIDEO2MR_RAW_GS_PATH=str(r/'avatar-raw.ply'),VIDEO2MR_EXPORT_POSED=str(r/'posed'),VIDEO2MR_EXPORT_STRIDE='1')
os.chdir(runtime/'source');sys.path.insert(0,str(runtime/'source'))
import numpy as np, torch, imageio_ffmpeg
from PIL import Image,ImageOps
from scipy.spatial.transform import Rotation
start=time.monotonic();r.mkdir(exist_ok=True);(r/'inputs').mkdir(exist_ok=True)
torch.cuda.set_per_process_memory_fraction((12.5 if a.views==8 else 8.5)*1024**3/torch.cuda.get_device_properties(0).total_memory)
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
source=r/'upload';source_is_image=False
try:
    im=Image.open(source); source_is_image=True; im=ImageOps.exif_transpose(im).convert('RGB'); im.thumbnail((1536,1536));im.save(r/'selected-frame.png')
except Exception:
    subprocess.run([ffmpeg,'-nostdin','-v','error','-ss',str(a.frame),'-i',str(source),'-frames:v','1','-vf','scale=1024:1024:force_original_aspect_ratio=decrease','-y',str(r/'selected-frame.png')],check=True,timeout=60)
if a.views==8:
    if source_is_image:raise ValueError('8-view mode requires a turn-around video, not a photo.')
    probe=imageio_ffmpeg.read_frames(str(source));metadata=next(probe);probe.close()
    duration=float(metadata.get('duration',0));fps=float(metadata.get('fps',30))
    if duration>0:a.end=min(a.end,duration-max(.05,1/max(fps,1)))
    if a.end<=a.frame:raise ValueError('The turn-around end must be after the start and before the video ends.')
from rembg import remove, new_session
matte_session=new_session('u2net_human_seg')
im=Image.open(r/'selected-frame.png').convert('RGB'); rgba=remove(im,session=matte_session)
bbox=rgba.getchannel('A').getbbox()
if not bbox:raise ValueError('No person found. Use a clear full-body photograph or frame.')
rgba=rgba.crop(bbox); canvas=Image.new('RGBA',(int(rgba.width*1.15),int(rgba.height*1.08)),(255,255,255,0));canvas.alpha_composite(rgba,((canvas.width-rgba.width)//2,(canvas.height-rgba.height)//2));background=Image.new('RGB',canvas.size,'white');background.paste(canvas,mask=canvas.getchannel('A'));background.save(r/'inputs/front.png')
refs=1
if a.views==8:
    for idx,t in enumerate(np.linspace(a.frame,a.end,8)[1:],1):
        raw=r/f'reference-{idx:02}.png'
        subprocess.run([ffmpeg,'-nostdin','-v','error','-ss',str(float(t)),'-i',str(source),'-frames:v','1','-y',str(raw)],check=True,timeout=60)
        ref=remove(Image.open(raw).convert('RGB'),session=matte_session); box=ref.getchannel('A').getbbox()
        if not box: raise ValueError('No person found in a multi-view frame.')
        ref=ref.crop(box); bg=Image.new('RGB',(int(ref.width*1.15),int(ref.height*1.08)),'white');bg.paste(ref,((bg.width-ref.width)//2,(bg.height-ref.height)//2),ref.getchannel('A'));bg.save(r/f'inputs/reference-{idx:02}.png')
    refs=8
for image_path in (r/'inputs').glob('*.png'):
    ref=Image.open(image_path).convert('RGB');ref=ImageOps.contain(ref,(504,840),Image.Resampling.LANCZOS);bg=Image.new('RGB',(504,840),'white');bg.paste(ref,((504-ref.width)//2,(840-ref.height)//2));bg.save(image_path)
motion=r/'turntable';(motion/'smplx_params').mkdir(parents=True,exist_ok=True);(motion/'samurai_seg').mkdir(exist_ok=True);(motion/'bbox').mkdir(exist_ok=True)
for i in range(6):
    pose=dict(root_pose=Rotation.from_euler('xyz',[math.pi,0,2*math.pi*i/6]).as_rotvec().tolist(),body_pose=[[0.,0.,0.] for _ in range(21)],jaw_pose=[0,0,0],leye_pose=[0,0,0],reye_pose=[0,0,0],lhand_pose=[[0,0,0] for _ in range(15)],rhand_pose=[[0,0,0] for _ in range(15)],trans=[0,0,3.8],betas=[0]*10,expr=[0]*100,focal=[1000,1000],princpt=[252,420],img_size_wh=[504,840],pad_ratio=0.)
    (motion/'smplx_params'/f'{i:05}.json').write_text(json.dumps(pose))
    Image.new('RGB',(504,840),'white').save(motion/'samurai_seg'/f'{i:05}.png')
    (motion/'bbox'/f'{i:05}.json').write_text(json.dumps([252,420,504,840]))
# Official Dance_I prior, camera-normalized; NOT motion captured from the upload.
dance_files=sorted((Path(__file__).parent/'assets/motion_video/Dance_I/smplx_params').glob('*.json'))
if len(dance_files)<240:raise RuntimeError('Official Dance_I motion assets are missing.')
neutral=json.loads((motion/'smplx_params/00000.json').read_text())
for k,src in enumerate(dance_files[:240:2],6):
    pose=dict(neutral);prior=json.loads(src.read_text())
    for key in ['root_pose','body_pose','lhand_pose','rhand_pose']:pose[key]=prior[key]
    (motion/'smplx_params'/f'{k:05}.json').write_text(json.dumps(pose))
    Image.new('RGB',(504,840),'white').save(motion/'samurai_seg'/f'{k:05}.png')
    (motion/'bbox'/f'{k:05}.json').write_text(json.dumps([252,420,504,840]))
(motion/'bbox/bbox.json').write_text(json.dumps({f'{i:05}':[252,420,504,840] for i in range(126)}))
subprocess.run([ffmpeg,'-nostdin','-v','error','-f','lavfi','-i','color=c=white:s=504x840:r=30:d=4.2','-pix_fmt','yuv420p','-y',str(motion/'turntable.mp4')],check=True,timeout=30)
# Fix upstream non-contiguous/multi-person tensor reshaping only in this process.
sys.path.insert(0, str(Path(__file__).parent))
from pose_compat import install_pose_compat, install_image_grid_compat
install_pose_compat()
install_image_grid_compat()
import core.utils.app_utils as app_utils
original_prepare=app_utils.prepare_input_and_output
def prepare(*args,**kwargs):
    values=list(original_prepare(*args,**kwargs));values[2]=str(motion/'smplx_params');return tuple(values)
app_utils.prepare_input_and_output=prepare
sys.argv=['test_app_case.py','--model_name','LHMPP-700M','--image_glob',str(r/'inputs/*.png'),'--motion_video',str(motion/'turntable.mp4'),'--ref_view',str(refs),'--motion_size','126','--render_fps','30','--output_dir',str(r/'neural')]
original_savez=np.savez
def bounded_savez(file,*args,**kwargs):
    if str(file).startswith(str(r/'posed/frame-')) and int(Path(file).stem.split('-')[-1])>=6:return
    return original_savez(file,*args,**kwargs)
np.savez=bounded_savez
print('CLASSROOM_STAGE inference',flush=True)
runpy.run_path(str(runtime/'source/scripts/test/test_app_case.py'),run_name='__main__')
videos=list((r/'neural').rglob('*.mp4'))
if not videos:raise RuntimeError('Model returned no preview')
shutil.copyfile(videos[-1],r/'all-views-and-dance.mp4')
subprocess.run([ffmpeg,'-nostdin','-v','error','-i',str(videos[-1]),'-vf',"select='lt(n,6)',setpts=N/(6*TB)",'-r','6','-an','-pix_fmt','yuv420p','-movflags','+faststart','-y',str(r/'preview.mp4')],check=True,timeout=60)
subprocess.run([ffmpeg,'-nostdin','-v','error','-i',str(videos[-1]),'-vf','trim=start_frame=6,setpts=PTS-STARTPTS','-r','30','-an','-pix_fmt','yuv420p','-movflags','+faststart','-y',str(r/'dance.mp4')],check=True,timeout=60)
subprocess.run([ffmpeg,'-nostdin','-v','error','-i',str(r/'preview.mp4'),'-frames:v','6','-vsync','0',str(r/'view-%02d.png')],check=True,timeout=30)
print('CLASSROOM_STAGE export',flush=True)
sys.path.insert(0,str(Path(__file__).parent));from export_assets import export
report=export(r)
report.update(model='Official LHM++ LHMPP-700M',runtime_revision='906b5d9fb967ab42efb92f6fa55bf22cac86b653',gpu=torch.cuda.get_device_name(),torch=torch.__version__,seconds=round(time.monotonic()-start,2),peak_vram_bytes=torch.cuda.max_memory_allocated(),source=f'{refs} authentic reference frame(s) from upload; no motion capture',rigged=False,reference_views=refs,dance_frames=120,dance_fps=30,dance_motion='Official LHM++ Dance_I prior; camera normalized; not source motion capture')
(r/'report.json').write_text(json.dumps(report,indent=2));print('CLASSROOM_DONE',json.dumps(report),flush=True)
