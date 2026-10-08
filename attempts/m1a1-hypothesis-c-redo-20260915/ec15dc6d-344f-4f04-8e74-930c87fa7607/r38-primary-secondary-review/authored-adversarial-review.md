# Separate adversarial review — r38 shoulder cleanup

Reviewer: independent `review_support` lane, 2026-10-06. **Recommend scoped construction retention, with an explicit downward-edge tradeoff. Whole-model visual recommendation remains no-go.** This is not a claim that every roof join is smooth or that the assembly is approved.

Checkpoint `d2236645f11cf33a2847ee59475e40df8ba93f7b6585e313991f6fc6954427b4`; GLB `a57611bc734b8e4e46501886988fee8ebe77bbdfd0cc9802c07c07178365abee`; native render hash `46013a5aa33137a5559a99831775c6988249fb194fc860abf947eb7be00b468d`. Baseline r37 checkpoint `5ebcbf4547e99dd629c1cd1f71a5c9cd84e549d149d31e5517499b53472bce7f`.

## Inspection and actual scope

Directly inspected all six r38 native PNGs in `candidate-render.json` before reading the updated component plan and junction audit. Compared with the six r37 views inspected for the preceding independent review. The current candidate compresses the three peer upper caps; it does not implement the rejected roof expansion described in this lane's initial baseline. The entire roof remains protected. That distinction matters: this is removal of a protruding overlap by lowering peers, not a globally blended roof surface.

Both side views preserve the low roof, gun seating, rising turret underside and open rear basket. Front retains paired cheek mass around the gun; rear retains the basket frame and hull grilles. The top view preserves the accepted oblique branch and asymmetric forward roof. In three-quarter view the roof still reads as a broad connected mass. Fine seam fragments remain, but I see no conspicuous new broad shelf, detached wedge, open crack, or shadow gutter at native whole-model scale. The local change is subtle in these flat views; visual subtlety alone cannot establish that a measured defect disappeared.

## Geometric tradeoff and materiality

Read the current `actual-junction-audit.json` after the native views. It binds the exact checkpoint/export and reports sampled local upward reversal now at most 0.097700 mm among its tested sections, compared with the prior 8.835318 mm lip. This supports removal of the targeted upward lip; it is not a global surface bound or proof of a seamless join.

The same audit exposes a real adverse change in an existing downward roof-wall edge. At X −3.92 across Y −1.247 to −1.248, the sampled drop grows from 80.088553 mm to 93.500903 mm, an increase of 13.412350 mm. At X −3.8 across Y −1.226 to −1.227, it grows from 72.721325 mm to 83.643183 mm, an increase of 10.921858 mm. These are total drops and increments respectively; the larger existing edge must not be described as a mere 13 mm total defect. These sampled discontinuities are also not, by themselves, proof of an open geometric hole.

This is a tradeoff, not monotonic improvement of every junction. At the specifically approximate neutral construction stage, I find the targeted lip removal worth retaining because the larger existing edge does not become an obvious new shelf/gap or materially disrupt the whole-view silhouette. The retained descending edge remains an unfinished mechanical/form limitation. Do not present this as complete shoulder smoothing. A closer view revealing a separated roof, new ledge across a substantial visible run, or damaged protected contacts would reverse this local recommendation.

## Core-category challenge

| Category | Strongest current objection and scoped assessment |
| --- | --- |
| Recognition | Gun, wedge turret, tracked hull and open bustle basket retain intended tank-family readability. The bare roof and simplified running gear still do not establish exact variant recognition; no recognition test is supplied by this cleanup. No visible local recognition regression. |
| Silhouette | Accepted roof branch and low side mass remain legible; the cleanup does not visibly add a horn or flatten the intended roof transition. Unresolved central correspondence and approximate dimensional authority remain. Thin-cap reduction is a construction choice, not a historically measured armor thickness. |
| Mechanical coherence | The upward overlap defect is reduced, but the existing downward roof-wall edge grows by up to the reported 13.412 mm at selected sections. Gun seating, basket openness and lower relationships still read coherently; the remaining edge prevents claiming a finished continuous shell. No visible material regression requiring restore at this stage. |
| Production integrity | Technical validity and unchanged siblings do not qualify finished surface treatment, detail, style, shading or game readiness. Flat neutral renders can conceal join quality under other lighting. This remains an unfinished diagnostic assembly and lacks a qualifying complete visual go. |

## Gate separation

`candidate-validation.json` reports passed, zero issues, deterministic rendering, 16,788 triangles, four materials and 71 objects for this checkpoint. That is technical evidence read from the receipt, not rerun validation by this reviewer. Exact sibling/contact/motion claims belong to the separate source audit; visual inspection alone does not prove them.

- `technicalValidation`: current native receipt passed; dependent isolation and mechanical confirmation remain the separate technical lane's responsibility.
- `visualRecommendation`: **scoped construction retain with the downward-edge tradeoff documented; whole-model no-go**. No scores invented or evaluator go implied.
- `humanApproval`: not granted here; remains an explicit exact-checkpoint decision.

No production calls or model mutations were performed. This review does not yet certify the new colored comparison sheet; uncertainty must remain light gray, green confined to assessed lateral agreement, and central continuation explicitly unassessed.
