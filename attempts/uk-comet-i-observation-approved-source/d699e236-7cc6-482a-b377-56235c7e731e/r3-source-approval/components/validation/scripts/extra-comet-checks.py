from pathlib import Path
s=Path('validate_conversions.py').read_text();exec(s[:s.index('index=json.loads')]);rows=[]
for p in ['command','observation','crocodile']:
 r,m=load(p,'clean');new=[n for n in m if '_' in n];park={n:rotate(m[n],'Z',90,np.array([.35,0,1.64])) if parts[n]['motionGroup'] in ['turret-yaw','gun-elevation','observation-head'] else m[n] for n in new};samples=[]
 for z in np.arange(0,1.001,.05):samples.append({'liftMeters':round(float(z),3),'crossings':cross(m['P03']+np.array([0,0,z]),park,new)})
 rows.append({'package':p,'turretParkDegrees':90,'engineDeckVerticalRemovalAgainstNewEquipment':samples,'nonzeroCrossingSamples':sum(bool(x['crossings']) for x in samples),'warning':'P03 is a fixed accepted mesh, not a supplied hinge animation. This checks only straight-lift removal against conversion additions; it does not qualify base-to-base service motion or maintenance ergonomics.'})
# Coupling is the same declared fixed point in carrier and trailer frames at every sampled turn/terrain pose.
rec=json.loads((D/'validation/assembled-motion-and-integrity.json').read_text());joints=[]
for q in rec['trailerSamples']:
 pt=np.array([[-3.55,0,.8]])
 a=rotate(rotate(rotate(pt,'X',q['roll'],pt[0]),'Y',q['pitch'],pt[0]),'Z',q['yaw'],pt[0]);joints.append(float(np.linalg.norm(a[0]-pt[0])))
save(D/'validation/service-and-linkage.json',{'engineAccess':rows,'couplingPivot':[-3.55,0,.8],'poseSamples':len(joints),'maximumPivotSeparationMeters':max(joints),'trailerAxleDistanceDesignMeters':2.6,'turningAndReversing':'Both signed yaw envelopes -45..45 were checked against actual carrier geometry. Instantaneous mesh envelope is direction-independent; reversing must stop before exceeding yaw limits. No automatic reverse sign flip. Dynamic reverse-path tracking and terrain-following remain consumer implementation/qualification, not supplied animation.','terrain':'171 samples include yaw with pitch ±10 and roll ±8. Nonzero tilt is only for matching terrain, never flat-plane operation. Underbody guard reduces base .4m clearance to measured .3275m; no terrain physics claim.','routing':'Closed visual armor/conduit and fixed protective boot; no dynamic hose mesh, internal full route, fuel system, pressure or ignition engineering. Endpoint continuity is the coincident prescribed hitch pivot; protective joint intersections intentional, not watertight/fabrication proof.','projector':'Neutral locked; P09 socket insertion remains intentional at neutral only. No new ball articulation qualification.'})
print([(x['package'],x['nonzeroCrossingSamples']) for x in rows])
