import {chromium} from 'playwright-core';
import fs from 'node:fs';
const out='/path/to/local-assets',tmp='/tmp/openclaw/shared-gaussian-avatar-ipad-mesh-english';
if(!process.env.OPENCLAW_BROWSER_LEASE_TOKEN)throw Error('Supervised profile lease required');
const r={profile:'agent-1',endpoint:'http://127.0.0.1:18800',errors:[],openedTargets:[],cleanup:{status:'blocked'}};let browser,page,id;
try{
 browser=await chromium.connectOverCDP(r.endpoint);const ctx=browser.contexts()[0];r.preserved=ctx.pages().map(p=>p.url());page=await ctx.newPage();await page.setViewportSize({width:1920,height:1080});const cdp=await ctx.newCDPSession(page);id=(await cdp.send('Target.getTargetInfo')).targetInfo.targetId;r.openedTargets.push({targetId:id,purpose:'Final delivered MP4 real browser playback'});fs.writeFileSync(tmp+'/final-browser-inventory.json',JSON.stringify(r,null,2));page.on('pageerror',e=>r.errors.push(e.message));
 await page.goto('http://127.0.0.1:8782/shared-gaussian-avatar-ipad-mesh-english/2026-10-08/');
 await page.evaluate(()=>{document.body.innerHTML='<video id="verifyMovie" controls style="width:100vw;height:100vh;object-fit:contain;background:#000" src="ryo-ipad-mesh-explainer-en.mp4"></video>';document.body.style.cssText='margin:0;background:#000;overflow:hidden';});
 await page.waitForFunction(()=>document.querySelector('video')?.readyState>=3,{timeout:30000});
 r.media=await page.evaluate(()=>{const v=document.querySelector('video');return {duration:v.duration,width:v.videoWidth,height:v.videoHeight,readyState:v.readyState,src:v.currentSrc}});
 await page.click('video');await page.evaluate(()=>document.querySelector('video').play());const started=await page.evaluate(()=>document.querySelector('video').currentTime);r.frames=[];
 for(const t of [2,8,15,23,31,39,47,55.8]){
  await page.waitForFunction(t=>document.querySelector('video').currentTime>=t,t,{timeout:60000});const state=await page.evaluate(()=>{const v=document.querySelector('video');return {time:v.currentTime,paused:v.paused,ended:v.ended,decoded:v.getVideoPlaybackQuality()?.totalVideoFrames,dropped:v.getVideoPlaybackQuality()?.droppedVideoFrames,error:v.error?.message}});r.frames.push(state);await page.screenshot({path:out+'/mp4-playback-'+String(Math.round(t)).padStart(2,'0')+'.png'});
 }
 await page.waitForFunction(()=>document.querySelector('video').ended,{timeout:10000});r.complete=await page.evaluate(()=>{const v=document.querySelector('video');return {time:v.currentTime,ended:v.ended,paused:v.paused,decoded:v.getVideoPlaybackQuality()?.totalVideoFrames,dropped:v.getVideoPlaybackQuality()?.droppedVideoFrames}});
 await page.screenshot({path:out+'/mp4-browser-playback-proof.png'});fs.writeFileSync(out+'/mp4-playback-verification.json',JSON.stringify(r,null,2));console.log('FULL_PLAYBACK_COMPLETE '+JSON.stringify(r.complete));
 const gate=tmp+'/final-playback-reviewed';if(!fs.existsSync(gate))await new Promise((resolve,reject)=>{const w=fs.watch(tmp,()=>{if(fs.existsSync(gate)){w.close();resolve()}});setTimeout(()=>{w.close();reject(Error('Final visual review timed out'))},180000)});
 r.cleanup.reviewedTargetIds=[id];r.cleanup.beforeEvidence=out+'/mp4-browser-playback-proof.png';
}catch(e){r.failure=e.stack;console.log('FINAL_VERIFY_FAILED '+e.message);process.exitCode=1}
finally{
 if(page){await page.close();r.cleanup.closedTargetIds=[id];r.cleanup.remainingPages=browser.contexts()[0].pages().map(p=>p.url());r.cleanup.preservedUnchanged=r.preserved.every(u=>r.cleanup.remainingPages.includes(u));r.cleanup.status='verified'}fs.writeFileSync(out+'/mp4-playback-verification.json',JSON.stringify(r,null,2));fs.writeFileSync(tmp+'/final-browser-inventory.json',JSON.stringify(r,null,2));if(browser)browser._connection.close();setTimeout(()=>process.exit(process.exitCode||0),50);
}
