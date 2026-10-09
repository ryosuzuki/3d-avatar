import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const mime={'.html':'text/html','.js':'text/javascript','.json':'application/json','.ply':'application/octet-stream','.css':'text/css','.mp4':'video/mp4'};
const port=Number(process.env.AVATAR_INTERACTION_PORT||8774);
const host=process.env.AVATAR_INTERACTION_HOST||'127.0.0.1';
http.createServer((req,res)=>{
 let pathname;try{pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);}catch{res.writeHead(400);res.end();return;}
 const file=path.resolve(root,'.'+(pathname==='/'?'/index.html':pathname));
 if(!file.startsWith(root+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()){res.writeHead(404);res.end('Not found');return;}
 res.setHeader('Content-Type',mime[path.extname(file)]||'application/octet-stream');
 res.setHeader('Cache-Control','no-cache');
 res.setHeader('Cross-Origin-Opener-Policy','same-origin');
 res.setHeader('Cross-Origin-Embedder-Policy','require-corp');
 fs.createReadStream(file).pipe(res);
}).listen(port,host,()=>console.log(`Shared-avatar interaction: http://${host}:${port}`));
