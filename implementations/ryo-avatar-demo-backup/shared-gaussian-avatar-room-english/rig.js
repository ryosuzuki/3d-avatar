import * as THREE from 'three';
const V=(a)=>new THREE.Vector3(...a);
export const FLOOR_OFFSET=1.38675;
// Added, manually fitted rest joints. These are not supplied SMPL-X parameters.
export const BONE_DEFS=[
 ['pelvis',[0,-.51,0],[0,-.13,0]],
 ['chest',[0,-.13,0],[0,.14,0]],
 ['head',[0,.14,0],[0,.43,0]],
 ['right-upper-arm',[-.16,.07,0],[-.405,-.09,0]],
 ['right-forearm',[-.405,-.09,0],[-.64,-.25,0]],
 ['right-hand',[-.64,-.25,0],[-.755,-.295,.015]],
 ['left-upper-arm',[.16,.07,0],[.405,-.09,0]],
 ['left-forearm',[.405,-.09,0],[.64,-.25,0]],
 ['left-hand',[.64,-.25,0],[.755,-.295,.015]],
 ['right-thigh',[-.095,-.49,0],[-.245,-.925,0]],
 ['right-shin',[-.245,-.925,0],[-.325,-1.295,.015]],
 ['right-foot',[-.325,-1.295,.015],[-.342,-1.345,.14]],
 ['left-thigh',[.095,-.49,0],[.245,-.925,0]],
 ['left-shin',[.245,-.925,0],[.325,-1.295,.015]],
 ['left-foot',[.325,-1.295,.015],[.342,-1.345,.14]],
];
const rest=BONE_DEFS.map(([name,a,b])=>({name,a:V(a),b:V(b),length:V(a).distanceTo(V(b))}));
export function twoBone(a,end,l1,l2,pole){
 const d=end.clone().sub(a),distance=Math.min(d.length(),l1+l2-.0001);d.normalize();
 const along=(l1*l1-l2*l2+distance*distance)/(2*distance);
 const height=Math.sqrt(Math.max(0,l1*l1-along*along));
 const bend=pole.clone().sub(d.clone().multiplyScalar(pole.dot(d))).normalize();
 return a.clone().addScaledVector(d,along).addScaledVector(bend,height);
}
function segmentDistanceSquared(x,y,z,a,b){
 const dx=b.x-a.x,dy=b.y-a.y,dz=b.z-a.z;
 const t=Math.max(0,Math.min(1,((x-a.x)*dx+(y-a.y)*dy+(z-a.z)*dz)/(dx*dx+dy*dy+dz*dz)));
 return (x-a.x-dx*t)**2+(y-a.y-dy*t)**2+(z-a.z-dz*t)**2;
}
export function bindGaussians(centers){
 const n=centers.length/3,w=1024,h=Math.ceil(n/w),data=new Float32Array(w*h*4),counts=new Array(15).fill(0);
 for(let i=0;i<n;i++){
  const x=centers[i*3],y=centers[i*3+1],z=centers[i*3+2],side=x<0?0:3,ax=Math.abs(x);
  let candidates;
  if(y<-.48){candidates=[9+side,10+side,11+side];if(y>-.67)candidates.push(0);}
  else if(ax>.21&&y<.14){candidates=[3+side,4+side,5+side];if(ax<.30)candidates.push(1,0);}
  else if(y>.11){candidates=[1,2];}
  else{candidates=[0,1];if(ax>.13&&y>-.19)candidates.push(3+side);}
  let a=-1,b=-1,da=Infinity,db=Infinity;
  for(const j of candidates){const d=segmentDistanceSquared(x,y,z,rest[j].a,rest[j].b);if(d<da){b=a;db=da;a=j;da=d;}else if(d<db){b=j;db=d;}}
  if(b<0){b=a;db=da;}
  // A 6cm blend band retains shape along segments while smoothing joint transitions.
  const ratio=Math.exp(Math.max(-40,(da-db)/(.06*.06))),wa=1/(1+ratio);
  data[i*4]=a;data[i*4+1]=b;data[i*4+2]=wa;data[i*4+3]=1-wa;counts[a]++;
 }
 const texture=new THREE.DataTexture(data,w,h,THREE.RGBAFormat,THREE.FloatType);
 texture.minFilter=texture.magFilter=THREE.NearestFilter;texture.needsUpdate=true;
 return {texture,data,w,h,counts,method:'Added manually fitted 15-bone anatomical segment adapter; two-influence smooth Gaussian LBS, not supplied SMPL-X weights'};
}
export class GaussianRig{
 constructor(){this.matrices=rest.map(()=>new THREE.Matrix4());this.segments=rest.map(()=>[new THREE.Vector3(),new THREE.Vector3()]);this.root=new THREE.Matrix4();this.armErrors=[];}
 update({position,yaw,gait,walking,grip,reach,center,withdraw=0,handTargets=null,handDirections=null,headYaw=0}){
  const bob=walking?.012*Math.cos(gait*2):0;
  const shift=new THREE.Vector3(0,FLOOR_OFFSET+bob,0);
  const local=rest.map(r=>[r.a.clone().add(shift),r.b.clone().add(shift)]);
  this.armErrors=[];
  for(let k=0;k<2;k++){
   const side=k===0?-1:1,ai=k===0?3:6,li=k===0?9:12;
   const shoulder=local[ai][0];
   const relaxed=V([side*.205,.90+bob,.03+(walking?.075*Math.sin(gait+(k?Math.PI:0)):0)]);
   const wristTarget=V([side*(.205+withdraw*.10),center[1],center[2]-.07]);
   const wrist=handTargets&&handTargets[k]?V(handTargets[k]):relaxed.lerp(wristTarget,reach);
   const elbow=twoBone(shoulder,wrist,rest[ai].length,rest[ai+1].length,V([side*.7,0,.8]));
   const reached=elbow.clone().add(wrist.clone().sub(elbow).normalize().multiplyScalar(rest[ai+1].length));
   this.armErrors.push(reached.distanceTo(wrist));
   local[ai]=[shoulder,elbow];local[ai+1]=[elbow,reached];
   const handRelax=reached.clone().add(V([side*.02,-.105,.025]));
   const handGrasp=V([side*(.105+withdraw*.10),center[1]-.007,center[2]+.027]);
   local[ai+2]=[reached,handDirections&&handDirections[k]?reached.clone().add(V(handDirections[k])):handRelax.lerp(handGrasp,reach)];
   const phase=gait+(k?Math.PI:0),stride=walking?.155*Math.sin(phase):0;
   const lift=walking?.075*Math.max(0,Math.cos(phase)):0;
   const hip=local[li][0],ankle=V([side*.115,.084+lift,.025+stride]);
   const knee=twoBone(hip,ankle,rest[li].length,rest[li+1].length,V([0,0,1]));
   local[li]=[hip,knee];local[li+1]=[knee,ankle];
   local[li+2]=[ankle,V([side*.115,.025+lift,.15+stride])];
  }
  this.root.compose(V(position),new THREE.Quaternion().setFromAxisAngle(V([0,1,0]),yaw),V([1,1,1]));
  for(let i=0;i<rest.length;i++){
   const [a,b]=local[i],q=new THREE.Quaternion().setFromUnitVectors(rest[i].b.clone().sub(rest[i].a).normalize(),b.clone().sub(a).normalize());
   if(i===2)q.multiply(new THREE.Quaternion().setFromAxisAngle(V([0,1,0]),headYaw));
   this.matrices[i].makeTranslation(...a.toArray()).multiply(new THREE.Matrix4().makeRotationFromQuaternion(q)).multiply(new THREE.Matrix4().makeTranslation(-rest[i].a.x,-rest[i].a.y,-rest[i].a.z)).premultiply(this.root);
   this.segments[i][0].copy(a).applyMatrix4(this.root);this.segments[i][1].copy(b).applyMatrix4(this.root);
  }
  return this;
 }
}
