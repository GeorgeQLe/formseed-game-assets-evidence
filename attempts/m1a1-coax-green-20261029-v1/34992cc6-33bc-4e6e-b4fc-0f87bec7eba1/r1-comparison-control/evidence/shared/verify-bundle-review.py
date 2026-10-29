import json,pathlib,struct,hashlib,numpy as np
P=pathlib.Path(__file__).parent
c=json.loads((P/'consolidated-corrected-evidence.json').read_text())['candidates']
def read(p):
 b=pathlib.Path(p).read_bytes();n=struct.unpack_from('<I',b,12)[0];d=json.loads(b[20:20+n]);blob=b[28+n:]
 def acc(i):
  a=d['accessors'][i];v=d['bufferViews'][a['bufferView']];n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']];t={5121:'u1',5123:'<u2',5125:'<u4',5126:'<f4'}[a['componentType']];s=np.dtype(t).itemsize
  return np.ndarray((a['count'],n),dtype=t,buffer=blob,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',n*s),s)).copy()
 parents={x:i for i,n in enumerate(d['nodes']) for x in n.get('children',[])}
 def mat(i):
  n=d['nodes'][i]
  if 'matrix' in n:m=np.array(n['matrix']).reshape(4,4,order='F')
  else:
   assert n.get('rotation',[0,0,0,1])==[0,0,0,1];m=np.eye(4);m[:3,3]=n.get('translation',[0,0,0]);m[:3,:3]=np.diag(n.get('scale',[1,1,1]))
  return mat(parents[i])@m if i in parents else m
 def images():
  return [hashlib.sha256(blob[d['bufferViews'][im['bufferView']].get('byteOffset',0):d['bufferViews'][im['bufferView']].get('byteOffset',0)+d['bufferViews'][im['bufferView']]['byteLength']]).hexdigest() for im in d.get('images',[])]
 return d,acc,parents,mat,images(),hashlib.sha256(b).hexdigest()
out={}
for f,j in c.items():
 mp=pathlib.Path(j['bundle']['manifestPath']);m=json.loads(mp.read_text());bp=mp.parent/next(x for x in m['hashes'] if x.endswith('.glb'));r,ra,rp,rm,ri,rsha=read(j['export']['glbPath']);b,ba,bpmap,bm,bi,bsha=read(bp);assert [{k:v for k,v in x.items() if k!='extras'} for x in r['materials']]==[{k:v for k,v in x.items() if k!='extras'} for x in b['materials']];assert ri==bi;assert len(r['nodes'])==len(b['nodes'])==275;assert rsha==j['export']['glbSha256'];assert bsha==m['hashes'][str(bp.relative_to(mp.parent))];checks=[]
 for i,rn in enumerate(r['nodes']):
  bn=b['nodes'][i];assert rn['name']==bn['name'];assert rp.get(i)==bpmap.get(i)
  if 'mesh' not in rn:continue
  rps=r['meshes'][rn['mesh']]['primitives'];bps=b['meshes'][bn['mesh']]['primitives'];assert len(rps)==len(bps)
  for x,y in zip(rps,bps):
   assert x.get('material')==y.get('material');assert set(x['attributes'])==set(y['attributes'])
   rattrs={k:ra(v) for k,v in x['attributes'].items()};battrs={k:ba(v) for k,v in y['attributes'].items()}
   for attrs,wm,convert in [(rattrs,rm(i),False),(battrs,bm(i),True)]:
    v=attrs['POSITION'];attrs['POSITION']=(np.column_stack([v,np.ones(len(v))])@wm.T)[:,:3]
    if 'NORMAL' in attrs:
     n=attrs['NORMAL']@np.linalg.inv(wm[:3,:3]);attrs['NORMAL']=n/np.linalg.norm(n,axis=1)[:,None]
    if convert:
     for k in ['POSITION','NORMAL']:
      if k in attrs:attrs[k]=attrs[k][:,[2,1,0]]*np.array([1,1,-1])
   def canonical(attrs,ids):
    merged=np.column_stack([attrs[k] for k in sorted(attrs)])
    vs=[tuple(np.round(v,6)) for v in merged];tris=[]
    for face in ids.reshape(-1,3):
     t=tuple(vs[int(q)] for q in face);tris.append(min(t,t[1:]+t[:1],t[2:]+t[:2]))
    return sorted(tris)
   assert canonical(rattrs,ra(x['indices']))==canonical(battrs,ba(y['indices'])),(f,rn['name'],'triangle attributes')
  checks.append(rn['name'])
 out[f]={'reviewGlbSha256':rsha,'bundleGlbPath':str(bp),'bundleGlbSha256':bsha,'logicalMeshCount':len(checks),'all269WorldGeometryEquivalentAt1Micrometer':len(checks)==269,'orientedTrianglePositionsNormalsUvsEquivalentAt1Micrometer':True,'materialBindingsExact':True,'worldNormalDirectionsEquivalent':True,'reviewHashMatchesReceipt':True,'bundleHashMatchesManifest':True,'all275NamesAndParentsExact':True,'materialPropertiesExactExcludingReviewExtras':True,'embeddedImageHashesExact':True,'coordinateConversion':'Bundle standard glTF +X forward to review glTF -Z forward: review XYZ = bundle Z,Y,-X. Both Y-up. Export metadata differs; raw file hashes intentionally distinct.'}
(P/'bundle-review-equivalence.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
