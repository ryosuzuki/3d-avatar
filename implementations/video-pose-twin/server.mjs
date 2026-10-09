import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const mime={'.html':'text/html','.js':'text/javascript','.json':'application/json','.ply':'application/octet-stream','.css':'text/css','.mjs':'text/javascript','.wasm':'application/wasm','.mp4':'video/mp4'};
const port=Number(process.env.AVATAR_INTERACTION_PORT||8857);
const host=process.env.AVATAR_INTERACTION_HOST||'127.0.0.1';
http.createServer((req,res)=>{
 let pathname;try{pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);}catch{res.writeHead(400);res.end();return;}
 const file=path.resolve(root,'.'+(pathname==='/'?'/index.html':pathname));
 if(!file.startsWith(root+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()){res.writeHead(404);res.end('Not found');return;}
 res.setHeader('Content-Type',mime[path.extname(file)]||'application/octet-stream');
 res.setHeader('Cache-Control','no-cache');
 res.setHeader('Cross-Origin-Opener-Policy','same-origin');
 res.setHeader('Cross-Origin-Embedder-Policy','require-corp');
 const size=fs.statSync(file).size;res.setHeader('Accept-Ranges','bytes');
 const range=req.headers.range;
 if(range){const m=/bytes=(\d+)-(\d*)/.exec(range);if(!m){res.writeHead(416);res.end();return;}const start=+m[1],end=m[2]?Math.min(+m[2],size-1):size-1;res.writeHead(206,{'Content-Range':`bytes ${start}-${end}/${size}`,'Content-Length':end-start+1});fs.createReadStream(file,{start,end}).pipe(res);}
 else{res.setHeader('Content-Length',size);fs.createReadStream(file).pipe(res);}
}).listen(port,host,()=>console.log(`Shared-avatar interaction: http://${host}:${port}`));
