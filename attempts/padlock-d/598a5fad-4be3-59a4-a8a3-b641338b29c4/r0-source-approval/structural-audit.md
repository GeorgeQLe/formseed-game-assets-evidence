# Structural audit — soft-rounded polish pass 2 (independent read-only auditor)

## Round 1 (6-px draft)

AUDIT: soft-rounded polish pass-2 draft (polish-v2/p2-recipe-request.json, sha256 93306d08…78a9; read-only, no MCP calls, no repo writes)

There is no blocker, and checks 1–3 pass. One thing needs a decision before dispatch: p2 doesn't touch the inherited checker contour objection, which p1's evaluation lists as an unresolved core objection. Unless it is addressed or explicitly recorded as an accepted trade-off, p2 stays no-go on backgroundReadability.

== CHECKS 1–3: PASS ==
- **Mask fidelity: PASS.**
  - Body (308 px) and shackle (86 px) are identical to the pass3 masks, with 0 duplicates and 0 pixels outside the masks.
  - 60 spans are run-length merged; I expanded them before comparing.
  - The keyhole region is byte-identical to pass3's.
  - The source is identical: dc00a000…, rev 0, fc6c21ca…a829.
  - All roles are flat with tone base, so the change is colour-only and alpha is unchanged.
  - New recipeId ee000579-4ca4-5660-8f44-b513462392c1, expectedRevision 0, new idempotency key.
- **Palette rule: PASS.** Body adds 2 tones (light, hue +2.2°; mid, −1.5°). Shackle adds 2 tones (light, +0.0°; mid, +2.0°). All four lie between their material's shadow and highlight. No body-low is used.
- **maxColors: PASS.** 8 roles plus the keyhole make 9 colours, and maxColors is 9. Roles, theme and usage match, with no duplicate RGB.
- **Delta against p1 (3213d0c6…):** exactly the 6 stated pixels and nothing else.
  - (19,6), (20,6), (21,7), (21,8): shackle-mid → base.
  - (18,14), (19,14): body-base → light.

== RIGHT-SHOULDER BANDING: RESOLVED ==
- The parallel mid ring is gone. Right shoulder rows 6–8 now read n-n-s-s-s-s (x14–21), .-.-n-s-s-s-s (x16–22) and n-s-s-s (x19–22).
- The only dark pixels left are on the inner-opening contour: the underside run (14–17,6), then (18,7), (19,8), (20,9–13). That is one continuous diagonal.
- There is no alternation and no single base pixel left at (18,6) or (21,6), and nothing ends abruptly at row 8.
- Remaining single-tone pixels: (10,6) base and the opening-contour stair pixels (12,8), (13,7), (18,7), (19,8). These are ordinary diagonal stair connections.

== NEW RIGHT-SHOULDER MASS OR BALANCE ISSUE: note, review-critical ==
- The right shoulder is now an undivided base mass: (16–20,5), (18–21,6), (19–22,7), (20–22,8), continuing into the leg at x21–23. This resembles the configuration behind the inherited pass3 "upper-right shoulder reads as one broad base mass / fuller" objection.
- The left shoulder differs from its mirror only by the light ring (11–13,6), (10,7), (10,8) and the crown highlight (13–15,5).
- The pass3 mechanism isn't present:
  - The left outer contour is solid base on both sides, so no pale left outer edge vanishes. The ring is one pixel inside, and outer contrast is identical on both sides: 4.55 on dark, 1.97 on checker.
  - The legs are mirror-exact.
- My prediction is that the risk is low to moderate: a lit left shoulder against a plain right one reads as lighting, not width.
- If you want a right-side shadow cue without reintroducing banding, attach it to the inner contour as a solid cluster rather than a separate ring. For example, make (19,7) and (20,8) mid, so the shadow is a 2-px band along (18,7)/(19,8). That doesn't recreate a base-mid-base-mid alternation.
- Optional; otherwise the post-pass reviews must judge right-shoulder fullness explicitly.

== x19 TERMINUS: improved, now anchored, still a hard cut (note) ==
- Row 14 light now runs x6–19 (14 px), with base x20–25.
- It ends exactly where the opening ends and the right leg lands (leg x20–23, inner mid column at x20). That ties the cut to a structural landmark instead of an arbitrary point at x17/18.
- It's still a one-step cut with no transition pixel. The light also runs continuously under the left leg's landing (x8–11), so occlusion doesn't explain it on both sides; it reads as falloff toward the shadow side starting at the right leg.
- Probably acceptable at 1×. Review it at 8×.
- Side effect: the whole bottom edge of the opening (x12–19, row 14) is now body-light. Seen through the opening on checker, that is 1.50 against #C0C0C0, so the opening's lower boundary is weak on checker. Note for review.

== DECIDE BEFORE DISPATCH (last pass) ==
- **Checker contour objection (D-CORE-01): untouched by p2, should-fix or explicit decision.**
  - The body-light left edge (x5 and row 14, 15 outer px) is at 1.50 against #C0C0C0.
  - 26 shackle-base outer pixels are at 1.97.
  - p1's adversarial review lists this as an unresolved core objection, slightly worse than v1. If nothing changes, p2 will carry the same forced no-go on backgroundReadability.
  - Options:
    - (a) Make the body's outer left column x5 (rows 15–27) body-base, at 2.22 against #C0C0C0, and keep the light one pixel in at x6. This copies the shackle's own "base outer, light ring inside" construction. The cost is about 13 px and a slightly narrower lit face.
    - (b) Record it as an accepted trade-off, with evidence. The shackle can't satisfy both backgrounds with one tone: base is 4.55 on dark but 1.97 on checker, and mid is 2.72 on dark but 3.29 on checker. Hue separation holds it.
  - Either is fine to choose, but make the choice before the last pass rather than leaving it implicit.
- **Style-drift objection: essentially unchanged.**
  - Body differs from restrained-bevel by 24/308 pixels (p1: 26). Shackle differs by 37/86 (p1: 39). p2 is 65 body / 24 shackle pixels from mostly-flat.
  - Role counts, p2 vs bevel:
    - body-base 228 vs 244; body-light 34 vs 31; body-mid 43 vs 33; body-highlight 3 vs 0
    - shackle-base 60 vs 32; shackle-light 5 vs 10; shackle-mid 18 vs 44; shackle-highlight 3 vs 0
  - Removing the right ring slightly reduces arch modelling. The requester's p1 preference is the governing evidence that the look is kept, so this is a note only. The reviewers should cite the requester feedback rather than re-litigate it.

== POST-PASS REVIEW NOTES (native and 8×, on light, dark and checker) ==
1. Right-shoulder fullness against the lit left shoulder, now that the right ring is gone; confirm the shoulder banding is resolved.
2. Whether the top-light end at x19/20 reads as anchored or abrupt.
3. Checker contrast: body left edge and opening bottom edge at 1.50; shackle outer at 1.97. Contrast on dark: right column x26, x25 taper and row 28 at 2.85, the softest dark edges.
4. Stripe-like runs are unchanged apart from the longer top light: row 14 light (14 px), x5 light (13 tall), x26/x25 mid, row 28 mid (20 px), and the mid L-frame. Nothing is darker than #875E2C.
5. Light direction is consistent upper-left: lit top and left, glint, crown highlight, left ring; mid right, bottom and inner-opening contour.
6. Residual stair pixels at (10,6), (12,8), (13,7), (18,7), (19,8).

**Gate status:**
- technicalValidation (recipe level): pass.
- visualRecommendation: not assessed (p1's no-go of 70 stands until there is new evidence).
- humanApproval: absent.


## Round 2 (final 8-px, dispatched)

FINAL AUDIT: soft-rounded polish pass-2 (polish-v2/p2-recipe-request.json, sha256 0b72526b…344f; read-only, no MCP calls, no repo writes)

Checks 1–3 still pass, the shoulder banding stays resolved with the new cue, and no blocker prevents dispatching the last pass.

**Checks 1–3: PASS**
- **Mask fidelity:**
  - Body (308 px) and shackle (86 px) match the pass3 masks exactly, with 0 duplicates and 0 pixels outside the masks. The 62 merged spans were expanded before comparing.
  - The keyhole region is byte-identical to pass3's.
  - The source is identical: dc00a000…, rev 0, fc6c21ca…a829.
  - All roles are flat with tone base, so the change is colour-only and alpha is unchanged.
  - recipeId ee000579… and idempotency key are unchanged; expectedRevision is 0.
- **Palette rule:** body adds 2 tones (light, hue +2.2°; mid, −1.5°) and shackle adds 2 (light, +0.0°; mid, +2.0°). All four lie between their material's shadow and highlight.
- **maxColors:** 8 roles plus the keyhole make 9 colours, and maxColors is 9.
- **Delta vs p1 (3213d0c6…):** exactly 8 px.
  - (19,6), (20,6), (21,7), (21,8): mid → base.
  - (19,7), (20,8): base → mid.
  - (18,14), (19,14): base → light.

**Banding: still RESOLVED**
- The right shoulder rows now read as single runs with no base/mid alternation:
  - row 6, x16–21: n n s s s s
  - row 7, x18–22: n n s s s
  - row 8, x19–22: n n s s
- The shadow is one solid 2-px band along the inner contour, (18,7), (19,7), (19,8), (20,8). It narrows into the leg's 1-px inner mid column, (20,9–13).
- Single-tone stair pixels remain only at (10,6), (12,8) and (13,7) on the left. These are ordinary diagonal connections.

**Blockers: none.**
- The checker contour objection stays open by the requester's decision (checker-tradeoff-decision-20261006.json): body-light left edge at 1.50 and shackle-base outer at 1.97 against #C0C0C0. It remains unresolved for the formal recommendation.

**AUDIT RECORD (paragraph to retain)**
I independently audited the final pass-2 recipe for the selected soft-rounded padlock D direction (polish-v2/p2-recipe-request.json, sha256 0b72526b940861466a5cdca718c5dc3383e1932f47e573e578d1d3a4ce6e344f; recipeId ee000579-4ca4-5660-8f44-b513462392c1) read-only. The recipe passes all structural checks against recipe-pass3.json. It uses the identical source assembly (dc00a000…, rev 0, fc6c21ca…a829), covers the body and shackle masks exactly once, leaves the keyhole region byte-identical, and changes colour only, so alpha and silhouette are unchanged. It meets the scope-decision-20261005 palette rule with 2 added tones per material, each same-hue and between that material's shadow and highlight, and maxColors is 9, matching its 9 colours. It differs from pass 1 by exactly 8 px. Relative to the selected v1 study, the polish passes deliver the authorized fixes:
- The lit left face is narrowed and smoothed to 2→1 px.
- The x7 streak is replaced by a 3-px corner glint.
- The right band is 2 px of #875E2C, with nothing darker.
- The dark-background minimum rises from 1.94 to 2.85 on the body; the shackle's outer edge is all base at 4.55.
- The legs are mirror-exact.
- The arch is cleaned, with the right-shoulder banding replaced by a solid 2-px inner-contour shadow.
- The top light now ends at x19, at the opening/right-leg boundary.

Lighting is consistently upper-left. The body is 24/308 pixels from restrained-bevel and the shackle 39/86. The requester's p1 preference is the evidence that the soft-rounded look is kept. The post-pass reviews must explicitly check these open items at native and 8× on light, dark and checker backgrounds:
- right-shoulder fullness against the lit left shoulder
- whether the x19 top-light end reads anchored or abrupt
- the softest dark edges (x26, the x25 taper and row 28 at 2.85)
- the mid L-frame and other stripe-like runs
- residual stair pixels
- the requester-accepted checker trade-off (1.50 / 1.97), which remains an unresolved objection for the formal recommendation

**Gate status:**
- technicalValidation (recipe level): pass.
- visualRecommendation: not assessed. The p1 no-go stands until new evidence.
- humanApproval: absent. The requester's trade-off acceptance and preference are not finished-art approval.

