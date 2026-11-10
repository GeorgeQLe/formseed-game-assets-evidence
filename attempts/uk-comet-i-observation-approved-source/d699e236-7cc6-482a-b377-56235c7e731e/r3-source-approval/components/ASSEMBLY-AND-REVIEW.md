# Comet optional conversion packages — artwork review candidate

Version **0.1.0-candidate.r3-fit2**. No artwork approval, catalog publication, release, game integration or performance qualification. Native source head r3 is a standalone component library; the complete vehicles are derived review fixtures, never three new tank sources.

## Evidence and historical scope

The inspected free primary evidence did not substantiate precise Comet command or dedicated artillery OP arrangements/dates. Both treatments are explicitly alternate-history proposals. Secondary postwar conversion counts are unresolved leads. The attributed Comet trailer photograph shows towing with the conventional bow gun; a functioning Comet flame conversion is not established. The operational Crocodile treatment is alternate history. No claim that absence of evidence proves nonexistence.

Reference packet: `research/reference-packet.json` and the shared `military-vehicle-references/comet/conversions-20261110/research.json`. Museum/period photographs inform visual vocabulary only. No purchased reference, third-party texture or copied donor mesh is included. Trailer/fitting dimensions are authored design envelopes, not authenticated manufacturing dimensions. The RMG/Tirpitz binocular lead was not used as a British-service claim; the proposed twin optic head is designed equipment.

Omega War reconciliation follows the current game bible: war begins 16 April 1946. Proposed adaptations are not added to canon, roster or balance. Radio/observation/flame gameplay functions, ammunition, unit availability and crew duties need owner decisions before consumer implementation.

## Exact dependency and reconstruction

Require `uk-comet-i@1.0.0`, early cowl-exhaust configuration, clean source r14 checkpoint `564be9ce-9c20-4b31-b254-9234fb54d26a`, SHA `8a309720170722a8805eccc52ee1ff00ef4cf761a2ef228bfa1f0cb45699610d`. Preserve all accepted sources, sealed delivery and existing six direct-clean condition recipes. The original static P36/P37 bands remain unchanged; no new animated tracked running gear is supplied or required.

1. Verify `SHA256SUMS.json`, `component-registry.json`, exact accepted base registries and the selected package recipe.
2. Begin from the clean73-part base once. Execute every explicit retain/replace/remove/add operation in the chosen recipe. `baseCondition` is provenance, not an instruction to apply another condition first. Never overlay D01 onto a previous D state.
3. Select native objects/meshes using each component source selector. Every component has its own standalone GLB and exact native source job/checkpoint/revision/hash.32 identities retain r2;12 corrected identities use r3. Native files contain a grid library: discard source-grid placements.
4. Use registry parent-local row-major transforms to reconstruct hierarchy in native +X forward,+Y left,+Z up metres. Standalone GLBs are local glTF +Y-up: C(x,y,z)=(-y,z,-x). Convert matrices with C M C^-1 exactly once. glTF matrices are column-major.
5. Preserve explicit installed wheel scale [1,.95,1] on T_P04/T_P05 and T_DP04A/T_WP05A. This narrows the instance along its axle, preserves diameter and source/export bytes, and removes shell/lid interference. It is a designed installation, not historical dimensions. Do not replace it with native grid scale or silently normalize it away.
6. Create independent object transforms/visibility per vehicle. Source geometry may be cached immutably only with an explicit consumer lifetime policy. Two separately loaded review instances were checked for isolated pose, visibility, geometry arrays and material disposal. Game adapter cache/resource behavior remains unqualified.
7. W03 inserts the exact accepted whole-turret wreck delta above all turret equipment. Use recipe resolved matrices for static review or reproduce the complete moving tree; never displace only the base shell while leaving conversion fittings behind.

Only the diagonal clean/D01/D02/D03/W01/W02/W03 pairings are supported:21 direct-base manifests.126 cross-condition combinations are explicitly unsupported. All three packages are mutually exclusive. Shared S equipment retains one identity with separate instances; no implicit command+OP or flame+command combination.

## Role, weapons and occupants

| Package | Main gun / turret | Secondary weapons | Stations and restrictions |
|---|---|---|---|
| Command | Live77mm and normal base controls retained | Both Besas retained | Five base stations; proposed extra communications duty. New equipment is accessory cases/field kit, not an exposed WS19 set. |
| Artillery OP | Live gun and muzzle brake removed; explicit short closed dummy; neutral pitch/recoil locked; turret yaw retained under interlocks | Coax removed and visibly closed; hull Besa retained | Five stations; observer/signaller/assistant duties proposed. Dedicated artillery role; no generic scouting bonus asserted. |
| Crocodile |77mm/turret retained with base restrictions | Coax retained; hull Besa barrel replaced by visual projector, retained collar | Five stations; hull operator duty proposed. Projector neutral locked, hull aiming only proposed. Essential separate trailer; no-trailer state cannot present powered flame. |

All seven existing rider anchors are declared unavailable for all21 conversions/conditions. Base anchor records are preserved; no shared rider/crew figure or additional capacity is bundled. Five crew-station locations remain separate from rider anchors. Occupied ergonomics remain a consumer review dependency.

## Motion and service guidance

Base turret pivot [.35,0,1.64]. New turret equipment sampled at24 yaw angles per clean,D01,D03 without new hull crossings. This is sampled additional-equipment verification, not replacement approval for all base controls. Commander hatch halves sampled to100°, loader halves to90°; hull hatches use existing turret-park90° interlock. Freeze traverse while crew occupy hatches. Forward main gun sampled -8°,0°,20° with recoil0,.15,.30m against new parts for command/Crocodile. Rearward depressed-gun combinations remain unqualified.

OP head pivot[-.62,-.06,2.94], yaw five samples(-180,-90,0,90,180), pitch±20 and0; no new obstacle crossing beyond intended bearing. Damaged optic/pedestal do not automatically inherit scanning; disable them pending condition-control qualification. Visual damage alone is not a gameplay functionality decision. D02 base gun/turret damage and existing base mobility restrictions remain authoritative. Wrecks disable ALL controls and powered operation.

Engine deck P03 straight-lift removal sampled0..1m at .05m with turret parked90° against conversion additions; zero crossings. No engine-deck hinge/interior authored; use base service constraints. Coupling/trailer service requires stationary vehicle and disabled effects.

Trailer root pivot[-3.55,0,.8], axle at[-6.15,0,.621], authored axle distance2.6m; wheels spin about localY. Coupling, boot and drawbar socket intentionally overlap at the shared pivot.171 actual mesh poses sample yaw-45..45 every5°, pitch-10/0/10°, roll-8/0/8°; no trailer/carrier crossings outside intended hitch contacts. Positive and negative yaw cover instantaneous turning/reversing envelopes. Reversing needs a consumer kinematic solver and stop before jackknife; no implicit yaw sign reversal. Nonzero pitch/roll requires matching terrain, never flat-plane operation. This is not continuous physics proof.

Underbody guard minimumZ .3275m lowers the unchanged nominal .4m base clearance by .0725m; route choice is an explicit designed compromise. Closed external armor/conduit plus protective boot suggest the historical system visually; no full internal route, real fuel fabrication, ignition engineering, operating pressures or flexible hose simulation is supplied. Damaged towing is disabled. D03 collapsed tyre has a solved static two-tyre ground-contact pose with fixed hitch. W02 trailer disconnected/offset; W03 disconnected/overturned; no invisible hose spans a detached gap.

## Condition packages

| Candidate | Treatment |
|---|---|
| command-clean | Clean designed conversion |
| command-D01 | Mobility strike with snapped communications aerial |
| command-D02 | Weapon strike and crushed radio accessory cases |
| command-D03 | Rear blast distorts cable reel |
| command-W01 | Burned rack and aerial stubs |
| command-W02 | Mobility wreck with aerial and command wallet lost |
| command-W03 | Detached turret carries wrecked communications equipment |
| observation-clean | Clean designed conversion |
| observation-D01 | Mobility strike and optical head impact |
| observation-D02 | Dummy tube broken and equipment cases crushed |
| observation-D03 | Rear blast bends observation pedestal and aerial |
| observation-W01 | Burned observation and communications equipment |
| observation-W02 | Optic head and plotting wallet lost in mobility wreck |
| observation-W03 | Detached turret with broken dummy and crushed optic |
| crocodile-clean | Clean designed conversion |
| crocodile-D01 | Mobility loss and deformed bow projector |
| crocodile-D02 | Weapon strike with bent towing presentation and underbody armor |
| crocodile-D03 | Rear blast dents trailer and collapses left tyre |
| crocodile-W01 | Burned carrier and ruptured trailer |
| crocodile-W02 | Broken towing connection with detached trailer |
| crocodile-W03 | Detached turret and overturned open trailer, roof lost |

Condition ownership collisions are explicitly resolved in each manifest. Conversion-owned P11/P72/P73/P06/P08/P10/P23 slots suppress conflicting base clean/DP/WP alternatives where applicable. Removed OP P07 never reappears through a base condition. Replacements reuse compatible DP/WP identities instead of making three versions of every part. W01 burn/collapse,W02 mobility/tow separation,W03 displaced/overturned outcomes have different selected geometry and placements, not recolours alone.

## Sources and physical ownership

| ID | Condition | Owner | Source revision | Parent | Standalone GLB |
|---|---|---|---|---|---|
| C_P01 | clean | C | r2 | turret-yaw | `parts/C/C_P01-r2.glb` |
| F_DP01A | damaged | F | r3 | hull-mg-pitch | `parts/F/F_DP01A-r3.glb` |
| F_DP02A | damaged | F | r2 | asset-root | `parts/F/F_DP02A-r2.glb` |
| F_P01 | clean | F | r3 | hull-mg-pitch | `parts/F/F_P01-r3.glb` |
| F_P02 | clean | F | r2 | asset-root | `parts/F/F_P02-r2.glb` |
| F_P03 | clean | F | r2 | asset-root | `parts/F/F_P03-r2.glb` |
| F_P04 | clean | F | r2 | asset-root | `parts/F/F_P04-r2.glb` |
| F_WP01A | wreck | F | r3 | hull-mg-pitch | `parts/F/F_WP01A-r3.glb` |
| O_DP01A | damaged | O | r2 | gun-elevation | `parts/O/O_DP01A-r2.glb` |
| O_DP03A | damaged | O | r2 | turret-yaw | `parts/O/O_DP03A-r2.glb` |
| O_DP04A | damaged | O | r2 | observation-head | `parts/O/O_DP04A-r2.glb` |
| O_P01 | clean | O | r2 | gun-elevation | `parts/O/O_P01-r2.glb` |
| O_P02 | clean | O | r2 | gun-elevation | `parts/O/O_P02-r2.glb` |
| O_P03 | clean | O | r2 | turret-yaw | `parts/O/O_P03-r2.glb` |
| O_P04 | clean | O | r2 | observation-head | `parts/O/O_P04-r2.glb` |
| O_P05 | clean | O | r2 | turret-yaw | `parts/O/O_P05-r2.glb` |
| O_WP01A | wreck | O | r2 | gun-elevation | `parts/O/O_WP01A-r2.glb` |
| O_WP04A | wreck | O | r2 | observation-head | `parts/O/O_WP04A-r2.glb` |
| S_DP01A | damaged | S | r2 | turret-yaw | `parts/S/S_DP01A-r2.glb` |
| S_DP02A | damaged | S | r2 | turret-yaw | `parts/S/S_DP02A-r2.glb` |
| S_DP05A | damaged | S | r2 | turret-yaw | `parts/S/S_DP05A-r2.glb` |
| S_P01 | clean | S | r2 | turret-yaw | `parts/S/S_P01-r2.glb` |
| S_P02 | clean | S | r2 | turret-yaw | `parts/S/S_P02-r2.glb` |
| S_P03 | clean | S | r2 | turret-yaw | `parts/S/S_P03-r2.glb` |
| S_P04 | clean | S | r2 | turret-yaw | `parts/S/S_P04-r2.glb` |
| S_P05 | clean | S | r2 | turret-yaw | `parts/S/S_P05-r2.glb` |
| S_WP01A | wreck | S | r2 | turret-yaw | `parts/S/S_WP01A-r2.glb` |
| S_WP02A | wreck | S | r2 | turret-yaw | `parts/S/S_WP02A-r2.glb` |
| S_WP03A | wreck | S | r2 | turret-yaw | `parts/S/S_WP03A-r2.glb` |
| S_WP05A | wreck | S | r2 | turret-yaw | `parts/S/S_WP05A-r2.glb` |
| T_DP01A | damaged | T | r2 | trailer-root | `parts/T/T_DP01A-r2.glb` |
| T_DP02A | damaged | T | r3 | trailer-root | `parts/T/T_DP02A-r3.glb` |
| T_DP04A | damaged | T | r3 | trailer-wheel-left | `parts/T/T_DP04A-r3.glb` |
| T_P01 | clean | T | r2 | trailer-root | `parts/T/T_P01-r2.glb` |
| T_P02 | clean | T | r3 | trailer-root | `parts/T/T_P02-r3.glb` |
| T_P03 | clean | T | r3 | trailer-root | `parts/T/T_P03-r3.glb` |
| T_P04 | clean | T | r3 | trailer-wheel-left | `parts/T/T_P04-r3.glb` |
| T_P05 | clean | T | r3 | trailer-wheel-right | `parts/T/T_P05-r3.glb` |
| T_P06 | clean | T | r2 | trailer-root | `parts/T/T_P06-r2.glb` |
| T_P07 | clean | T | r2 | trailer-root | `parts/T/T_P07-r2.glb` |
| T_WP01A | wreck | T | r2 | trailer-root | `parts/T/T_WP01A-r2.glb` |
| T_WP02A | wreck | T | r3 | trailer-root | `parts/T/T_WP02A-r3.glb` |
| T_WP03A | wreck | T | r3 | trailer-root | `parts/T/T_WP03A-r3.glb` |
| T_WP05A | wreck | T | r3 | trailer-wheel-right | `parts/T/T_WP05A-r3.glb` |

S=shared communications equipment,C=command,O=OP,F=carrier flame equipment,T=trailer. Every physical component owns a unique native mesh; dark nozzle cup and colored wheel hub are joined material islands belonging to that physical part. No hidden accepted Comet mesh is incorporated into a conversion source. Exact unchanged accepted payload/material correspondence is checked in every assembled preview.

## Review decision and delivery limits

Review `review/batch-artwork-review-r3-fit2-provenance.png`: columns Command,Artillery OP,Crocodile; rows clean,D01,D02,D03,W01,W02,W03; opposing oblique views per cell. Full203 frames include opposing sides,top,underside and equipment/projector/tow/trailer closeups.168 unlabelled256px views support recognition assessment. PNGs show actual selected components. Typed provenance copy preserves all protected pixels; source r3 checkpoint labels describe the current source head, while retained r2 component provenance remains in the registry.

The producer backend supports native job/checkpoint/export/validation/isolation, but no first-class conversion-package publication, per-component artwork approval, package condition composition or consumer assembly semantics. These are explicit local preparation contracts. Producer stage remains blockout-review with no human workflow review recorded. Exact local rubric assessments and independent findings are separate from backend approval.

Review is for these precise optional asset candidates and condition appearances. A human artwork decision does not authorize integration/publication/release. Game loadouts/canon/balance, adapter implementation, towing/terrain, real runtime controls, cache lifetime, browser/native delivery and target performance remain separate. No automatic promotion/completion call was used.

Historical attempts and objections remain under evidence/history on T9. No requester ceiling was specified; ledger records autonomous candidates and rejected/restored attempts without resetting counts. Base220-file preservation and cleanup reports are in validation.


## Current recommendation and human decision

Technical source/assembly verification passes within the recorded scope. The deterministic model-quality evaluations are75/100 (go threshold75); the style evaluations are75/100 (no-go threshold80). Every style category scored3; the independent reviewer independently assigned all eight3 and found no reference-quality4. No score was raised to meet a threshold. The positive model-quality result does not override the style no-go. Recommend selective corrections before final artwork acceptance, with the exact candidates available for the requested batch human artwork review and feedback.

Priority observations: fine olive fitting edges and OP optical-end contrast can merge at256px; command W02 front-only role discrimination is weak, although the rear collapsed cases/reel distinguish it from the base wreck. Case/optic edge and material treatment is coherent rather than exceptional. No new core form/interface blocker remains. The decision here is an artwork judgment on the21 pinned appearances, not permission to integrate, promote or publish. Human approval remains absent. See `delivery/ASSESSMENT.json` and42 structured assessments/evaluator results.
