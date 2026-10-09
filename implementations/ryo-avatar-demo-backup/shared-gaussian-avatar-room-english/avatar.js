import * as THREE from 'three';
import {bindGaussians,BONE_DEFS} from './rig.js';
export function installSkinning(viewer,rig){
 const controller={};
 let mesh=viewer.getSplatMesh();let centers=new Float32Array(mesh.splatDataTextures.baseData.centers);let binding=bindGaussians(centers);
 const material=mesh.material;
 material.uniforms.addedBinding={value:binding.texture};material.uniforms.addedBindingSize={value:new THREE.Vector2(binding.w,binding.h)};material.uniforms.addedBones={value:rig.matrices};
 material.vertexShader=material.vertexShader.replace('void main () {',`uniform sampler2D addedBinding; uniform vec2 addedBindingSize; uniform mat4 addedBones[15];\nvoid main () {`);
 const src='vec3 splatCenter = uintBitsToFloat(uvec3(sampledCenterColor.gba));';
 if(!material.vertexShader.includes(src)||!material.vertexShader.includes('mat3 J;'))throw Error('Renderer skinning injection anchors missing');
 material.vertexShader=material.vertexShader.replace(src,src+`\nvec4 skin = texture(addedBinding,getDataUV(1,0,addedBindingSize));\nmat4 skinMatrix = addedBones[int(skin.x)]*skin.z + addedBones[int(skin.y)]*skin.w;\nsplatCenter=(skinMatrix*vec4(splatCenter,1.)).xyz;`);
 material.vertexShader=material.vertexShader.replace('mat3 J;',`mat3 skinRotation=mat3(skinMatrix); Vrk=skinRotation*Vrk*transpose(skinRotation);\nmat3 J;`);material.needsUpdate=true;
 viewer.sortWorker?.terminate();viewer.sortWorker=null;viewer.runSplatSort=()=>{};
 const n=centers.length/3;let depth=new Float32Array(n),indexes=new Uint32Array(n),keys=new Uint16Array(n),buckets=new Uint32Array(65536);
 window.assetEvidence={source:'Hyeon Slack p1791493832405329 / ryo_tpose.ply',originalGaussians:160000,renderGaussians:n,avatarRepresentation:'Original anisotropic 3D Gaussian centers, covariance, color and opacity; GPU smooth skin deformation',bindingMethod:binding.method,bindingPrimaryCounts:binding.counts,addedBoneNames:BONE_DEFS.map(x=>x[0]),suppliedSkeleton:false,regenerated:false,billboard:false,room:'Ryo Quest take 20261002_215403; measured geometry; transparent cutaway',sceneTransform:'Quest [x-3.5,y+1.222106,z+1.7] meters; prototype avatar/table placements',physics:'Authored explanation timeline and analytic handIK; no realtimeAI or facial lipsync'};
function sortSkinned(camera){
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

controller.sort=sortSkinned;controller.mesh=mesh;controller.binding=binding;return controller;
}
