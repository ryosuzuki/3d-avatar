import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.ply':'application/octet-stream','.css':'text/css','.mp4':'video/mp4','.wav':'audio/wav','.jpg':'image/jpeg','.srt':'text/plain','.vtt':'text/vtt'};
const port=Number(process.env.AVATAR_EXPLAINER_PORT||8776),host=process.env.AVATAR_EXPLAINER_HOST||'127.0.0.1';
http.createServer((req,res)=>{
 let pathname;try{pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);}catch{res.writeHead(400);res.end();return;}
 const file=path.resolve(root,'.'+(pathname==='/'?'/index.html':pathname));
 if(!file.startsWith(root+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()){res.writeHead(404);res.end('Not found');return;}
 res.setHeader('Content-Type',mime[path.extname(file)]||'application/octet-stream');res.setHeader('Cache-Control','no-cache');res.setHeader('Cross-Origin-Opener-Policy','same-origin');res.setHeader('Cross-Origin-Embedder-Policy','require-corp');
 const size=fs.statSync(file).size;res.setHeader('Accept-Ranges','bytes');const range=req.headers.range;
 if(range){const match=/bytes=(\d+)-(\d*)/.exec(range);if(!match){res.writeHead(416);res.end();return;}const start=+match[1],end=match[2]?Math.min(+match[2],size-1):size-1;if(start>=size||end<start){res.writeHead(416);res.end();return;}res.writeHead(206,{'Content-Range':`bytes ${start}-${end}/${size}`,'Content-Length':end-start+1});fs.createReadStream(file,{start,end}).pipe(res);}
 else{res.setHeader('Content-Length',size);fs.createReadStream(file).pipe(res);}
}).listen(port,host,()=>console.log(`Ryo spatial explainer: http://${host}:${port}`));
