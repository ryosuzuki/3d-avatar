import {chromium} from 'playwright-core';
import fs from 'node:fs';
const out='/path/to/local-assets',tmp='/tmp/openclaw/shared-gaussian-avatar-interaction';
const mode=process.argv[2]||'review';
const evidence={profile:'agent-1',endpoint:'http://127.0.0.1:18800',mode,openedTargets:[],errors:[],cleanup:{status:'blocked'}};
if(!process.env.OPENCLAW_BROWSER_LEASE_TOKEN)throw Error('Supervised owner lease required');
let browser,page,id;
try{
 browser=await chromium.connectOverCDP(evidence.endpoint);const ctx=browser.contexts()[0];evidence.preservedBefore=ctx.pages().map(p=>p.url());
 page=await ctx.newPage();await page.setViewportSize({width:1280,height:900});const cdp=await ctx.newCDPSession(page);id=(await cdp.send('Target.getTargetInfo')).targetInfo.targetId;evidence.openedTargets.push({targetId:id,purpose:'Exact shared Gaussian avatar continuous interaction verification'});
 fs.writeFileSync(tmp+'/browser-inventory.json',JSON.stringify(evidence,null,2));
 page.on('pageerror',e=>evidence.errors.push(e.message));page.on('console',m=>{if(m.type()==='error')evidence.errors.push(m.text());});
 await page.goto('http://127.0.0.1:8774/');await page.waitForFunction(()=>window.ready||window.loadError,{timeout:60000});const loadError=await page.evaluate(()=>window.loadError);if(loadError)throw Error(loadError);
 await page.evaluate(()=>window.seek(0));await page.screenshot({path:out+'/interaction-ready.png'});evidence.first=await page.evaluate(()=>window.getEvidence());
 for(const [t,name] of [[3,'walk'],[5.85,'reach'],[7.5,'grasp'],[11,'carry'],[14.5,'release'],[18,'complete']]){const s=await page.evaluate(t=>window.seek(t),t);evidence[name]=s;await page.screenshot({path:out+'/interaction-'+name+'.png'});}
 fs.writeFileSync(out+'/initial-render-readback.json',JSON.stringify(evidence,null,2));console.log('VISUAL_REVIEW_READY');
 // The model visually reviews task-owned screenshots before releasing this stage.
 if(mode==='review'){
  const signal=tmp+'/review-complete';
  await new Promise((resolve,reject)=>{if(fs.existsSync(signal))return resolve();const watcher=fs.watch(tmp,()=>{if(fs.existsSync(signal)){watcher.close();resolve();}});setTimeout(()=>{watcher.close();reject(Error('Visual review stage timed out'));},180000);});
 }
 if(mode==='capture'){
  evidence.interactions={};
  await page.click('#reset');const reset=await page.evaluate(()=>window.state);await page.click('#walk');await page.waitForFunction(()=>window.state.time>1.25,{timeout:5000});const walk=await page.evaluate(()=>window.state);await page.click('#pause');
  evidence.interactions.walkButton={before:reset.avatarRoot,after:walk.avatarRoot,walking:walk.walking};
  await page.click('#grasp');await page.waitForFunction(()=>window.state.attached,{timeout:5000});await page.click('#pause');evidence.interactions.graspButton=await page.evaluate(()=>window.state);
  await page.click('#rig');evidence.interactions.rigShown=await page.evaluate(()=>window.getEvidence().rigVisible);await page.click('#rig');
  await page.click('#room');evidence.interactions.roomHidden=await page.evaluate(()=>!window.getEvidence().roomVisible);await page.click('#room');
  const before=await page.evaluate(()=>window.viewer.camera.position.toArray());await page.mouse.move(770,410);await page.mouse.down();await page.mouse.move(910,450,{steps:8});await page.mouse.up();evidence.interactions.orbit={before,after:await page.evaluate(()=>window.viewer.camera.position.toArray())};
  await page.evaluate(()=>window.setCamera([2.8,2.35,3.7],[-.15,.91,.64]));
  fs.mkdirSync(tmp+'/frames',{recursive:true});evidence.trajectory=[];
  for(let i=0;i<360;i++){const t=i/20;const s=await page.evaluate(t=>window.drawFrame(t),t);evidence.trajectory.push(s);await page.screenshot({path:tmp+'/frames/frame-'+String(i).padStart(4,'0')+'.png'});if(i%60===0)console.log(`Captured ${i}/360 frames`);}
  console.log('Captured 360/360 frames');
 }
 await page.screenshot({path:out+'/cleanup-owned-target-before.png'});evidence.cleanup.reviewedTargetIds=[id];evidence.cleanup.beforeEvidence=out+'/cleanup-owned-target-before.png';
}catch(e){evidence.failure=e.stack;console.log('VERIFY_FAILED '+e.message);process.exitCode=1;}
finally{
 if(page){await page.close();evidence.cleanup.closedTargetIds=[id];evidence.cleanup.retainedTargetIds=[];evidence.cleanup.status='verified';evidence.cleanup.remainingPages=browser.contexts()[0].pages().map(p=>p.url());evidence.cleanup.preservedBeforeUnchanged=evidence.preservedBefore.every(u=>evidence.cleanup.remainingPages.includes(u));}
 fs.writeFileSync(out+(mode==='capture'?'/interaction-verification.json':'/render-review.json'),JSON.stringify(evidence,null,2));
 fs.writeFileSync(tmp+'/browser-inventory.json',JSON.stringify(evidence,null,2));if(browser)browser._connection.close();
 setTimeout(()=>process.exit(process.exitCode||0),50);
}
