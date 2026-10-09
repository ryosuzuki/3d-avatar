import * as THREE from 'three';
import * as GS from './vendor/gaussian-splats-3d.module.js';
import {GaussianRig} from './rig.js';
import {loadCapturedRoom} from './room.js';
import {installSkinning} from './avatar.js';
import {COLORS,NODE,validatePlan,cueFor,nodeFocus} from './service-adapter.js';
const story=await(await fetch('./story.json')).json(),duration=story.duration;
const baselineMode=new URLSearchParams(location.search).has('baseline');
const apiPlan=baselineMode?null:validatePlan(await(await fetch('./service/plan.json')).json());
if(apiPlan){document.querySelector('#credit').textContent='JEV-PLANNED REPLAY · SYNTHETIC ENGLISH VOICE';document.querySelector('.tag').textContent='JEV × ORIGINAL RYO AVATAR';}
window.apiPlanEvidence=apiPlan;
const scene=new THREE.Scene();scene.background=new THREE.Color(0x102333);scene.add(new THREE.HemisphereLight(0xd1f1ff,0x405168,3));
const light=new THREE.DirectionalLight(0xc8edff,3);light.position.set(0,4,3);scene.add(light);
const root=document.querySelector('#root');const renderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});renderer.setPixelRatio(1);renderer.setSize(root.clientWidth,root.clientHeight);renderer.outputColorSpace=THREE.SRGBColorSpace;root.appendChild(renderer.domElement);
const camera=new THREE.PerspectiveCamera(38,root.clientWidth/root.clientHeight,.03,100);camera.position.set(1.15,1.85,4.4);camera.lookAt(.22,1.0,.12);
const viewer=new GS.Viewer({rootElement:root,renderer,camera,threeScene:scene,selfDrivenMode:false,dynamicScene:false,useBuiltInControls:true,enableOptionalEffects:false,gpuAcceleratedSort:false,sharedMemoryForWorkers:true,enableSIMDInSort:true,integerBasedSort:true,halfPrecisionCovariancesOnGPU:false,sphericalHarmonicsDegree:0,sceneRevealMode:GS.SceneRevealMode.Instant,optimizeSplatData:false,ignoreDevicePixelRatio:true});
const rig=new GaussianRig();window.viewer=viewer;window.ready=false;let controller,time=0,playing=false;
const clamp=x=>Math.min(1,Math.max(0,x)),smooth=x=>{x=clamp(x);return x*x*(3-2*x)},lerp=(a,b,t)=>a+(b-a)*t;
// Room floor is supplied by the captured mesh, never a fabricated stage.


const shadow=new THREE.Mesh(new THREE.CircleGeometry(.31,48),new THREE.MeshBasicMaterial({color:0x06121c,transparent:true,opacity:.55,depthWrite:false}));shadow.rotation.x=-Math.PI/2;shadow.position.set(-.68,-.007,.035);scene.add(shadow);
const roomGroup=await loadCapturedRoom(scene);window.roomBackgroundVisible=true;
// Transparent board and all marks are actual3D geometry/textures, not a video billboard.
const BW=1.75,BH=1.20,LEFT=-.21,BOTTOM=.65,BZ=.17;
const glass=new THREE.Mesh(new THREE.PlaneGeometry(BW,BH),new THREE.MeshBasicMaterial({color:0x102b39,transparent:true,opacity:.36,side:THREE.DoubleSide,depthWrite:false}));glass.position.set(LEFT+BW/2,BOTTOM+BH/2,BZ);scene.add(glass);
const frame=new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.PlaneGeometry(BW,BH)),new THREE.LineBasicMaterial({color:0x74c6cc,transparent:true,opacity:.5}));frame.position.copy(glass.position);scene.add(frame);
const boardCanvas=document.createElement('canvas');boardCanvas.width=1024;boardCanvas.height=768;const bc=boardCanvas.getContext('2d');const boardTex=new THREE.CanvasTexture(boardCanvas);
const ink=new THREE.Mesh(new THREE.PlaneGeometry(BW,BH),new THREE.MeshBasicMaterial({map:boardTex,transparent:true,side:THREE.DoubleSide,depthWrite:false}));ink.position.copy(glass.position);ink.position.z+=.008;scene.add(ink);
function boardPoint(x,y){return new THREE.Vector3(LEFT+x/1024*BW,BOTTOM+(1-y/768)*BH,BZ+.022)}
function strokePath(points,p){const seg=(points.length-1)*clamp(p),idx=Math.min(points.length-2,Math.floor(seg)),f=seg-idx;return [lerp(points[idx][0],points[idx+1][0],f),lerp(points[idx][1],points[idx+1][1],f)]}
function drawStroke(points,p,color='#84efda',width=5){if(p<=0)return;bc.strokeStyle=color;bc.lineWidth=width;bc.lineCap='round';bc.lineJoin='round';bc.beginPath();bc.moveTo(...points[0]);const n=(points.length-1)*clamp(p);for(let i=1;i<=Math.floor(n);i++)bc.lineTo(...points[i]);if(n<points.length-1)bc.lineTo(...strokePath(points,p));bc.stroke();}
const drawing=[[165,470],[187,452],[199,438],[210,446],[222,410],[237,430],[252,389],[269,400],[287,373],[305,385],[320,354]];
const circle=[[320,354],...Array.from({length:49},(_,i)=>[310+52*Math.cos(i/48*Math.PI*2),355+52*Math.sin(i/48*Math.PI*2)])];
function text(s,x,y,size=30,color='#d6f0f2',align='left'){bc.font=`500 ${size}px system-ui,sans-serif`;bc.fillStyle=color;bc.textAlign=align;bc.fillText(s,x,y)}
function pill(s,x,y,w,color='#5faea6'){bc.fillStyle=color+'30';bc.strokeStyle=color;bc.lineWidth=2;bc.beginPath();bc.roundRect(x,y,w,60,12);bc.fill();bc.stroke();text(s,x+w/2,y+39,26,'#e6f8f8','center')}
function phaseProgress(i,t){const s=story.segments[i];return clamp((t-s.start)/s.duration)}
function boardDraw(t){
 const cue=apiPlan?cueFor(apiPlan,story.segments[currentSegment(t)].id):null,accent=COLORS[cue?.emphasis_color]||COLORS.teal;
 bc.clearRect(0,0,1024,768);text('VOICE  ×  GESTURE  ×  SPACE',425,60,24,'#89b9c4');text('ONE IDEA. SHARED TIMING.',425,119,29);
 const seg=story.segments[1],d=clamp((t-seg.start-.65)/(seg.duration-.65));drawStroke(drawing,d/.58,accent);drawStroke(circle,(d-.58)/.42,accent);
 if(cue&&t>=story.segments[4].start)text('FOCUS / '+['VOICE','GESTURE','SPACE'][nodeFocus(cue,phaseProgress(currentSegment(t),t))],425,174,20,accent);
 if(t>=story.segments[2].start){const p=phaseProgress(2,t);text('ONE TIMELINE',420,215,25,'#8de6d0');drawStroke([[425,320],[925,320]],p,accent,5);
  for(let i=0;i<5;i++){const x=465+i*100;if(p>i*.16){bc.fillStyle=i%2?'#ecba80':'#8de9d8';bc.beginPath();bc.arc(x,320,7,0,Math.PI*2);bc.fill();}}
  text('VOICE',455,277,26);text('GESTURE',585,277,26);text('INK',820,277,26);
  if(p>.3)drawStroke([[363,355],[415,320]],(p-.3)/.3,'#88cfdf',4);
 }
 if(t>=story.segments[3].start){const p=phaseProgress(3,t),x=425+500*p;bc.strokeStyle='#f7c98e';bc.lineWidth=3;bc.beginPath();bc.moveTo(x,293);bc.lineTo(x,345);bc.stroke();bc.fillStyle='#f6cf92';bc.beginPath();bc.arc(x,320,12,0,Math.PI*2);bc.fill();
  const paths=[[[438,425],[515,400],[585,425],[670,370],[750,390],[832,345],[910,360]],[[438,505],[545,505],[585,475],[705,475],[750,440],[910,440]]];drawStroke(paths[0],p,accent,4);drawStroke(paths[1],p,'#a6b6f4',4);text('speech',434,563,22,'#87e1cf');text('gesture + ink',650,563,22,'#bec8f5');
 }
 if(t>=story.segments[4].start){const p=phaseProgress(4,t);bc.globalAlpha=.78-p*.32;pill('VOICE',465,620,135);pill('BODY',640,620,135,'#9dafe7');pill('SPACE',815,620,150,'#d6b181');bc.globalAlpha=1;}
 if(t>=story.segments[6].start){text('SAVED PLAN  →  SYNCHRONIZED REPLAY',425,720,21,'#aec8d5');}
 boardTex.needsUpdate=true;
}
// Persistent nodes visibly leave the board, gaining depth and linked3D relationships.
function makeNode(word,color){const c=document.createElement('canvas');c.width=512;c.height=256;const ctx=c.getContext('2d');ctx.clearRect(0,0,512,256);ctx.fillStyle='#112536';ctx.strokeStyle=color;ctx.lineWidth=4;ctx.beginPath();ctx.roundRect(12,45,488,158,40);ctx.fill();ctx.stroke();ctx.font='500 53px system-ui';ctx.fillStyle='#e2f4f5';ctx.textAlign='center';ctx.fillText(word,256,143);const label=new THREE.Mesh(new THREE.PlaneGeometry(.47,.235),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(c),transparent:true,side:THREE.DoubleSide,depthWrite:false}));const group=new THREE.Group();group.add(label);const orb=new THREE.Mesh(new THREE.SphereGeometry(.055,24,16),new THREE.MeshStandardMaterial({color,emissive:color,emissiveIntensity:.55,roughness:.25}));orb.position.y=.19;group.add(orb);scene.add(group);return group;}
const nodes=[makeNode('VOICE','#7ee6cb'),makeNode('GESTURE','#a6b9f7'),makeNode('SPACE','#edc08b')];
const nodeStart=[boardPoint(530,650),boardPoint(707,650),boardPoint(885,650)],nodeEnd=[new THREE.Vector3(.48,1.51,.81),new THREE.Vector3(.94,1.1,.76),new THREE.Vector3(1.27,1.62,.48)];
const connectors=new THREE.LineSegments(new THREE.BufferGeometry().setAttribute('position',new THREE.BufferAttribute(new Float32Array(18),3)),new THREE.LineBasicMaterial({color:0x9cdddc,transparent:true,opacity:.75,depthTest:false}));scene.add(connectors);
const contact=new THREE.Mesh(new THREE.RingGeometry(.016,.023,32),new THREE.MeshBasicMaterial({color:0x9cffe4,side:THREE.DoubleSide,transparent:true,opacity:.9,depthTest:false}));scene.add(contact);
const pen=new THREE.Mesh(new THREE.CylinderGeometry(.007,.004,.065,12),new THREE.MeshStandardMaterial({color:0xaffbe3,emissive:0x44cbb7,emissiveIntensity:.55}));scene.add(pen);
const pointer=new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(),new THREE.Vector3()]),new THREE.LineDashedMaterial({color:0xa3e9d9,dashSize:.028,gapSize:.023,transparent:true,opacity:.65,depthTest:false}));scene.add(pointer);
function currentSegment(t){let i=0;for(let j=0;j<story.segments.length;j++)if(t>=story.segments[j].start)i=j;return i}
let cameraTourEnabled=true;
viewer.controls.addEventListener('start',()=>{cameraTourEnabled=false});
function cameraTour(t){
 const close=[-.25,1.65,3.05],target=[.22,1.00,.14],wide=[-.25,1.85,3.6],wideTarget=[.15,1.00,.14];
 let p=smooth((t-2)/5);if(t>story.segments[4].start)p=1-.15*smooth((t-story.segments[4].start)/2);if(t>story.segments[7].start)p=.85-.55*smooth((t-story.segments[7].start)/story.segments[7].duration);
 camera.position.fromArray(wide).lerp(new THREE.Vector3(...close),p);const at=new THREE.Vector3(...wideTarget).lerp(new THREE.Vector3(...target),p);camera.lookAt(at);viewer.controls.target.copy(at);camera.updateMatrixWorld();
}
function draw(t){
 time=Math.max(0,Math.min(duration,t));const i=currentSegment(time),p=phaseProgress(i,time),d=clamp((time-story.segments[1].start-.65)/(story.segments[1].duration-.65)),sp=phaseProgress(4,time);
 const cue=apiPlan?cueFor(apiPlan,story.segments[i].id):null,selectedNode=cue?nodeFocus(cue,p):i===5?Math.floor(p*2.99):0;
 if(cameraTourEnabled)cameraTour(time);
 boardDraw(time);
 for(let j=0;j<3;j++){nodes[j].visible=time>=story.segments[4].start;nodes[j].position.copy(nodeStart[j]).lerp(nodeEnd[j],smooth(sp));nodes[j].scale.setScalar(lerp(.4,1,smooth(sp)));nodes[j].children[1].scale.setScalar((j===selectedNode&&apiPlan?1.3:1)+.1*Math.sin(time*2+j));nodes[j].children[1].material.emissiveIntensity=cue&&j===(NODE[cue.focus_node]??0)?.95:.55;}
 connectors.visible=time>=story.segments[4].start;const a=connectors.geometry.attributes.position;for(let j=0;j<3;j++){a.setXYZ(j*2,...nodes[j].position.toArray());a.setXYZ(j*2+1,...nodes[(j+1)%3].position.toArray());}a.needsUpdate=true;
 let desired=new THREE.Vector3(-.13,1.31,.20),writing=i===1&&time>=story.segments[1].start+.65,pointing=i>=2&&i<7,rootX=-.68;
 if(i===1){const xy=d<.58?strokePath(drawing,d/.58):strokePath(circle,(d-.58)/.42);desired=boardPoint(...xy);rootX=desired.x-.51;}
 else if(i===2){desired=boardPoint(420,320);rootX=-.30;}
 else if(i===3){desired=boardPoint(425+500*p,320);rootX=-.18;}
 else if(i>=4&&i<7){desired.copy(nodes[selectedNode].position);rootX=-.26;}
 else if(i>=7){rootX=-.38;desired.set(-.03,1.23,.36);}
 const previousRoot=[-.68,-.68,-.102,-.30,-.18,-.26,-.26,-.26][i];
 const previousTarget=[new THREE.Vector3(-.13,1.31,.20),new THREE.Vector3(-.13,1.31,.20),boardPoint(...circle[circle.length-1]),boardPoint(420,320),boardPoint(925,320),nodeEnd[0],nodeEnd[2],nodeEnd[0]][i];
 const transition=smooth((time-story.segments[i].start)/.65);rootX=lerp(previousRoot,rootX,transition);desired.lerp(previousTarget,1-transition);
 const easeIn=smooth((time-story.segments[1].start)/.65),easeOut=i===7?1-smooth(p*.95):1;
 const rootPos=[rootX,0,.035];shadow.position.x=rootX;
 const wristWorld=desired.clone().add(new THREE.Vector3(0,.02,.12)),shoulder=new THREE.Vector3(rootX+.16,1.45675,.035);
 // Reach only physically reachable target; detached diagrams are pointed at with a ray.
 const v=wristWorld.clone().sub(shoulder);if(v.length()>.545)wristWorld.copy(shoulder).add(v.setLength(.545));
 const relaxed=new THREE.Vector3(rootX+.205,.90,.065);wristWorld.lerp(relaxed,1-easeIn*easeOut);
 if(cue?.gesture==='open_explain'&&i!==1){wristWorld.set(rootX+.24,1.10+.025*Math.sin(time*1.2),.32);pointer.visible=false;}
 const localLeft=wristWorld.clone().sub(new THREE.Vector3(...rootPos)),localRight=cue&&['open_explain','closing'].includes(cue.gesture)?[-.27,1.09+.035*Math.sin(time*1.1),.30]:[-.205,.91+.025*Math.sin(time*1.1),.06+.025*Math.cos(time*1.5)];
 const toward=cue?.gesture==='open_explain'&&i!==1?new THREE.Vector3(.02,.035,.105):desired.clone().sub(wristWorld).normalize().multiplyScalar(.112);
 rig.update({position:rootPos,yaw:0,gait:0,walking:false,grip:false,reach:0,center:[0,1.1,.3],handTargets:[localRight,localLeft.toArray()],handDirections:[cue&&['open_explain','closing'].includes(cue.gesture)?[-.02,.035,.10]:[0,-.11,.02],toward.toArray()],headYaw:i===1?.23:i>=2&&i<7?.15:-.02});
 const hand=rig.segments[8][1],axis=desired.clone().sub(hand);pen.visible=writing;contact.visible=writing;contact.position.copy(desired);contact.position.z+=.003;
 pen.position.copy(hand).add(axis.clone().setLength(.025));pen.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),axis.clone().normalize());
 pointer.visible=pointing&&cue?.gesture!=='open_explain';const pp=pointer.geometry.attributes.position;pp.setXYZ(0,...hand.toArray());pp.setXYZ(1,...desired.toArray());pp.needsUpdate=true;pointer.computeLineDistances();
 viewer.update();controller.sort(camera);viewer.render(); const bg=scene.background;scene.background=null;renderer.autoClear=false;renderer.render(scene,camera);renderer.autoClear=true;scene.background=bg;
 document.querySelector('#chaptertext').textContent=String(i+1).padStart(2,'0')+' / '+['INTRODUCTION','LIVING BLACKBOARD','SHARED TIMELINE','VOICE-LED MOTION','INTO THE ROOM','ONE CONNECTED IDEA','NOW → NEXT','SPATIAL UNDERSTANDING'][i];document.querySelector('#headline').textContent=story.segments[i].headline;
 document.querySelector('#caption').textContent=time>=story.segments[i].start&&time<=story.segments[i].end?story.segments[i].narration:'';
 document.querySelector('#progress i').style.width=(time/duration*100)+'%';document.querySelector('#marker').textContent=time.toFixed(1)+' / '+duration.toFixed(1)+' s';document.querySelector('#timeline').value=time;
 window.state={time,segment:story.segments[i].id,writing,pointing,desiredPoint:desired.toArray(),leftHand:hand.toArray(),penContactError:writing?Math.max(0,hand.distanceTo(desired)-.065):null,armErrors:rig.armErrors.slice(),apiCue:cue,selectedNode,root:rootPos,spatialProgress:sp,nodes:nodes.map(n=>n.position.toArray())};return window.state;
}
window.drawFrame=t=>{playing=false;return draw(t)};window.seek=t=>{playing=false;document.querySelector('#voice').pause();document.querySelector('#voice').currentTime=t;return draw(t)};window.getEvidence=()=>({asset:window.assetEvidence,state:window.state,voice:story.voice,apiPlan,duration,renderer:renderer.getContext().getParameter(renderer.getContext().VERSION),roomVisible:roomGroup.visible,room:window.roomEvidence,camera:camera.position.toArray()});
window.setCamera=(pos,target)=>{cameraTourEnabled=false;camera.position.fromArray(pos);viewer.controls.target.fromArray(target);camera.lookAt(new THREE.Vector3().fromArray(target));draw(time)};
const voice=document.querySelector('#voice');document.querySelector('#timeline').max=duration;document.querySelector('#play').onclick=async()=>{if(playing){voice.pause();playing=false;}else{if(time>=duration-.1){voice.currentTime=0;time=0;}await voice.play();playing=true;}document.querySelector('#play').textContent=playing?'Pause':'Play'};document.querySelector('#restart').onclick=async()=>{voice.currentTime=0;await voice.play();playing=true;document.querySelector('#play').textContent='Pause'};document.querySelector('#timeline').oninput=e=>window.seek(+e.target.value);document.querySelector('#room').onclick=e=>{roomGroup.visible=!roomGroup.visible;window.roomBackgroundVisible=roomGroup.visible;e.target.classList.toggle('on',roomGroup.visible);draw(time)};voice.onended=()=>{playing=false;draw(duration);document.querySelector('#play').textContent='Replay'};
function tick(){requestAnimationFrame(tick);if(!window.ready)return;if(playing)draw(voice.currentTime);}requestAnimationFrame(tick);window.addEventListener('resize',()=>{renderer.setSize(root.clientWidth,root.clientHeight);camera.aspect=root.clientWidth/root.clientHeight;camera.updateProjectionMatrix();if(window.ready)draw(time)});if(new URLSearchParams(location.search).has('film'))document.body.classList.add('film');
try{
 await viewer.addSplatScenes([{path:'./assets/ryo_tpose.ply',splatAlphaRemovalThreshold:1},{path:'./assets/ipad-room.ply',splatAlphaRemovalThreshold:1}],{showLoadingUI:false,optimizeSplatData:false});viewer.controls.target.set(.22,1.0,.12);viewer.controls.enableDamping=false;controller=installSkinning(viewer,rig);window.assetEvidence.room='Today iPad Scaniverse Gaussian splat room';window.assetEvidence.task='Original Ryo Gaussian body, transparent-board pen stroke, progressive timing diagram and spatial linked nodes';window.ready=true;document.querySelector('#loading').remove();draw(0);
}catch(e){window.loadError=e.stack;document.querySelector('#error').textContent=e.message;console.error(e)}
