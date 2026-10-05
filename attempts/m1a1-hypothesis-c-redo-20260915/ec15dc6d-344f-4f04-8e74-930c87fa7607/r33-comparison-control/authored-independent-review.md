# Independent authored retention review — r33

Candidate checkpoint `3ce4f7a3a4c8bdc16e34453775b531561dece6537abfaafdef3e75ae4f8c3e00`, GLB SHA-256 `ad4ebea100dcf693e66866efe421f9c302ab8fce93cf0aafda78a8bbede5a7cf`. Baseline is restored r32, identical to r30 checkpoint `12157475f74cf3c4e6d313cc20e3214ea1add8cb6b3a36a2ca72016ab298ac7b`. Read-only reviewer; no producer mutation. All six native render hashes independently verified against `candidate-render.json`.

## Whole-form observations before measurements

- Physical left: continuous long hull and turret wedge; long ramp and rising aft underside channel remain coherent.
- Physical right: opposite side remains coherent, with preserved gun/roof relationship and no new broad underside opening.
- Front: clear sloping lateral shoulders beneath a narrower roof; central mantlet remains connected.
- Rear: narrower upper outline transitions into the lower mass without a detached shell.
- Top: continuous inset roof boundary within wider outer armor; no broad roof hole or disconnected shoulder visible.
- Three-quarter: upper mass retains the stronger shoulder/roof relationship. The doubled lower-aft shelf line identified in r31 is absent; the lower aft flank now reads as a continuous connection.

## Reference and baseline challenge

Against the retained USMC front/plan references and the earlier independent reference-map observations, the inset upper boundary is a supported improvement over r30's rectangular/slab-like envelope. Basket equipment remains separate from the inferred armor mass. Neither the side trace nor this correction claims exact hidden anatomy or a factory dimensional reconstruction.

The accepted ramp/underside interpretation remains intact in both side views. The observed r31 aft shelf failure has been specifically challenged rather than dismissed as shading: the visible repair agrees with independently measured actual geometry below. No new roof overhang, exposed slit, doubled shoulder or detached cavity is established in these six views. Flat lighting and the small subject footprint limit fine seam visibility; this is a bounded primary-form retention finding, not complete production qualification.

## Actual exported geometry

All four authored components match the reviewed recipe's float32 vertex sets and triangle counts: left cheek 632 vertices/1260 triangles, right cheek 649/1294, bustle 1316/2628, roof 71/138. Every recipe vertex is present, with equal unique-vertex counts. All 48 other exported meshes retain identical vertices, faces and material arrays relative to r30.

Independently recomputed actual floor/bustle sections at the previously failing stations:

| X | Floor half-width | Bustle maximum half-width | Floor minus bustle |
| --- | --- | --- | --- |
| −6.248 | 1.30013048999 m | 1.30013048999 m | 0 |
| −6.1 | 1.31944866038 m | 1.31944868478 m | −2.4401e−8 m |
| −5.9 | 1.34555429682 m | 1.34555427437 m | 2.2451e−8 m |

The prior 22.7–59.4 mm unsupported lateral shelf is closed to float precision in the authored export. The prior recipe review's complete supporting-plane/protected-cell reasoning applies because the exported vertex sets and counts match; the station checks independently verify the known failure sites. Parent-owned full motion, native isolation and technical validation remain separate results.

## Scoped recommendation

**Retain r33 as the successful targeted construction correction, conditional on the production owner's remaining technical/motion/isolation checks passing.** No visual reason to restore r30 remains in this bounded review. Preserve r31's rejected attempt and the r32 restoration history. This recommendation does not authorize further candidates, reset allowance, or approve the overall model.

technicalValidation: image/GLB identity, reviewed recipe realization, unchanged siblings and known aft-interface failure sites independently verified; parent-owned full technical/motion/isolation checks separate.

visualRecommendation: retain for the bounded upper-taper/rising-interface correction if remaining technical checks pass; overall production/model visual go remains no-go pending its complete required assessment.

humanApproval: targeted correction requested; resulting model approval absent.
