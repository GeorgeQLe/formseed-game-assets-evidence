"""George-directed 2026-11-11 (r20 decision page reply):
  1. r20 not approved; keep as working baseline and polish further.
  2. Flange option A: local P06 pad on the EXISTING Polsten axis + complete P09 ring (P06 change authorized).
  3. Mantlet follow-up: lifting eyes only (check references first, infer nothing).

Reference: photo-2-larger (private research, sha 6fad0642...) shows a dark bolted ring flange seated on a flat
face in a raised cast boss on the turret cheek, and two small loop lifting eyes on top of the mantlet near its ends.

Geometry facts (read-only): P06 (fingerprint f6c847b9, unchanged since r8) is rebuilt from the exact r8 create_mesh.
M.polsten-ball sits at turret-local (1.12, 0.82, 0.35) with its axis along +X (datum-verified X/Y/Z). The cheek is
oblique to that axis: at r=0.19 its surface runs from Polsten-local x=-0.162 (outboard) to +0.118 (inboard).

Design (all radii/thicknesses are design choices proportioned from photo-2; no dimension, axis, articulation or recoil
inferred):
  P06  spot face square to the existing axis at Polsten-local x=-0.03: a cylindrical cutter (r 0.197, x>=-0.033; r 0.205 grazed the front-face edge by 0.2 mm and the boolean was rejected as non-manifold) is
       boolean-subtracted (opens an inboard recess) and a closed boss cylinder (r 0.196, x -0.28..-0.03) is joined
       (stands proud outboard). Everything else in P06 is the r8 source.
  P09  single-skin lathe dome (same outer profile as r18/r19 from x=-0.06; rear and front closed with flat caps,
       replacing the r19 collapsed inner skin and 0.043 bore), complete ring flange r 0.158..0.195, x -0.03..-0.005,
       and 8 bolt heads (photo shows more; 8 is a budget simplification).
  P07  r20 mesh unchanged plus two closed square-section loop lifting eyes in the lateral (y-z) plane at x=0.08,
       centred 0.39 m either side of the mantlet's lateral centre. Loop plane orientation is a design choice; the photo
       resolution does not settle it.
Known limitation: the ring belongs to P09 under M.polsten-ball as authorized; if Polsten articulation is ever added
the fixed flange would need to move to the turret side.
"""
import json, math, hashlib, collections
from pathlib import Path

O = Path(__file__).parent
J = O.parents[1]
JOB = 'b16e5570-ac6d-4b20-bd0a-f0c9be3b0b1e'
N = 24
PX, PY, PZ = 1.12, 0.82, 0.35  # Polsten-ball origin in M.turret space
tri = lambda m: sum(len(f) - 2 for f in m['faces'])


def check(mesh):
    edges = collections.Counter(tuple(sorted((a, b))) for f in mesh['faces'] for a, b in zip(f, f[1:] + f[:1]))
    bad = [e for e, n in edges.items() if n != 2]
    assert not bad, (mesh['name'], 'not closed 2-manifold', bad[:5])
    assert all(len(set(f)) == len(f) for f in mesh['faces'])


class Builder:
    def __init__(s): s.v = []; s.f = []

    def add_v(s, p): s.v.append([round(c, 6) for c in p]); return len(s.v) - 1

    def ring(s, pts): return [s.add_v(p) for p in pts]

    def band(s, a, b):  # a, b rings with outward winding a->b
        n = len(a)
        for k in range(n): s.f.append([a[k], a[(k + 1) % n], b[(k + 1) % n], b[k]])

    def cap(s, r, reverse=False): s.f.append(list(reversed(r)) if reverse else list(r))

    def mesh(s, name): return {'type': 'create_mesh', 'name': name, 'vertices': s.v, 'faces': s.f}


def circle(x, r, cx=0.0, cy=0.0, cz=0.0, n=N, phase=0.0):
    return [[cx + x, cy + r * math.cos(2 * math.pi * k / n + phase), cz + r * math.sin(2 * math.pi * k / n + phase)]
            for k in range(n)]


def cylinder(b, x0, x1, r, **kw):
    a = b.ring(circle(x0, r, **kw)); c = b.ring(circle(x1, r, **kw))
    b.band(a, c); b.cap(a, reverse=True); b.cap(c, reverse=False)  # outward caps (rear faces -X)


# ---------------- P06 ----------------
r8 = json.loads((J / 'evidence/blockout-r4/turret-r8-operations.json').read_text())
p06src = [o for o in r8 if (o.get('name') or o.get('object')) == 'P06']
p06mesh = next(o for o in p06src if o['type'] == 'create_mesh')
check(p06mesh)
X_FACE = -0.03
cut = Builder(); cylinder(cut, X_FACE - 0.003, 0.25, 0.197, cx=PX, cy=PY, cz=PZ)
boss = Builder(); cylinder(boss, -0.28, X_FACE, 0.196, cx=PX, cy=PY, cz=PZ)
cutter = cut.mesh('P06-spotface-cutter'); bossm = boss.mesh('P06-boss')
check(cutter); check(bossm)
p06ops = [p06mesh, cutter,
          {'type': 'recalculate_normals', 'object': 'P06-spotface-cutter', 'direction': 'OUTSIDE'},
          {'type': 'boolean_difference', 'object': 'P06', 'cutter': 'P06-spotface-cutter', 'removeCutter': True},
          bossm,
          {'type': 'join_objects', 'objects': ['P06', 'P06-boss'], 'name': 'P06'}] + \
         [o for o in p06src if o['type'] != 'create_mesh']
assert [o['type'] for o in p06ops[6:]] == ['set_parent', 'recalculate_normals', 'set_material']

# ---------------- P09 ----------------
b = Builder()
profile = [(-.06, .1607), (-.025, .163), (.025, .160), (.085, .142), (.145, .112), (.19, .054)]
rings = [b.ring(circle(x, r)) for x, r in profile]
for a, c in zip(rings, rings[1:]): b.band(a, c)
b.cap(rings[0], reverse=True); b.cap(rings[-1], reverse=False)
# ring flange (rectangular section)
RI, RO, X0, X1 = .158, .195, X_FACE, -0.005
q = [b.ring(circle(X0, RI)), b.ring(circle(X0, RO)), b.ring(circle(X1, RO)), b.ring(circle(X1, RI))]
for i in range(4): b.band(q[(i + 1) % 4], q[i])
# 8 bolt heads (closed boxes), radial-aligned, on the ring front face
for k in range(8):
    a = 2 * math.pi * (k + .5) / 8; rr = (RI + RO) / 2; h = .009
    ur = (0, math.cos(a), math.sin(a)); ut = (0, -math.sin(a), math.cos(a))
    corners = []
    for x in (X1 - .002, X1 + .010):
        for sr, st in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            corners.append(b.add_v([x, rr * ur[1] + h * (sr * ur[1] + st * ut[1]), rr * ur[2] + h * (sr * ur[2] + st * ut[2])]))
    bot, top = corners[:4], corners[4:]
    b.band(bot, top); b.cap(bot); b.cap(top, reverse=True)
p09 = b.mesh('P09')
check(p09)
r19 = json.loads((J / 'evidence/polish-r19-r20/p09-r19-request.json').read_text())
p09ops = [p09] + [o for o in r19['operations'] if o['type'] != 'create_mesh']

# ---------------- P07 ----------------
r20 = json.loads((J / 'evidence/polish-r19-r20/p07-r20-request.json').read_text())
p07old = next(o for o in r20['operations'] if o['type'] == 'create_mesh')
b = Builder(); b.v = [list(p) for p in p07old['vertices']]; b.f = [list(f) for f in p07old['faces']]
EX = .08
TOP = .42 + .02 * (EX + .06) / .30  # mantlet top between x=-0.06 (z .42) and x=.24 (z .44)
R, T = .035, .008
YC = (-.64 + .58) / 2
eyes = []
for c in (YC - .39, YC + .39):
    zt, zb = TOP + .03, TOP - .012
    path = [(c - R, zb), (c - R, zt)] + [(c + R * math.cos(math.radians(a)), zt + R * math.sin(math.radians(a))) for a in (135, 90, 45)] + [(c + R, zt), (c + R, zb)]
    secs = []
    for i, (y, z) in enumerate(path):
        p0 = path[max(i - 1, 0)]; p1 = path[min(i + 1, len(path) - 1)]
        ty, tz = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(ty, tz); ny, nz = -tz / L, ty / L
        secs.append(b.ring([[EX - T, y - T * ny, z - T * nz], [EX + T, y - T * ny, z - T * nz],
                            [EX + T, y + T * ny, z + T * nz], [EX - T, y + T * ny, z + T * nz]]))
    for s0, s1 in zip(secs, secs[1:]): b.band(s0, s1)
    b.cap(secs[0]); b.cap(secs[-1], reverse=True)
    eyes.append({'centreY': c, 'x': EX, 'baseZ': zb, 'topZ': zt + R + T, 'outerWidth': 2 * (R + T), 'section': 2 * T})
p07 = b.mesh('P07')
check(p07)
p07ops = [p07] + [o for o in r20['operations'] if o['type'] != 'create_mesh']

ops = p06ops + p07ops + p09ops
req = {'jobId': JOB, 'expectedRevision': 20, 'idempotencyKey': 'centurion-r21-flangeA-eyes-20261111-v3',
       'removeObjects': ['P06', 'P07', 'P09'], 'operations': ops}
(O / 'r21-request.json').write_text(json.dumps(req) + '\n')
old09 = next(o for o in r19['operations'] if o['type'] == 'create_mesh')
info = {
    'requestSha256': hashlib.sha256((O / 'r21-request.json').read_bytes()).hexdigest(),
    'p06': {'sourceTriangles': tri(p06mesh), 'cutterTriangles': tri(cutter), 'bossTriangles': tri(bossm),
            'faceX_polstenLocal': X_FACE, 'cutterRadius': .197, 'bossRadius': .196, 'sourceFingerprintExpected': 'f6c847b929b4394a…'},
    'p09': {'trianglesBefore': tri(old09), 'trianglesAfter': tri(p09), 'ring': [RI, RO, X0, X1], 'bolts': 8},
    'p07': {'trianglesBefore': tri(p07old), 'trianglesAfter': tri(p07), 'eyes': eyes},
    'projectedTrianglesExcludingBooleanCut': 49680 - tri(old09) + tri(p09) - tri(p07old) + tri(p07) + tri(bossm),
    'triangleBudget': 50000}
(O / 'build-r21.json').write_text(json.dumps(info, indent=2) + '\n')
print(json.dumps(info, indent=2))
