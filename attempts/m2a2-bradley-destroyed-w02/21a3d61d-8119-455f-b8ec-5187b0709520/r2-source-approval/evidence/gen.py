"""Deterministic generator for Bradley condition-recipe part alternatives
(D02, D03, W02, W03). Reads the approved r5 clean kit parts, applies declared
damage (dents, tears, sag, reposes, burned materials) in Blender space
(x forward, y left, z up) and writes typed FormSeed3D replacement payloads for
apply_derivative_replacement. All damage layouts are design choices informed by
the condition references in the job brief; none is a historical claim.
Usage: python3 gen.py <out-dir>"""
import json, math, os, sys
import glbmesh

KIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../bradley-interchangeable-r1/kit')
HULL_SIDE = 1.306  # armor inner face; dents never push into the hull side


def separate_touching(v, f):
    """Position welding joins separate source solids that merely touch along an
    edge (edges with four or more faces). At each such edge, sort its faces by
    angle around the edge and pair each face with its neighbour on the solid's
    interior side (from the outward normal), then give each resulting solid its
    own copy of the seam vertices so the welded part stays manifold."""
    def sub(a, b): return [a[i] - b[i] for i in range(3)]
    def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
    def dot(a, b): return sum(a[i] * b[i] for i in range(3))
    edges = {}
    for idx, face in enumerate(f):
        for k in range(3): edges.setdefault(frozenset((face[k], face[(k + 1) % 3])), []).append(idx)
    bad = {e: fs for e, fs in edges.items() if len(fs) > 2}
    if not bad: return v, f
    parent = list(range(len(f)))
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b): parent[find(a)] = find(b)
    for e, fs in edges.items():
        if e not in bad:
            for o in fs[1:]: union(o, fs[0])
    for e, fs in bad.items():
        i, j = sorted(e); axis = sub(v[j], v[i]); n0 = math.sqrt(dot(axis, axis)) or 1; axis = [x / n0 for x in axis]
        ref = None; items = []
        for idx in fs:
            face = f[idx]; other = next(x for x in face if x not in e)
            d = sub(v[other], v[i]); d = sub(d, [axis[k] * dot(d, axis) for k in range(3)])
            if ref is None: ref = d; ref2 = cross(axis, ref)
            theta = math.atan2(dot(d, ref2), dot(d, ref))
            normal = cross(sub(v[face[1]], v[face[0]]), sub(v[face[2]], v[face[0]]))
            items.append((theta, idx, dot(normal, cross(axis, d))))
        items.sort(); n = len(items)
        for k, (_, idx, toward) in enumerate(items):
            partner = items[(k - 1) % n][1] if toward > 0 else items[(k + 1) % n][1]
            union(idx, partner)
    seam = {i for e in bad for i in e}
    copies, out = {}, []
    for idx, face in enumerate(f):
        comp = find(idx); nf = []
        for i in face:
            if i in seam:
                key = (i, comp)
                if key not in copies: copies[key] = len(v); v.append(list(v[i]))
                nf.append(copies[key])
            else: nf.append(i)
        out.append(nf)
    return v, out


def part(name):
    files = {f.split('-', 1)[1][:-4]: f for f in os.listdir(KIT) if f.startswith('P') and f.endswith('.glb')}
    v, f, m = glbmesh.load(os.path.join(KIT, files[name]))
    v, f = separate_touching([list(p) for p in v], f)
    return v, f, m


def noise(*k):
    """Deterministic hash noise in [-1, 1]."""
    s = math.sin(sum(x * c for x, c in zip(k, (12.9898, 78.233, 37.719, 4.581))) ) * 43758.5453
    return (s - math.floor(s)) * 2 - 1


def subdivide(v, f, m, regions, levels):
    """Midpoint-split triangles whose centroid lies within any (center, radius)
    region, then split their neighbours to match (conforming 2/3/4-way splits),
    so the surface stays closed with no T-junctions."""
    for _ in range(levels):
        mid = {}
        def midpoint(a, b):
            k = (min(a, b), max(a, b))
            if k not in mid: mid[k] = len(v); v.append([(v[a][i] + v[b][i]) / 2 for i in range(3)])
            return mid[k]
        chosen = []
        for face in f:
            c = [sum(v[i][d] for i in face) / 3 for d in range(3)]
            chosen.append(any(math.dist(c, rc) < rr for rc, rr in regions))
        for face, pick in zip(f, chosen):
            if pick: [midpoint(face[k], face[(k + 1) % 3]) for k in range(3)]
        nf, nm = [], []
        for face, mat, pick in zip(f, m, chosen):
            a, b, c = face
            ab, bc, ca = (mid.get((min(x, y), max(x, y))) for x, y in ((a, b), (b, c), (c, a)))
            split = [x is not None for x in (ab, bc, ca)]
            if all(split): tris = [[a, ab, ca], [ab, b, bc], [ca, bc, c], [ab, bc, ca]]
            elif sum(split) == 0: tris = [face]
            elif sum(split) == 1:
                if ab is not None: tris = [[a, ab, c], [ab, b, c]]
                elif bc is not None: tris = [[a, b, bc], [a, bc, c]]
                else: tris = [[a, b, ca], [ca, b, c]]
            else:
                if ab is None: tris = [[a, b, bc], [a, bc, ca], [ca, bc, c]]
                elif bc is None: tris = [[a, ab, ca], [ab, b, c], [ab, c, ca]]
                else: tris = [[a, ab, c], [ab, b, bc], [ab, bc, c]]
            nf += tris; nm += [mat] * len(tris)
        f, m = nf, nm
    return v, f, m


def crater(v, center, rx, rz, floor_y, axis=(0, 2)):
    """Closed-surface penetration: push the outer skin inside a jagged ellipse
    back toward floor_y (the hull side) so it reads as a dark hole without
    opening the mesh."""
    for p in v:
        dx, dz = (p[axis[0]] - center[axis[0]]) / rx, (p[axis[1]] - center[axis[1]]) / rz
        ang = math.atan2(dz, dx); jag = 1 + 0.28 * noise(round(ang * 3), 7) + 0.12 * noise(round(ang * 9), 3)
        d = math.hypot(dx, dz) / jag
        if d < 1 and p[1] > floor_y: p[1] = floor_y + (p[1] - floor_y) * min(1, d ** 3)


def notch(v, x0, x1, z_top, depth):
    """Closed-surface bitten edge: lift the lower edge inside [x0, x1] to a
    ragged line so the skirt bottom reads as torn away."""
    for p in v:
        if x0 < p[0] < x1:
            t = (p[0] - x0) / (x1 - x0); line = z_top - depth * math.sin(math.pi * t) * (0.8 + 0.2 * noise(round(p[0] * 12), 9))
            if p[2] < line: p[2] = line - (line - p[2]) * 0.2


def dent(v, center, radius, depth, direction, clamp=None):
    n = math.sqrt(sum(d * d for d in direction)); direction = [d / n for d in direction]
    for p in v:
        d = math.dist(p, center)
        if d < radius:
            w = (1 - (d / radius) ** 2) ** 2
            for i in range(3): p[i] += direction[i] * depth * w
            if clamp: clamp(p)


def tear(v, f, m, center, rx, rz, axis=(0, 2)):
    """Remove faces whose centroid falls in a jagged ellipse (the hole)."""
    keep_f, keep_m = [], []
    for face, mat in zip(f, m):
        c = [sum(v[i][d] for i in face) / 3 for d in range(3)]
        dx, dz = (c[axis[0]] - center[axis[0]]) / rx, (c[axis[1]] - center[axis[1]]) / rz
        ang = math.atan2(dz, dx); jag = 1 + 0.28 * noise(round(ang * 3), 7) + 0.12 * noise(round(ang * 9), 3)
        if dx * dx + dz * dz < jag * jag: continue
        keep_f.append(face); keep_m.append(mat)
    return keep_f, keep_m


def rotate(v, pivot, axis, degrees):
    a = math.radians(degrees); c, s = math.cos(a), math.sin(a)
    i, j = {'x': (1, 2), 'y': (2, 0), 'z': (0, 1)}[axis]
    for p in v:
        di, dj = p[i] - pivot[i], p[j] - pivot[j]
        p[i], p[j] = pivot[i] + di * c - dj * s, pivot[j] + di * s + dj * c


def compact(v, f, m):
    """Drop unused vertices, merge coplanar triangle pairs into quads, round to mm."""
    used = sorted({i for face in f for i in face}); remap = {o: n for n, o in enumerate(used)}
    v = [[round(v[o][d], 3) for d in range(3)] for o in used]; f = [[remap[i] for i in face] for face in f]
    def normal(face):
        a, b, c = (v[i] for i in face[:3]); u = [b[k] - a[k] for k in range(3)]; w = [c[k] - a[k] for k in range(3)]
        n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]; l = math.sqrt(sum(x * x for x in n)) or 1
        return [x / l for x in n]
    edges = {}
    for idx, face in enumerate(f):
        for k in range(3): edges.setdefault(frozenset((face[k], face[(k + 1) % 3])), []).append(idx)
    used_f, out_f, out_m = set(), [], []
    for idx, face in enumerate(f):
        if idx in used_f: continue
        merged = False
        for k in range(3):
            a, b = face[k], face[(k + 1) % 3]
            for o in edges[frozenset((a, b))]:
                if o == idx or o in used_f or m[o] != m[idx]: continue
                if sum(x * y for x, y in zip(normal(face), normal(f[o]))) < 0.9995: continue
                other = [x for x in f[o] if x not in (a, b)]
                if len(other) != 1: continue
                c = face[(k + 2) % 3]; quad = [a, other[0], b, c]
                out_f.append(quad); out_m.append(m[idx]); used_f |= {idx, o}; merged = True; break
            if merged: break
        if not merged: out_f.append(face); out_m.append(m[idx]); used_f.add(idx)
    return v, out_f, out_m


def cluster(v, f, m, cell):
    """Weld vertices on a uniform grid (vertex clustering) and drop collapsed faces."""
    key, out, remap = {}, [], []
    for p in v:
        k = tuple(round(c / cell) for c in p)
        if k not in key: key[k] = len(out); out.append([round(c / cell) * cell for c in k] and list(p))
        remap.append(key[k])
    nf, nm = [], []
    for face, mat in zip(f, m):
        g = [remap[i] for i in face]
        if len(set(g)) == 3: nf.append(g); nm.append(mat)
    return out, nf, nm


def mesh_ops(name, v, f, m, material_map=None, parent=None, whole=None, cell=None):
    if cell: v, f, m = cluster(v, f, m, cell)
    v, f, m = compact(v, f, m)
    ops = [{'type': 'create_mesh', 'name': name, 'vertices': v, 'faces': f},
           {'type': 'recalculate_normals', 'object': name, 'direction': 'OUTSIDE'}]
    if whole: ops.append({'type': 'assign_material_slot', 'object': name, 'materialName': whole})
    else:
        mats = [(material_map or {}).get(x, x) for x in m]
        first = mats[0]; ops.append({'type': 'assign_material_slot', 'object': name, 'materialName': first})
        for mat in sorted(set(mats) - {first}):
            ops.append({'type': 'assign_material_slot', 'object': name, 'materialName': mat, 'faceIndices': [i for i, x in enumerate(mats) if x == mat]})
    if parent: ops.append({'type': 'set_parent', 'object': name, 'parent': parent, 'keepTransform': True})
    return ops, len(v), len(f)


def dup_ops(source, name, material=None, pivot=None, location=None, rotation=None, scale=None, parent=None, unparent=False, cell=None):
    """Rigid or paint-only alternative of a retained source mesh. The service removes
    replaced sources before running operations, so the repose (world = location +
    R·S·(p − pivot), Blender XYZ Euler) is baked into the kit vertices here and the
    part is created inline like every other replacement."""
    v, f, m = part(source)
    if pivot is not None:
        sx, sy, sz = scale or (1, 1, 1)
        for p in v:
            p[0], p[1], p[2] = (p[0] - pivot[0]) * sx, (p[1] - pivot[1]) * sy, (p[2] - pivot[2]) * sz
        for axis, deg in zip('xyz', rotation or (0, 0, 0)):
            if deg: rotate(v, (0, 0, 0), axis, deg)
        loc = location or pivot
        for p in v:
            for i in range(3): p[i] += loc[i]
    return mesh_ops(name, v, f, m, whole=material, parent=parent, cell=cell)


def scorch(v, f, m, spots, material='dark', max_area=0.02, axis=(0, 2)):
    """Reassign faces near impacts to an existing dark material (soot and
    scorch around penetrations and dents); jagged by deterministic noise."""
    out = list(m)
    def area(face):
        a, b, c = (v[i] for i in face[:3]); u = [b[k] - a[k] for k in range(3)]; w = [c[k] - a[k] for k in range(3)]
        return math.sqrt(sum(x * x for x in (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]))) / 2
    for idx, face in enumerate(f):
        if area(face) > max_area: continue  # large flat faces never take a scorch patch
        c = [sum(v[i][d] for i in face) / len(face) for d in range(3)]
        for (cx, cz, rx, rz) in spots:
            dx, dz = (c[axis[0]] - cx) / rx, (c[axis[1]] - cz) / rz
            ang = math.atan2(dz, dx)
            edge = 1 + 0.22 * noise(round(ang * 2.5), round(cx * 10), 11) + 0.1 * noise(round(ang * 7), 5)
            if dx * dx + dz * dz < edge * edge: out[idx] = material; break
    return out


def scorch3(v, f, m, spots, material='dark', max_area=0.02):
    """Scorch faces whose centroid lies inside a jagged sphere around each impact."""
    out = list(m)
    for idx, face in enumerate(f):
        a, b, c = (v[i] for i in face[:3])
        u = [b[k] - a[k] for k in range(3)]; w = [c[k] - a[k] for k in range(3)]
        if math.sqrt(sum(x * x for x in (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]))) / 2 > max_area: continue
        cen = [sum(v[i][d] for i in face) / len(face) for d in range(3)]
        for center, r in spots:
            d = [cen[k] - center[k] for k in range(3)]
            ang = math.atan2(d[2], d[0] + d[1])
            if math.dist(cen, center) < r * (1 + 0.22 * noise(round(ang * 2.5), round(center[0] * 10), 13)): out[idx] = material; break
    return out


def armor_clamp(p):
    if p[1] < HULL_SIDE: p[1] = HULL_SIDE


def recipes():
    out = {}
    # D02 — left-flank hits: DP04A torn, dented skirt with a bitten lower edge; left headlight lost.
    v, f, m = part('LeftArmor')
    v, f, m = subdivide(v, f, m, [((1.55, 1.5, 1.05), 0.52), ((-0.5, 1.5, 0.8), 0.6)], 2)
    v, f, m = subdivide(v, f, m, [((0.55, 1.5, 1.3), 0.45), ((-1.7, 1.5, 1.5), 0.35)], 1)
    dent(v, (0.55, 1.7, 1.3), 0.42, 0.075, (0, -1, 0), armor_clamp)
    dent(v, (-1.7, 1.7, 1.5), 0.28, 0.045, (0, -1, 0), armor_clamp)
    for p in v:  # tear rim petals pushed inward by the penetration; front lower lip bent outward
        d = math.hypot((p[0] - 1.55) / 0.38, (p[2] - 1.05) / 0.26)
        if 0.9 < d < 1.8: p[1] -= 0.05 * (1.8 - d) / 0.9; armor_clamp(p)
        if p[0] > 2.3 and p[2] < 0.9: p[1] += 0.10 * min(1, (p[0] - 2.3) / 0.76) * min(1, (0.9 - p[2]) / 0.25)
    crater(v, (1.55, 0, 1.05), 0.38, 0.26, HULL_SIDE + 0.004)  # penetration driven back to the hull side
    notch(v, -0.95, -0.05, 0.65, -0.32)  # lower edge bitten away, exposing the road wheels
    m = scorch(v, f, m, [(1.55, 1.05, 0.5, 0.35), (-0.5, 0.68, 0.5, 0.3)])
    ops, nv, nf = mesh_ops('LeftArmorDamaged', v, f, m)
    out['D02'] = {'removeObjects': ['LeftArmor', 'LeftHeadlight'], 'operations': ops,
                  'parts': {'LeftArmor': {'partId': 'DP04A', 'sourceObject': 'LeftArmorDamaged', 'vertices': nv, 'faces': nf}, 'LeftHeadlight': None}}

    # D03 — frontal hits: DP01A glacis dents, DP14A crumpled grille, DP09A dented turret top.
    v, f, m = part('Hull')
    regions = [((2.95, 0.6, 1.35), 0.75), ((3.05, -0.75, 1.0), 0.5)]
    v, f, m = subdivide(v, f, m, regions, 2)
    dent(v, (2.95, 0.6, 1.35), 0.5, 0.07, (-0.6, 0, -0.8))
    dent(v, (3.05, -0.75, 1.0), 0.32, 0.04, (-1, 0, -0.2))
    m = scorch3(v, f, m, [((2.95, 0.6, 1.3), 0.3), ((3.1, -0.75, 1.0), 0.2)])
    hull_ops, hv, hf = mesh_ops('HullDamaged', v, f, m)
    v, f, m = part('FrontGrille')
    v, f, m = subdivide(v, f, m, [((1.6, -0.5, 1.75), 0.5)], 1)
    dent(v, (1.6, -0.5, 1.8), 0.35, 0.06, (0, 0, -1))
    for p in v:
        if math.dist(p, (1.6, -0.5, 1.75)) < 0.45: p[2] += 0.012 * noise(round(p[0] * 40), round(p[1] * 40), 2)
    dent(v, (1.95, -1.1, 1.6), 0.25, 0.05, (0.3, 0, 1))
    m = scorch3(v, f, m, [((1.6, -0.5, 1.75), 0.26)])
    grille_ops, gv, gf = mesh_ops('FrontGrilleDamaged', v, f, m)
    v, f, m = part('TurretTop')
    v, f, m = subdivide(v, f, m, [((-0.5, 0.1, 3.0), 0.4)], 1)
    dent(v, (-0.5, 0.1, 3.03), 0.3, 0.055, (0, 0, -1))
    for c in ((-0.9, -0.5, 2.95), (-0.25, 0.45, 2.98), (-0.7, 0.35, 3.0)): dent(v, c, 0.09, 0.02, (0, 0, -1))
    m = scorch3(v, f, m, [((-0.5, 0.1, 3.0), 0.22)])
    top_ops, tv, tf = mesh_ops('TurretTopDamaged', v, f, m, parent='TurretYaw')
    out['D03'] = {'removeObjects': ['Hull', 'FrontGrille', 'TurretTop'], 'operations': hull_ops + grille_ops + top_ops,
                  'parts': {'Hull': {'partId': 'DP01A', 'sourceObject': 'HullDamaged', 'vertices': hv, 'faces': hf},
                            'FrontGrille': {'partId': 'DP14A', 'sourceObject': 'FrontGrilleDamaged', 'vertices': gv, 'faces': gf},
                            'TurretTop': {'partId': 'DP09A', 'sourceObject': 'TurretTopDamaged', 'vertices': tv, 'faces': tf}}}

    # W02 — burned out, left track thrown, rear ramp dropped, left skirt hanging.
    v, f, m = part('Hull')
    v, f, m = subdivide(v, f, m, [((-2.6, 0, 1.85), 1.2), ((0.5, 1.31, 1.2), 0.9)], 2)
    dent(v, (-2.6, 0, 1.9), 0.9, 0.06, (0, 0, -1))
    dent(v, (0.5, 1.2, 1.2), 0.6, 0.035, (0, 1, 0))
    w_hull, whv, whf = mesh_ops('HullBurned', v, f, m, whole='dark')
    v, f, m = part('RearRamp')
    rotate(v, (-3.25, 0, 0.5), 'y', -118)  # top swings rearward (-x) and down to rest near the ground
    w_ramp, wrv, wrf = mesh_ops('RearRampBurned', v, f, m, whole='dark')
    # thrown: loop collapses flat on the ground and slides outward off the wheels
    w_track, wtv, wtf = dup_ops('LeftTrack', 'LeftTrackBurned', pivot=[0, 1.22, 0], location=[0.15, 1.77, 0.02], rotation=[0, 0, 4], scale=[1.03, 1, 0.12])
    # hanging outward from its top fixings
    w_armor, wav, waf = dup_ops('LeftArmor', 'LeftArmorBurned', material='wheel', pivot=[0, 1.48, 1.86], location=[0, 1.48, 1.82], rotation=[18, 0, 0])
    w_turret, wuv, wuf = dup_ops('Turret', 'TurretBurned', material='dark', parent='TurretYaw')
    burned = {}
    for src, name, mat, parent in [('RightArmor', 'RightArmorBurned', 'dark', None), ('TurretTop', 'TurretTopBurned', 'dark', 'TurretYaw'),
                                   ('FrontGrille', 'FrontGrilleBurned', 'wheel', None), ('DriverHatch', 'DriverHatchBurned', 'wheel', None),
                                   ('GunMantlet', 'GunMantletBurned', 'wheel', 'GunPitch')]:
        burned[src] = (name,) + dup_ops(src, name, material=mat, parent=parent)
    out['W02'] = {'removeObjects': ['Hull', 'RearRamp', 'LeftTrack', 'LeftArmor', 'Turret', 'LeftHeadlight'] + list(burned),
                  'operations': w_hull + w_ramp + w_track + w_armor + w_turret + [o for b in burned.values() for o in b[1]],
                  'parts': {'Hull': {'partId': 'WP01B', 'sourceObject': 'HullBurned', 'vertices': whv, 'faces': whf},
                            'RearRamp': {'partId': 'WP10A', 'sourceObject': 'RearRampBurned', 'vertices': wrv, 'faces': wrf},
                            'LeftTrack': {'partId': 'WP02A', 'sourceObject': 'LeftTrackBurned', 'vertices': wtv, 'faces': wtf},
                            'LeftArmor': {'partId': 'WP04B', 'sourceObject': 'LeftArmorBurned', 'vertices': wav, 'faces': waf},
                            'Turret': {'partId': 'WP06B', 'sourceObject': 'TurretBurned', 'vertices': wuv, 'faces': wuf},
                            **{src: {'partId': pid, 'sourceObject': b[0], 'vertices': b[2], 'faces': b[3]} for (src, b), pid in zip(burned.items(), ['WP05B', 'WP09C', 'WP14B', 'WP13B', 'WP33B'])},
                            'LeftHeadlight': None}}

    # W03 — catastrophic: collapsed TOW launcher, blown turret roof, crushed hull front, scorched turret.
    # WP08A (collapsed TOW launcher) is deferred: the source launcher's touching seams cannot be rebuilt
    # manifold from the kit GLB, so W03 keeps the clean launcher and loses only its protective cover.
    v, f, m = part('TurretTop')
    v, f, m = subdivide(v, f, m, [((-0.6, -0.1, 2.95), 0.5)], 1)
    dent(v, (-0.6, -0.1, 2.9), 0.5, 0.11, (0, 0, 1))  # roof bulged upward by internal blast
    m = scorch(v, f, m, [(-0.55, 0, 0.3, 0.24)], material='wheel', axis=(0, 1))  # blast-torn roof plate, heat-darkened
    top3, t9v, t9f = mesh_ops('TurretTopBurned', v, f, m, whole='dark', parent='TurretYaw')
    v, f, m = part('Hull')
    v, f, m = subdivide(v, f, m, [((3.1, 0.9, 1.1), 0.8)], 2)
    dent(v, (3.2, 0.95, 1.15), 0.65, 0.12, (-0.7, -0.2, -0.6))
    hull3, h3v, h3f = mesh_ops('HullBurned', v, f, m, whole='dark')
    turret3, u3v, u3f = dup_ops('Turret', 'TurretBurned', material='wheel', parent='TurretYaw')
    burned3 = {}
    for src, name, mat, parent in [('LeftArmor', 'LeftArmorBurned', 'dark', None), ('RightArmor', 'RightArmorBurned', 'wheel', None),
                                   ('FrontGrille', 'FrontGrilleBurned', 'dark', None), ('DriverHatch', 'DriverHatchBurned', 'dark', None),
                                   ('GunMantlet', 'GunMantletBurned', 'dark', 'GunPitch')]:
        burned3[src] = (name,) + dup_ops(src, name, material=mat, parent=parent)
    out['W03'] = {'removeObjects': ['TurretTop', 'Hull', 'Turret', 'TowProtectiveCover'] + list(burned3),
                  'operations': top3 + hull3 + turret3 + [o for b in burned3.values() for o in b[1]],
                  'parts': {'TurretTop': {'partId': 'WP09B', 'sourceObject': 'TurretTopBurned', 'vertices': t9v, 'faces': t9f},
                            'Hull': {'partId': 'WP01C', 'sourceObject': 'HullBurned', 'vertices': h3v, 'faces': h3f},
                            'Turret': {'partId': 'WP06C', 'sourceObject': 'TurretBurned', 'vertices': u3v, 'faces': u3f},
                            **{src: {'partId': pid, 'sourceObject': b[0], 'vertices': b[2], 'faces': b[3]} for (src, b), pid in zip(burned3.items(), ['WP04C', 'WP05C', 'WP14C', 'WP13C', 'WP33C'])},
                            'TowProtectiveCover': None}}
    return out


if __name__ == '__main__':
    out_dir = sys.argv[1]; os.makedirs(out_dir, exist_ok=True)
    for rid, r in recipes().items():
        payload = {'removeObjects': r['removeObjects'], 'operations': r['operations']}
        json.dump(payload, open(os.path.join(out_dir, f'payload-{rid}.json'), 'w'), separators=(',', ':'))
        json.dump(r['parts'], open(os.path.join(out_dir, f'parts-{rid}.json'), 'w'), indent=1)
        size = os.path.getsize(os.path.join(out_dir, f'payload-{rid}.json'))
        print(rid, size, 'bytes', {k: (x and (x['partId'], x['vertices'], x['faces'])) for k, x in r['parts'].items()})
