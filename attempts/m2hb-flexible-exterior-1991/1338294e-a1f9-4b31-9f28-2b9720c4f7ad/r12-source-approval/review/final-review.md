I recommend **go** for r12 and passing it to you for review, with no unresolved core objections. The rear leaf now sits on its base with no gap and nothing overhangs. The other 11 meshes are byte-identical to r11, and every hash I recomputed matches. Two things need your attention: the dimension-record route did not follow your decision as written, and a few small mechanical simplifications remain. I changed no files. The only things I created are game-scale downsamples in `/tmp/r12rev/`.

## Hashes recomputed with `shasum -a 256`

| Item | Recomputed | Result |
|---|---|---|
| `operations.json` | b10e8ab1…bb19 | matches `plan.json` and `evidence-sha256.txt` |
| Checkpoint `65347ef5….blend` | 6086aee3…15ca | matches `status-r12.json` |
| Review GLB `940604b9…/review.glb` | 3b54bb91…c4c9 | matches `review-glb-receipt.json` |

**bc06d303 compared with b10e8ab1: consistent by design, not a defect.**
- FormSeed computes the status hash in `coordinator-runtime/src/mutation-receipt.ts:18`. It hashes `stable({operations, productionOperation, productionInput})`, so it covers more than the file's bytes.
- I could not reproduce bc06d303 because the coordinator-resolved `productionInput` is not kept in `finishing-r12/`.
- I closed the gap through the geometry instead. The GLB's P11 has 280 unique vertices, and each one matches `operations.json` within 6.8e-9 m (float32 precision), with 532 triangles. The committed batch is therefore this file.
- Gap: keep the mutation's `productionInput`, or a construction receipt, so the hash can be reproduced directly.

## 1. Did r12 do exactly and only what the plan authorized?

Yes.
- **P11 only.**
  - The 5 operations match r11 except for the vertices of operation 0. Faces, normals, material, parent and smoothing are identical.
  - 224 vertices changed: indices 16–31, 48–71 and 96–279, exactly the sets in `prepare.py`. The base, cheeks and windage knob are byte-exact.
- **17 retained fingerprints.**
  - The 11 other meshes are byte-identical between the r11 and r12 review GLBs.
  - Their `geometryHashes` in `mask-receipt.json` also equal r10's `native-masks.json`, and P11 is the only difference.
  - The other 6 objects (camera and empties) have no r12 evidence, because there is no `construction-receipt.json` this time. They rest on the tool's word.
- **Totals.** 7492 triangles, 2 materials and 18 objects (`status-r12.json` validation). The GLB has 13 nodes = 12 meshes + root.
- **P11 bounds** (from `mask-receipt.json`): x 0.052–0.133 and z 0.073–0.100, as planned. Parts:

| Part | x | z | Note |
|---|---|---|---|
| Leaf frame | 0.0755–0.127 | 0.082–0.088 | seated on base top 0.082 |
| Knob | 0.123–0.133 | 0.082–0.088 | flush with the base end, so no overhang |
| Shaft end | ≤0.123 | | |
| Pin | | 0.0815–0.0885 | centred 0.085; right end y 0.0135 |

- **Plan hygiene.** The `heightBlocker` field in `plan.json` still says the height cannot be retargeted on this job, but it was. The plan is stale on that point.

## 2. Dimensions and technical state

**All bound to the same checkpoint.** These all carry checkpoint 2906b4d4 with hash 6086aee3…, revision 12:
- dimension report: spec 71e209e9…; 12 of 12 blocking checks pass; height observed 0.19400 against target 0.194; report hash fa5b4ce6…
- render baseline: first and second hashes both 028e5814…, deterministic
- `validate_asset`: passed, 0 issues
- closeups, masks and the GLB all share scene fingerprint 06c90a5a…

The closeup receipt's spec hash 885c937d… looked unrelated at first. I recomputed it: it is the canonical-JSON hash of the whole `dimension-binding-v4-supersede.json` wrapper, so it is consistent. The closeups are diagnostic only (`qualifiesProductionGate:false`).

**The supersession's content is legitimate.**
- I diffed v3 (19e8efdc) against v4-supersede (71e209e9) after recomputing both canonical hashes.
- Only these changed: the height (0.232 → 0.194), its basis text, the configuration condition, `expectedBounds.max.y` (0.145 → 0.107), one added fact line, the decision entry, the revision/ID and the supersession block.
- This matches `changedCriterionIds`. Tolerances (1% envelope, 1 mm datum), length, width and datums are unchanged, so nothing was loosened.
- Decision input 49174841 is the report hash inside `finishing-r11/dimension-validation.json`.

**Three problems with the route:**
1. **Route differs from your decision.** The decision says "go ahead with a finishing **successor** bound to a folded-leaf dimension-ready record." It was carried out as an in-place supersession on the same job, not as a successor job. `finishing-successor-v4/dimension-binding-v4.json`, with asset ID `-folded`, was prepared and then not used. The effect is equivalent, but you should confirm this route.
2. **The target was set to the measurement.** 0.194 m is the model's own measured value, so the height check now confirms consistency, not correctness. The basis text says so honestly ("interpreted").
3. **Record inconsistencies:**
   - `boundAt` is 03:20Z, after the r12 commit at 03:15Z, yet it is labelled `bindingRevision 11`. The supersession itself was recorded at 03:13Z, before the commit.
   - `authority.productionAuthorized:false` sits beside a decision that grants production authorization.

## 3. Visual critique

- **Folded leaf seat:** fixed.
  - In `r12-closeup-rear-sight-side.png`, the run from the knob end across the leaf (to z 0.088) and down to the base is solid, with no background showing under the leaf and nothing past x 0.133.
  - Under flat Workbench shading (no shadows or cavity), though, the leaf has the same tone as the base. In `r12-closeup-rear-sight-top.png` and `r12-native-top.png` the folded leaf almost disappears, leaving only thin edge lines. The quarter closeup is the only view that shows its form.
- **Knob overlap:**
  - The 6 mm knob is coplanar with the 6 mm-thick leaf (z 0.082–0.088), so its 4 mm overlap is fully buried. The visible 6 mm reads as an end knob resting on the base top.
  - It is acceptable, but it is a fused simplification rather than a knob on a mounting.
- **Peep/tab mismatch:** carried over from r11. It only matters if an upright variant or fold animation is ever needed, and the plan scopes the part as static-only. The 10 mm peep is still the most noticeable feature of the folded sight in `r12-closeup-rear-sight-rear.png`.
- **No hinge knuckle:** the leaf just meets the pin. That is invisible at game scale. In closeups it reads as a block, not a hinged leaf. It is a noted simplification, not a blocker.
- **Whole gun at 256 px** (from `r12-native-front-right.png`): reads clearly as an M2HB. The spade grips, boxy receiver, perforated barrel support and long heavy barrel are all clear.
- **At 128 px** (from `r12-native-right.png`): reads as a heavy machine gun. The front blade is a 1–2 px tick and the folded rear sight is invisible, which is correct for a folded leaf. There is no AA sight anywhere. The front blade is upright.

## 4. Scores (model-quality 1.0.0)

All scores meet the minimums: 2 for every category and 3 for the core ones.

| Category | Score | Observation |
|---|---|---|
| identity-recognition (core) | 3 | `r12-native-right.png`: spade grips, receiver, perforated barrel support and HB barrel read as an M2HB. |
| proportion-mass | 3 | `r12-native-right.png`: receiver-to-barrel mass is credible; folding the leaf lowers the rear profile as intended. |
| silhouette (core) | 3 | `r12-native-right.png`: clean profile, tall front blade, low folded rear sight, nothing protruding. |
| form-hierarchy | 3 | `r12-native-top.png`: the primary to secondary forms read clearly; the folded leaf merges into its base from above. |
| mechanical-coherence (core) | 3 | `r12-closeup-rear-sight-quarter.png`: leaf seated, no gap or overhang; no hinge knuckle and the knob is fused (at the floor). |
| surface-material | 2 | `r12-native-front-right.png`: uniform flat steel plus black grips; serviceable, with little material separation. |
| viewpoint-robustness | 3 | `r12-native-rear-left.png`: coherent in every view; the rear sight is unreadable in the top view. |
| production-integrity (core) | 3 | `r12-native-right.png`: hashes, 12/12 dimension checks, deterministic baseline and validation all bind 2906b4d4; small evidence gaps. |

## 5. Unresolved core objections

None.

These are non-core and need your attention:
1. Confirm the in-place supersession route, since your decision named a successor.
2. Fix the record: the `boundAt` time, the `productionAuthorized` flag, and the stale `heightBlocker` in `plan.json`.
3. Keep the `productionInput`/construction receipt, so the 17-fingerprint claim and bc06d303 can be checked directly.
4. The missing hinge knuckle, the fused knob and the peep/tab mismatch are noted static-only simplifications.

```json
{"scores":{"identity-recognition":{"score":3,"view":"right","observation":"r12-native-right.png: spade grips, receiver, perforated barrel support and HB barrel read as M2HB"},"proportion-mass":{"score":3,"view":"right","observation":"r12-native-right.png: credible receiver-to-barrel mass; folded leaf lowers rear profile as directed"},"silhouette":{"score":3,"view":"right","observation":"r12-native-right.png: clean profile, upright front blade, low folded rear sight, no overhang"},"form-hierarchy":{"score":3,"view":"top","observation":"r12-native-top.png: primary/secondary forms clear; folded leaf merges tonally into its base from above"},"mechanical-coherence":{"score":3,"view":"front-right","observation":"r12-closeup-rear-sight-quarter.png: leaf seated on base with no gap/overhang; no hinge knuckle and knob fused 4 mm into leaf end"},"surface-material":{"score":2,"view":"front-right","observation":"r12-native-front-right.png: uniform flat steel plus black grips; serviceable, little material separation"},"viewpoint-robustness":{"score":3,"view":"rear-left","observation":"r12-native-rear-left.png: coherent across views; rear sight unreadable from top"},"production-integrity":{"score":3,"view":"right","observation":"r12-native-right.png: blend/GLB/ops hashes recomputed, 12/12 dims, deterministic baseline and validate_asset bind 2906b4d4; productionInput and non-mesh fingerprints not retained"}},"objections":[]}
```
technicalValidation: pass - recomputed hashes match, the GLB's P11 equals operations.json, and the 12/12 dimension report, deterministic baseline, validate_asset, masks, closeups and GLB all bind checkpoint 2906b4d4 (the record gaps above are non-blocking).
visualRecommendation: go - the folded leaf is seated with no gap or overhang and the gun reads as an M2HB at 256 and 128 px; the hinge, fused knob and peep/tab simplifications are noted, not blocking.
humanApproval: not granted (pending George)

A read-only search I ran in the background was stopped when it hit its time limit. It was looking for the committed batch's inputs in FormSeed's staging folder, to reproduce the status hash bc06d303 directly. It found nothing before it stopped, and I'm not restarting it.

The verdict doesn't change. I had already tied the committed batch to `operations.json` another way: every P11 vertex in the review GLB matches the file to within float32 precision, with 532 triangles. bc06d303 still can't be reproduced from what's kept in `finishing-r12/`, which is the non-core evidence gap I listed in item 3.
