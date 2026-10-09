import * as THREE from 'three';
import * as GS from './vendor/gaussian-splats-3d.module.js';
import {GaussianRig,bindGaussians,BONE_DEFS} from './rig.js';
const root=document.querySelector('#root'),scene=new THREE.Scene();
scene.background=new THREE.Color(0xd5e1e3);
scene.add(new THREE.HemisphereLight(0xffffff,0x58616b,2.5));
const sun=new THREE.DirectionalLight(0xffffff,2);sun.position.set(3,6,5);scene.add(sun);
const renderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});renderer.setPixelRatio(1);renderer.setSize(root.clientWidth,root.clientHeight);root.appendChild(renderer.domElement);renderer.outputColorSpace=THREE.SRGBColorSpace;
const camera=new THREE.PerspectiveCamera(45,root.clientWidth/root.clientHeight,.03,100);camera.position.set(2.8,2.35,3.7);camera.lookAt(-.15,.91,.64);
const viewer=new GS.Viewer({rootElement:root,renderer,camera,threeScene:scene,selfDrivenMode:false,dynamicScene:false,useBuiltInControls:true,enableOptionalEffects:false,gpuAcceleratedSort:false,sharedMemoryForWorkers:true,enableSIMDInSort:true,integerBasedSort:true,halfPrecisionCovariancesOnGPU:false,sphericalHarmonicsDegree:0,sceneRevealMode:GS.SceneRevealMode.Instant,optimizeSplatData:false,ignoreDevicePixelRatio:true});
window.viewer=viewer;window.ready=false;
const rig=new GaussianRig(),scanGroup=new THREE.Group();scene.add(scanGroup);
const boxSize=.28,initialBox=new THREE.Vector3(.48,1.09,0),finalBox=new THREE.Vector3(0,1.09,1.88);
const cube=new THREE.Mesh(new THREE.BoxGeometry(boxSize,boxSize,boxSize),new THREE.MeshStandardMaterial({color:0xf1a04c,roughness:.45}));cube.position.copy(initialBox);scene.add(cube);
const edges=new THREE.LineSegments(new THREE.EdgesGeometry(cube.geometry),new THREE.LineBasicMaterial({color:0x9c5418}));cube.add(edges);
const labelCanvas=document.createElement('canvas');labelCanvas.width=256;labelCanvas.height=128;const lc=labelCanvas.getContext('2d');lc.fillStyle='#173344';lc.fillRect(0,0,256,128);lc.fillStyle='#fff';lc.font='bold 28px sans-serif';lc.textAlign='center';lc.fillText('MOVE ME',128,76);const decal=new THREE.Mesh(new THREE.PlaneGeometry(.21,.09),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(labelCanvas)}));decal.position.set(0,0,.141);cube.add(decal);
function table(x,z,color){
 const group=new THREE.Group();group.position.set(x,0,z);scene.add(group);
 const mat=new THREE.MeshStandardMaterial({color,roughness:.6}),top=new THREE.Mesh(new THREE.BoxGeometry(.64,.065,.6),mat);top.position.y=.918;group.add(top);
 for(const dx of [-.245,.245])for(const dz of [-.21,.21]){const leg=new THREE.Mesh(new THREE.BoxGeometry(.045,.888,.045),mat);leg.position.set(dx,.444,dz);group.add(leg);}
}
table(.60,0,0x456575);table(0,1.88,0x456575);
const floor=new THREE.Mesh(new THREE.PlaneGeometry(12,12),new THREE.MeshStandardMaterial({color:0xc9d7db,roughness:.95}));floor.rotation.x=-Math.PI/2;floor.position.y=-.013;scene.add(floor);
const grid=new THREE.GridHelper(12,24,0x879ca7,0xb6c7cf);grid.position.y=-.010;scene.add(grid);
function marker(x,z,text,color){const c=document.createElement('canvas');c.width=512;c.height=128;const ctx=c.getContext('2d');ctx.fillStyle=color;ctx.fillRect(0,0,512,128);ctx.fillStyle='#fff';ctx.font='bold 38px sans-serif';ctx.textAlign='center';ctx.fillText(text,256,78);const m=new THREE.Mesh(new THREE.PlaneGeometry(.72,.18),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(c),transparent:true}));m.rotation.x=-Math.PI/2;m.position.set(x,.001,z);scene.add(m);}
marker(-1.2,-.38,'START','#365965');marker(.6,-.52,'PICK UP','#a06628');marker(0,2.4,'PLACE','#387966');
const route=new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(-1.2,.006,0),new THREE.Vector3(0,.006,0),new THREE.Vector3(0,.006,1.4)]),new THREE.LineDashedMaterial({color:0x2e9386,dashSize:.10,gapSize:.08}));route.computeLineDistances();scene.add(route);
const rigGroup=new THREE.Group(),overlayScene=new THREE.Scene();rigGroup.visible=false;overlayScene.add(rigGroup);const rigLines=new THREE.LineSegments(new THREE.BufferGeometry().setAttribute('position',new THREE.BufferAttribute(new Float32Array(15*6),3)),new THREE.LineBasicMaterial({color:0x31f7c5,depthTest:false,transparent:true,opacity:.85}));rigLines.renderOrder=5;rigGroup.add(rigLines);
const clamp=(x)=>Math.min(1,Math.max(0,x)),smooth=(x)=>{x=clamp(x);return x*x*(3-2*x);},lerp=(a,b,t)=>a+(b-a)*t;
let playing=false,time=0,last=performance.now(),frameCount=0,stopAt=18,mesh,binding,centers,depth,indexes,keys,buckets;
let trackedPose=null;
let manual=false, manualPosition=[-1.2,0,0],manualYaw=Math.PI/2,manualGait=0,manualWalking=false;
const pressed=new Set();
window.addEventListener('keydown',e=>{if(['w','a','s','d'].includes(e.key.toLowerCase())){e.preventDefault();if(!manual){manualPosition=window.state.avatarRoot.slice();manualYaw=window.state.yaw;}manual=true;playing=false;pressed.add(e.key.toLowerCase());}});
window.addEventListener('keyup',e=>pressed.delete(e.key.toLowerCase()));
window.addEventListener('blur',()=>pressed.clear());
function taskState(t){
 if(manual)return {position:manualPosition.slice(),yaw:manualYaw,walking:manualWalking,gait:manualGait,reach:0,center:[0,1.09,.48],attached:false,grip:false,withdraw:0,phase:'Free walk · W/S move · A/D turn'};
 let position=[-1.2,0,0],yaw=Math.PI/2,walking=false,gait=0,reach=0,center=[0,1.09,.48],attached=false,phase='Ready · run the task',withdraw=0;
 if(t>=1&&t<5){const p=(t-1)/4;position=[lerp(-1.2,0,p),0,0];walking=true;gait=(t-1)*Math.PI*2*1.18;phase='1 · Walk to the box';}
 else if(t>=5){position=[0,0,0];phase='2 · Reach with both hands';reach=smooth(t-5);}
 if(t>=6&&t<7){attached=true;phase='3 · Grasp and lift';center=[0,lerp(1.09,1.33,smooth(t-6)),lerp(.48,.42,smooth(t-6))];}
 else if(t>=7&&t<8){attached=true;center=[0,1.33,.42];phase='3 · Box attached to palms';}
 else if(t>=8&&t<9){attached=true;center=[0,1.33,.42];yaw=lerp(Math.PI/2,0,smooth(t-8));phase='4 · Turn while holding';}
 else if(t>=9&&t<13){attached=true;center=[0,1.33,.42];yaw=0;position=[0,0,lerp(0,1.4,(t-9)/4)];walking=true;gait=(t-9)*Math.PI*2*1.18;phase='5 · Carry to the other table';}
 else if(t>=13&&t<14){attached=true;position=[0,0,1.4];yaw=0;center=[0,lerp(1.33,1.09,smooth(t-13)),lerp(.42,.48,smooth(t-13))];phase='6 · Place the box';}
 else if(t>=14){position=[0,0,1.4];yaw=0;center=[0,1.09,.48];withdraw=smooth((t-14)/.45);reach=1-smooth((t-14.45)/.55);phase='7 · Release · box stays on table';}
 if(t>=15&&t<17){position=[0,0,lerp(1.4,.8,(t-15)/2)];walking=true;gait=(t-15)*Math.PI*2*1.18;phase='8 · Step back · hands free';}
 if(t>=17){position=[0,0,.8];phase='Complete · box transferred';}
 return {position,yaw,walking,gait,reach,center,attached,grip:attached,withdraw,phase};
}
function installSkinning(){
 mesh=viewer.getSplatMesh();centers=new Float32Array(mesh.splatDataTextures.baseData.centers);binding=bindGaussians(centers);
 const material=mesh.material;
 material.uniforms.addedBinding={value:binding.texture};material.uniforms.addedBindingSize={value:new THREE.Vector2(binding.w,binding.h)};material.uniforms.addedBones={value:rig.matrices};
 material.vertexShader=material.vertexShader.replace('void main () {',`uniform sampler2D addedBinding; uniform vec2 addedBindingSize; uniform mat4 addedBones[15];\nvoid main () {`);
 const src='vec3 splatCenter = uintBitsToFloat(uvec3(sampledCenterColor.gba));';
 if(!material.vertexShader.includes(src)||!material.vertexShader.includes('mat3 J;'))throw Error('Renderer skinning injection anchors missing');
 material.vertexShader=material.vertexShader.replace(src,src+`\nvec4 skin = texture(addedBinding,getDataUV(1,0,addedBindingSize));\nmat4 skinMatrix = addedBones[int(skin.x)]*skin.z + addedBones[int(skin.y)]*skin.w;\nsplatCenter=(skinMatrix*vec4(splatCenter,1.)).xyz;`);
 material.vertexShader=material.vertexShader.replace('mat3 J;',`mat3 skinRotation=mat3(skinMatrix); Vrk=skinRotation*Vrk*transpose(skinRotation);\nmat3 J;`);material.needsUpdate=true;
 viewer.sortWorker?.terminate();viewer.sortWorker=null;viewer.runSplatSort=()=>{};
 const n=centers.length/3;depth=new Float32Array(n);indexes=new Uint32Array(n);keys=new Uint16Array(n);buckets=new Uint32Array(65536);
 window.assetEvidence={source:'Hyeon Slack p1791493832405329 / ryo_tpose.ply',originalGaussians:160000,renderGaussians:n,avatarRepresentation:'Original anisotropic 3D Gaussian centers, covariance, color and opacity; GPU smooth skin deformation',bindingMethod:binding.method,bindingPrimaryCounts:binding.counts,addedBoneNames:BONE_DEFS.map(x=>x[0]),suppliedSkeleton:false,regenerated:false,billboard:false,room:'Ryo Quest take 20261002_215403; measured geometry; transparent cutaway',sceneTransform:'Quest [x-3.5,y+1.222106,z+1.7] meters; prototype avatar/table placements',physics:'Scripted gait, analytic two-arm IK, deterministic object attachment; no physics engine or autonomous policy'};
}
function sortSkinned(){
 // Depth-sort deformed centers, not the original rest pose. Counting sort is O(N).
 camera.updateMatrixWorld();const vm=camera.matrixWorldInverse,rows=new Float32Array(15*4),temp=new THREE.Matrix4();
 for(let j=0;j<15;j++){temp.multiplyMatrices(vm,rig.matrices[j]);const e=temp.elements;rows.set([e[2],e[6],e[10],e[14]],j*4);}
 let min=Infinity,max=-Infinity;const bd=binding.data;
 for(let i=0;i<depth.length;i++){const x=centers[i*3],y=centers[i*3+1],z=centers[i*3+2],a=bd[i*4]*4,b=bd[i*4+1]*4,wa=bd[i*4+2],wb=bd[i*4+3];const d=wa*(rows[a]*x+rows[a+1]*y+rows[a+2]*z+rows[a+3])+wb*(rows[b]*x+rows[b+1]*y+rows[b+2]*z+rows[b+3]);depth[i]=d;if(d<min)min=d;if(d>max)max=d;}
 buckets.fill(0);const scale=65534/Math.max(1e-6,max-min);
 for(let i=0;i<depth.length;i++){const k=Math.floor((depth[i]-min)*scale);keys[i]=k;buckets[k]++;}
 let sum=0;for(let k=0;k<65536;k++){const n=buckets[k];buckets[k]=sum;sum+=n;}
 for(let i=0;i<depth.length;i++)indexes[buckets[keys[i]]++]=i;
 mesh.updateRenderIndexes(indexes,indexes.length);
}
function readback(s){
 const palmCenter=new THREE.Vector3(0,s.center[1],s.center[2]).applyMatrix4(rig.root);
 return {time,phase:s.phase,avatarRoot:s.position,yaw:s.yaw,walking:s.walking,attached:s.attached,box:cube.position.toArray(),boxQuaternion:cube.quaternion.toArray(),graspCenter:palmCenter.toArray(),attachmentError:s.attached?cube.position.distanceTo(palmCenter):null,armIKErrors:rig.armErrors.slice(),rightHand:rig.segments[5].map(p=>p.toArray()),leftHand:rig.segments[8].map(p=>p.toArray()),feet:[rig.segments[11][0].toArray(),rig.segments[14][0].toArray()],renderedFrame:frameCount};
}
function draw(t){
 time=Math.max(0,Math.min(18,t));const s=taskState(time);rig.update(s);if(trackedPose){rig.applySegments(trackedPose.segments,trackedPose.position,trackedPose.yaw);s.phase="Recorded/live body pose · "+trackedPose.source;s.position=trackedPose.position;s.yaw=trackedPose.yaw;s.walking=false;s.attached=false;}
 if(s.attached){cube.position.set(0,s.center[1],s.center[2]).applyMatrix4(rig.root);cube.quaternion.setFromAxisAngle(new THREE.Vector3(0,1,0),s.yaw);}
 else{cube.position.copy(time>=14?finalBox:initialBox);cube.quaternion.setFromAxisAngle(new THREE.Vector3(0,1,0),time>=14?0:Math.PI/2);}
 const rp=rigLines.geometry.attributes.position;for(let i=0;i<15;i++){rp.setXYZ(i*2,...rig.segments[i][0].toArray());rp.setXYZ(i*2+1,...rig.segments[i][1].toArray());}rp.needsUpdate=true;
 viewer.update();sortSkinned();viewer.render();if(rigGroup.visible){const auto=renderer.autoClear;renderer.autoClear=false;renderer.render(overlayScene,camera);renderer.autoClear=auto;}frameCount++;
 document.querySelector('#phase').textContent=s.phase;document.querySelector('#grip').textContent=s.attached?'Box: held by both palms':time>=14?'Box: released · stationary on destination':'Box: on pickup table';document.querySelector('#time').textContent=time.toFixed(1)+' / 18.0 s';document.querySelector('#timeline').value=time;document.querySelector('#pause').textContent=playing?'Pause':time===0?'Play':time>=18?'Replay':'Resume';window.state=readback(s);
 return window.state;
}
window.seek=t=>{playing=false;return draw(t);};window.drawFrame=t=>{playing=false;return draw(t);};window.getEvidence=()=>({asset:window.assetEvidence,state:window.state,renderer:renderer.getContext().getParameter(renderer.getContext().VERSION),roomVisible:scanGroup.visible,rigVisible:rigGroup.visible});window.setCamera=(p,target)=>{camera.position.fromArray(p);viewer.controls.target.fromArray(target);camera.lookAt(new THREE.Vector3().fromArray(target));draw(time);};
document.querySelector('#run').onclick=()=>{manual=false;time=0;stopAt=18;playing=true;last=performance.now();};
document.querySelector('#pause').onclick=e=>{if(time>=18)time=0;playing=!playing;last=performance.now();e.target.textContent=playing?'Pause':'Resume';};
document.querySelector('#walk').onclick=()=>{manual=false;time=1;stopAt=5;playing=true;last=performance.now();};
document.querySelector('#grasp').onclick=()=>{manual=false;time=5;stopAt=18;playing=true;last=performance.now();};
document.querySelector('#reset').onclick=()=>{manual=false;playing=false;draw(0);};
document.querySelector('#timeline').oninput=e=>{playing=false;draw(+e.target.value);};
document.querySelector('#room').onclick=e=>{scanGroup.visible=!scanGroup.visible;e.target.classList.toggle('on',scanGroup.visible);draw(time);};
document.querySelector('#rig').onclick=e=>{rigGroup.visible=!rigGroup.visible;e.target.classList.toggle('on',rigGroup.visible);draw(time);};
function tick(now){requestAnimationFrame(tick);if(!window.ready)return;const dt=Math.min(.15,(now-last)/1000);last=now;if(manual){const forward=Number(pressed.has('w'))-Number(pressed.has('s'));manualYaw+=(Number(pressed.has('a'))-Number(pressed.has('d')))*dt*1.6;manualWalking=forward!==0;if(manualWalking){manualGait+=dt*Math.PI*2*1.18;manualPosition[0]+=Math.sin(manualYaw)*forward*dt*.5;manualPosition[2]+=Math.cos(manualYaw)*forward*dt*.5;}}if(playing){time+=dt;if(time>=stopAt){time=stopAt;playing=false;}}draw(time);}requestAnimationFrame(tick);
window.addEventListener('resize',()=>{renderer.setSize(root.clientWidth,root.clientHeight);camera.aspect=root.clientWidth/root.clientHeight;camera.updateProjectionMatrix();});
try{
 const room=await (await fetch('./assets/quest-room-geometry.json')).json();
 const colors={GLOBAL_MESH:0x668393,STORAGE:0x456878,TABLE:0x688899,COUCH:0x75898e,BED:0x7a9899,WALL_FACE:0x99abb3,FLOOR:0x8a9fa4};
 for(let i=0;i<34;i++){const p=room.parts[i];if(!p||['CEILING','FLOOR'].includes(p.label))continue;const positions=new Float32Array(p.vertices);for(let j=0;j<positions.length;j+=3){positions[j]-=3.5;positions[j+1]+=1.222106;positions[j+2]+=1.7;}const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(positions,3));g.setIndex(p.triangles);g.computeVertexNormals();const global=p.label==='GLOBAL_MESH',m=new THREE.MeshStandardMaterial({color:colors[p.label]||0x96a7ad,side:THREE.DoubleSide,transparent:true,opacity:global?.095:['WALL_FACE','DOOR_FRAME','WINDOW_FRAME'].includes(p.label)?.13:.21,depthWrite:false,roughness:.9});const part=new THREE.Mesh(g,m);scanGroup.add(part);}
 await viewer.addSplatScene('./assets/ryo_tpose.ply',{splatAlphaRemovalThreshold:1,showLoadingUI:false,progressiveLoad:false,optimizeSplatData:false});
 viewer.controls.target.set(-.15,.91,.64);viewer.controls.enableDamping=false;viewer.controls.maxDistance=16;viewer.controls.minDistance=2;
 installSkinning();window.ready=true;draw(0);
 document.querySelector('#status').textContent='160,000 source Gaussians · live articulated body';document.querySelector('#loading').textContent='Same avatar · smooth deformation · real captured room';
}catch(e){window.loadError=e.stack;document.querySelector('#error').textContent=e.message;console.error(e);}

window.poseDriver={
 setPose(p){if(!p||!Array.isArray(p.segments)||p.segments.length!==15||!p.segments.flat(2).every(Number.isFinite))throw Error('Expected15 finite segment pairs');playing=false;manual=false;trackedPose={segments:p.segments,position:p.position||[0,0,0],yaw:p.yaw||0,source:p.source||'external pose'};draw(time);},
 clear(){trackedPose=null;},
 getRest(){return BONE_DEFS.map(([name,a,b])=>({name,a:[a[0],a[1]+1.38675,a[2]],b:[b[0],b[1]+1.38675,b[2]]}));},
 getState(){return {tracked:!!trackedPose,segments:rig.segments.map(x=>x.map(v=>v.toArray())),root:rig.root.toArray()};}
};
