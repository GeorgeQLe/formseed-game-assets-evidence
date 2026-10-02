# Independent authored review — r31

Candidate checkpoint `4d0f044e727470dd2d4fb497aed3b1754df4c3c742960c92b47a7466d7a40d63`, GLB SHA-256 `9b53176dc2936baeda671f3530a8d93fb06f88475d7a330f9eb6688d1410a21c`. Baseline r30 checkpoint `12157475f74cf3c4e6d313cc20e3214ea1add8cb6b3a36a2ca72016ab298ac7b`. All six native PNG hashes independently match `candidate-render.json`. No producer mutation performed by this reviewer.

## Observations before measurements

- Physical left: continuous hull/ramp and rising aft underside channel; low turret wedge and gun relationship remain recognizable.
- Physical right: coherent opposite side with the same primary relationships; no broad new opening visible.
- Front: clear inward-sloping shoulders beneath a narrower roof, improving the formerly rectangular turret envelope.
- Rear: inward-sloping sides, with a shallow lateral step visible near the right shell region.
- Top: inset roof perimeter inside the wider continuous outer shell; clear roof/shoulder separation.
- Three-quarter: upper mass reads less like a slab; fine doubled line/ledge appears at the lower aft near-side shell. No broad roof hole or detached cavity is visible, but this line needs geometric identification.

## Reference and baseline comparison

The front/plan upper taper supports the USMC reference interpretation and improves the selected target relative to r30. It does not establish exact historical dimensions or resolve the broader model. The accepted ramp/underside direction remains the preservation target. The side silhouette alone hides an interface change that is visible obliquely.

**Concrete new regression: the unchanged rising aft floor now protrudes outside the inset bustle.** Horizontal floor/bustle mating levels rise above the global Z=1.815 protection threshold toward the rear. The floor stays unchanged while its mating bustle surface moves inward. Independently intersecting the actual exported meshes with longitudinal planes gives:

| X station | Floor maximum half-width | r30 bustle maximum half-width | r31 bustle maximum half-width | New lateral protrusion per side |
| --- | --- | --- | --- | --- |
| −6.248 | 1.30013049 m | 1.30013049 m | 1.24073264 m | 59.40 mm |
| −6.1 | 1.31944866 m | 1.31944866 m | 1.27530120 m | 44.15 mm |
| −5.9 | 1.34555430 m | 1.34555427 m | 1.32288554 m | 22.67 mm |

At X=−6.248 the floor occupies approximately Z=1.91976–1.95982 and the bustle begins at Z=1.94476. Thus this is an overlapping but newly stepped mating interface, not a numerical open-gap assertion. It explains the doubled lower-aft contour in the native three-quarter view. The sparse references do not establish this new shelf as an intended construction feature. Protecting a single global height successfully preserved low surface cells but failed to preserve this higher aft underside interface.

## Actual-export checks

All four changed components have exactly the recipe's float32 vertex sets and triangle counts: 1216, 1250, 2248 and 138. No missing or extra candidate vertices were found. All other exported meshes have identical vertex, face and material arrays to r30. This confirms the defect is in the construction target/mapping rather than an unexpected authoring transform. Parent-owned technical validation, isolation and motion checks remain separate.

## Recommendation

**Restore r30 rather than retain r31 as the successful bounded correction.** The upper target improved, but the newly exposed aft shelf contradicts preserving the accepted underside interface. Preserve this attempt and its evidence. Any future correction must protect the actual rising floor/bustle mating contour, not merely all geometry below one height. This review does not authorize another candidate or reset the iteration allowance.

technicalValidation: reference/image/export identity and selected preservation verified; authoring matches recipe; parent-owned full validation/motion results separate.

visualRecommendation: restore baseline for this bounded retention decision; no-go for the candidate and broader model approval.

humanApproval: no candidate approval inferred from direction or CC0 authorization.
