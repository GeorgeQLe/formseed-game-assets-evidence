"""Read-only sampled checks on exact installed review component geometry."""
from pathlib import Path
import json,sys,hashlib,copy,math
import numpy as np
BASE=Path('/Users/georgele/Developer/Projects/tools/dev/formseed/projects/uk-comet-i/delivery');ROOT=Path('/Users/georgele/Developer/Projects/tools/dev/formseed/projects/uk-comet-i-conversions');D=ROOT/'delivery'
sys.path.insert(0,str(BASE/'validation/scripts'))
from package_comet_parts import read_glb,accessor,mesh_signature,sha,save
from assess_comet_clearance import intersection_count,rotate
regs=json.loads((D/'component-registry.json').read_text())['components'];parts={p['componentId']:{**p,'file':D/p['export']['path']} for p in regs}
for pre in ['P','DP','WP']:
 for p in json.loads((BASE/f'component-registry-{pre}.json').read_text())['components']:parts[p['componentId']]={**p,'file':BASE/p['export']['path']}
local={};signatures={}
for n,p in parts.items():
 assert sha(p['file'])==p['export']['sha256'];assert sha(D/p['source']['nativeSource'] if n[0] in 'SCOFT' and '_' in n else BASE/p['source']['nativeSource'])==p['source']['nativeSourceSha256'];d,b=read_glb(p['file']);ts=[]
 for pr in d['meshes'][0]['primitives']:
  v=np.array(accessor(d,b,pr['attributes']['POSITION']));assert np.isfinite(v).all();v=np.column_stack((-v[:,2],-v[:,0],v[:,1]));ix=np.array(accessor(d,b,pr['indices'])).reshape(-1,3);assert ix.min()>=0 and ix.max()<len(v);ts.append(v[ix])
 local[n]=np.concatenate(ts);signatures[n]=mesh_signature(d,b,0)
def xform(t,m):return t@m[:3,:3].T+m[:3,3]
def load(package,state):
 f=D/'packages'/package/'recipes'/f'{state}.json';r=json.loads(f.read_text());m={n:xform(local[n],np.array(r['assembly']['resolvedSourceWorldMatrices'][n]).reshape(4,4)) for n in r['selectedParts']};return r,m
def cross(a,m,names):return [[n,intersection_count(a,m[n])] for n in names if intersection_count(a,m[n])]
index=json.loads((D/'recipe-index.json').read_text())['recipes'];rows=[];cleanStatic={};motion={};hatches={};gun={};optic=[];trailer=[]
for row in index:
 r,m=load(row['package'],row['condition']);assert sha(D/row['manifest'])==row['manifestSha256'];assert sha(D/row['path'])==row['sha256'];d,b=read_glb(D/row['path']);assert [x['name'] for x in d['nodes']]==r['selectedParts']
 for i,n in enumerate(r['selectedParts']):assert mesh_signature(d,b,i)==signatures[n]
 assert len([o for o in r['operations'] if o['op'] in ['retain','replace','remove']])==73
 if row['condition'].startswith('W'):assert r['motion']['survivingArticulation']==[]
 # Every compiled node matrix must reconstruct the declared source world mount exactly.
 C=np.array([[0,-1,0,0],[0,0,1,0],[-1,0,0,0],[0,0,0,1]],float)
 for node in d['nodes']:
  n=node['name'];actual=C.T@np.array(node['matrix']).reshape(4,4).T@C;assert np.allclose(actual,np.array(r['assembly']['resolvedSourceWorldMatrices'][n]).reshape(4,4),atol=1e-12)
 rows.append({'recipe':row['recipeId'],'manifestSha256':row['manifestSha256'],'assemblySha256':row['sha256'],'parts':len(m),'allPayloadsAndTransformsExact':True,'newComponentMinZ':{n:float(t[:,:,2].min()) for n,t in m.items() if '_' in n},'addonGroundPenetrations':[n for n,t in m.items() if '_' in n and t[:,:,2].min()<-.002]})
 if row['condition']=='clean':
  names=list(m);new=[n for n in names if '_' in n];hits=[]
  for i,n in enumerate(names):
   for k in names[i+1:]:
    if n not in new and k not in new:continue
    c=intersection_count(m[n],m[k])
    if c:hits.append([n,k,c])
  cleanStatic[row['package']]=hits
for package in ['command','observation','crocodile']:
 for state in ['clean','D01','D03']:
  r,m=load(package,state);moving=[n for n in m if '_' in n and parts[n]['motionGroup'] in ['turret-yaw','gun-elevation','observation-head']];fixed=[n for n in m if '_' not in n and parts[n]['mount']['parent'] not in ['turret-yaw','gun-elevation','gun-recoil','commander-hatch-a','commander-hatch-b','loader-hatch-front','loader-hatch-rear']]
  samples=[]
  for angle in range(0,360,15):
   hits=[]
   for n in moving:
    a=rotate(m[n],'Z',angle,np.array([.35,0,1.64]))
    for k in fixed:
     c=intersection_count(a,m[k])
     if c:hits.append([n,k,c])
   samples.append({'yaw':angle,'crossings':hits})
  motion[package+'-'+state]=samples
 r,m=load(package,'clean');new=[n for n in m if '_' in n];hs=[]
 for n,axis,sign,pivot,limit in [('P15','X',1,[.08,.23,2.55],100),('P16','X',-1,[.08,.87,2.55],100),('P17','Y',1,[.78,-.515,2.4],90),('P38','Y',-1,[.11,-.515,2.4],90),('P18','Y',-1,[1.79,-.565,1.66],90),('P19','Y',-1,[1.79,.565,1.66],90)]:
  # Hull hatches use existing mandatory turret-park-at-90 interlock.
  other={k:rotate(v,'Z',90,np.array([.35,0,1.64])) if k in new and parts[k]['motionGroup'] in ['turret-yaw','gun-elevation','observation-head'] and n in ['P18','P19'] else v for k,v in m.items()}
  for angle in list(range(0,limit+1,10)):
   a=rotate(m[n],axis,angle*sign,np.array(pivot));hits=[]
   for k in new:
    c=intersection_count(a,other[k])
    if c:hits.append([k,c])
   hs.append({'hatch':n,'angle':angle,'turretParkDegrees':90 if n in ['P18','P19'] else 0,'newEquipmentCrossings':hits})
 hatches[package]=hs
 # Forward gun against all new conversion equipment; observation has locked dummy.
 if package!='observation':
  samples=[]
  for el in [-8,0,20]:
   for recoil in [0,.15,.30]:
    hits=[]
    for n in ['P05','P06','P07','P08']:
     a=rotate(m[n]-([recoil,0,0] if n in ['P06','P07'] else np.zeros(3)),'Y',-el,np.array([1.35,0,2]))
     for k in new:
      c=intersection_count(a,m[k])
      if c:hits.append([n,k,c])
    samples.append({'elevationDegrees':el,'recoilMeters':recoil,'crossings':hits})
  gun[package]=samples
r,m=load('observation','clean')
for yaw in [-180,-90,0,90,180]:
 for pitch in [-20,0,20]:
  a=rotate(rotate(m['O_P04'],'Y',pitch,np.array([-.62,-.06,2.94])),'Z',yaw,np.array([-.62,-.06,2.94]));hits=[]
  for n in m:
   if n in ['O_P04','O_P03']:continue
   c=intersection_count(a,m[n])
   if c:hits.append([n,c])
  optic.append({'yaw':yaw,'pitch':pitch,'crossings':hits})
r,m=load('crocodile','clean');towparts=[n for n in m if n.startswith('T_')];carrier=[n for n in m if not n.startswith('T_') and n not in ['F_P03','F_P04']];pivot=np.array([-3.55,0,.8])
for yaw in range(-45,46,5):
 for pitch in [-10,0,10]:
  for roll in [-8,0,8]:
   hit=[];ground=[];low=999
   for n in towparts:
    a=rotate(rotate(rotate(m[n],'X',roll,pivot),'Y',pitch,pivot),'Z',yaw,pivot);low=min(low,float(a[:,:,2].min()))
    for k in carrier:
     c=intersection_count(a,m[k])
     if c:hit.append([n,k,c])
    if a[:,:,2].min()<-.002:ground.append(n)
   trailer.append({'yaw':yaw,'pitch':pitch,'roll':roll,'carrierCrossings':hit,'flatPlanePenetrations':ground,'minimumZ':low,'terrainMeaning':'Nonzero pitch/roll requires matching terrain; flat-plane crossing does not authorize that pose on flat ground.'})
save(D/'validation/assembled-motion-and-integrity.json',{'recordType':'comet-conversion-exact-export-sampled-assessment','sourceCheckpointSha256':'7143badee86e377626fcfc9091fe5b646304c47d0c678a30b1e7d08622d9d3f1','recipes':rows,'staticCleanSurfaceCrossings':cleanStatic,'turretAddonYaw':motion,'hatchesAgainstNewEquipment':hatches,'forwardGunAgainstNewEquipment':gun,'opticSamples':optic,'trailerSamples':trailer,'limitations':['Sampled triangle surface crossing test, excludes coplanar contact and complete containment; not continuous collision proof, physics, load, ergonomic or real fuel-system qualification.','Fixed bearing/socket/strap intersections require separately recorded intended-contact interpretation.','Trailer pitch/roll samples require matching ground support; do not use nonzero pitch/roll on flat terrain. Reverse kinematics and terrain adaptation remain consumer work; samples include both positive and negative hitch yaw.']})
print(json.dumps({'recipes':len(rows),'staticCrossings':cleanStatic,'groundPenetrations':{x['recipe']:x['addonGroundPenetrations'] for x in rows if x['addonGroundPenetrations']},'turretHitSamples':{k:sum(bool(x['crossings']) for x in v) for k,v in motion.items()},'hatchHitSamples':{k:[x for x in v if x['newEquipmentCrossings']] for k,v in hatches.items()},'gunHitSamples':{k:[x for x in v if x['crossings']] for k,v in gun.items()},'opticHitSamples':[x for x in optic if x['crossings']],'trailerHitSamples':[x for x in trailer if x['carrierCrossings']]}))
