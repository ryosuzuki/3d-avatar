import * as THREE from 'three';
export async function loadCapturedRoom(scene){
 const data=await(await fetch('./assets/room-texture-projection.json')).json();
 const group=new THREE.Group();group.name='Real captured Quest room';scene.add(group);
 const positions=new Float32Array(data.vertices);for(let i=0;i<positions.length;i+=3){positions[i]-=3.5;positions[i+1]+=1.222106;positions[i+2]+=1.7;}
 const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.BufferAttribute(positions,3));
 const grouped=Array.from({length:data.views.length+1},()=>[]);for(let i=0;i<data.triangle_view.length;i++){const bucket=data.unseen[i]?data.views.length:data.triangle_view[i];grouped[bucket].push(...data.triangles.slice(i*3,i*3+3));}
 const indices=[];grouped.forEach((g,j)=>{geometry.addGroup(indices.length,g.length,j);indices.push(...g)});geometry.setIndex(indices);geometry.computeVertexNormals();
 const ins=data.intrinsics,loader=new THREE.TextureLoader();
 const materials=await Promise.all(data.views.map(async v=>{
  const texture=await loader.loadAsync('./assets/'+v.image);texture.colorSpace=THREE.SRGBColorSpace;texture.minFilter=THREE.LinearMipmapLinearFilter;texture.anisotropy=4;
  const pos=new THREE.Vector3(...v.position).add(new THREE.Vector3(-3.5,1.222106,1.7));const matrix=new THREE.Matrix4().compose(pos,new THREE.Quaternion(...v.quaternion),new THREE.Vector3(1,1,1)).invert();
  return new THREE.ShaderMaterial({uniforms:{capturedMap:{value:texture},projectView:{value:matrix},intrinsics:{value:new THREE.Vector4(ins.fx/ins.width,ins.fy/ins.height,ins.cx/ins.width,1-ins.cy/ins.height)}},vertexShader:`uniform mat4 projectView; varying vec3 projected; void main(){projected=(projectView*vec4(position,1.0)).xyz;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}`,fragmentShader:`uniform sampler2D capturedMap;uniform vec4 intrinsics;varying vec3 projected;void main(){float d=-projected.z;vec2 uv=vec2(intrinsics.x*projected.x/d+intrinsics.z,intrinsics.y*projected.y/d+intrinsics.w);if(d<0.05||uv.x<0.0||uv.x>1.0||uv.y<0.0||uv.y>1.0)gl_FragColor=vec4(0.14,0.20,0.23,1.0);else gl_FragColor=texture2D(capturedMap,uv);\n#include <tonemapping_fragment>\n#include <colorspace_fragment>\n}`,side:THREE.DoubleSide});
 }));
 materials.push(new THREE.MeshBasicMaterial({color:0x263c44,side:THREE.DoubleSide}));
 group.add(new THREE.Mesh(geometry,materials));
 window.roomEvidence={capture:data.capture,representation:data.derived_from,geometryTriangles:data.triangles.length/3,sourceViews:data.views.map(x=>({frame:x.frame_index,t:x.timestamp,sourceHash:x.source_sha256})),transform:data.transform,noGeneratedRoom:true,physicalRegistration:false,limits:data.limits};
 return group;
}
