import http from 'node:http';
import fs from 'node:fs';
import fsp from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {execFile,spawn} from 'node:child_process';
import {promisify} from 'node:util';
import Busboy from 'busboy';
const exec=promisify(execFile),ROOT=path.dirname(fileURLToPath(import.meta.url));
if(process.env.AVATAR_STORAGE_GUARD)await exec('/bin/bash',[process.env.AVATAR_STORAGE_GUARD],{timeout:10000});
const DATA=process.env.AVATAR_DATA||path.join(ROOT,'data');
const HOST=process.env.AVATAR_HOST||'127.0.0.1',PORT=Number(process.env.PORT||8848),REMOTE=process.env.AVATAR_REMOTE||'gpu-lab/classroom-avatar-lab',SSH=process.env.AVATAR_SSH||'avatar-gpu';
const PYTHON=process.env.AVATAR_PYTHON||'../video2mr-person-20261015/env/bin/python';
if(!/^[a-zA-Z0-9_./~-]+$/.test(REMOTE)||! /^[a-zA-Z0-9_./~-]+$/.test(PYTHON))throw Error('Use shell-safe worker paths without spaces');
const files={'dance.mp4':'video/mp4','mixamo-avatar.zip':'application/zip','avatar-textured.obj':'text/plain','avatar-textured.mtl':'text/plain','avatar-texture.png':'image/png','avatar.ply':'application/octet-stream','avatar.splat':'application/octet-stream','avatar-static.glb':'model/gltf-binary','avatar-static.obj':'text/plain','avatar-static.ply':'application/octet-stream','preview.mp4':'video/mp4','selected-frame.png':'image/png','view-01.png':'image/png','report.json':'application/json','classroom-avatar.zip':'application/zip'};
await fsp.mkdir(DATA,{recursive:true,mode:0o700});
let jobs=new Map(),busy=false;
for(const name of await fsp.readdir(DATA)){if(!/^[a-f0-9]{48}$/.test(name))continue;try{const j=JSON.parse(await fsp.readFile(path.join(DATA,name,'job.json')));if(['running','uploading'].includes(j.status)){j.status='failed';j.message='The server restarted. Please submit again.';}jobs.set(name,j);}catch{}}
const dir=id=>path.join(DATA,id),save=async j=>{j.updated=new Date().toISOString();await fsp.writeFile(path.join(dir(j.id),'job.json'),JSON.stringify(j));};
const json=(res,status,x)=>{res.writeHead(status,{'Content-Type':'application/json','Cache-Control':'no-store'});res.end(JSON.stringify(x));};
function permitted(ip){if(Date.now()<Number(process.env.AVATAR_PUBLIC_UNTIL||0))return true;ip=ip?.replace(/^::ffff:/,'');return ip==='127.0.0.1'||ip==='::1'||ip?.startsWith('128.138.')||(process.env.AVATAR_ALLOWED_IPS||'').split(',').includes(ip);}
function originOK(req){if(!req.headers.origin)return true;try{return new URL(req.headers.origin).host===req.headers.host;}catch{return false;}}
async function command(bin,args,timeout=60000){return exec(bin,args,{timeout,maxBuffer:2*1024*1024});}
async function run(j){
  j.status='running';j.message='Preparing your reference frame on the lab GPU worker…';await save(j);
  const remote=`${REMOTE}/jobs/${j.id}`;
  await command('ssh',['-o','BatchMode=yes','-o','ConnectTimeout=15',SSH,`mkdir -m 700 -p ${remote}`]);
  await command('scp',['-q',path.join(dir(j.id),'upload'),`${SSH}:${remote}/upload`],120000);
  const logfile=fs.createWriteStream(path.join(dir(j.id),'worker.log'),{flags:'a',mode:0o600});
  const code=await new Promise((resolve,reject)=>{
    const p=spawn('ssh',['-o','BatchMode=yes','-o','ServerAliveInterval=15',SSH,`cd ${REMOTE} && gpu-run --vram ${j.views===8?12.5:8.5} --ram 18 --job classroom-lhmpp-${j.id.slice(0,8)} -- timeout 900 ${PYTHON} -u worker.py jobs/${j.id} --frame ${j.frame} --views ${j.views||1} --end ${j.end||8}`]);
    const timer=setTimeout(()=>{p.kill('SIGTERM');reject(Error('GPU worker timed out.'));},960000);
    p.stdout.on('data',b=>{logfile.write(b);const s=b.toString();if(s.includes('CLASSROOM_STAGE inference')){j.message='Generating neural views and a dance with LHM++ on RTX 4090…';save(j);}if(s.includes('CLASSROOM_STAGE export')){j.message='Baking Gaussian colors and building static mesh downloads…';save(j);}});p.stderr.on('data',b=>logfile.write(b));p.on('error',e=>{clearTimeout(timer);logfile.end();reject(e);});p.on('close',c=>{clearTimeout(timer);logfile.end();resolve(c);});
  });
  if(code===75){j.status='queued';j.message='Waiting for enough free GPU memory. Existing lab jobs are preserved.';await save(j);return;}
  if(code!==0){const log=await fsp.readFile(path.join(dir(j.id),'worker.log'),'utf8');if(/8-view mode requires/.test(log))throw Error('8-view mode requires a turn-around video, not a photo.');if(/turn-around end must/.test(log))throw Error('Choose start and end times inside the video.');if(/Input image invalid|No person found/.test(log))throw Error('Please use a clear head-to-toe view of one person. Select another frame and try again.');throw Error('Generation failed. Try a clear full-body frame. Your job ID can be shared with the instructor.');}
  for(const name of Object.keys(files).filter(n=>n!=='classroom-avatar.zip'))await command('scp',['-q',`${SSH}:${remote}/${name}`,path.join(dir(j.id),name)],120000);
  await fsp.copyFile(path.join(ROOT,'GUIDE.md'),path.join(dir(j.id),'GUIDE.md'));
  await fsp.cp(path.join(ROOT,'unity'),path.join(dir(j.id),'Unity'),{recursive:true});
  await exec('/usr/bin/zip',['-q','-r','classroom-avatar.zip',...Object.keys(files).filter(n=>n!=='classroom-avatar.zip'),'GUIDE.md','Unity'],{cwd:dir(j.id),timeout:60000,maxBuffer:1024*1024});
  j.report=JSON.parse(await fsp.readFile(path.join(dir(j.id),'report.json')));j.status='done';j.message='Your avatar is ready. Download your files below.';j.completed=new Date().toISOString();await save(j);
}
async function pump(){if(busy)return;const j=[...jobs.values()].find(j=>j.status==='queued');if(!j)return;busy=true;try{await run(j);}catch(e){j.status='failed';j.message=e.message;await save(j);}finally{busy=false;}}
setInterval(pump,5000);
async function cleanup(){for(const [id,j] of jobs){if(Date.now()-Date.parse(j.created)<24*3600000||['running','uploading'].includes(j.status))continue;await fsp.rm(dir(id),{recursive:true,force:true});jobs.delete(id);await command('ssh',['-o','BatchMode=yes',SSH,`rm -rf -- ${REMOTE}/jobs/${id}`]).catch(()=>{});}}setInterval(()=>cleanup().catch(console.error),300000);
const server=http.createServer(async(req,res)=>{
 res.setHeader('X-Content-Type-Options','nosniff');res.setHeader('Referrer-Policy','no-referrer');res.setHeader('X-Frame-Options','DENY');res.setHeader('Content-Security-Policy',"default-src 'self'; script-src 'self' 'wasm-unsafe-eval'; worker-src 'self' blob:; style-src 'self' 'unsafe-inline'; img-src 'self' blob: data:; media-src 'self' blob:; connect-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'self'");
 if(!permitted(req.socket.remoteAddress))return json(res,403,{error:'This classroom service is available on the CU Boulder network only.'});
 const u=new URL(req.url,'http://classroom');
 try{
  if(req.method==='GET'&&u.pathname==='/api/health')return json(res,200,{ok:true,service:'Classroom Avatar Lab',model:'LHM++ LHMPP-700M',queued:[...jobs.values()].filter(j=>j.status==='queued').length,processing:busy,retentionHours:24});
  if(req.method==='POST'&&u.pathname==='/api/jobs'){
   if(!originOK(req))return json(res,403,{error:'Please submit from this website.'});
   if(Number(req.headers['content-length']||0)>151*1024*1024)return json(res,413,{error:'Choose a file under 150 MB.'});
   if([...jobs.values()].filter(j=>['queued','running','uploading'].includes(j.status)).length>=30)return json(res,429,{error:'The class queue is full. Please try again shortly.'});
   const id=crypto.randomBytes(24).toString('hex'),j={id,status:'uploading',message:'Uploading…',created:new Date().toISOString(),frame:0};await fsp.mkdir(dir(id),{mode:0o700});jobs.set(id,j);
   try{
    const fields={};let got=false,truncated=false;
    await new Promise((resolve,reject)=>{const bb=Busboy({headers:req.headers,limits:{fileSize:150*1024*1024,files:1,fields:5,fieldSize:100}});const writes=[];bb.on('field',(k,v)=>fields[k]=v);bb.on('file',(k,s,info)=>{if(k!=='file'){s.resume();return;}got=true;const out=fs.createWriteStream(path.join(dir(id),'upload'),{mode:0o600});s.on('limit',()=>truncated=true);s.pipe(out);writes.push(new Promise((r,e)=>{out.on('finish',r);out.on('error',e);s.on('error',e);}));});bb.on('error',reject);bb.on('filesLimit',()=>reject(Error('Upload one file at a time.')));req.on('aborted',()=>reject(Error('Upload interrupted.')));bb.on('close',()=>Promise.all(writes).then(resolve,reject));req.pipe(bb);});
    if(!got||truncated||fields.consent!=='yes')throw Error('Upload one video or image under 150 MB and confirm permission to process it.');
    j.frame=Number(fields.frame||0);if(!Number.isFinite(j.frame)||j.frame<0||j.frame>120)throw Error('Choose a frame time between 0 and 120 seconds.');
    j.views=fields.views==='8'?8:1;j.end=Number(fields.end||8);if(!Number.isFinite(j.end)||j.end>120||j.end<=j.frame&&j.views===8)throw Error('Choose an end time after the start, within 120 seconds.');
    j.status='queued';j.message='Waiting for the lab GPU. Keep this private result link.';await save(j);json(res,202,{id,url:`/#job=${id}`});pump();return;
   }catch(e){jobs.delete(id);await fsp.rm(dir(id),{recursive:true,force:true});return json(res,400,{error:e.message});}
  }
  const match=u.pathname.match(/^\/api\/jobs\/([a-f0-9]{48})(?:\/files\/([a-zA-Z0-9.-]+))?$/);
  if(match){const [,id,file]=match,j=jobs.get(id);if(!j)return json(res,404,{error:'This result was not found or has expired.'});if(req.method!=='GET')return json(res,405,{error:'Method not allowed'});if(!file)return json(res,200,{...j,queuePosition:j.status==='queued'?[...jobs.values()].filter(x=>x.status==='queued').indexOf(j)+1:0,downloads:j.status==='done'?Object.keys(files).filter(n=>fs.existsSync(path.join(dir(id),n))):[]});if(j.status!=='done'||!files[file])return json(res,404,{error:'File unavailable'});const f=path.join(dir(id),file);if(!fs.existsSync(f))return json(res,404,{error:'This older result does not include that file. Generate again for new features.'});const stat=await fsp.stat(f);const headers={'Content-Type':files[file],'Cache-Control':'private, no-store','Accept-Ranges':'bytes','Content-Disposition':`${/\.(png|mp4)$/.test(file)?'inline':'attachment'}; filename="${file}"`};let start=0,end=stat.size-1,status=200;if(req.headers.range){const range=req.headers.range.match(/^bytes=(\d*)-(\d*)$/);if(!range||(!range[1]&&!range[2])){res.writeHead(416,{'Content-Range':`bytes */${stat.size}`});res.end();return;}if(range[1]){start=Number(range[1]);end=range[2]?Math.min(end,Number(range[2])):end;}else{start=Math.max(0,stat.size-Number(range[2]));}if(start>end||start>=stat.size){res.writeHead(416,{'Content-Range':`bytes */${stat.size}`});res.end();return;}status=206;headers['Content-Range']=`bytes ${start}-${end}/${stat.size}`;}headers['Content-Length']=end-start+1;res.writeHead(status,headers);fs.createReadStream(f,{start,end}).pipe(res);return;}
  if(req.method==='GET'&&u.pathname.startsWith('/characters/')){
   const name=u.pathname.slice('/characters/'.length);
   const allowed={'human-mixamo.zip':'application/zip','human-male.fbx':'application/octet-stream','human-female.fbx':'application/octet-stream','human-rigged.glb':'model/gltf-binary','license.txt':'text/plain','mixamo-remy-demo.mp4':'video/mp4','character-click-guide.mp4':'video/mp4','character-click-guide.pdf':'application/pdf','unity-character-demo.mp4':'video/mp4','unity-character-starter.zip':'application/zip',...Object.fromEntries(Array.from({length:14},(_,i)=>[`step-${String(i+1).padStart(2,'0')}.png`,'image/png']))};
   if(!allowed[name])return json(res,404,{error:'Not found'});
   const f=path.join(DATA,'character-lesson',name);if(!fs.existsSync(f))return json(res,404,{error:'Artifact not available'});
   const stat=await fsp.stat(f);const headers={'Content-Type':allowed[name],'Content-Length':stat.size,'Cache-Control':'no-cache','Content-Disposition':`${/\.(png|mp4)$/.test(name)?'inline':'attachment'}; filename="${name}"`};
   res.writeHead(200,headers);fs.createReadStream(f).pipe(res);return;
  }
  if(req.method==='GET'&&u.pathname.startsWith('/tutorial/')){
   const tutorialName=u.pathname.slice('/tutorial/'.length);const tutorialAllowed={'unity-click-guide.mp4':'video/mp4','unity-click-guide.pdf':'application/pdf','unity-gaussian-starter.zip':'application/zip','unity-gaussian-readme.md':'text/plain','unity-click-guide.vtt':'text/vtt',...Object.fromEntries(Array.from({length:6},(_,i)=>[`step-${String(i+1).padStart(2,'0')}.png`,'image/png']))};
   if(!tutorialAllowed[tutorialName])return json(res,404,{error:'Not found'});
   const f=path.join(DATA,'tutorial',tutorialName);if(!fs.existsSync(f))return json(res,404,{error:'Tutorial artifact is being prepared.'});const stat=await fsp.stat(f);let start=0,end=stat.size-1,status=200;const headers={'Content-Type':tutorialAllowed[tutorialName],'Cache-Control':'no-store','Accept-Ranges':'bytes'};
   if(req.headers.range){const range=req.headers.range.match(/^bytes=(\d*)-(\d*)$/);if(!range||(!range[1]&&!range[2])){res.writeHead(416,{'Content-Range':`bytes */${stat.size}`});return res.end();}if(range[1]){start=Number(range[1]);end=range[2]?Math.min(end,Number(range[2])):end;}else start=Math.max(0,stat.size-Number(range[2]));if(start>end||start>=stat.size){res.writeHead(416,{'Content-Range':`bytes */${stat.size}`});return res.end();}status=206;headers['Content-Range']=`bytes ${start}-${end}/${stat.size}`;}headers['Content-Length']=end-start+1;res.writeHead(status,headers);fs.createReadStream(f,{start,end}).pipe(res);return;
  }
  if(req.method==='GET'){
   const staticPaths={'/characters':'characters.html','/downloads':'downloads.html','/downloads.js':'downloads.js','/tutorial':'tutorial.html','/':'index.html','/app.js':'app.js','/style.css':'style.css','/guide':'guide.html','/GUIDE.md':'GUIDE.md','/unity/PlaceAvatarOnPlane.cs':'unity/PlaceAvatarOnPlane.cs'};
   const f=staticPaths[u.pathname];if(f){res.setHeader('Cache-Control','no-store');res.setHeader('Content-Type',f.endsWith('.html')?'text/html; charset=utf-8':f.endsWith('.css')?'text/css':f.endsWith('.js')?'text/javascript':'text/plain');res.end(await fsp.readFile(path.join(ROOT,f)));return;}
  }json(res,404,{error:'Not found'});
 }catch(e){console.error(e.message);if(!res.headersSent)json(res,500,{error:'The request could not be completed.'});else res.end();}
});
server.requestTimeout=180000;server.listen(PORT,HOST,()=>console.log(`Classroom Avatar Lab listening on http://${HOST}:${PORT}`));
