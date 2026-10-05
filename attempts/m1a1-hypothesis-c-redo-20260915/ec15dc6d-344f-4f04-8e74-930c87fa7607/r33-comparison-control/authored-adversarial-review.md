# Abrams r33 — separate adversarial authored review

Reviewer: `/root/review_support`, 2026-10-02. Exact job `ec15dc6d-344f-4f04-8e74-930c87fa7607`, main r33, checkpoint `3ce4f7a3a4c8bdc16e34453775b531561dece6537abfaafdef3e75ae4f8c3e00`. Render-set hash `af4f5fbcae6972cd4af05c8fadf7f4c42925a27e90409c88e7d2a8bc98fdd99f`. No producer writes or lease operations performed.

## Whole-model observations before new author rationale

Inspected all six native r33 images first, before opening this candidate's recipe, export verification or construction explanation. The reviewer already knew the subject, prior r31 failure and intended correction from the task; this is not a blind recognition test. Existing r30 views and USMC reference crops had been inspected during the preceding separate review.

Both sides read as the same long, low tracked tank: the gun remains seated, the forward cheek wedge transitions to a flat aft roof, and the accepted rear underside/deck channel remains present. Front and rear retain the narrower upper roof and sloping outer shoulders. Top shows the roof inset inside the wider lower shell without a new asymmetric notch. Oblique shows the upper inset and a continuous lower aft shell contour; the fine protruding lower ledge identified on r31 is no longer apparent. There is no visible detached roof, broad new cavity, disconnected gun or adverse side-profile kink. These observations cover the complete tank, including its still-plain roof, rear, hull and running gear; they do not establish exact reference reconstruction.

## Reference and actual-geometry challenge

The parent `reference-map.json` remains a qualified construction interpretation of the USMC front/plan/side drawings. Front and plan support an upper boundary inset from the outer armor, but not one uniquely determined three-dimensional surface. Fittings, different projected stations and drawing uncertainty still prevent treating the selected taper as measured armor anatomy. The r33 inset maintains the supported direction relative to r30; restoring the lower contour does not visibly erase that improvement.

The strongest local objection was the r31 floor/bustle shelf. This reviewer independently loaded the actual baseline r30 and candidate r33 GLBs with `readAssembly`, which checks their receipt SHA-256 hashes, and reproduced all 97 longitudinal sections listed in `export-verification.json`. Maximum positive floor-minus-bustle half-width is `2.7971660321313152e-8` m; maximum difference between r33 and r30 bustle half-width is `6.079021042104671e-8` m. The prior 22.67–59.40 mm protrusions are therefore absent at the measured stations, to export precision. These are envelope checks, not claims about complete intersection-free volumes or continuous motion.

Independently evaluated every baseline floor vertex against the recipe protection plane. The maximum `floorZ - planeZ` is `-0.004999999999999893` m. Because signed distance to a plane is affine over each triangular face, the whole baseline floor surface lies below the protection plane with the stated 5 mm vertical guard. This closes the specific global-height error that let the rising aft interface move on r31; source/export seam and preservation verification still remain distinct obligations. The supplied export report states exact float32 candidate vertices, oriented face/material matches, 48 unchanged sibling meshes and 60 unchanged parent/transform entries. This lane independently reproduced the plane and section findings, not every claim in that report.

## Strongest unresolved core objections

| Category | Why whole-model production-ready qualification remains unsupported | r33 local disposition |
| --- | --- | --- |
| Identity-recognition | Plain front, rear and roof do not yet establish M1A1-specific recognition across all required 256 px views; no blind recognition evidence was produced in this lane. | Existing cannon, wedge-turret and seven-wheel cues remain. No observed loss of those cues. |
| Silhouette | The upper inset is reference-informed, but exact shoulder/roof/bustle relationships remain uncertain; a selected width ratio is not a complete reconstruction. | Supported upper taper remains, while the measured and visible r31 lower shelf objection is closed for the scoped correction. No new whole-view silhouette regression is established. |
| Mechanical-coherence | Simplified armor/support and running-gear anatomy remain incomplete. Rendered contact does not prove hidden gun clearance, complete seam integrity or continuous movement. | New protection follows the full rising floor envelope. Native views and measured sections no longer establish the failed floor/bustle relationship. Final isolation/seam/motion checks are separate. |
| Production-integrity | Missing authoritative dimensions, resolved immutable style binding, complete evidence and whole-model readiness cannot be supplied by deterministic output or a successful local correction. | Exact render/checkpoint and selected actual geometry bindings inspected. Final producer validation and other technical checks must remain explicit; no pass is invented here. |

All four broader objections remain unresolved. They are carried-forward qualification limitations, not new defects introduced by this specific human-directed correction. No favorable numeric scores are assigned, and no model-quality gate is approved by this report.

## Recommendation

**Recommend retaining r33 for the specifically directed local upper-taper/floor-interface correction, conditional on completing current validation, isolation, seam and motion checks for this exact checkpoint.** No visual or independently reproduced geometric regression in this review calls for restoration. This recommendation closes the concrete r31 shelf objection; it does not claim a completed or approved Abrams model.

Restore the baseline through the authorized workflow if the remaining checks establish an unintended changed deck/support/gun/pivot relationship, an open or shifted coupled seam, a new unintended intrusion, a materially protruding floor edge, or stale/mismatched render evidence. A later contradiction in matched reference contours requires reconciliation before another edit. Do not launch another candidate solely on this review, reset the prior autonomous allowance, or treat the specifically directed correction as candidate approval.

technicalValidation: actual GLB hashes, 97 sampled aft envelope sections and full-floor plane bound independently checked as above. `candidate-validation.json` was not present when this lane checked; final producer validation, native isolation and motion remain parent-owned and must be reported separately.

visualRecommendation: local retention recommendation with the explicit technical conditions above; **whole-model no-go**, with corrections and unresolved evidence required before the model-quality gate. No deterministic visual go is claimed.

humanApproval: absent for r33; human direction to perform the correction is not approval of its result.

## Evidence pins

Independently computed hashes:

| Record/view | SHA-256 |
| --- | --- |
| candidate-render.json | `45c83fc1e07193dbc86e3ef85e258774f7d159ceff826e47be040ad9eceb1148` |
| candidate-export.json | `dc6a1899c6710542d841e53003d3da3afd9c69234756a14e2d427ded76286ec8` |
| export-verification.json | `146db6778281f5028fd17913fd91be6819acba1889d4873b2244aece31f03978` |
| candidate-recipe.json | `cca6509fb51568b174be2dd6fcf8920a45b83804e0d75f5f837935f8933d5494` |
| physical-left | `4800565ecc8d088b2dcd137c1493e47e5744dcdddca6c8d47294d31434357d9a` |
| physical-right | `734d867d9e51f5462c96da09654d60f881598827a49f350d35d8ebeee2dfe274` |
| front | `34185bc1d796abbe2a11baa7418f2e1ce495a50f06f182029d7097e4b851d7da` |
| rear | `e5c9c8922272fbbc76eba6eb482347d7e2cb57489d6008f624d1f6e31a1b458a` |
| top | `af402f99977a00d0ef502dbe046caf6ccb8253949e723c360b250a2fa3edc850` |
| three-quarter | `9446f1564f5d2e9665f5a17138f5295d11d047c37c27d02efde301ade4f2ab0d` |
