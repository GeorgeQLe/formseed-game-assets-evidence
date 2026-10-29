import pathlib,json,hashlib,numpy as np,importlib.util,collections,sys
P=pathlib.Path(__file__).parent;O=P.parent/'abrams-mantlet-forward-20261029'
spec=importlib.util.spec_from_file_location('prior_decoder',O/'audit-correction.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
f=sys.argv[1] if len(sys.argv)>1 else 'desert';oldrev=2 if f=='nato' else 1
old,b,od=mod.load(O/f'{f}-r{oldrev}-export.json');new,a,nd=mod.load(P/f'{f}-r1-export.json');checks=[];changed=[]
def digest(q):
 h=hashlib.sha256();h.update(q['vertices'].tobytes());h.update(q['faces'].tobytes());h.update(json.dumps({k:q[k] for k in ['attributes','materials','parent']},sort_keys=True).encode());return h.hexdigest()
for name,q in a.items():
 before=b[name];same=all(np.array_equal(q[k],before[k]) for k in ['vertices','faces']) and all(q[k]==before[k] for k in ['attributes','materials','parent']);checks.append({'component':name,'beforeSha256':digest(before),'afterSha256':digest(q),'exactGeometryAttributesMaterialsParentUnchanged':same})
 if not same:changed.append(name)
assert changed==['CoaxShroud'],changed
assert len(a)==269 and od['materials']==nd['materials'];n0=json.loads((P/f'{f}-before-native-receipt.json').read_text());n1=json.loads((P/f'{f}-r1-native.json').read_text());n0=n0.get('structuredContent',n0);n1=n1.get('structuredContent',n1);nativechanges=[];materialUserDeltas=[]
def normalized_native(v):
 v=json.loads(json.dumps(v));v.pop('contentSha256',None)
 for name,m in v.get('materials',{}).items():m.pop('users',None)
 return v
for name,v in n1['native']['objects'].items():
 oldv=n0['native']['objects'][name]
 if normalized_native(v)!=normalized_native(oldv):nativechanges.append(name)
 for mn,m in v.get('materials',{}).items():
  if mn in oldv.get('materials',{}):
   om=oldv['materials'][mn];assert m['sha256']==om['sha256']
   if m.get('users')!=om.get('users'):
    added=sorted(set(m.get('users',[]))-set(om.get('users',[])));removed=sorted(set(om.get('users',[]))-set(m.get('users',[])));assert mn=='rubber' and added==['CoaxShroud'] and not removed
    materialUserDeltas.append({'object':name,'material':mn,'addedUsers':added,'removedUsers':removed})
assert nativechanges==['CoaxShroud'],nativechanges

q=a['CoaxShroud'];v=q['vertices'];tri=v[q['faces']];areas=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)/2;assert areas.min()>1e-10
uv,inv=np.unique(np.round(v,6),axis=0,return_inverse=True);edges=collections.Counter();
for face in inv[q['faces']]:
 for i in range(3):edges[tuple(sorted([int(face[i]),int(face[(i+1)%3])]))]+=1
assert set(edges.values())=={2};rad=np.sqrt((v[:,1]+.2)**2+(v[:,2]-2.035)**2);assert abs(rad.max()-.036)<1e-6;assert abs(v[:,0].min()+2.3)<1e-6 and abs(v[:,0].max()+1.43)<1e-6
front=v[np.abs(v[:,0]+1.43)<1e-6];rearcap=v[np.abs(v[:,0]+1.465)<1e-6];assert len(front)>0 and len(rearcap)>0
geom={n:sorted(tuple(tuple(np.round(p,6)) for p in t) for t in q['vertices'][q['faces']]) for n,q in a.items()};geometrySha=hashlib.sha256(json.dumps(geom,sort_keys=True).encode()).hexdigest()
out={'jobId':new['jobId'],'revision':new['revision'],'checkpoint':new['checkpoint'],'reviewGlbSha256':new['glbSha256'],'priorReviewGlbSha256':old['glbSha256'],'meshes':269,'triangles':sum(len(q['faces']) for q in a.values()),'changedMeshes':changed,'all268UnaffectedExact':True,'allOtherNativeGeometryUvMaterialContentAndTransformsExact':True,'nativeBookkeepingNote':'Global rubber material users adds CoaxShroud; derived contentSha256 includes this user inventory, so raw native object hashes change for shared users without geometry/material-content changes. Explicitly checked allowed delta only.','nativeMaterialUserDeltas':materialUserDeltas,'nativeChanges':nativechanges,'materialTableExact':True,'nativeComplete':n1['native']['complete'],'nativeStatePreserved':n1['statePreserved'],'coax':{'parent':q['parent'],'bounds':[v.min(axis=0).tolist(),v.max(axis=0).tolist()],'bodyDiameter':.064,'rimDiameter':.072,'rimLength':.04,'recessDepth':.035,'rimTabs':5,'sourceTabCountUncertainty':1,'triangles':len(q['faces']),'minTriangleArea':float(areas.min()),'allGeometricEdgesHaveTwoIncidentTriangles':True,'uniqueNativeMeshUsers':n1['native']['objects']['CoaxShroud']['mesh']['users']},'triangleGeometryMapSha256':geometrySha,'checks':checks,'limitations':['Dimensiontargetsareboundedvisualconstructionchoices,notcalibratedhistoricalmeasurements.','No physicalguninternals/continuousmotion/engineeringcertification.','Sameaxis/endpoints;actualmodelreviewmustjudgeanyremainingmajorformobjection.']}
(P/f'{f}-r1-preservation-form-audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['jobId','meshes','triangles','changedMeshes','all268UnaffectedExact','triangleGeometryMapSha256']}))
