import * as THREE from 'three';
import * as GS from './vendor/gaussian-splats-3d.module.js';
import {GaussianRig} from './rig.js';
import {loadCapturedRoom} from './room.js';
import {installSkinning} from './avatar.js';
const story=await(await fetch('./story.json')).json(),duration=story.duration;
const baselineMode=new URLSearchParams(location.search).has('baseline');
const apiPlan=null;
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

const BW=.8,BH=.60,LEFT=-.10,BOTTOM=1.14,BZ=.20;
const boardCanvas=document.createElement('canvas');boardCanvas.width=1400;boardCanvas.height=882;const bc=boardCanvas.getContext('2d');const boardTex=new THREE.CanvasTexture(boardCanvas);
const board=new THREE.Mesh(new THREE.PlaneGeometry(BW,BH),new THREE.MeshBasicMaterial({map:boardTex,transparent:true,side:THREE.DoubleSide,depthWrite:false}));board.position.set(LEFT+BW/2,BOTTOM+BH/2,BZ);scene.add(board);
function boardPoint(x,y){return new THREE.Vector3(LEFT+x/1400*BW,BOTTOM+(1-y/882)*BH,BZ+.008)}
// Original single-line lettering: every visible line is traversed by the pen tip.
const glyph={A:'0,7 2,0 4,7|1,4 3,4',B:'0,7 0,0 3,0 4,1 4,2 3,3 0,3|3,3 4,4 4,6 3,7 0,7',C:'4,0 1,0 0,1 0,6 1,7 4,7',D:'0,7 0,0 2,0 4,2 4,5 2,7 0,7',E:'4,0 0,0 0,7 4,7|0,3 3,3',F:'0,7 0,0 4,0|0,3 3,3',G:'4,0 1,0 0,1 0,6 1,7 4,7 4,4 2,4',H:'0,0 0,7|4,0 4,7|0,3 4,3',I:'0,0 4,0|2,0 2,7|0,7 4,7',J:'0,6 1,7 3,7 4,6 4,0',K:'0,0 0,7|4,0 0,4 4,7',L:'0,0 0,7 4,7',M:'0,7 0,0 2,3 4,0 4,7',N:'0,7 0,0 4,7 4,0',O:'1,0 3,0 4,1 4,6 3,7 1,7 0,6 0,1 1,0',P:'0,7 0,0 3,0 4,1 4,2 3,3 0,3',Q:'1,0 3,0 4,1 4,6 3,7 1,7 0,6 0,1 1,0|2,5 5,8',R:'0,7 0,0 3,0 4,1 4,2 3,3 0,3|2,3 4,7',S:'4,0 1,0 0,1 0,2 1,3 3,4 4,5 4,6 3,7 0,7',T:'0,0 4,0|2,0 2,7',U:'0,0 0,6 1,7 3,7 4,6 4,0',V:'0,0 2,7 4,0',W:'0,0 1,7 2,4 3,7 4,0',X:'0,0 4,7|4,0 0,7',Y:'0,0 2,3 4,0|2,3 2,7',Z:'0,0 4,0 0,7 4,7','0':'1,0 3,0 4,1 4,6 3,7 1,7 0,6 0,1 1,0','1':'1,1 2,0 2,7|0,7 4,7','2':'0,1 1,0 3,0 4,1 4,2 0,7 4,7','3':'0,0 4,0 2,3 4,4 4,6 3,7 0,7','+':'0,3 4,3|2,1 2,5','=':'0,2 4,2|0,5 4,5','%':'0,7 4,0|0,0 1,0 1,1 0,1 0,0|3,6 4,6 4,7 3,7 3,6','-':'0,3 4,3','/':'0,7 4,0','.':'2,6 2,7'};
const pages=[];let paths;
function stroke(points,color='#a2ffe3'){paths.push({points,color,length:points.slice(1).reduce((a,v,i)=>a+Math.hypot(v[0]-points[i][0],v[1]-points[i][1]),0)})}
function label(s,x,y,size=46,color='#efffff'){let xx=x;for(const ch of s){for(const st of (glyph[ch]||'').split('|'))if(st)stroke(st.split(' ').map(pt=>{const a=pt.split(',').map(Number);return [xx+a[0]*size/7,y+a[1]*size/7]}),color);xx+=size*.82}}
function arrow(x,y,X,Y,color='#a2ffe3'){stroke([[x,y],[X,Y]],color);const a=Math.atan2(Y-y,X-x);stroke([[X-22*Math.cos(a-.55),Y-22*Math.sin(a-.55)],[X,Y],[X-22*Math.cos(a+.55),Y-22*Math.sin(a+.55)]],color)}
function rect(x,y,w,h,color='#a2ffe3'){stroke([[x,y],[x+w,y],[x+w,y+h],[x,y+h],[x,y]],color)}
function circle(x,y,r,color='#ffd68c'){stroke(Array.from({length:49},(_,i)=>[x+r*Math.cos(i/48*Math.PI*2),y+r*Math.sin(i/48*Math.PI*2)]),color)}
paths=[];
stroke([[230,190],[820,190]],'#c1fff0');
stroke([[510,190],[510,535]],'#c1fff0');
circle(510,630,95,'#ffc76b');
const drawPaths=paths;
let penState={x:230,y:190,lift:0};
const liveLines=[];
function line(points,color){const g=new THREE.BufferGeometry().setFromPoints(points);const m=new THREE.LineBasicMaterial({color,transparent:true,opacity:1,depthTest:false});const o=new THREE.Line(g,m);o.renderOrder=50;scene.add(o);liveLines.push(o);return o}
function setLine(o,pts){o.geometry.dispose();o.geometry=new THREE.BufferGeometry().setFromPoints(pts)}
const strokes=drawPaths.map(s=>line(s.points.map(([x,y])=>boardPoint(x,y)),s.color));
const latitude=[];for(let j=0;j<5;j++)latitude.push(line([boardPoint(510,630),boardPoint(510,630)],'#ffc76b'));
const trace=line([boardPoint(890,640),boardPoint(890,640)],'#b3acff');
const axis=line([boardPoint(870,450),boardPoint(870,750),boardPoint(1350,750)],'#729399');
function pendulum(t){const m=smooth((t-9)/6),swing=t>18?.46*Math.sin((t-18)*1.7)*smooth((t-18)/2):0;return {m,swing}}
function transform(x,y,z,t){const {m,swing}=pendulum(t),v=boardPoint(x,y);v.z+=m*.35;const pivot=boardPoint(510,190);pivot.z+=m*.35;v.sub(pivot);if(y>190)v.applyAxisAngle(new THREE.Vector3(0,0,1),swing);v.add(pivot);v.z+=z*m;return v}
function drawBoard(i,p,t){bc.clearRect(0,0,1400,882);boardTex.needsUpdate=true;
 const lengths=drawPaths.map(s=>s.length),total=lengths.reduce((a,b)=>a+b,0);let rem=clamp(t/9)*total,last=[230,190];
 drawPaths.forEach((s,k)=>{let r=Math.max(0,Math.min(s.length,rem));rem-=s.length;const pts=[transform(...s.points[0],0,t)];if(r>0)last=s.points[0];for(let j=1;j<s.points.length;j++){const a=s.points[j-1],b=s.points[j],d=Math.hypot(b[0]-a[0],b[1]-a[1]);if(r>=d){pts.push(transform(...b,0,t));last=b;r-=d}else{if(r>0){last=[lerp(a[0],b[0],r/d),lerp(a[1],b[1],r/d)];pts.push(transform(...last,0,t))}break}}strokes[k].visible=pts.length>1;setLine(strokes[k],pts)});
 const {m,swing}=pendulum(t);latitude.forEach((o,k)=>{o.visible=t>9;const ph=(k+1)*Math.PI/6;const pts=[];for(let j=0;j<=64;j++){const a=j/64*Math.PI*2;let x,y,z;if(k<3){x=510+95*Math.cos(a);y=630+95*Math.sin(a)*Math.cos(ph*m);z=95/1400*BW*Math.sin(a)*Math.sin(ph*m)}else{x=510+95*Math.cos(a)*Math.cos(ph*m);y=630+95*Math.sin(a);z=95/1400*BW*Math.cos(a)*Math.sin(ph*m)}pts.push(transform(x,y,z,t))}setLine(o,pts)});
 const wp=[];const wpP=clamp((t-25)/7);for(let j=0;j<=Math.max(1,Math.floor(wpP*100));j++){const x=890+j*4.3,y=600-100*Math.sin(j/100*Math.PI*4);wp.push(boardPoint(x,y))}trace.visible=t>25;axis.visible=t>24;setLine(trace,wp);
 if(t<9){penState={x:last[0],y:last[1],lift:0};window.penTarget=boardPoint(...last)}else if(t<15){window.penTarget=transform(605,630,0,t)}else if(t<18){window.penTarget=transform(605,630,0,t)}else if(t<24){window.penTarget=transform(650,500,0,t)}else if(t<32){window.penTarget=wp.at(-1)}else{window.penTarget=transform(650,500,0,t)}
 window.morphEvidence={depth:m*.35,swing,waveProgress:wpP,strokes:drawPaths.length};
}
const pen=new THREE.Group();const shaft=new THREE.Mesh(new THREE.CylinderGeometry(.008,.008,.16,12),new THREE.MeshStandardMaterial({color:0xffc15b,metalness:.5,roughness:.3}));shaft.position.y=.095;pen.add(shaft);const tip=new THREE.Mesh(new THREE.ConeGeometry(.008,.03,12),new THREE.MeshStandardMaterial({color:0xffffff}));tip.rotation.z=Math.PI;tip.position.y=.015;pen.add(tip);scene.add(pen);
const headPlanes=[];for(let j=0;j<3;j++){const c=document.createElement('canvas');c.width=330;c.height=270;const tx=new THREE.CanvasTexture(c);const g=new THREE.Mesh(new THREE.PlaneGeometry(330/1400*BW,270/882*BH),new THREE.MeshBasicMaterial({map:tx,transparent:true,side:THREE.DoubleSide,depthWrite:false}));g.userData={canvas:c,tex:tx};scene.add(g);headPlanes.push(g)}
function currentSegment(t){let i=0;for(let j=0;j<story.segments.length;j++)if(t>=story.segments[j].start)i=j;return i}
function phaseProgress(i,t){const s=story.segments[i];return clamp((t-s.start)/s.duration)}
let cameraTourEnabled=true;viewer.controls.addEventListener('start',()=>{cameraTourEnabled=false});
function draw(t){time=Math.max(0,Math.min(duration,t));const i=currentSegment(time),p=phaseProgress(i,time);if(cameraTourEnabled){camera.position.set(.05+smooth((time-10)/8)*.45,1.75,3.10);const at=new THREE.Vector3(.43,1.05,.14);camera.lookAt(at);viewer.controls.target.copy(at);camera.updateMatrixWorld()}
 drawBoard(i,p,time);
 const desired=window.penTarget.clone(),rootPos=[.14,0,-.05];shadow.position.x=rootPos[0];const wrist=desired.clone().add(new THREE.Vector3(-.02,-.055,-.10-penState.lift));const local=wrist.clone().sub(new THREE.Vector3(...rootPos));
 rig.update({position:rootPos,yaw:0,gait:0,walking:false,grip:true,reach:0,center:[0,1.1,.3],handTargets:[[-.205,.94,.09],local.toArray()],handDirections:[[0,-.11,.02],[.02,.055,.10]],headYaw:.17});
 pen.position.copy(desired);pen.position.z-=penState.lift;pen.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),new THREE.Vector3(-.02,-.055,-.1).normalize());
 headPlanes.forEach((g,j)=>{g.visible=false;g.position.copy(boardPoint(255+j*420,385));g.position.z+=smooth((p-.82)*8)*(j+1)*.17;});
 const hand=rig.segments[8][1];
 viewer.update();window.debugMode=2;controller.sort(camera);viewer.render();renderer.autoClear=false;renderer.clearDepth();scene.background=null;window.debugMode=1;controller.sort(camera);viewer.render();window.debugMode=0;renderer.autoClear=true;scene.background=new THREE.Color(0x102333);const bg=scene.background;scene.background=null;renderer.autoClear=false;renderer.render(scene,camera);renderer.autoClear=true;scene.background=bg;
 document.querySelector('#chaptertext').textContent=String(i+1).padStart(2,'0')+' / '+story.segments[i].headline;document.querySelector('#headline').textContent=story.segments[i].headline;
 // Short sentence-level captions share each measured speech segment.
 const sentences=story.segments[i].narration.match(/[^.!?]+[.!?]+/g)||[story.segments[i].narration];const total=sentences.reduce((n,s)=>n+s.length,0);let cursor=0,cap=sentences.at(-1);for(const s of sentences){cursor+=s.length/total;if(p<=cursor){cap=s.trim();break}}
 document.querySelector('#caption').textContent=time>=story.segments[i].start&&time<=story.segments[i].end?cap:'';document.querySelector('#progress i').style.width=(time/duration*100)+'%';document.querySelector('#marker').textContent=time.toFixed(1)+' / '+duration.toFixed(1)+' s';document.querySelector('#timeline').value=time;
 window.state={time,segment:story.segments[i].id,pointing:true,penTip:pen.position.toArray(),contactError:pen.position.distanceTo(desired),penLift:penState.lift,desiredPoint:desired.toArray(),leftHand:hand.toArray(),armErrors:rig.armErrors.slice(),root:rootPos,diagram:story.segments[i].headline,illustrative:true};return window.state;
}
window.drawFrame=t=>{playing=false;return draw(t)};window.seek=t=>{playing=false;document.querySelector('#voice').pause();document.querySelector('#voice').currentTime=t;return draw(t)};window.getEvidence=()=>({asset:window.assetEvidence,state:window.state,voice:story.voice,apiPlan,duration,renderer:renderer.getContext().getParameter(renderer.getContext().VERSION),roomVisible:roomGroup.visible,room:window.roomEvidence,camera:camera.position.toArray()});
window.setCamera=(pos,target)=>{cameraTourEnabled=false;camera.position.fromArray(pos);viewer.controls.target.fromArray(target);camera.lookAt(new THREE.Vector3().fromArray(target));draw(time)};
let questionEnd=null;const conversation=[];const voice=document.querySelector('#voice');document.querySelector('#timeline').max=duration;document.querySelector('#play').onclick=async()=>{if(playing){voice.pause();playing=false;}else{if(time>=duration-.1){voice.currentTime=0;time=0;}await voice.play();playing=true;}document.querySelector('#play').textContent=playing?'Pause':'Play'};document.querySelector('#restart').onclick=async()=>{voice.currentTime=0;await voice.play();playing=true;document.querySelector('#play').textContent='Pause'};document.querySelector('#timeline').oninput=e=>window.seek(+e.target.value);document.querySelector('#room').onclick=e=>{roomGroup.visible=!roomGroup.visible;window.roomBackgroundVisible=roomGroup.visible;e.target.classList.toggle('on',roomGroup.visible);draw(time)};voice.onended=()=>{playing=false;draw(duration);document.querySelector('#play').textContent='Replay'};
function tick(){requestAnimationFrame(tick);if(!window.ready)return;if(playing){draw(voice.currentTime);if(questionEnd!==null&&voice.currentTime>=questionEnd){voice.pause();playing=false;questionEnd=null;document.querySelector('#play').textContent='Play'}}}requestAnimationFrame(tick);window.addEventListener('resize',()=>{renderer.setSize(root.clientWidth,root.clientHeight);camera.aspect=root.clientWidth/root.clientHeight;camera.updateProjectionMatrix();if(window.ready)draw(time)});if(new URLSearchParams(location.search).has('film'))document.body.classList.add('film');
try{
 await viewer.addSplatScenes([{path:'./assets/ryo_tpose.ply',splatAlphaRemovalThreshold:1},{path:'./assets/ipad-room.ply',splatAlphaRemovalThreshold:1}],{showLoadingUI:false,optimizeSplatData:false});viewer.controls.target.set(.22,1.0,.12);viewer.controls.enableDamping=false;controller=installSkinning(viewer,rig);window.assetEvidence.room='Today iPad Scaniverse Gaussian splat room';window.assetEvidence.task='Living pendulum sketch; original Ryo Gaussian avatar and today iPad room';window.ready=true;document.querySelector('#loading').remove();draw(0);
}catch(e){window.loadError=e.stack;document.querySelector('#error').textContent=e.message;console.error(e)}
