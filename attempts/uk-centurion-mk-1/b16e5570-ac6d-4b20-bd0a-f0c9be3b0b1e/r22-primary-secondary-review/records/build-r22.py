"""George-directed r22 flange pass (human-directed, budgetCharge 0), based on approved r21 (e43c5542...2fce5).

Direction (verbatim, recorded in status.json polishAuthorization.georgeDirectionR22):
  "Next flange pass: Full reviewer package: wider ring (~0.24-0.26 m), more/larger bolts, blended cast boss
   with flat land, remove overlap (P06+P09, same axis)" / "Flange tone: Split: dark ring and bolts, olive collar" /
  "Lifting eyes: Keep as designed".

Reference re-check (private photo-2-larger, sha 6fad0642..., research only): a dark flat bolted ring, outer diameter
clearly larger than the lighter collar (collar about 60% of the ring diameter); about five bolt heads on the visible
upper/right arc, so more than eight in total; the ring sits on a flat face inside a lighter rounded cast swelling that
blends back into the cheek with no hard edge.

Fixed (read-only, not inferred): P09 parent M.polsten-ball at turret-local (1.12, 0.82, 0.35), axis +X. P07 unchanged.
Measured constraints from the r21 scene (Polsten-local): the P07 mantlet side face is about 0.258-0.263 m from the axis
in the ring plane, and the turret roof edge is about 0.238 m above it. RO 0.245 is inside George's 0.24-0.26 range and
keeps about 13-18 mm clearance to the mantlet.

Design choices (proportioned from photo-2; no dimension, axis, articulation or recoil inferred):
  P09  ONE closed single-skin lathe: rear face on the boss land (x -0.03), ring outer wall r 0.245, front chamfer, ring
       front face at x -0.004 down to the collar, then the r21 collar/dome profile forward. Collar and ring share one
       surface, so the r21 3-5 mm dome/ring interpenetration is gone. 12 square bolt heads (26 mm, 14 mm proud,
       2 mm seated) on the ring face; square rather than hex is a triangle-budget choice. Ring, chamfer, rear face and bolts use the existing dark "steel"
       material (assign_material_slot faceIndices); the collar keeps "olive". Smooth-shaded, 35 degree auto-smooth.
  P06  r8 shell (unchanged source) minus a spot-face recess (cylinder r 0.272, x >= -0.033), joined with a smooth-shaded
       cast boss lathe (20 segments): flat land r 0.270 at x -0.03 (25 mm visible land outside the ring), a 45 degree edge
       step to r 0.287 softened by 50 degree auto-smooth, then a skirt flaring back to r 0.37 so the outboard side meets
       the cheek at a shallower angle. The boss
       bottom is clipped flat inside the turret (z_turret 0.045) by a bounded box difference so nothing hangs below the
       turret floor. The ring is still owned by P09 under M.polsten-ball (authorized known limitation).
"""
import json, math, hashlib, collections, sys
from pathlib import Path

O = Path(__file__).parent
J = O.parents[1]
JOB = 'b16e5570-ac6d-4b20-bd0a-f0c9be3b0b1e'
PX, PY, PZ = 1.12, 0.82, 0.35
P = dict(N09=24, N06=20, RO=0.245, RL=0.270, RC=0.272, NB=12, BOLT_HALF=0.013, BOLT_H=0.014, X_FACE=-0.03, X_RFRONT=-0.004,
         CLIP_Z=0.045)
if len(sys.argv) > 1:
    P.update(json.loads(sys.argv[1]))
tri = lambda m: sum(len(f) - 2 for f in m['faces'])


def check(mesh, oriented=True):
    edges = collections.Counter(tuple(sorted((a, b))) for f in mesh['faces'] for a, b in zip(f, f[1:] + f[:1]))
    bad = [e for e, n in edges.items() if n != 2]
    assert not bad, (mesh['name'], 'not closed 2-manifold', bad[:5])
    directed = collections.Counter((a, b) for f in mesh['faces'] for a, b in zip(f, f[1:] + f[:1]))
    assert all(n == 1 for n in directed.values()), (mesh['name'], 'inconsistent winding')
    assert all(len(set(f)) == len(f) for f in mesh['faces'])
    V = mesh['vertices']  # signed volume must be positive (outward winding)
    vol = 0.0
    for f in mesh['faces']:
        a = V[f[0]]
        for i in range(1, len(f) - 1):
            b, c = V[f[i]], V[f[i + 1]]
            vol += (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6
    assert vol > 0 or not oriented, (mesh['name'], 'inward winding', vol)
    return vol


class Builder:
    def __init__(s): s.v = []; s.f = []

    def add_v(s, p): s.v.append([round(c, 6) for c in p]); return len(s.v) - 1

    def ring(s, pts): return [s.add_v(p) for p in pts]

    def band(s, a, b):  # surface from ring a to ring b; outward when the profile runs rear->front with r on the outside
        n = len(a); out = []
        for k in range(n): s.f.append([a[k], a[(k + 1) % n], b[(k + 1) % n], b[k]]); out.append(len(s.f) - 1)
        return out

    def cap(s, r, front):  # front cap faces +X, rear cap faces -X
        s.f.append(list(r) if front else list(reversed(r))); return [len(s.f) - 1]

    def mesh(s, name): return {'type': 'create_mesh', 'name': name, 'vertices': s.v, 'faces': s.f}


def circle(x, r, n, c=(0.0, 0.0, 0.0), phase=0.0):
    return [[c[0] + x, c[1] + r * math.cos(2 * math.pi * k / n + phase), c[2] + r * math.sin(2 * math.pi * k / n + phase)]
            for k in range(n)]


def lathe(b, profile, n, c=(0.0, 0.0, 0.0)):
    """profile: (x, r) rear->front. Returns per-band face index lists and cap face indices."""
    rings = [b.ring(circle(x, r, n, c)) for x, r in profile]
    rear = b.cap(rings[0], front=False)
    bands = [b.band(a, d) for a, d in zip(rings, rings[1:])]
    front = b.cap(rings[-1], front=True)
    return rear, bands, front


# winding sanity for band(): ring a at x0, ring b at x1>x0, k increasing counter-clockwise seen from +X.
# Face [a_k, a_k+1, b_k+1, b_k]: edge a_k->a_k+1 is +theta, then +profile; normal = theta x profile, outward for a
# rear->front profile (theta x X = +r) and +X for an inward step at constant x (theta x -r = +X). check() verifies.

# ---------------- P09: single-skin ring + collar ----------------
N09, RO, XF, XR = P['N09'], P['RO'], P['X_FACE'], P['X_RFRONT']
dome = [(-.06, .1607), (-.025, .163), (.025, .160), (.085, .142), (.145, .112), (.19, .054)]  # r21 profile


def dome_r(x):
    for (x0, r0), (x1, r1) in zip(dome, dome[1:]):
        if x0 <= x <= x1: return r0 + (r1 - r0) * (x - x0) / (x1 - x0)
    raise ValueError(x)


RD = round(dome_r(XR), 5)
CH = 0.006
p09prof = [(XF, RO), (XR - CH, RO), (XR, RO - CH), (XR, RD)] + [(x, r) for x, r in dome if x > XR]
b = Builder()
rear, bands, front = lathe(b, p09prof, N09)
dark = rear + bands[0] + bands[1] + bands[2]  # ring outer wall, chamfer, ring front face; rear face sits on the land
# 12 square bolt heads (26 mm, flats tangential) on the ring front face, seated 2 mm into the face.
# Square rather than hex is a triangle-budget design choice (12 vs 20 triangles per head).
NB, BR, BH = P['NB'], P['BOLT_HALF'] * math.sqrt(2), P['BOLT_H']
RB = (RD + RO - CH) / 2
for k in range(NB):
    a = 2 * math.pi * (k + .5) / NB
    ur = (math.cos(a), math.sin(a)); ut = (-math.sin(a), math.cos(a))
    cy, cz = RB * ur[0], RB * ur[1]
    hexes = []
    for x in (XR - .002, XR + BH):
        pts = []
        for j in range(4):  # corners on the diagonals, flats radial/tangential
            t = 2 * math.pi * j / 4 + math.pi / 4
            pts.append([x, cy + BR * (math.cos(t) * ur[0] + math.sin(t) * ut[0]), cz + BR * (math.cos(t) * ur[1] + math.sin(t) * ut[1])])
        hexes.append(b.ring(pts))
    first = len(b.f)
    b.cap(hexes[0], front=False); b.band(hexes[0], hexes[1]); b.cap(hexes[1], front=True)
    dark += list(range(first, len(b.f)))
p09 = b.mesh('P09')
p09vol = check(p09)
p09dark = sorted(dark)
assert RB - BR > RD + .004 and RB + BR < RO - CH, 'bolts must sit on the ring face'

r21 = json.loads((J / 'evidence/polish-r21/r21-request.json').read_text())
olive = {'type': 'set_material', 'object': 'P09', 'materialName': 'olive', 'baseColor': [0.18, 0.205, 0.125, 1], 'roughness': 0.85, 'metallic': 0.15}
p09ops = [p09,
          {'type': 'set_parent', 'object': 'P09', 'parent': 'M.polsten-ball', 'keepTransform': False},
          {'type': 'recalculate_normals', 'object': 'P09', 'direction': 'OUTSIDE'},
          olive,
          {'type': 'assign_material_slot', 'object': 'P09', 'materialName': 'steel', 'faceIndices': p09dark},
          {'type': 'set_smoothing', 'object': 'P09', 'smooth': True, 'autoSmoothAngleDegrees': 35}]
r21p09aux = [o for o in r21['operations'] if o.get('object') == 'P09']
assert [o['type'] for o in r21p09aux] == ['set_parent', 'recalculate_normals', 'set_material', 'set_smoothing']
assert r21p09aux[0] == p09ops[1] and r21p09aux[2] == olive and r21p09aux[3] == p09ops[5]

# ---------------- P06: recess + blended cast boss ----------------
C = (PX, PY, PZ)
N06, RL, RC = P['N06'], P['RL'], P['RC']
r8 = json.loads((J / 'evidence/blockout-r4/turret-r8-operations.json').read_text())
p06src = [o for o in r8 if (o.get('name') or o.get('object')) == 'P06']
p06mesh = next(o for o in p06src if o['type'] == 'create_mesh')
check(p06mesh, oriented=False)  # unchanged r8 source; its own recalculate_normals op orients it
cut = Builder(); lathe(cut, [(XF - .003, RC), (0.25, RC)], N06, C)
cutter = cut.mesh('P06-spotface-cutter'); check(cutter)
# boss: flat land, one 45 degree edge step softened by 50 degree auto-smooth, flaring skirt (budget: 4 rings)
edge = [(XF, RL), (XF - 0.015, RL + 0.017)]
skirt = [(-0.16, 0.305), (-0.42, 0.370)]
bossprof = list(reversed(edge + skirt))  # rear -> front
bb = Builder(); lathe(bb, bossprof, N06, C)
bossm = bb.mesh('P06-boss'); check(bossm)
# bounded clip box below the turret floor plane (turret-local z < CLIP_Z), only around the boss
cz0, cz1 = -0.20, P['CLIP_Z']
cb = Builder()
xs, ys = (PX - 0.50, PX + 0.05), (PY - 0.50, PY + 0.50)
corners = [[x, y, z] for z in (cz0, cz1) for (x, y) in ((xs[0], ys[0]), (xs[1], ys[0]), (xs[1], ys[1]), (xs[0], ys[1]))]
for p in corners: cb.add_v(p)
cb.f = [[3, 2, 1, 0], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
clip = cb.mesh('P06-boss-floor-clip'); check(clip)
smooth = lambda o, a=35: {'type': 'set_smoothing', 'object': o, 'smooth': True, 'autoSmoothAngleDegrees': a}
p06ops = [p06mesh, cutter,
          {'type': 'recalculate_normals', 'object': 'P06-spotface-cutter', 'direction': 'OUTSIDE'},
          smooth('P06-spotface-cutter'),
          {'type': 'boolean_difference', 'object': 'P06', 'cutter': 'P06-spotface-cutter', 'removeCutter': True},
          bossm,
          {'type': 'recalculate_normals', 'object': 'P06-boss', 'direction': 'OUTSIDE'},
          clip,
          {'type': 'recalculate_normals', 'object': 'P06-boss-floor-clip', 'direction': 'OUTSIDE'},
          {'type': 'boolean_difference', 'object': 'P06-boss', 'cutter': 'P06-boss-floor-clip', 'removeCutter': True},
          smooth('P06-boss', 50),
          {'type': 'join_objects', 'objects': ['P06', 'P06-boss'], 'name': 'P06'}] + \
         [o for o in p06src if o['type'] != 'create_mesh']
assert [o['type'] for o in p06ops[12:]] == ['set_parent', 'recalculate_normals', 'set_material']
r21p06aux = [o for o in r21['operations'] if o.get('object') == 'P06' and o['type'] in ('set_parent', 'set_material')]
assert r21p06aux == [p06ops[12], p06ops[14]]

ops = p06ops + p09ops
KEY = P.get('KEY', 'centurion-r22-flange-package-20261112-v1')
req = {'jobId': JOB, 'expectedRevision': 21, 'idempotencyKey': KEY, 'removeObjects': ['P06', 'P09'], 'operations': ops}
out = Path(P.get('OUT', O / 'r22-request.json'))
out.write_text(json.dumps(req) + '\n')
r21p09 = next(o for o in r21['operations'] if o.get('name') == 'P09' and o['type'] == 'create_mesh')
info = {
    'requestPath': str(out), 'requestSha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'parameters': P,
    'operations': len(ops),
    'p09': {'trianglesR21': tri(r21p09), 'trianglesR22': tri(p09), 'profile': p09prof, 'ringOuterRadius': RO,
            'ringFaceRadiusInner': RD, 'collarToRingDiameterRatio': round(RD / RO, 3), 'bolts': NB,
            'boltHeadSquare': 2 * P['BOLT_HALF'], 'boltProud': BH, 'boltCircleRadius': round(RB, 4), 'darkFaces': len(p09dark),
            'closedVolume': round(p09vol, 6), 'overlap': 'none: ring and collar are one closed single-skin lathe'},
    'p06': {'sourceTriangles': tri(p06mesh), 'cutterTriangles': tri(cutter), 'bossTriangles': tri(bossm), 'clipTriangles': tri(clip),
            'bossProfile': bossprof, 'landRadius': RL, 'cutterRadius': RC, 'flatLandOutsideRing': round(RL - RO, 4)},
    'r21TrianglesTotal': 49938, 'triangleBudget': 50000}
if 'OUT' not in P:
    (O / 'build-r22.json').write_text(json.dumps(info, indent=2) + '\n')
print(json.dumps(info, indent=2))
