"""Extract exact producer meshes; compile direct-base review fixtures, never author Blender geometry."""
from pathlib import Path
import sys,json,copy,hashlib,shutil,math
import numpy as np
BASE=Path('/Users/georgele/Developer/Projects/tools/dev/formseed/projects/uk-comet-i/delivery')
ROOT=Path('/Users/georgele/Developer/Projects/tools/dev/formseed/projects/uk-comet-i-conversions');OUT=ROOT/'delivery'
sys.path.insert(0,str(BASE/'validation/scripts'))
from package_comet_parts import read_glb,write_glb,extract,accessor,mesh_signature,sha,canonical,save
C=np.array([[0,-1,0,0],[0,0,1,0],[-1,0,0,0],[0,0,0,1]],dtype=float)
def tr(v):m=np.eye(4);m[:3,3]=v;return m
def rz(a):a=math.radians(a);m=np.eye(4);m[:2,:2]=[[math.cos(a),-math.sin(a)],[math.sin(a),math.cos(a)]];return m
def rx(a):a=math.radians(a);m=np.eye(4);m[1:3,1:3]=[[math.cos(a),-math.sin(a)],[math.sin(a),math.cos(a)]];return m
def ry(a):a=math.radians(a);m=np.eye(4);m[0,0]=m[2,2]=math.cos(a);m[0,2]=math.sin(a);m[2,0]=-math.sin(a);return m
def points(n,m):
 a=allparts[n];d,b=read_glb(a['_file']);v=np.array([p for pr in d['meshes'][0]['primitives'] for p in accessor(d,b,pr['attributes']['POSITION'])]);v=np.column_stack((-v[:,2],-v[:,0],v[:,1]));return v@m[:3,:3].T+m[:3,3]
r=json.loads((ROOT/'evidence/producer-r3-records.json').read_text());ck=r['checkpoint'];e=r['reviewGLB'];assert sha(ck['path'])==ck['contentHash'];assert sha(e['glbPath'])==e['glbSha256'];assert sha(r['nativeReceipt']['path'])==r['nativeReceipt']['sha256'];native=json.loads(Path(r['nativeReceipt']['path']).read_text());assert native['native']['complete'] and native['statePreserved']
plan=json.loads((ROOT/'authoring/component-motion-plan.json').read_text());pm={p['nativeObject']:copy.deepcopy(p) for p in plan['parts']};corrections=json.loads((ROOT/'authoring/installed-mount-reconciliation.json').read_text())
for n,m in corrections['changes'].items():pm[n]['mountWorld']=m;pm[n]['mountRevision']=2
for n in ['T_P04','T_P05','T_DP04A','T_WP05A']:pm[n]['installedScale']=[1,.95,1];pm[n]['mountRevision']=3
pm['F_P01']['label']='Comet-designed recessed visual projector ball'
def mount_scale(p):return np.diag([*p.get('installedScale',[1,1,1]),1])
d,b=read_glb(e['glbPath']);OUT.mkdir(exist_ok=True);src=OUT/'sources'/f'components-r3-{ck["contentHash"][:12]}.blend';src.parent.mkdir(exist_ok=True);shutil.copyfile(ck['path'],src)
prior={p['componentId']:p for p in json.loads((OUT/'component-registry.json').read_text())['components']};changed=set(json.loads((Path(__file__).parent/'correction-operations.json').read_text())['removeObjects']);reg=[]
for row in e['nodeMapping']:
 n=row['sourceObject']
 if n not in pm:continue
 assert row['sourceType']=='MESH';p=pm[n];dd,bb=extract(d,b,row['glbMeshIndex'],n);f=OUT/'parts'/p['owner']/f'{n}-r{3 if n in changed else 2}.glb';write_glb(f,dd,bb);ed,eb=read_glb(f);sig=mesh_signature(d,b,row['glbMeshIndex']);assert mesh_signature(ed,eb,0)==sig
 no=native['native']['objects'][n];assert no['mesh']['users']==[n];p['nativeLibraryLocation']=[row['sourceWorldMatrix'][i*4+3] for i in range(3)]
 meshNames=[k for k,v in native['native']['meshDatablocks'].items() if n in v.get('users',[])]
 parent={'turret-yaw':[.35,0,1.64],'gun-elevation':[1.35,0,2],'hull-mg-pitch':[2.565,.54,1.49],'trailer-root':[-3.55,0,.8],'trailer-wheel-left':[-6.15,1,.621],'trailer-wheel-right':[-6.15,-1,.621],'observation-head':[-.62,-.06,2.94]}.get(p['motionGroup'],[0,0,0]);local=[p['mountWorld'][i]-parent[i] for i in range(3)]
 reg.append({**p,'candidateRevision':3 if n in changed else 2,'source':{'jobId':e['jobId'],'branchId':e['branchId'],'checkpointId':ck['id'],'checkpointSha256':ck['contentHash'],'revision':3,'nativeSource':str(src.relative_to(OUT)),'nativeSourceSha256':sha(src),'selector':{'object':n,'mesh':meshNames},'nativeObjectSha256':no['objectSha256'],'nativeMeshSha256':no['mesh']['sha256'],'nativeContentSha256':no['contentSha256'],'isolationReceiptSha256':r['nativeReceipt']['sha256']},'mount':{'parent':p['motionGroup'],'parentLocalMatrixRowMajor':(tr(local)@rz(corrections.get('rotationsSourceZDegrees',{}).get(n,0))@mount_scale(p)).reshape(-1).tolist(),'sourceWorldMatrixRowMajor':(tr(p['mountWorld'])@rz(corrections.get('rotationsSourceZDegrees',{}).get(n,0))@mount_scale(p)).reshape(-1).tolist(),'sourceLibraryWorldMatrixRowMajor':row['sourceWorldMatrix'],'standaloneFrame':'component-local signed-axis glTF Y-up; source +X becomes -Z, +Y becomes -X'},'export':{'path':str(f.relative_to(OUT)),'sha256':sha(f),'bytes':f.stat().st_size,'logicalMeshSha256':sig,'triangleCount':sum(len(accessor(ed,eb,pr['indices']))//3 for pr in ed['meshes'][0]['primitives']),'selfContained':True},'approval':{'humanArtwork':None,'source':None,'catalog':False},'_file':str(f)})
for p in reg:
 if p['componentId'] not in changed:
  old=prior[p['componentId']];assert p['export']['sha256']==old['export']['sha256'];assert p['source']['nativeMeshSha256']==old['source']['nativeMeshSha256'];p['source']=old['source'];p['sourceCorrespondenceAtR3']={'checkpointSha256':ck['contentHash'],'nativeMeshSha256':p['source']['nativeMeshSha256'],'retainedExact':True}
assert len(reg)==44
allparts={p['componentId']:p for p in reg};baseparts={}
for prefix in ['P','DP','WP']:
 rr=json.loads((BASE/f'component-registry-{prefix}.json').read_text())
 for p in rr['components']:
  p=copy.deepcopy(p);p['_file']=str(BASE/p['export']['path']);assert sha(p['_file'])==p['export']['sha256'];baseparts[p['componentId']]=p;allparts[p['componentId']]=p
clean=[p['componentId'] for p in json.loads((BASE/'component-registry-P.json').read_text())['components']]
save(OUT/'component-registry.json',{'recordType':'comet-conversion-standalone-component-registry','candidate':'0.1.0-candidate.r3-fit2','confirmedVersion':None,'components':[{k:v for k,v in p.items() if not k.startswith('_')} for p in reg],'backendSemantics':'Local preparation registry, exact shared native source plus independent selectors and standalone GLBs. Backend has no package/component publication or approval semantics. Nothing completed or promoted.'})
def pin(n):
 p=allparts[n];return {'componentId':n,'revision':p['candidateRevision'],'source':p['source'],'export':p['export'],'dependency':'uk-comet-i@1.0.0 sealed delivery' if n in baseparts else 'uk-comet-i-conversions@0.1.0-candidate.r3-fit2'}
def merge(selected,matrices,path):
 doc={'asset':{'version':'2.0','generator':'Comet conversion direct-base review fixture; no approval'},'scene':0,'scenes':[{'nodes':[]}],'nodes':[],'meshes':[],'accessors':[],'bufferViews':[],'materials':[]};blob=bytearray();mats={}
 for n in selected:
  p=allparts[n];assert sha(p['_file'])==p['export']['sha256'];x,bb=read_glb(p['_file']);vo=len(doc['bufferViews']);ao=len(doc['accessors']);blob+=b'\0'*((-len(blob))%4);off=len(blob);blob+=bb
  for v in x['bufferViews']:
   v=copy.deepcopy(v);v['byteOffset']=v.get('byteOffset',0)+off;v['buffer']=0;doc['bufferViews'].append(v)
  for a in x['accessors']:
   a=copy.deepcopy(a);a['bufferView']+=vo;doc['accessors'].append(a)
  mm={}
  for i,mat in enumerate(x['materials']):
   key=canonical(mat)
   if key not in mats:mats[key]=len(doc['materials']);doc['materials'].append(mat)
   mm[i]=mats[key]
  mesh=copy.deepcopy(x['meshes'][0])
  for p in mesh['primitives']:
   p['attributes']={k:v+ao for k,v in p['attributes'].items()};p['indices']+=ao;p['material']=mm[p['material']]
  mi=len(doc['meshes']);doc['meshes'].append(mesh);m=C@matrices[n]@C.T;doc['nodes'].append({'name':n,'mesh':mi,'matrix':m.T.reshape(-1).tolist()});doc['scenes'][0]['nodes'].append(mi)
 write_glb(path,doc,bytes(blob));dd,bb=read_glb(path)
 for i,n in enumerate(selected):
  x,xb=read_glb(allparts[n]['_file']);assert mesh_signature(dd,bb,i)==mesh_signature(x,xb,0),(n,'compiled payload mismatch')
 return {'path':str(path.relative_to(OUT)),'sha256':sha(path),'bytes':path.stat().st_size,'meshCount':len(selected),'triangles':sum(allparts[n]['export']['triangleCount'] for n in selected),'materials':len(doc['materials']),'logicalPayloadsExact':True}
sets={'command':[p['componentId'] for p in reg if p['role']=='clean' and p['owner'] in ['S','C']],'observation':[p['componentId'] for p in reg if p['role']=='clean' and p['owner'] in ['S','O']],'crocodile':[p['componentId'] for p in reg if p['role']=='clean' and p['owner'] in ['F','T']]}
conditions={
'command':{'D01':({'S_P02':'S_DP02A'},[],'Mobility strike with snapped communications aerial'),'D02':({'S_P01':'S_DP01A'},[],'Weapon strike and crushed radio accessory cases'),'D03':({'S_P05':'S_DP05A'},[],'Rear blast distorts cable reel'),'W01':({'S_P01':'S_WP01A','S_P02':'S_WP02A','S_P03':'S_WP03A'},[],'Burned rack and aerial stubs'),'W02':({'S_P01':'S_WP01A','S_P05':'S_WP05A'},['S_P02','S_P03','C_P01'],'Mobility wreck with aerial and command wallet lost'),'W03':({'S_P01':'S_WP01A','S_P02':'S_WP02A','S_P03':'S_WP03A','S_P05':'S_WP05A'},['S_P04'],'Detached turret carries wrecked communications equipment')},
'observation':{'D01':({'O_P04':'O_DP04A'},[],'Mobility strike and optical head impact'),'D02':({'O_P01':'O_DP01A','S_P01':'S_DP01A'},[],'Dummy tube broken and equipment cases crushed'),'D03':({'O_P03':'O_DP03A','S_P02':'S_DP02A'},[],'Rear blast bends observation pedestal and aerial'),'W01':({'S_P01':'S_WP01A','S_P02':'S_WP02A','S_P03':'S_WP03A','O_P04':'O_WP04A'},[],'Burned observation and communications equipment'),'W02':({'S_P01':'S_WP01A','S_P05':'S_WP05A'},['O_P04','S_P02','S_P03','O_P05'],'Optic head and plotting wallet lost in mobility wreck'),'W03':({'S_P01':'S_WP01A','S_P02':'S_WP02A','S_P03':'S_WP03A','O_P01':'O_WP01A','O_P04':'O_WP04A'},['S_P04'],'Detached turret with broken dummy and crushed optic')},
'crocodile':{'D01':({'F_P01':'F_DP01A'},[],'Mobility loss and deformed bow projector'),'D02':({'T_P01':'T_DP01A','F_P02':'F_DP02A'},[],'Weapon strike with bent towing presentation and underbody armor'),'D03':({'T_P02':'T_DP02A','T_P04':'T_DP04A'},[],'Rear blast dents trailer and collapses left tyre'),'W01':({'F_P01':'F_WP01A','T_P02':'T_WP02A','T_P03':'T_WP03A'},[],'Burned carrier and ruptured trailer'),'W02':({'F_P01':'F_WP01A','T_P01':'T_WP01A','T_P05':'T_WP05A'},['F_P04'],'Broken towing connection with detached trailer'),'W03':({'F_P01':'F_WP01A','T_P01':'T_WP01A','T_P02':'T_WP02A','T_P05':'T_WP05A'},['T_P03','F_P04'],'Detached turret and overturned open trailer, roof lost')}}
index=[];compat=[];proof=[]
for package,addon in sets.items():
 pindex=[]
 for state in ['clean','D01','D02','D03','W01','W02','W03']:
  basefile=BASE/'recipes'/f'{state}.json';base=json.loads(basefile.read_text());baseops={};extras=[]
  for op in base['operations']:
   if op['op']=='retain':baseops[op['part']['componentId']]=op['part']['componentId']
   elif op['op']=='replace':baseops[op['from']['componentId']]=op['to']['componentId']
   elif op['op']=='remove':baseops[op['from']['componentId']]=None
   elif op['op']=='add' and 'part' in op:extras.append(op['part']['componentId'])
  replacements={p['replacesBase']:p['componentId'] for p in reg if p['componentId'] in addon and p.get('replacesBase')};rem=['P07'] if package=='observation' else [];cr,er,desc=conditions[package].get(state,({},[],'Clean designed conversion'));er=list(er)
  if package in ['command','observation'] and state.startswith('W') and 'S_P04' not in er:er.append('S_P04')
  chosen={h:t for h,t in baseops.items()};collisions=[]
  for h,n in replacements.items():
   if baseops[h]!=h:collisions.append({'baseHost':h,'baseConditionTarget':baseops[h],'resolution':'Conversion owns this socket; suppress base condition target and use explicit conversion condition replacement.','selected':cr.get(n,n)})
   chosen[h]=None if n in er else cr.get(n,n)
  for h in rem:
   if baseops[h] and baseops[h]!=h:collisions.append({'baseHost':h,'baseConditionTarget':baseops[h],'resolution':'Conversion explicitly removes this host; no muzzle/brake remains.','selected':None})
   chosen[h]=None
  ops=[];selected=[];matrices={};mounts={};dt=np.eye(4)
  if state=='W03':dt=np.array(base['assembly']['resolvedSourceWorldMatrices']['P14']).reshape(4,4)@np.linalg.inv(np.array(baseparts['P14']['mount']['sourceWorldMatrixRowMajor']).reshape(4,4))
  for h in clean:
   n=chosen[h]
   if n is None:ops.append({'op':'remove','from':pin(h)});continue
   selected.append(n);ops.append({'op':'retain','part':pin(n)} if n==h else {'op':'replace','from':pin(h),'to':pin(n)})
   if n in baseparts:matrices[n]=np.array(base['assembly']['resolvedSourceWorldMatrices'][n]).reshape(4,4)
   else:
    p=allparts[n];matrices[n]=np.array(p['mount']['sourceWorldMatrixRowMajor']).reshape(4,4)
    if state=='W03' and p['motionGroup'] in ['turret-yaw','gun-elevation','observation-head']:matrices[n]=dt@matrices[n]
  for n in extras:selected.append(n);ops.append({'op':'add','part':pin(n)});matrices[n]=np.array(base['assembly']['resolvedSourceWorldMatrices'][n]).reshape(4,4)
  for cleanaddon in addon:
   if cleanaddon in replacements.values() or cleanaddon in er:continue
   n=cr.get(cleanaddon,cleanaddon);selected.append(n);ops.append({'op':'add','part':pin(n)});p=allparts[n];matrices[n]=np.array(p['mount']['sourceWorldMatrixRowMajor']).reshape(4,4)
   if state=='W03' and p['motionGroup'] in ['turret-yaw','gun-elevation','observation-head']:matrices[n]=dt@matrices[n]
  # W02/W03 trailer is detached, rigid and cold. No fake connected hose spans the gap.
  trailer=[n for n in selected if n.startswith('T_')]
  trailerRestPose=None
  if package=='crocodile' and state=='D03':
   pivot=np.array([-3.55,0,.8]);angle=np.array([-3.,-8.]);original={n:matrices[n].copy() for n in trailer}
   def pose(a):return tr(pivot)@ry(a[0])@rx(a[1])@tr(-pivot)
   def gaps(a):return np.array([points(n,pose(a)@original[n])[:,2].min()-.0001 for n in ['T_DP04A','T_P05']])
   for _ in range(12):
    f=gaps(angle)
    if np.max(np.abs(f))<1e-8:break
    jac=np.column_stack([(gaps(angle+np.eye(2)[i]*.0001)-f)/.0001 for i in range(2)]);angle-=np.linalg.solve(jac,f)
   assert abs(angle[0])<=10 and abs(angle[1])<=12 and np.max(np.abs(gaps(angle)))<.0001
   for n in trailer:matrices[n]=pose(angle)@original[n]
   trailerRestPose={'pitchDegrees':float(angle[0]),'rollDegrees':float(angle[1]),'fixedHitchPivot':pivot.tolist(),'bothTyreMinimumZ':(gaps(angle)+.0001).tolist(),'towing':'disabled; static collapsed-tyre resting pose only'}
  if package=='crocodile' and state in ['W02','W03']:
   pivot=np.array([-6.15,0,.59]);delta=tr([0,2.2,0])@tr(pivot)@rz(20)@tr(-pivot)
   if state=='W03':
    delta=tr(pivot)@rz(-18)@rx(80)@tr(-pivot);pts=np.concatenate([points(n,delta@matrices[n]) for n in trailer]);delta=tr([0,-2.4,.025-pts[:,2].min()])@delta
   for n in trailer:matrices[n]=delta@matrices[n]
  assert len(selected)==len(set(selected));assert all(n not in selected for n in er)
  aid=package+'-'+state;preview=merge(selected,matrices,OUT/'assemblies'/f'{aid}.glb')
  motion=copy.deepcopy(base['motion']);motion['packageInterlocks']=['No riders at any of the seven base anchors','Use exact base hatch/weapon interlocks; all W states fully frozen','Observation dummy gun elevation/recoil locked neutral; no main/coax firing' if package=='observation' else 'Retain base main gun control restrictions; Crocodile projector presentation locked neutral, hull-aim only pending ball-mount clearance qualification' if package=='crocodile' else 'Retain base main gun control restrictions','Damaged optical head/pedestal or radio equipment visual damage is not a gameplay functionality decision','Crocodile D states prohibit towing until condition-specific tow envelope review; all flame presentation controls disabled' if package=='crocodile' and state!='clean' else 'Trailer clean limits require consumer kinematics qualification' if package=='crocodile' else 'Equipment follows complete turret hierarchy']
  if trailerRestPose:motion['trailerRestPose']=trailerRestPose
  if state.startswith('W'):motion={'survivingArticulation':[],'disabledControls':'ALL; no powered operation, towing, active radio, optical scanning or flame presentation','detachedTrailer':package=='crocodile' and state in ['W02','W03'],'packageInterlocks':['All crew and rider figures omitted']}
  manifest={'recordType':'comet-direct-base-conversion-condition-manifest','schemaVersion':1,'packageId':'uk-comet-i-'+package,'version':'0.1.0-candidate.r3-fit2','confirmedVersion':None,'recipeId':state,'description':desc,'historicalStatus':'Alternate-history designed Comet treatment; donor precedents and uncertainty in research packet','baseDependency':{'assetId':'uk-comet-i','version':'1.0.0','cleanRegistrySha256':sha(BASE/'component-registry-P.json'),'baseCondition':state,'baseConditionManifestSha256':sha(basefile),'baseConditionManifestPath':str(basefile)},'compilation':'Resolve directly from pinned clean 73-part base. Operations below are complete and sufficient; baseCondition is provenance, not a preceding application step.','operations':ops,'ownershipCollisionsResolved':collisions,'equipmentRemoved':er,'selectedParts':selected,'assembly':{'axes':'+X forward +Y left +Z up meters','resolvedSourceWorldMatrices':{n:m.reshape(-1).tolist() for n,m in matrices.items()},'addonMounts':{n:allparts[n]['mount'] for n in selected if n not in baseparts},'baseW03WholeTurretDeltaRowMajor':dt.reshape(-1).tolist() if state=='W03' else None,'previewHierarchy':'Static flattened fixture only; reconstruct motion hierarchy from base controls plus addon mount parent/local matrices. W03 inserts exact whole-turret delta above the entire tree.'},'motion':motion,'compiledReviewAssembly':preview,'reviewOnly':True,'approval':{'technicalValidation':'source r3 passed; assembled checks separate','visualRecommendation':None,'humanArtwork':None,'gameIntegration':False,'performanceQualification':False}}
  f=OUT/'packages'/package/'recipes'/f'{state}.json';save(f,manifest);row={'recipeId':aid,'package':package,'condition':state,'manifest':str(f.relative_to(OUT)),'manifestSha256':sha(f),**preview};index.append(row);pindex.append(row)
  proof.append({'recipe':aid,'allSelectedLogicalGeometryAndMaterialsExact':True,'retainedBaseCount':sum(n in clean for n in selected),'baseConditionRecipeUnchangedSha256':sha(basefile),'unchangedAcceptedSourceCopiedIntoDerivative':False})
  for bstate in ['clean','D01','D02','D03','W01','W02','W03']:compat.append({'package':package,'packageCondition':state,'baseCondition':bstate,'supported':state==bstate,'manifest':str(f.relative_to(OUT)) if state==bstate else None,'reason':'Explicit direct-base candidate exists; artwork pending' if state==bstate else 'Unreviewed cross-composition; do not overlay automatically'})
 save(OUT/'packages'/package/'PACKAGE.json',{'packageId':'uk-comet-i-'+package,'version':'0.1.0-candidate.r3-fit2','confirmedVersion':None,'requiresBase':'uk-comet-i@1.0.0 early cowl-exhaust clean r14; existing static bands retained','mutuallyExclusivePackages':[p for p in sets if p!=package],'cleanComponents':addon,'essentialSeparateAssembly':'comet-crocodile-type-trailer@0.1.0-candidate.r3-fit2' if package=='crocodile' else None,'recipes':pindex,'approval':None,'published':False})
save(OUT/'recipe-index.json',{'recipes':index,'completeVehiclesAreReviewEvidenceOnly':True,'sourceOfTruth':'Standalone native/export component registry and direct-base manifests, not complete tank files.'})
save(OUT/'compatibility-matrix.json',{'combinations':compat,'unsupportedCrossCompositions':126,'sharedEquipment':['S_P01','S_P02','S_P03','S_P04','S_P05'],'separateInstancesRequired':True,'noCrossVehicleComponentReuse':'No Centurion, Cromwell or Churchill mesh reused; donor photographs do not prove component identity.'})
save(OUT/'validation/accepted-surface-correspondence.json',{'allExact':True,'method':'Each compiled mesh logical accessor arrays, indices and material state compared exactly against its pinned standalone GLB; accepted base input hashes validated before assembly. No unchanged accepted mesh is incorporated into newly authored conversion component source.','recipes':proof})
save(OUT/'trailer-assembly.json',{'assemblyId':'comet-crocodile-type-trailer','version':'0.1.0-candidate.r3-fit2','essentialFor':['uk-comet-i-crocodile@0.1.0-candidate.r3-fit2'],'components':[p['componentId'] for p in reg if p['owner']=='T'],'root':{'parent':'asset-root','pivot':[-3.55,0,.8],'axisConvention':'+X forward +Y left +Z up'},'wheels':{'left':'T_P04','right':'T_P05','axis':'local +Y','radiusDesignMeters':.6209386,'warning':'Authored tread relief determines actual ground contact; nominal tyre radius is not historical measurement.'},'linkage':'Exact component-registry sources/exports; package recipes pin specific clean/DP/WP revisions and hashes','motion':'Clean proposed yaw ±45 pitch ±10 roll ±8; sampled clearance report governs. Damaged towing disabled pending specific qualification. Wreck all controls disabled, W02/W03 detached.'})
print(json.dumps({'components':len(reg),'recipes':len(index),'exactPayloads':True,'assembliesBytes':sum(p['bytes'] for p in index)}))
