"""George-directed r24 bolt restore (human-directed, budgetCharge 0), based on r23 (d5661b5e...5b26cdf76; not approved).

r24 direction (verbatim, status.json polishAuthorization.georgeDirectionR24):
  "1. Artwork review: Not approved; correct in r24
   2. Bolts: Restore the same 12 bolts after the floor cut, seated on the ring face; no other change
   3. Kink: Accept the softened kink"
r24 change vs r23: the 12 bolt heads (same size, count, bolt circle and phase) are built as a separate closed mesh
P06-bolts whose rear face sits exactly on the ring face (x = X_RFRONT, no embedding), created AFTER the floor-clip
boolean and joined into P06-flange, so the EXACT boolean can no longer drop them. Only P06 is replaced; P09 is retained.
Everything else in this script is the r23 construction, unchanged.

r23 history follows.

Direction (verbatim, recorded in status.json polishAuthorization.georgeDirectionR23):
  "1. Artwork review: Not approved; further P06/P09 pass on r22
   2. Flange attachment: A: move ring/bolts/collar to the fixed turret side; ball moves alone (same axis, same shapes)
   3. Further pass scope: smooth boss outline and remove kink"
Not selected (left as is): inboard wedge pocket fill, remaining hidden overlap removal.

Fixed (read-only, not inferred): Polsten axis at turret-local (1.12, 0.82, 0.35), +X; M.polsten-ball and P10 unchanged.
No dimension, axis, articulation or recoil is inferred from the private reference (photo-2, research only).

Construction:
  Fixed side (joined into P06, parent M.turret): ONE closed 24-segment lathe, rear->front
     straight cast skirt (-0.42, 0.37) -> rounded edge (-0.045, 0.288) -> flat land (-0.03, 0.270 -> 0.245)
     -> r22 ring wall r 0.245 -> r22 6 mm chamfer -> r22 ring face x -0.004 -> r22 collar to the split plane x 0.025,
     plus the r22 12 square bolt heads on the ring face. Ring, chamfer, ring face and bolts use "steel"; skirt, land and
     collar use "olive". The r22 two-segment skirt (corner at x -0.16) is replaced by one straight flare, and the boss
     goes from 20 to 24 segments, matching the ring (r22 land/ring coincident caps are gone because they are one surface).
  Moving side (P09, parent M.polsten-ball): the r22 dome forward of x 0.025 unchanged in shape, closed by a rear cap.
  Split plane x 0.025 (where the r21/r22 profile turns from the near-cylindrical collar into the tapering dome) is an
  interpretation of "collar" and a design choice.
  P06 shell: unchanged r8 source minus the spot-face recess (now 24 segments, r 0.273 so its flats clear the land).
  Bounded floor clip at turret-local z 0.045 kept from r22. Triangle budget 50,000 is the binding constraint.
Design choices: boss profile (skirt, edge, land), 12-bolt count and square heads, collar/ball split plane.
"""
import json, math, hashlib, collections, sys
from pathlib import Path

O = Path(__file__).parent
J = O.parents[1]
JOB = 'b16e5570-ac6d-4b20-bd0a-f0c9be3b0b1e'
PX, PY, PZ = 1.12, 0.82, 0.35
P = dict(N=24, RO=0.245, RL=0.270, RC=0.273, NB=12, BOLT_HALF=0.013, BOLT_H=0.014, X_FACE=-0.03, X_RFRONT=-0.004,
         X_SPLIT=0.025, CLIP_Z=0.045, SKIRT=(-0.42, 0.37), EDGE=(-0.045, 0.288))
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


N, RO, XF, XR, XS = P['N'], P['RO'], P['X_FACE'], P['X_RFRONT'], P['X_SPLIT']
C = (PX, PY, PZ)
dome = [(-.06, .1607), (-.025, .163), (.025, .160), (.085, .142), (.145, .112), (.19, .054)]  # r21/r22 profile


def dome_r(x):
    for (x0, r0), (x1, r1) in zip(dome, dome[1:]):
        if x0 <= x <= x1: return r0 + (r1 - r0) * (x - x0) / (x1 - x0)
    raise ValueError(x)


RD = round(dome_r(XR), 5)
CH = 0.006
assert any(abs(x - XS) < 1e-9 for x, _ in dome), 'split must sit on an existing profile ring'
RS = dome_r(XS)
fixedprof = [tuple(P['SKIRT']), tuple(P['EDGE']), (XF, P['RL']), (XF, RO), (XR - CH, RO), (XR, RO - CH), (XR, RD), (XS, RS)]
b = Builder()
rings = [b.ring(circle(x, r, N, C)) for x, r in fixedprof]
rear = b.cap(rings[0], front=False)
bands = [b.band(a, d) for a, d in zip(rings, rings[1:])]
front = b.cap(rings[-1], front=True)
# bands: 0 skirt, 1 edge, 2 land, 3 ring wall, 4 chamfer, 5 ring face, 6 collar
dark = bands[3] + bands[4] + bands[5]
NB, BR, BH = P['NB'], P['BOLT_HALF'] * math.sqrt(2), P['BOLT_H']
RB = (RD + RO - CH) / 2
flange = b.mesh('P06-flange')
flvol = check(flange)
darkfaces = sorted(dark)
b = Builder()  # r24: bolts are their own closed mesh, added after the floor clip
for k in range(NB):
    a = 2 * math.pi * (k + .5) / NB
    ur = (math.cos(a), math.sin(a)); ut = (-math.sin(a), math.cos(a))
    cy, cz = RB * ur[0], RB * ur[1]
    sq = []
    for x in (XR, XR + BH):  # r24: seated on the ring face (r23: XR - .002, embedded)
        pts = []
        for j in range(4):
            t = 2 * math.pi * j / 4 + math.pi / 4
            pts.append([C[0] + x, C[1] + cy + BR * (math.cos(t) * ur[0] + math.sin(t) * ut[0]), C[2] + cz + BR * (math.cos(t) * ur[1] + math.sin(t) * ut[1])])
        sq.append(b.ring(pts))
    b.cap(sq[0], front=False); b.band(sq[0], sq[1]); b.cap(sq[1], front=True)
assert RB - BR > RD + .004 and RB + BR < RO - CH, 'bolts must sit on the ring face'
bolts = b.mesh('P06-bolts')
boltsvol = sum(check({'name': 'bolt', 'vertices': bolts['vertices'], 'faces': bolts['faces'][6 * k:6 * k + 6]}) for k in range(NB))
assert len(bolts['faces']) == 6 * NB
assert PZ - (RB + BR) > P['CLIP_Z'], 'bolts clear of the floor clip'

bb = Builder(); ballprof = [(x, r) for x, r in dome if x >= XS - 1e-9]
lathe(bb, ballprof, N)
ball = bb.mesh('P09'); ballvol = check(ball)

r22 = json.loads((J / 'evidence/polish-r22/r22-request.json').read_text())
r22ops = r22['operations']
olive = next(o for o in r22ops if o['type'] == 'set_material' and o['object'] == 'P09')
assert olive['materialName'] == 'olive'
smooth = lambda o, a: {'type': 'set_smoothing', 'object': o, 'smooth': True, 'autoSmoothAngleDegrees': a}
p09ops = [ball,
          {'type': 'set_parent', 'object': 'P09', 'parent': 'M.polsten-ball', 'keepTransform': False},
          {'type': 'recalculate_normals', 'object': 'P09', 'direction': 'OUTSIDE'},
          olive, smooth('P09', 35)]
r22p09aux = [o for o in r22ops if o.get('object') == 'P09' and o['type'] in ('set_parent', 'recalculate_normals', 'set_smoothing')]
assert r22p09aux == [p09ops[1], p09ops[2], p09ops[4]]

r8 = json.loads((J / 'evidence/blockout-r4/turret-r8-operations.json').read_text())
p06src = [o for o in r8 if (o.get('name') or o.get('object')) == 'P06']
p06mesh = next(o for o in p06src if o['type'] == 'create_mesh')
check(p06mesh, oriented=False)
cut = Builder(); lathe(cut, [(XF - .003, P['RC']), (0.25, P['RC'])], N, C)
cutter = cut.mesh('P06-spotface-cutter'); check(cutter)
assert P['RC'] * math.cos(math.pi / N) > P['RL'], 'recess flats must clear the land corners'
cz0, cz1 = -0.20, P['CLIP_Z']
cb = Builder()
xs, ys = (PX - 0.50, PX + 0.05), (PY - 0.50, PY + 0.50)
for p in [[x, y, z] for z in (cz0, cz1) for (x, y) in ((xs[0], ys[0]), (xs[1], ys[0]), (xs[1], ys[1]), (xs[0], ys[1]))]: cb.add_v(p)
cb.f = [[3, 2, 1, 0], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
clip = cb.mesh('P06-flange-floor-clip'); check(clip)
assert all(PZ - RO > cz1 for _ in [0]), 'clip must not touch the ring'
p06ops = [p06mesh, cutter,
          {'type': 'recalculate_normals', 'object': 'P06-spotface-cutter', 'direction': 'OUTSIDE'},
          smooth('P06-spotface-cutter', 35),
          {'type': 'boolean_difference', 'object': 'P06', 'cutter': 'P06-spotface-cutter', 'removeCutter': True},
          flange,
          {'type': 'recalculate_normals', 'object': 'P06-flange', 'direction': 'OUTSIDE'},
          dict(olive, object='P06-flange'),
          {'type': 'assign_material_slot', 'object': 'P06-flange', 'materialName': 'steel', 'faceIndices': darkfaces},
          clip,
          {'type': 'recalculate_normals', 'object': 'P06-flange-floor-clip', 'direction': 'OUTSIDE'},
          {'type': 'boolean_difference', 'object': 'P06-flange', 'cutter': 'P06-flange-floor-clip', 'removeCutter': True},
          smooth('P06-flange', 50),
          bolts,
          {'type': 'recalculate_normals', 'object': 'P06-bolts', 'direction': 'OUTSIDE'},
          dict(olive, object='P06-bolts'),
          {'type': 'assign_material_slot', 'object': 'P06-bolts', 'materialName': 'steel', 'faceIndices': list(range(len(bolts['faces'])))},
          smooth('P06-bolts', 50),
          {'type': 'join_objects', 'objects': ['P06-flange', 'P06-bolts'], 'name': 'P06-flange'},
          {'type': 'join_objects', 'objects': ['P06', 'P06-flange'], 'name': 'P06'}] + \
         [o for o in p06src if o['type'] != 'create_mesh']
assert [o['type'] for o in p06ops[20:]] == ['set_parent', 'recalculate_normals', 'set_material']
r22p06aux = [o for o in r22ops if o.get('object') == 'P06' and o['type'] in ('set_parent', 'set_material')]
assert r22p06aux == [p06ops[20], p06ops[22]]

ops = p06ops  # r24: P09 retained unchanged from r23
r23req = json.loads((J / 'evidence/polish-r23/r23-request.json').read_text())
r23p06 = r23req['operations'][:len(r23req['operations']) - 5]
same = [o for o in p06ops if o['type'] != 'create_mesh' or o['name'] != 'P06-flange']
same = [o for o in same if o.get('object') != 'P06-bolts' and o.get('name') != 'P06-bolts' and o.get('objects') != ['P06-flange', 'P06-bolts']]
r23same = [o for o in r23p06 if o['type'] != 'create_mesh' or o['name'] != 'P06-flange']
diff = [(x, y) for x, y in zip(same, r23same) if x != y]
assert len(same) == len(r23same) and len(diff) == 1, 'r24 P06 ops other than the flange mesh, bolts and steel slot must equal r23'
(x, y), = diff
assert x['type'] == y['type'] == 'assign_material_slot' and x['object'] == 'P06-flange'
assert y['faceIndices'][:len(x['faceIndices'])] == x['faceIndices'] and len(y['faceIndices']) - len(x['faceIndices']) == 6 * NB, 'steel slot = r23 minus the bolt faces'
r23fl = next(o for o in r23p06 if o.get('name') == 'P06-flange')
nfl = len(flange['vertices'])
assert r23fl['vertices'][:nfl] == flange['vertices'] and r23fl['faces'][:len(flange['faces'])] == flange['faces'], 'flange lathe identical to r23'
r23bolt = r23fl['vertices'][nfl:]
assert len(r23bolt) == len(bolts['vertices']) == 8 * NB
for a, c in zip(r23bolt, bolts['vertices']):
    assert abs(a[1] - c[1]) < 1e-9 and abs(a[2] - c[2]) < 1e-9 and (abs(a[0] - c[0]) < 1e-9 or abs(a[0] + .002 - c[0]) < 1e-9), 'same bolts, rear face moved onto ring face'
KEY = P.get('KEY', 'centurion-r24-bolt-restore-20261112-v1')
req = {'jobId': JOB, 'expectedRevision': 23, 'idempotencyKey': KEY, 'removeObjects': ['P06'], 'operations': ops}
out = Path(P.get('OUT', O / 'r24-request.json'))
out.write_text(json.dumps(req) + '\n')
r22p09 = next(o for o in r22ops if o.get('name') == 'P09' and o['type'] == 'create_mesh')
r22boss = next(o for o in r22ops if o.get('name') == 'P06-boss')
info = {
    'requestPath': str(out), 'requestSha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'parameters': P,
    'operations': len(ops),
    'fixedFlange': {'owner': 'P06 (parent M.turret)', 'profile': fixedprof, 'segments': N, 'triangles': tri(flange),
                    'darkFaces': len(darkfaces), 'bolts': NB, 'boltCircleRadius': round(RB, 4), 'closedVolume': round(flvol, 6),
                    'ringFaceRadiusInner': RD, 'splitRadius': RS},
    'ball': {'owner': 'P09 (parent M.polsten-ball)', 'profile': ballprof, 'segments': N, 'triangles': tri(ball), 'closedVolume': round(ballvol, 6)},
    'r22Comparison': {'p09Triangles': tri(r22p09), 'bossTriangles': tri(r22boss), 'bossSegments': 20,
                      'bossProfile': [[-0.42, 0.37], [-0.16, 0.305], [-0.045, 0.287], [-0.03, 0.27]]},
    'bolts': {'count': NB, 'triangles': tri(bolts), 'rearFaceX': XR, 'frontFaceX': XR + BH, 'closedVolume': round(boltsvol, 7), 'boltCircleRadius': round(RB, 4)},
    'estimatedTriangleDeltaVsR23': tri(bolts), 'r23TrianglesTotal': 49838,
    'cutter': {'segments': N, 'radius': P['RC'], 'flatRadius': round(P['RC'] * math.cos(math.pi / N), 5), 'triangles': tri(cutter)},
    'r22TrianglesTotal': 49940, 'triangleBudget': 50000}
if 'OUT' not in P:
    (O / 'build-r24.json').write_text(json.dumps(info, indent=2) + '\n')
print(json.dumps({k: info[k] for k in ('estimatedTriangleDeltaVsR23', 'requestSha256', 'operations')}), info['fixedFlange']['triangles'], info['bolts'])
