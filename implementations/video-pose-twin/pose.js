import {PoseLandmarker,FilesetResolver} from './vendor/mediapipe/vision_bundle.mjs';
import * as THREE from 'three';
const video=document.querySelector('#sourceVideo'),canvas=document.querySelector('#landmarks'),ctx=canvas.getContext('2d'),status=document.querySelector('#poseStatus');
let tracker,tracks=[],live=false,anchor=null,lastLive=-1,lastPose=null;window.poseEvidence={inferenceCount:0,lostFrames:0,cameraActivated:false,source:'PXL_20261008_192648621.mp4 source26–44s',method:'MediaPipe Pose Landmarker Lite VIDEO, world landmarks →15-bone Gaussian adapter'};
const v=a=>new THREE.Vector3(...a),arr=a=>a.toArray();
const point=(w,i)=>v([w[i].x,-w[i].y,-w[i].z]);
const mid=(a,b)=>a.clone().add(b).multiplyScalar(.5);
function endpoint(start,a,b,len){const d=b.clone().sub(a);if(d.length()<1e-5)d.set(0,-1,0);return start.clone().addScaledVector(d.normalize(),len);}
function retarget(frame){
 const w=frame.world,n=frame.image;if(!w||w.length<33)return null;
 const axis=point(w,23).sub(point(w,24));const yaw=Math.atan2(-axis.z,axis.x);const inv=new THREE.Quaternion().setFromAxisAngle(v([0,1,0]),-yaw);const p=i=>point(w,i).applyQuaternion(inv),hip=mid(p(23),p(24)),shoulder=mid(p(11),p(12)),up=shoulder.clone().sub(hip).normalize(),right=p(23).sub(p(24)).normalize();
 const root=v([0,.887,0]),chest=root.clone().addScaledVector(up,.38),neck=chest.clone().addScaledVector(up,.27),head=neck.clone().addScaledVector(up,.29);
 const seg=[[arr(root),arr(chest)],[arr(chest),arr(neck)],[arr(neck),arr(head)]];
 for(const [a,b,c,d,side] of [[12,14,16,20,-1],[11,13,15,19,1]]){const s=chest.clone().addScaledVector(up,.20).addScaledVector(right,side*.16),el=endpoint(s,p(a),p(b),.293),wr=endpoint(el,p(b),p(c),.285),hand=endpoint(wr,p(c),p(d),.123);seg.push([arr(s),arr(el)],[arr(el),arr(wr)],[arr(wr),arr(hand)]);}
 for(const [a,b,c,d,side] of [[24,26,28,32,-1],[23,25,27,31,1]]){const h=root.clone().addScaledVector(right,side*.095),k=endpoint(h,p(a),p(b),.460),ank=endpoint(k,p(b),p(c),.379),foot=endpoint(ank,p(c),p(d),.135);seg.push([arr(h),arr(k)],[arr(k),arr(ank)],[arr(ank),arr(foot)]);}
 const bottom=Math.min(...seg.slice(9).flat().map(a=>a[1]));for(const pair of seg)for(const q of pair)q[1]+=.035-bottom;
 const hipx=(n[23].x+n[24].x)/2,height=Math.max(.25,Math.max(n[27].y,n[28].y)-Math.min(n[0].y,n[11].y,n[12].y));
 if(!anchor)anchor={x:hipx,height};
 const rootx=Math.max(-1,Math.min(1,(hipx-anchor.x)*1.8/anchor.height*video.videoWidth/video.videoHeight)),rootz=Math.max(-.6,Math.min(.6,(anchor.height/height-1)*2));
 return {segments:seg,position:[rootx,0,rootz],yaw,source:live?'local camera estimation':'recorded video inference'};
}
function overlay(frame){canvas.width=video.videoWidth;canvas.height=video.videoHeight;ctx.clearRect(0,0,canvas.width,canvas.height);if(!frame)return;const n=frame.image;ctx.strokeStyle='#70ffc8';ctx.lineWidth=3;ctx.fillStyle='#d7fff1';for(const [a,b] of [[11,12],[11,13],[13,15],[12,14],[14,16],[11,23],[12,24],[23,24],[23,25],[25,27],[24,26],[26,28]]){if(n[a].visibility<.3||n[b].visibility<.3)continue;ctx.beginPath();ctx.moveTo(n[a].x*canvas.width,n[a].y*canvas.height);ctx.lineTo(n[b].x*canvas.width,n[b].y*canvas.height);ctx.stroke();}for(const p of n){if(p.visibility<.3)continue;ctx.beginPath();ctx.arc(p.x*canvas.width,p.y*canvas.height,3,0,Math.PI*2);ctx.fill();}}
async function getTracker(){if(!tracker){const files=await FilesetResolver.forVisionTasks('./vendor/mediapipe/wasm');tracker=await PoseLandmarker.createFromOptions(files,{baseOptions:{modelAssetPath:'./assets/pose_landmarker_lite.task',delegate:'CPU'},runningMode:'VIDEO',numPoses:1,minPoseDetectionConfidence:.5,minPosePresenceConfidence:.5,minTrackingConfidence:.5});}return tracker;}
function infer(t){const r=tracker.detectForVideo(video,t);window.poseEvidence.inferenceCount++;if(!r.landmarks.length){window.poseEvidence.lostFrames++;return null;}return {time:video.currentTime,image:r.landmarks[0],world:r.worldLandmarks[0]};}
function apply(frame){if(!frame||!window.ready)return;lastPose=frame;const pose=retarget(frame);window.poseDriver.setPose(pose);overlay(frame);window.currentPose={time:frame.time,root:pose.position,segments:pose.segments};status.textContent=`${live?'LIVE':'TRACKED'} · ${frame.time.toFixed(1)} s · ${frame.image.length} landmarks`;}
window.trackVideo=async(step=.1)=>{await getTracker();if(video.readyState<2)await new Promise(r=>video.addEventListener('loadeddata',r,{once:true}));video.pause();const result=[];for(let t=0;t<video.duration-.08;t+=step){video.currentTime=t;await new Promise(r=>video.addEventListener('seeked',r,{once:true}));const frame=infer(t*1000+100);if(frame)result.push(frame);}tracks=result;video.currentTime=0;return {frames:result,evidence:window.poseEvidence};};
window.seekVideo=async t=>{video.pause();video.currentTime=t;await new Promise(r=>video.addEventListener('seeked',r,{once:true}));const f=nearest(t);apply(f);return window.currentPose;};
function nearest(t){if(!tracks.length)return null;let best=tracks[0];for(const f of tracks){if(Math.abs(f.time-t)<Math.abs(best.time-t))best=f;}return best;}
function tick(){requestAnimationFrame(tick);if(!window.ready)return;if(live&&tracker&&video.readyState>=2){if(video.currentTime!==lastLive){lastLive=video.currentTime;const f=infer(performance.now());if(f)apply(f);else status.textContent='Tracking lost · last pose held';}}else if(tracks.length){apply(nearest(video.currentTime));document.querySelector('#videoSeek').value=video.currentTime;}}requestAnimationFrame(tick);
document.querySelector('#videoPlay').onclick=()=>video.paused?video.play():video.pause();
document.querySelector('#videoSeek').oninput=e=>{video.currentTime=+e.target.value;};
document.querySelector('#reanchor').onclick=()=>{anchor=null;if(lastPose)apply(lastPose);};
document.querySelector('#webcam').onclick=async()=>{try{video.pause();await getTracker();const stream=await navigator.mediaDevices.getUserMedia({video:{width:640,height:480},audio:false});video.srcObject=stream;live=true;anchor=null;window.poseEvidence.cameraActivated=true;await video.play();document.querySelector('#sourceTag').textContent='Local camera · no upload';}catch(e){status.textContent='Camera unavailable: '+e.message;}};
document.querySelector('#recorded').onclick=()=>{video.srcObject?.getTracks().forEach(t=>t.stop());video.srcObject=null;video.src='./assets/ryo-source.mp4';live=false;anchor=null;document.querySelector('#sourceTag').textContent='Ryo’s recorded video ·26–44s excerpt';};
try{const r=await fetch('./assets/pose-tracks.json');if(r.ok){const d=await r.json();tracks=d.frames;window.poseEvidence.recordedInference=d.evidence;status.textContent=`Ready · ${tracks.length} actual inferred poses`;}}catch{}
const readyTimer=setInterval(()=>{if(window.ready){clearInterval(readyTimer);window.setCamera([0,1.4,3.6],[0,.95,0]);document.querySelector('#status').textContent='Original 160,000-Gaussian body';window.poseUIReady=true;}},100);
