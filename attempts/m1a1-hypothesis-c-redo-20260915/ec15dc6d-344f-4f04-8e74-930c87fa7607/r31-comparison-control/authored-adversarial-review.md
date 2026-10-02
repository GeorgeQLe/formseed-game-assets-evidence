# Abrams r31 — separate adversarial authored review

Reviewer: `/root/review_support`, 2026-10-02. No producer operation, lease, or source mutation performed. This review judges the bounded upper shoulder/roof direction separately from whole-model qualification.

Exact subject: `ec15dc6d-344f-4f04-8e74-930c87fa7607`, main r31, checkpoint `4d0f044e727470dd2d4fb497aed3b1754df4c3c742960c92b47a7466d7a40d63`. Native render-set hash: `5cb347514e2496d598971e070e71bf636eb1bffd8a1d39bf01ccec4fb505b9f4`. `candidate-render.json` SHA-256: `28420ec5f2682ab53c59531542bc281116513ea8aad4476e70ec59b703620d15`.

## Review sequence and neutral observations

Read AGENTS, rubric requirements and the historical r30 assessment. Inspected all six r31 native whole-model views before reading the candidate reference map or construction rationale. Then inspected the reference map, its three actual USMC drawing crops, and all six native r30 counterpart views. This is not a blind recognition test: the requested subject identity and historical assessment were known.

At first inspection the object reads as a tracked tank with seven road wheels, a long cannon, a broad forward wedge turret and an aft bustle. The front and rear have shoulders that slope inward toward a flat upper roof. Top and oblique show a continuous inset roof bounded by a wider outer shoulder. Both sides retain the long forward roof incline and flat aft roof, with the rear underside/deck separating band still present. The gun remains centered and visually attached. No visibly detached roof, open shoulder crack, new broad underside cavity, or new side-profile kink is apparent in these native views. The model remains a plain construction study, especially at roof, rear and running gear.

## Comparison and reference challenge

Relative to r30, the clearest change is the front/rear upper silhouette: vertical outer walls become inward-sloping shoulders. Top and oblique acquire an explicit inset roof boundary instead of allowing the roof to occupy the full outer width. Side silhouettes show no evident adverse change to the accepted deck/underside or gun relation. The USMC front crop supports an upper armor extent narrower than the lower cheek extent; its plan crop also shows an inset upper boundary around the front and sides. This gives the local taper a cross-view basis.

The strongest counterargument is that drawing envelope extrema at different longitudinal stations do not reconstruct one exact shoulder surface. The aft turret may control the front silhouette, and fittings obscure portions of the roof. Therefore the chosen inset magnitude and rear treatment remain construction choices; these images do not establish factory dimensions or exact station correspondence. In oblique the new edge remains a simple broad planar shoulder. It does not yet establish the full reference surface hierarchy. That limits the claim to a supported local direction, rather than proving an accurate completed Abrams roof.

## Core-category objections

After the initial visual inspection, the separate export reviewer identified a lower-aft shelf regression in `authored-independent-review.md`. This reviewer then independently loaded both hash-verified actual GLBs through `readAssembly` and intersected the floor and bustle triangles at X=-6.248, -6.1 and -5.9. The measured protrusions reproduce **59.40, 44.15 and 22.67 mm per side**, respectively. At X=-6.248, the unchanged floor half-width is 1.30013049 m, while the r31 bustle half-width is 1.24073264 m; both were 1.30013049 m at r30. Floor Z spans 1.91976–1.95982 m there, and the bustle starts at 1.94476 m. This is an overlapping stepped interface, not an open-gap claim.

The initial native-only observations did not identify the significance of the fine doubled lower-aft oblique line. The actual geometry now gives that line a concrete explanation: the floor rises above the global protected height while the adjacent bustle moves inward. Therefore the accepted underside interface is not preserved as a coupled exterior contour, even though the floor itself is unchanged. Sparse reference lines do not justify introducing that shelf. This is a new in-scope regression, unlike the pre-existing detail/style/dimension gaps.

| Core category | Strongest reason production-ready qualification remains unsupported | Local regression finding |
| --- | --- | --- |
| Identity-recognition | Front, rear and top remain generic plain tank masses without enough variant-specific structures; no independent all-required-view 256 px recognition evidence distinguishes M1A1 from neighboring modern tanks. | The taper preserves cannon, wedge cheeks, wheel count and broad hull/turret relationship. No observed loss of existing identity cues. |
| Silhouette | Upper inset has reference support, but exact roof/shoulder stations, aft surface shape and completed reference silhouette remain unresolved. An approximate width ratio cannot close these targets. | Front/rear and plan improve the inset reading, but the newly protruding aft floor creates an unsupported lower shelf. This concrete oblique contour regression triggers restoration. |
| Mechanical-coherence | Simplified running gear and armor supports retain broader unresolved construction assumptions. Additionally, the coupled aft floor/bustle interface now steps outward despite its preservation requirement. | Independently reproduced actual-export sections establish 22.67–59.40 mm lateral floor protrusion at three aft stations. Connected overlap does not excuse this new exterior ledge. |
| Production-integrity | Current deterministic technical output does not supply missing authoritative dimensions, resolved immutable style binding, recognition evidence or whole-model completion. | Candidate validation is bound to r31 and reports success with no issues. This lane does not independently certify export preservation, masks, seam geometry or motion. Those must be checked for this exact checkpoint before final local retention. |

All four whole-model objections remain unresolved. No new numeric scores are assigned here, and no category is raised to production-ready by relative improvement. Deferred fittings, style resolution and dimension authority are carried-forward qualification gaps, not newly introduced defects or reasons by themselves to undo this bounded taper.

## Retain/restore recommendation and triggers

**Restore r30 content; do not retain r31 as the successful bounded correction.** The initially favorable upper-direction observation is insufficient after the actual-export check establishes an unsupported new lower-aft shelf. The upper inset remains a supported research direction, but this particular authored candidate violates its coupled-interface preservation requirement. Preserve the failed attempt and its evidence.

The rollback trigger is met by the changed floor/bustle exterior interface; no open gap, collision or side-silhouette failure is needed to establish it. Other rollback triggers remain an out-of-scope deck, support, pivot or gun-interface change; a new open roof/cheek join or unintended intrusion; a materially pinched/disconnected upper shell; loss of the preserved side silhouette; or a failure to bind these views to the authored checkpoint. Any future authorized recipe must protect the actual rising mating contour rather than one global height. No further candidate is authorized by this review; it does not reset the consumed allowance or substitute for new budget or a specifically human-directed correction.

Before whole-model qualification, prioritize a supported reconciliation of the remaining primary shoulder/roof/bustle relationships, then complete stage-appropriate structural and identity evidence under the existing scope and budget. Do not infer authority for those later mutations from this review.

## Evidence pins and status

The following SHA-256 values were independently computed from the native files listed in `candidate-render.json`:

| View | SHA-256 |
| --- | --- |
| physical-left | `efe86db0820cff79163fa9e959d5e8e4b1dd8b9613fd8de84117a231c7981920` |
| physical-right | `24f8ba5b2818cbca5862bd6e7b26480371e03a997801cd03bccf633fd2b8e366` |
| front | `1561c677a546884d99da07049b3db1fbb22177a4f28b7160b6c242040d8db3cb` |
| rear | `292c4d2604d8b93fc3cc7715ad990e4e8316ce611f3781857b3bcd20ea2a73fb` |
| top | `75453ab0e1cbaf9b55fca62d9e62de0e6f80def094aa1965f2bc0056d43f8fbf` |
| three-quarter | `f1edad6b24586ea76bd47868795a92afb5344794284b2026fdfcb5f4a2c6b405` |

- technicalValidation: `candidate-validation.json` reports r31 passed, deterministic, zero issues, 15,384 triangles, four materials and 64 objects. Render/checkpoint binding inspected. Independently reproduced selected actual-export sections identify a coupled exterior-contour preservation failure despite that generic validation success; complete motion/isolation verification remains separate.
- visualRecommendation: **restore r30 for the bounded retention decision; r31 no-go**, with whole-model qualification still no-go. The upper-taper research direction does not excuse the new aft shelf; no deterministic visual go is claimed.
- humanApproval: absent for r31. Prior direction or CC0 permission cannot supply candidate approval.
