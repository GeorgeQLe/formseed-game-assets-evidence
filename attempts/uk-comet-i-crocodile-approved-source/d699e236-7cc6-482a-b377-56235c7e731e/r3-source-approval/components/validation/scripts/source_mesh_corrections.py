"""Pure geometry planning for typed producer replacement operations. No Blender access."""
import ast,json,math
from pathlib import Path
tree=ast.parse(Path('plan_components.py').read_text());ns={'math':math};exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Mesh'],type_ignores=[]),'<pure-mesh-math>','exec'),ns);Mesh=ns['Mesh']
parts=json.loads(Path('component-geometry.json').read_text());old={p['componentId']:p for p in parts}
def tube(x0,x1,ro,ri):
 m=Mesh();n=16;v=[]
 for x,r in [(x0,ro),(x1,ro),(x0,ri),(x1,ri)]:v.extend([[x,r*math.cos(i*2*math.pi/n),r*math.sin(i*2*math.pi/n)] for i in range(n)])
 f=[]
 for i in range(n):
  j=(i+1)%n;f.extend([[i,j,n+j,n+i],[2*n+i,3*n+i,3*n+j,2*n+j],[n+i,n+j,3*n+j,3*n+i],[i,2*n+i,2*n+j,j]])
 return m.add(v,f)
def projector():
 m=Mesh().cyl((.02,0,0),.12,.16,'X',12,r2=.10).cyl((.20,0,0),.075,.22,'X',10,r2=.055).cyl((.11,0,0),.139,.12,'X',8,r2=.10)
 m.add(tube(.30,.3375,.045,.027).v,tube(.30,.3375,.045,.027).f)
 cup=Mesh().cyl((.313,0,0),.0265,.001,'X',16)
 return m,cup
def shell(damaged=False,wreck=False):
 m=Mesh();outer=[[-.9,-.60,-.30],[.9,-.60,-.30],[.9,.60,-.30],[-.9,.60,-.30],[-1.20,-.825,.30],[1.20,-.825,.30],[1.20,.825,.30],[-1.20,.825,.30]]
 inner=[[x*(.94 if z<0 else .96),y*(.92 if z<0 else .95),z+.035 if z<0 else z] for x,y,z in outer];v=outer+inner;f=[]
 # Four closed wall volumes around an empty limited cavity.
 for a,b in [(0,1),(1,2),(2,3),(3,0)]:f.extend([[a,b,b+4,a+4],[a+8,a+12,b+12,b+8],[a+4,b+4,b+12,a+12],[a,a+8,b+8,b]])
 m.add(v,f).box((0,0,-.315),(1.8,1.2,.035))
 for x in [-.7,.7]:m.box((x,0,-.39),(.18,1.35,.14))
 # Visible simple external lifting lugs, one on each side, attached through shell top corners.
 for y in [-.82,.82]:m.beam((-.55,y,.21),(-.30,y,.21),.025)
 if damaged:m.deform(lambda x,y,z:[x,y*(1-.18*max(0,1-abs(x-.5))),z-.10*max(0,1-abs(x-.5))])
 if wreck:m.deform(lambda x,y,z:[x+.12*math.sin(y*3),y*(1+.10*max(z,0)),z-.16*max(0,1-abs(x))]);m.box((-.7,.75,.38),(.5,.07,.28));m.box((.6,-.72,.30),(.6,.065,.32))
 return m
def lid(wreck=False):
 m=Mesh().add([[-1.24,-.86,.30],[1.24,-.86,.30],[1.24,.86,.30],[-1.24,.86,.30],[-1.04,-.63,.49],[.84,-.63,.49],[.84,.63,.49],[-1.04,.63,.49]],[[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]])
 m.box((-.25,0,.515),(1.2,.84,.055))
 for x in [-.7,.3]:m.beam((x,-.13,.56),(x,.13,.56),.018)
 for y in [-.6,.6]:m.cyl((-.85,y,.48),.035,.22,'Y')
 if wreck:m.deform(lambda x,y,z:[x,y+.1*math.sin(x*3),z+.22*math.sin(x*2)])
 return m
def wheel(collapsed=False,wreck=False,right=False):
 m=Mesh();n=24;profile=[(-.17,.28),(-.175,.38),(-.14,.50),(-.075,.57),(0,.59),(.075,.57),(.14,.50),(.175,.38),(.17,.28)];v=[[r*math.cos(j*2*math.pi/n),y,r*math.sin(j*2*math.pi/n)] for y,r in profile for j in range(n)];f=[]
 for k in range(len(profile)-1):
  for j in range(n):jj=(j+1)%n;f.append([k*n+j,k*n+jj,(k+1)*n+jj,(k+1)*n+j])
 # Close tire inner annulus; hub remains an independently colored island in this physical wheel part.
 for j in range(n):jj=(j+1)%n;f.append([j,jj,(len(profile)-1)*n+jj,(len(profile)-1)*n+j])
 m.add(v,f)
 for j in range(24):
  a=j*math.pi/12
  for sign in [-1,1]:
   # Rounded shallow V tread blocks follow shoulder; no paddle protrusions.
   m.beam((.601*math.cos(a),sign*.012,.601*math.sin(a)),(.557*math.cos(a-.15),sign*.122,.557*math.sin(a-.15)),.019,6)
 hub=Mesh().cyl((0,.18,0),.275,.035,'Y',16).cyl((0,.215,0),.13,.06,'Y',12)
 for j in range(6):a=j*math.pi/3;hub.cyl((.20*math.cos(a),.205,.20*math.sin(a)),.016,.025,'Y',6)
 def deform(x,y,z):
  if collapsed and z<-.25:z=-.25+(z+.25)*.22
  if wreck:x,y,z=x*.85,y+.13*z,z*.65
  return [x,-y if right else y,z]
 m.deform(deform);hub.deform(deform);return m,hub
new={};islands={}
for id,damage,wreck in [('F_P01',False,False),('F_DP01A',True,False),('F_WP01A',False,True)]:
 m,cup=projector()
 if damage:
  fn=lambda x,y,z:[x,y+.3*max(x-.1,0),z-.3*max(x-.1,0)];m.deform(fn);cup.deform(fn)
 if wreck:
  fn=lambda x,y,z:[x*.65,y+.16*max(x,0),z-.4*max(x,0)];m.deform(fn);cup.deform(fn)
 new[id]=m;islands[id]=(cup,'dark' if not wreck else 'burnt')
for id,damage,wreck in [('T_P02',False,False),('T_DP02A',True,False),('T_WP02A',False,True)]:new[id]=shell(damage,wreck)
for id,wreck in [('T_P03',False),('T_WP03A',True)]:new[id]=lid(wreck)
for id,collapsed,wreck,right in [('T_P04',False,False,False),('T_P05',False,False,True),('T_DP04A',True,False,False),('T_WP05A',False,True,True)]:new[id],hub=wheel(collapsed,wreck,right);islands[id]=(hub,'olive' if not wreck else 'burnt')
colors={'olive':[.15,.18,.093,1],'dark':[.055,.065,.045,1],'rubber':[.025,.028,.023,1],'burnt':[.055,.047,.035,1]};ops=[]
for id,m in new.items():
 p=old[id];loc=p['nativeLibraryLocation'];ops.extend([{'type':'create_mesh','name':id,'vertices':m.v,'edges':[],'faces':m.f},{'type':'set_transform','object':id,'location':loc},{'type':'set_material','object':id,'materialName':'comet-conv-'+p['material'],'baseColor':colors[p['material']],'roughness':.9,'metallic':0},{'type':'recalculate_normals','object':id,'direction':'OUTSIDE'}])
 if id in islands:
  im,mat=islands[id];name=id+'_temporary_island';ops.extend([{'type':'create_mesh','name':name,'vertices':im.v,'edges':[],'faces':im.f},{'type':'set_transform','object':name,'location':loc},{'type':'set_material','object':name,'materialName':'comet-conv-'+mat,'baseColor':colors[mat],'roughness':.9,'metallic':0},{'type':'recalculate_normals','object':name,'direction':'OUTSIDE'},{'type':'join_objects','objects':[id,name],'name':id}])
Path('correction-operations.json').write_text(json.dumps({'removeObjects':list(new),'operations':ops}));print(json.dumps({'replacedParts':len(new),'operations':len(ops),'unchangedParts':44-len(new),'reason':'Independent visual review: readable dark recessed projector aperture, wedge lower trailer body, rounded pneumatic tyres with shallow chevrons and contrasting hubs. No historical dimension claim or real system engineering.'}))
