"""Author declarative mesh operations and package plans; never runs Blender."""
from pathlib import Path
import json, math, hashlib, copy
ROOT=Path('/Users/georgele/Developer/Projects/tools/dev/formseed/projects/uk-comet-i-conversions')
WORK=Path(__file__).parent
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
class Mesh:
 def __init__(self):self.v=[];self.f=[]
 def add(self,v,f):
  o=len(self.v);self.v.extend(v);self.f.extend([[o+i for i in face] for face in f]);return self
 def box(self,c,s):
  x,y,z=c;a,b,d=[q/2 for q in s]
  return self.add([[x+u*a,y+v*b,z+w*d] for u,v,w in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]],[[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]])
 def cyl(self,c,r,l,axis='Z',n=12,r2=None):
  r2=r if r2 is None else r2;v=[]
  for k,rr in [(-1,r),(1,r2)]:
   for j in range(n):
    a=2*math.pi*j/n;p=[rr*math.cos(a),rr*math.sin(a),k*l/2]
    if axis=='X':p=[p[2],p[0],p[1]]
    if axis=='Y':p=[p[1],p[2],p[0]]
    v.append([p[i]+c[i] for i in range(3)])
  return self.add(v,[list(range(n-1,-1,-1)),list(range(n,n*2))]+[[j,(j+1)%n,(j+1)%n+n,j+n] for j in range(n)])
 def beam(self,a,b,r=.015,n=8):
  delta=[b[i]-a[i] for i in range(3)];l=math.sqrt(sum(x*x for x in delta));w=[x/l for x in delta];ref=[0,0,1] if abs(w[2])<.9 else [0,1,0]
  u=[w[1]*ref[2]-w[2]*ref[1],w[2]*ref[0]-w[0]*ref[2],w[0]*ref[1]-w[1]*ref[0]];ll=math.sqrt(sum(x*x for x in u));u=[x/ll for x in u];v=[w[1]*u[2]-w[2]*u[1],w[2]*u[0]-w[0]*u[2],w[0]*u[1]-w[1]*u[0]]
  return self.add([[p[i]+r*(u[i]*math.cos(j*2*math.pi/n)+v[i]*math.sin(j*2*math.pi/n)) for i in range(3)] for p in [a,b] for j in range(n)],[list(range(n-1,-1,-1)),list(range(n,n*2))]+[[j,(j+1)%n,(j+1)%n+n,j+n] for j in range(n)])
 def deform(self,fn):self.v=[fn(*v) for v in self.v];return self
parts=[]
colors={'olive':[.15,.18,.093,1],'dark':[.055,.065,.045,1],'steel':[.19,.205,.18,1],'rubber':[.025,.028,.023,1],'canvas':[.25,.245,.145,1],'burnt':[.055,.047,.035,1]}
def part(id,label,mount,group,mesh,material='olive',replaces=None,role='clean',owner=None):
 row={'componentId':id,'nativeObject':id,'label':label,'role':role,'owner':owner or id.split('_')[0],'mountWorld':mount,'motionGroup':group,'replacesBase':replaces,'material':material,'geometry':{'vertices':mesh.v,'faces':mesh.f},'historicalStatus':'alternate-history-designed-fit; not a documented Comet configuration','candidateRevision':1}
 parts.append(row);return row
def rack(damaged=False,wreck=False):
 m=Mesh();m.box((-.22,0,-.14),(.43,1.48,.055))
 for y in [-.69,.69]:m.box((-.22,y,.06),(.43,.055,.4));m.box((-.03,y,-.08),(.09,.065,.28))
 for y in [-.36,.36]:
  m.box((-.24,y,.04),(.36,.60,.31 if not wreck else .18));m.box((-.24,y,.21 if not wreck else .16),(.38,.62,.04))
  for yy in [y-.24,y+.24]:m.box((-.44,yy,.05),(.026,.055,.2))
  m.beam((-.444,y-.06,.12),(-.444,y+.06,.12),.012)
 if damaged:m.deform(lambda x,y,z:[x-.10*max(z,0),y+.08*max(z,0),z*.65+.05*y])
 if wreck:m.deform(lambda x,y,z:[x-.08*max(z,0),y*1.05,z*.65-.07*abs(y)])
 return m
def aerial(height=1.3,bent=False,stub=False):
 m=Mesh().cyl((0,0,.028),.05,.056).cyl((0,0,.095),.027,.075)
 if stub:m.beam((0,0,.12),(.16,-.08,.25),.009)
 elif bent:m.beam((0,0,.12),(0,0,.55),.009).beam((0,0,.55),(-.58,.12,.71),.007)
 else:m.beam((0,0,.12),(0,0,height),.008)
 return m
part('S_P01','Comet bustle equipment rack and weatherproof cases',[-.82,0,1.98],'turret-yaw',rack(),replaces='P11')
part('S_P02','Rear aerial and exact Comet base footprint',[-.56,-.68,2.4],'turret-yaw',aerial(),material='dark',replaces='P72')
part('S_P03','Forward aerial and exact Comet base footprint',[1,.63,2.4],'turret-yaw',aerial(.86),material='dark',replaces='P73')
m=Mesh()
for y in [-.1,-.04,.02]:m.cyl((0,y,0),.022,1.15,'Y' if False else 'X')
for x in [-.4,.4]:m.box((x,-.04,0),(.06,.20,.085))
part('S_P04','Stowed field aerial poles with clamps',[-1.17,0,2.39],'turret-yaw',m,material='canvas')
def reel(bent=False,wreck=False):
 m=Mesh().cyl((0,0,0),.15,.12,'X').cyl((-.08,0,0),.20,.025,'X').cyl((.08,0,0),.20,.025,'X')
 for y in [-.13,.13]:m.box((.10,y,-.1),(.06,.05,.24))
 if bent:m.deform(lambda x,y,z:[x+.12*z,y,z+.06*y])
 if wreck:m.deform(lambda x,y,z:[x+.3*z,y*.8,z*.45])
 return m
part('S_P05','Field telephone cable reel and clamp',[-1.4,-.48,2.04],'turret-yaw',reel(),material='dark')
part('C_P01','Command map wallet and rolled signal flags',[-1.35,.45,2.1],'turret-yaw',Mesh().box((0,0,0),(.13,.4,.25)).cyl((-.07,0,.18),.06,.50,'Y'),material='canvas')
def dummy(broken=False,wreck=False):
 m=Mesh().cyl((.14,0,0),.095,.28,'X').cyl((.49 if not broken else .3,0,0),.064,.42 if not broken else .16,'X')
 if wreck:m.deform(lambda x,y,z:[x,y+.35*max(x-.2,0),z-.15*max(x-.2,0)])
 return m
part('O_P01','Short sealed dummy main gun, no brake',[1.35,0,2],'gun-elevation',dummy(),material='olive',replaces='P06')
part('O_P02','Coax aperture closed cap',[1.35,.45,2],'gun-elevation',Mesh().cyl((.08,0,0),.046,.055,'X'),replaces='P08')
def pedestal(bent=False):
 m=Mesh().cyl((0,0,.025),.105,.05).cyl((0,0,.22),.043,.38).box((0,0,.43),(.18,.23,.06))
 for y in [-.13,.13]:m.box((0,y,.49),(.08,.04,.16))
 if bent:m.deform(lambda x,y,z:[x+.25*z,y,z*.9])
 return m
part('O_P03','Designed observation optic roof pedestal',[-.62,-.06,2.4],'turret-yaw',pedestal())
def optic(damage=False,wreck=False):
 m=Mesh().box((0,0,0),(.2,.33,.10))
 for y in [-.1,.1]:
  m.cyl((.10,y,.02),.065,.3,'X').cyl((-.07,y,.10),.035,.12)
  m.cyl((.255,y,.02),.067,.012,'X')
 if damage:m.deform(lambda x,y,z:[x,y+.2*x,z-.2*max(x,0)])
 if wreck:m.deform(lambda x,y,z:[x*.7,y,z*.45-.06])
 return m
part('O_P04','Designed right-angle observation head',[-.62,-.06,2.94],'observation-head',optic(),material='dark')
part('O_P05','Observation plotting wallet',[-1.35,.45,2.1],'turret-yaw',Mesh().box((0,0,0),(.12,.48,.29)).box((-.075,0,.13),(.03,.46,.04)),material='canvas')
def projector(damage=False,wreck=False):
 m=Mesh().cyl((.02,0,0),.12,.16,'X',12,r2=.10).cyl((.20,0,0),.075,.22,'X',10,r2=.055)
 # Faceted external shield, closed visual aperture; no ignition or fabrication model.
 m.cyl((.11,0,0),.139,.12,'X',8,r2=.10).cyl((.32,0,0),.045,.035,'X',10)
 if damage:m.deform(lambda x,y,z:[x,y+.3*max(x-.1,0),z-.3*max(x-.1,0)])
 if wreck:m.deform(lambda x,y,z:[x*.65,y+.16*max(x,0),z-.4*max(x,0)])
 return m
part('F_P01','Comet-designed closed visual projector ball',[2.565,.54,1.49],'hull-mg-pitch',projector(),replaces='P10')
def guard(damage=False):
 m=Mesh().box((0,0,0),(5.5,.24,.055))
 for x in [-2.5,-1.5,-.5,.5,1.5,2.5]:m.box((x,0,.025),(.08,.38,.04))
 if damage:m.deform(lambda x,y,z:[x,y+.035*math.sin(x*3),z-.055*max(0,1-abs(x))])
 return m
part('F_P02','Underbody visible routing armor, enclosed nonfunctional',[-.10,0,.355],'asset-root',guard())
m=Mesh().box((0,0,0),(.12,1.42,.16)).box((-.18,0,-.02),(.34,.30,.15)).cyl((-.34,0,-.02),.13,.20,'X')
part('F_P03','Comet-specific rear coupling crossmember',[-3.16,0,.82],'asset-root',m,replaces='P23')
part('F_P04','External connector protective boot',[-3.55,0,.80],'asset-root',Mesh().cyl((0,0,0),.115,.24,'X'),material='dark')
def drawbar(broken=False,wreck=False):
 m=Mesh()
 for y in [-.56,.56]:m.beam((-.16,0,0),(-1.36,y,-.05),.065)
 m.beam((-.10,0,-.12),(-1.45,0,-.12),.055)
 m.cyl((-.04,0,0),.105,.18,'Y')
 if broken or wreck:m.deform(lambda x,y,z:[x,y+(.22 if wreck else .10)*max(-x-.35,0),z-(.12 if wreck else .04)*max(-x-.35,0)])
 return m
part('T_P01','Trailer A-drawbar and protected presentation conduit',[-3.55,0,.80],'trailer-root',drawbar())
def shell(damaged=False,wreck=False):
 m=Mesh();m.box((0,0,-.30),(2.4,1.65,.065))
 # Finite thickness panels; shell cavity intentionally limited and empty.
 for y in [-.80,.80]:m.box((0,y,.02),(2.4,.05,.58))
 m.box((-1.18,0,.02),(.055,1.65,.58));m.box((1.18,0,-.06),(.055,1.65,.42))
 for x in [-.8,.8]:m.box((x,0,-.39),(.18,1.5,.14))
 if damaged:m.deform(lambda x,y,z:[x,y*(1-.18*max(0,1-abs(x-.5))),z-.10*max(0,1-abs(x-.5))])
 if wreck:
  # Open deformed walls, finite floor and ragged separated upper sheets; no complete interior.
  m.deform(lambda x,y,z:[x+.12*math.sin(y*3),y*(1+.10*max(z,0)),z-.16*max(0,1-abs(x))])
  m.box((-.7,.75,.38),(.5,.07,.28));m.box((.6,-.72,.30),(.6,.065,.32))
 return m
part('T_P02','Designed Crocodile-type armored trailer shell',[-6,0,.82],'trailer-root',shell())
def lid(wreck=False):
 m=Mesh()
 # Wedge roof with a stepped raised center cover rather than a plain box silhouette.
 m.add([[-1.24,-.86,.1],[1.24,-.86,.1],[1.24,.86,.1],[-1.24,.86,.1],[-1.04,-.63,.49],[.84,-.63,.49],[.84,.63,.49],[-1.04,.63,.49]],[[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]])
 m.box((-.25,0,.515),(1.2,.84,.055))
 for x in [-.7,.3]:m.beam((x,-.13,.56),(x,.13,.56),.018)
 for y in [-.6,.6]:m.cyl((-.85,y,.48),.035,.22,'Y')
 if wreck:m.deform(lambda x,y,z:[x,y+.10*math.sin(x*3),z+.22*math.sin(x*2)])
 return m
part('T_P03','Sloping trailer roof and service lid',[-6,0,.82],'trailer-root',lid())
def wheel(collapsed=False,wreck=False):
 m=Mesh().cyl((0,0,0),.56,.25,'Y',20).cyl((0,.14,0),.31,.055,'Y',12).cyl((0,.19,0),.14,.08,'Y',10)
 for j in range(20):
  a=j*math.pi/10
  for yy in [-.075,.075]:
   m.beam((.54*math.cos(a-.05),yy-.045,.54*math.sin(a-.05)),(.59*math.cos(a+.05),yy+.045,.59*math.sin(a+.05)),.035,4)
 if collapsed:m.deform(lambda x,y,z:[x,y,z if z>-.25 else -.25+(z+.25)*.22])
 if wreck:m.deform(lambda x,y,z:[x*.85,y+.13*z,z*.65])
 return m
part('T_P04','Left trailer wheel and tyre',[-6.15,1.0,.59],'trailer-wheel-left',wheel(),material='rubber')
part('T_P05','Right trailer wheel and tyre',[-6.15,-1.0,.59],'trailer-wheel-right',wheel().deform(lambda x,y,z:[x,-y,z]),material='rubber')
part('T_P06','Trailer axle and underside supports',[-6.15,0,.59],'trailer-root',Mesh().cyl((0,0,0),.065,1.9,'Y').box((0,0,.10),(.35,.75,.12)),material='steel')
part('T_P07','Trailer rear fittings and lifting lugs',[-7.24,0,.97],'trailer-root',Mesh().box((0,0,0),(.06,.64,.20)).beam((-.06,-.55,0),(-.06,-.55,.18),.027).beam((-.06,.55,0),(-.06,.55,.18),.027))
# Reusable condition replacements, created independently; no accepted base geometry in this library.
for id,label,source,mesh,mat,role in [
 ('S_DP01A','Crushed equipment cases','S_P01',rack(True),'olive','damaged'),('S_DP02A','Bent broken rear aerial','S_P02',aerial(bent=True),'dark','damaged'),('S_DP05A','Bent cable reel flange','S_P05',reel(True),'dark','damaged'),
 ('S_WP01A','Collapsed burned equipment rack','S_P01',rack(wreck=True),'burnt','wreck'),('S_WP02A','Rear aerial wreck stub','S_P02',aerial(stub=True),'burnt','wreck'),('S_WP03A','Forward aerial wreck stub','S_P03',aerial(stub=True),'burnt','wreck'),('S_WP05A','Broken reel','S_P05',reel(wreck=True),'burnt','wreck'),
 ('O_DP01A','Broken sealed dummy barrel','O_P01',dummy(True),'olive','damaged'),('O_DP03A','Bent observation pedestal','O_P03',pedestal(True),'olive','damaged'),('O_DP04A','Impact-distorted optical head','O_P04',optic(True),'dark','damaged'),('O_WP01A','Wreck dummy stub','O_P01',dummy(True,True),'burnt','wreck'),('O_WP04A','Crushed optical head','O_P04',optic(wreck=True),'burnt','wreck'),
 ('F_DP01A','Bent closed projector shield','F_P01',projector(True),'olive','damaged'),('F_DP02A','Buckled underbody route armor','F_P02',guard(True),'olive','damaged'),('F_WP01A','Crushed cold projector','F_P01',projector(wreck=True),'burnt','wreck'),
 ('T_DP01A','Bent drawbar and enclosed conduit','T_P01',drawbar(True),'olive','damaged'),('T_DP02A','Dented trailer shell','T_P02',shell(True),'olive','damaged'),('T_DP04A','Collapsed left trailer tyre','T_P04',wheel(True),'rubber','damaged'),('T_WP01A','Broken separated drawbar','T_P01',drawbar(wreck=True),'burnt','wreck'),('T_WP02A','Ruptured burned trailer shell','T_P02',shell(wreck=True),'burnt','wreck'),('T_WP03A','Warped trailer roof','T_P03',lid(True),'burnt','wreck'),('T_WP05A','Destroyed right trailer wheel','T_P05',wheel(wreck=True).deform(lambda x,y,z:[x,-y,z]),'burnt','wreck')]:
 s=next(p for p in parts if p['componentId']==source);r=part(id,label,s['mountWorld'],s['motionGroup'],mesh,mat,role=role,owner=s['owner']);r['replacementOf']=source
ops=[]
for i,p in enumerate(parts):
 # Grid is only native source storage. Installed transforms are separate authoritative data.
 location=[(i%8)*3.5,(i//8)*3.0,1.0];p['nativeLibraryLocation']=location
 ops += [{'type':'create_mesh','name':p['nativeObject'],'vertices':p['geometry']['vertices'],'edges':[],'faces':p['geometry']['faces']},{'type':'set_transform','object':p['nativeObject'],'location':location},{'type':'set_material','object':p['nativeObject'],'materialName':'comet-conv-'+p['material'],'baseColor':colors[p['material']],'roughness':.9,'metallic':0},{'type':'recalculate_normals','object':p['nativeObject'],'inside':False}]
plan={'recordType':'comet-conversion-component-motion-plan','candidate':'r1','base':'uk-comet-i@1.0.0 clean r14, exact delivery hashes in status','sourceSpace':'+X forward +Y left +Z up; meters','geometryOwnership':'Independent conversion source library only; no accepted Comet mesh copied or changed. Every native object owns a unique mesh. Standalone component exports are component-local. Native grid transforms must never be installed.','packageConflicts':'Command, observation and operational Crocodile mutually exclusive; shared S parts instantiated independently per vehicle. Trailer essential for Crocodile treatment, separate assembly, not optional equipment hidden inside vehicle.','retainedBase':'All base parts except explicit replacements/removals; exact static P36/P37 and approved base DP/WP reused.','removals':{'command':[],'observation':['P07'],'crocodile':[]},'replacementOwnership':{p['componentId']:p['replacesBase'] for p in parts if p.get('replacesBase')},'crewAndRiders':{'crew':'Five base stations retained as locations; observation duties/empty gunner station treatment proposed, no extra crew figures. Projector gunner uses existing hull MG station. No interiors or figure assets.','unavailableRiderAnchors':'All seven base rider anchors conservatively unavailable in every conversion pending consumer occupant-clearance qualification. No rider mesh bundled.','hatchRequirement':'All base hatches retain their original controls; optic pedestal behind both roof hatch sweep boxes; conservative optic use requires closed roof hatches until assembled sweep verification.'},'motion':{'turret-yaw':'Base mount pivot [.35,0,1.64], all S/C/O roof equipment follows entire moving tree including W03 displaced wreck root.','observation-head':'Yaw at [-.62,-.06,2.94] and local Y pitch ±20 proposed; no native animation clip authored; closed dummy main gun elevation locked neutral and recoil disabled.','trailer-root':'Pivot [-3.55,0,.80], yaw ±45, pitch ±10, roll ±8 proposed visual limits pending actual mesh envelope checks; trailer wheels rotate about local Y. Reversing does not reverse articulation signs automatically; consumer must implement hitch kinematics/limit handling.','flame':'No fluid simulation, operating pressure, ignition, powered flame or fabrication engineering. Solid presentation conduit and protective boot only; no deforming hose claim.','wrecks':'All controls disabled; detached trailer or turret uses fixed recipe transforms, no towing or powered operation.'},'dimensionAuthority':{'base':'Exact approved model interface measurements only; no base reshaping.','newEquipment':'Authored alternate-history visual dimensions; no claim of historical manufacturing dimensions or drop-in Churchill compatibility.','trailer':'Crocodile-type visual reconstruction from attributable photographs; actual historical trailer dimensions uncorroborated. New design envelope is explicit, and fit is checked on the unchanged Comet rather than asserted from historical measurements.'},'conditionPlan':{'damaged':'D01 local/mobility strike, D02 weapon/equipment strike, D03 rear/trailer strike. Geometry replacements, not recolour-only.','wreck':'W01 burn/collapse, W02 towing or mobility separation, W03 displaced/overturned assemblies; base W03 transform must be propagated to equipment.','composition':'Each complete manifest resolves from clean pinned base once; select base condition operations then conversion ownership deterministically, recording every collision. Only reviewed matrix combinations supported; no hidden sequential damage application.'},'parts':[{k:v for k,v in p.items() if k!='geometry'} for p in parts]}
dump(ROOT/'authoring/component-motion-plan.json',plan);dump(WORK/'component-plan.json',plan);dump(WORK/'mesh-operations.json',ops);dump(WORK/'component-geometry.json',parts)
print(json.dumps({'parts':len(parts),'operations':len(ops),'trianglesApprox':sum(sum(len(f)-2 for f in p['geometry']['faces']) for p in parts),'planSha256':hashlib.sha256((ROOT/'authoring/component-motion-plan.json').read_bytes()).hexdigest()}))
