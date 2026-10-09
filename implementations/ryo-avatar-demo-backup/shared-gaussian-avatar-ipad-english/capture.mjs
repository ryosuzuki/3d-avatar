import {chromium} from 'playwright-core';
import fs from 'node:fs';
import {spawn} from 'node:child_process';
const out='/path/to/local-assets',tmp='/tmp/openclaw/shared-gaussian-avatar-ipad-english';
const capture=process.argv.includes('--capture'),evidence={profile:'agent-1',endpoint:'http://127.0.0.1:18800',mode:capture?'capture':'proof',errors:[],openedTargets:[],cleanup:{status:'blocked'}};
if(!process.env.OPENCLAW_BROWSER_LEASE_TOKEN)throw Error('Supervised profile lease required');
let browser,page,id,encoder;
try{
 browser=await chromium.connectOverCDP(evidence.endpoint);const ctx=browser.contexts()[0];evidence.preserved=ctx.pages().map(p=>p.url());
 page=await ctx.newPage();await page.setViewportSize({width:1920,height:1080});const cdp=await ctx.newCDPSession(page);id=(await cdp.send('Target.getTargetInfo')).targetInfo.targetId;evidence.openedTargets.push({targetId:id,purpose:'Ryo spatial explainer proof / deterministic export'});fs.writeFileSync(tmp+'/browser-inventory.json',JSON.stringify(evidence,null,2));
 page.on('pageerror',e=>evidence.errors.push(e.message));page.on('console',m=>{if(m.type()==='error')evidence.errors.push(m.text())});
 await page.goto('http://127.0.0.1:8780/?film');await page.waitForFunction(()=>window.ready||window.loadError,{timeout:60000});const err=await page.evaluate(()=>window.loadError);if(err)throw Error(err);
 console.log(await page.evaluate(()=>({counts:window.viewer.splatMesh.scenes.map(s=>s.splatBuffer.getSplatCount())}))); if(process.argv.includes('--debug')){for(const mode of [1,2]){await page.evaluate(m=>{window.debugMode=m;window.drawFrame(11.5)},mode);await page.screenshot({path:out+'/debug-'+mode+'.png'});}} const story=JSON.parse(fs.readFileSync(out+'/story.json'));evidence.first=await page.evaluate(()=>window.getEvidence());evidence.samples=[];
 for(let i=0;i<story.segments.length;i++){
  const s=story.segments[i],t=s.start+s.duration*.65;const state=await page.evaluate(t=>window.drawFrame(t),t);evidence.samples.push(state);await page.screenshot({path:out+`/proof-${String(i+1).padStart(2,'0')}.png`});
 }
 fs.writeFileSync(out+'/render-proof.json',JSON.stringify(evidence,null,2));console.log('PROOF_READY');
 if(capture){
  const gate=tmp+'/visual-proof-approved';if(!fs.existsSync(gate))await new Promise((resolve,reject)=>{const w=fs.watch(tmp,()=>{if(fs.existsSync(gate)){w.close();resolve()}});setTimeout(()=>{w.close();reject(Error('Visual proof review timed out'))},180000)});
  // Verify interactive audio-linked playback and exact geometry state before offline export.
  await page.goto('http://127.0.0.1:8780/');await page.waitForFunction(()=>window.ready||window.loadError,{timeout:60000});await page.click('#play');await page.waitForFunction(()=>window.state.time>.5,{timeout:10000});await page.click('#play');evidence.playback=await page.evaluate(()=>({state:window.state,audioTime:document.querySelector('#voice').currentTime,paused:document.querySelector('#voice').paused}));await page.click('#room');evidence.roomToggle=await page.evaluate(()=>!window.getEvidence().roomVisible);await page.click('#room');await page.evaluate(()=>document.body.classList.add('film'));
  encoder=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate','30','-vcodec','mjpeg','-i','pipe:0','-an','-vf','scale=in_range=pc:out_range=tv,format=yuv420p','-color_range','tv','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-r','30','-movflags','+faststart',out+'/visual-master.mp4'],{stdio:['pipe','inherit','inherit']});const complete=new Promise((res,rej)=>encoder.on('exit',code=>code===0?res():rej(Error('encoder exit '+code))));
  const count=Math.ceil(story.duration*30);evidence.frameCount=count;evidence.fps=30;evidence.trajectory=[];
  for(let f=0;f<count;f++){
   const state=await page.evaluate(t=>window.drawFrame(t),f/30);if(f%15===0)evidence.trajectory.push(state);
   const jpg=await page.screenshot({type:'jpeg',quality:94});if(!encoder.stdin.write(jpg))await new Promise(res=>encoder.stdin.once('drain',res));if(f%120===0)console.log(`FRAME ${f}/${count}`);
  }
  encoder.stdin.end();await complete;encoder=null;console.log(`CAPTURE_COMPLETE ${count}/${count}`);
 }
 await page.screenshot({path:out+'/cleanup-before.png'});evidence.cleanup.reviewedTargetIds=[id];evidence.cleanup.beforeEvidence=out+'/cleanup-before.png';
}catch(e){evidence.failure=e.stack;console.log('RENDER_FAILED '+e.message);process.exitCode=1;if(encoder){encoder.stdin.end();encoder.kill('SIGTERM')}}
finally{
 if(page){await page.close();evidence.cleanup.closedTargetIds=[id];evidence.cleanup.remainingPages=browser.contexts()[0].pages().map(p=>p.url());evidence.cleanup.preservedUnchanged=evidence.preserved.every(u=>evidence.cleanup.remainingPages.includes(u));evidence.cleanup.status='verified';}
 fs.writeFileSync(out+(capture?'/capture-verification.json':'/render-proof.json'),JSON.stringify(evidence,null,2));fs.writeFileSync(tmp+'/browser-inventory.json',JSON.stringify(evidence,null,2));if(browser)browser._connection.close();setTimeout(()=>process.exit(process.exitCode||0),50);
}
