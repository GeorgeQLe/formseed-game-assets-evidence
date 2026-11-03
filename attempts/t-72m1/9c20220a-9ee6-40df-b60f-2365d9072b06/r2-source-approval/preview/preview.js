import * as T from 'three';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
const embedded=window.T72_DATA;
const loader=new GLTFLoader();
const bytes=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0)).buffer;
const gltf=await loader.parseAsync(bytes(embedded.glb),'');
const scene=new T.Scene();scene.background=new T.Color('#202a30');scene.fog=new T.Fog('#202a30',38,80);
scene.add(new T.HemisphereLight(0xdceafa,0x9a8565,2.1));const sun=new T.DirectionalLight(0xffedcf,3.1);sun.position.set(6,12,8);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);sun.shadow.camera.left=-14;sun.shadow.camera.right=14;sun.shadow.camera.top=14;sun.shadow.camera.bottom=-14;sun.shadow.bias=-.0003;scene.add(sun);
const floor=new T.Mesh(new T.PlaneGeometry(200,200),new T.MeshStandardMaterial({color:0x706c5e,roughness:1}));floor.rotation.x=-Math.PI/2;floor.receiveShadow=true;scene.add(floor);
const tank=gltf.scene;scene.add(tank);tank.traverse(o=>{if(o.isMesh){o.castShadow=true;o.receiveShadow=true;}});
const camera=new T.PerspectiveCamera(40,1280/720,.1,150);camera.position.set(14,11,-18);camera.lookAt(0,3,3);camera.updateMatrixWorld(true);
const renderer=new T.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});renderer.setPixelRatio(1);renderer.setSize(1280,720);renderer.shadowMap.enabled=true;renderer.shadowMap.type=T.PCFSoftShadowMap;renderer.outputColorSpace=T.SRGBColorSpace;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.05;document.querySelector('#stage').appendChild(renderer.domElement);
const mixer=new T.AnimationMixer(tank),clip=gltf.animations.find(a=>a.name==='T72_CatastrophicCookoff');if(!clip)throw Error('Expected exported clip missing');const action=mixer.clipAction(clip);action.setLoop(T.LoopOnce,1);action.clampWhenFinished=true;
const count=900,positions=new Float32Array(count*3),colors=new Float32Array(count*3),sizes=new Float32Array(count),alphas=new Float32Array(count);
const geom=new T.BufferGeometry();geom.setAttribute('position',new T.BufferAttribute(positions,3));geom.setAttribute('tint',new T.BufferAttribute(colors,3));geom.setAttribute('radius',new T.BufferAttribute(sizes,1));geom.setAttribute('opacity',new T.BufferAttribute(alphas,1));
const mat=new T.ShaderMaterial({transparent:true,depthWrite:false,vertexShader:`attribute vec3 tint;attribute float radius;attribute float opacity;varying vec3 c;varying float a;void main(){c=tint;a=opacity;vec4 v=modelViewMatrix*vec4(position,1.);gl_Position=projectionMatrix*v;gl_PointSize=max(1.,radius*1800./max(1.,-v.z));}`,fragmentShader:`varying vec3 c;varying float a;void main(){vec2 p=gl_PointCoord*2.-1.;float q=dot(p,p);if(q>1.)discard;gl_FragColor=vec4(c,a*pow(1.-q,1.5));}`});
const particles=new T.Points(geom,mat);particles.frustumCulled=false;scene.add(particles);
const firelight=new T.PointLight(0xff8b29,0,10,2);firelight.position.set(-.48,2,0);scene.add(firelight);
const rand=(a,b=0)=>{const x=Math.sin(a*127.1+b*311.7)*43758.5453;return x-Math.floor(x);};
function effects(t,on){sizes.fill(0);alphas.fill(0);let j=0;
 function p(x,y,z,r,color,alpha){if(j>=count)return;positions.set([x,y,z],j*3);colors.set(color,j*3);sizes[j]=r;alphas[j]=alpha;j++;}
 if(on){
  // Source ring: native [-.48,0,1.55]; GLB uses [X,Z,-Y].
  // Ring ignition is an authored readable cue, not a measured footage claim.
  for(let i=0;i<240;i++){const birth=i*.012,age=t-birth,life=.6;if(age<0||age>life||birth>1.6)continue;const a=rand(i,3)*Math.PI*2,r=1.38+age*.65,k=1-age/life;p(-.48+Math.cos(a)*r,1.55+age*(.85+birth*.7),Math.sin(a)*r,.12+k*(.25+birth*.11),[1,.2+rand(i,2)*.45,.018],k*.9);}
  // Bright radial sparks originate at the hull/turret seam, with short trails.
  for(let i=0;i<170;i++){const birth=.08+i*.009,age=t-birth,life=.28+rand(i,11)*.4;if(age<0||age>life)continue;const a=rand(i,12)*6.283,v=1.5+rand(i,13)*3,r=1.38+age*v,y=1.56+age*(1+rand(i,14)*3)-2.5*age*age;for(let q=0;q<3;q++)p(-.48+Math.cos(a)*(r-q*.035),y-q*.025,Math.sin(a)*(r-q*.035),.025+(2-q)*.01,[1,.65,.12],(1-age/life)*(1-q*.2));}
  // Smoke follows the vent and drifts above the opening, leaving the flight readable.
  for(let i=0;i<150;i++){const birth=.18+i*.033,age=t-birth,life=2.6;if(age<0||age>life)continue;const strong=birth>=1.4,a=rand(i,21)*6.283,r=.65+age*.4,y=(strong?2.8:1.65)+age*(strong?2.7:.8);p(-.48+Math.cos(a)*r+age*.55,y,Math.sin(a)*r,.3+age*.42,[.12,.135,.14],(strong&&t<3.6?.22:.38)*Math.min(age/.2,1)*(1-age/life));}
  // A short pressure flare leads into the main release, followed by sustained venting.
  const strength=t<1.24?0:t<1.5?(t-1.24)/.26:t<3.2?1:Math.max(.22,1-(t-3.2)*.48);
  for(let i=0;i<410;i++){const birth=1.24+i*.009,age=t-birth,life=.85;if(age<0||age>life)continue;const a=rand(i,5)*6.283,k=1-age/life,r=.18+age*.52,y=1.57+age*7.8*strength;p(-.48+Math.cos(a)*r+Math.sin(age*10+i)*.12,y,Math.sin(a)*r,.20+k*.36+age*.2,[1,.25+k*.65,.025+k*.17],k*.85*strength);}
  const blast=t-1.5;if(blast>=0&&blast<.48){for(let i=0;i<65;i++){const a=rand(i,25)*6.283,k=1-blast/.48;p(-.48+Math.cos(a)*blast*6,1.65+rand(i,26)*blast*8,Math.sin(a)*blast*6,.24+blast*.9,[1,.48,.08],k*.75);}}
  const impact=t-3.5;if(impact>=0&&impact<1.3){for(let i=0;i<65;i++){const a=rand(i,8)*6.283,r=1.3+impact*(1.6+rand(i,9));p(-12+Math.cos(a)*r,.08+Math.sin(Math.min(impact,1)*Math.PI)*.3,26+Math.sin(a)*r,.6+impact*.65,[.70,.60,.43],.48*(1-impact/1.3));}}
 }
 for(const a of Object.values(geom.attributes))a.needsUpdate=true;firelight.intensity=on?(t>=1.5&&t<1.62?95:5+Math.sin(t*35)*1.7):0;
}
let playing=true,time=0,last=performance.now(),fx=true;
const phase=t=>t<1.24?'RING IGNITION':t<1.5?'PRESSURE FLARE':t<3.5?'ERUPTION / TURRET FLIGHT':t<4.3?'DISTANT GROUND IMPACT':'BURNING WRECK';
function sample(t){action.reset().play();mixer.setTime(Math.max(0,Math.min(4.8,t)));tank.updateMatrixWorld(true);}
function render(t,enabled=fx){time=Math.max(0,Math.min(4.8,t));sample(time);effects(time,enabled);document.querySelector('#phase').textContent=phase(time);document.querySelector('#clock').textContent=time.toFixed(2)+' / 4.80 s';document.querySelector('#seek').value=time;renderer.render(scene,camera);return {time,phase:phase(time)};}
window.renderAt=(t,enabled=true)=>{playing=false;return render(t,enabled)};
window.reviewMetadata={sourceSha256:embedded.sha256,checkpointSha256:embedded.checkpoint,revision:2,clip:clip.name,duration:clip.duration,meshCount:0,animationTracks:clip.tracks.map(t=>({name:t.name,keys:t.times.length}))};tank.traverse(o=>{if(o.isMesh)window.reviewMetadata.meshCount++});
window.inspectAt=t=>{sample(t);const parts={};const overall=new T.Box3();tank.traverse(o=>{if(!o.isMesh)return;const pos=o.geometry.getAttribute('position');const box=new T.Box3();for(let i=0;i<pos.count;i++)box.expandByPoint(new T.Vector3().fromBufferAttribute(pos,i).applyMatrix4(o.matrixWorld));overall.union(box);parts[o.name]={min:box.min.toArray(),max:box.max.toArray(),vertices:pos.count};});const toss=tank.getObjectByName('T72_TurretToss');return {time:t,parts,overall:{min:overall.min.toArray(),max:overall.max.toArray()},controlPosition:toss?.getWorldPosition(new T.Vector3()).toArray(),controlQuaternion:toss?.getWorldQuaternion(new T.Quaternion()).toArray()};};
window.frameVisibility=t=>{sample(t);let clipped=0,vertices=0;let lo=[1,1],hi=[-1,-1];tank.traverse(o=>{if(!o.isMesh)return;const p=o.geometry.getAttribute('position');for(let i=0;i<p.count;i++){const v=new T.Vector3().fromBufferAttribute(p,i).applyMatrix4(o.matrixWorld).project(camera);vertices++;if(Math.abs(v.x)>1||Math.abs(v.y)>1)clipped++;lo=[Math.min(lo[0],v.x),Math.min(lo[1],v.y)];hi=[Math.max(hi[0],v.x),Math.max(hi[1],v.y)];}});return {time:t,vertices,clipped,ndcMin:lo,ndcMax:hi}};
document.querySelector('#play').onclick=()=>{playing=!playing;document.querySelector('#play').textContent=playing?'Pause':'Play';last=performance.now()};document.querySelector('#replay').onclick=()=>{time=0;playing=true;document.querySelector('#play').textContent='Pause'};document.querySelector('#seek').oninput=e=>{playing=false;document.querySelector('#play').textContent='Play';render(Number(e.target.value))};document.querySelector('#effects').onchange=e=>{fx=e.target.checked;render(time)};
let hold=0;function tick(now){if(playing){const dt=(now-last)/1000;if(time>=4.8){hold+=dt;if(hold>=1){time=0;hold=0}}else time+=dt;render(Math.min(time,4.8));}last=now;requestAnimationFrame(tick)}render(0);window.reviewReady=true;requestAnimationFrame(tick);
