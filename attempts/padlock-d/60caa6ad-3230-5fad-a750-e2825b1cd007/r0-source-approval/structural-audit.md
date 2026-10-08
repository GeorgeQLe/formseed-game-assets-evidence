# Structural audit — soft-rounded polish pass 1 (independent read-only auditor)

## Round 1 (draft-a, design_p1-draft-a.py)

AUDIT: soft-rounded polish pass-1 draft (polish-v1/p1-recipe-request.json, sha256 e5e64ff9…5f86; read-only, no MCP calls, no repo writes)

There is no blocker. Checks 1–3 pass. Before dispatching pass 1, I recommend two should-fix changes (S1 and S2 below). The budget allows only 2 passes, and the paired-member objection otherwise survives in p1.

I compared p1 against the selected soft-rounded study request (studies-v1/soft-rounded-recipe-request.json, 4f616cca…, which is the produced and selected r0) and against restrained-bevel (083150b2…). Scripts are in my session scratchpad; nothing was written to the repository.

== 1. CHECKS 1–3: PASS ==
- **Mask fidelity: PASS.**
  - Body (308 px) and shackle (86 px) are identical to the pass3 masks, with 0 duplicate pixels and 0 pixels outside the masks.
  - 60 spans are run-length merged, which is fine because pixels are compared after expansion.
  - The keyhole region is byte-identical to pass3's (spans not merged).
  - The source is identical: dc00a000…, rev 0, fc6c21ca…a829.
  - All roles are flat with tone base, so the change is colour-only and alpha is unchanged.
  - The new recipeId is 14f65e60-0fb5-5108-a172-ae24da0afaa1, with expectedRevision 0 and a new idempotency key.
- **Palette rule: PASS.**
  - Body adds 2 tones (light 194,149,78, hue +2.2°; mid 135,94,44, hue −1.5°). Shackle adds 2 tones (light 154,178,194, +0.0°; mid 81,102,118, +2.0°).
  - All four lie componentwise between their material's shadow and highlight.
  - The theme tones used are body-base, body-highlight, shackle-base and shackle-highlight. body-low is no longer used.
- **maxColors: PASS.** 8 roles plus the keyhole make 9 distinct colours, and maxColors is 9. The theme roles match the declared and used roles exactly, with no duplicate RGB.

== 2. FIX ITEMS (p1 vs selected v1) ==
1. **Narrow and smooth the lit left face: ADDRESSED.**
   - The light face is now 2 px (x5–6) on rows 15–24 and 1 px (x5) on rows 25–27. In v1 it tapered 4/3/2/1/0 across rows 14–27.
   - There is a single 1-px step at (6,24)→(6,25), and the stepped bottom-left corner is gone: (5,27) light meets the row-28 mid at (6,28).
   - The 2-px light left face now mirrors the 2-px mid right band in width.
   - Unchanged: the top row's light still stops abruptly between x18 and x19 (light x6–18, base x19–25). The primary review raised this under pixel discipline (see R5).
2. **Shorten or soften the x7 streak: ADDRESSED.**
   - The 4-px body-highlight streak at (7,16–19) is gone.
   - In its place is a 3-px corner glint at (6,15), (7,15) and (6,16), which is interior and off the contour.
   - Note: the primary evaluation calls this streak "x8". The canonical tone map puts it at x7.
3. **Thin the right dark band to 2 px: ADDRESSED.**
   - x25–26, rows 15–27, are body-mid. The body-low column is removed.
   - No body pixel is darker than #875E2C, so the adversarial acceptance criterion ("no run darker than #875E2C forms a ≥2-px stripe") is met.
4. **Firm edges on the dark background: PARTLY.**
   - Contrast against #202020 improved. The right body edge goes from 1.94 to 2.85 (low replaced by mid). The right-leg outer column x23 goes from 2.72 to 4.55 (mid replaced by base). (22,7) and (22,8) are now base.
   - Still soft:
     - The right body column and bottom row 28 are both body-mid at 2.85; the primary review listed 2.85 as an edge-loss value.
     - The right crown rim (19,5), (20,5), (21,6) is shackle-mid at 2.72, the lowest value on the dark background.
   - Checker is unchanged and was not on the fix list, but the primary review called it "not closed":
     - The left body edge (x5, row 14 x6–18) is body-light at 1.50 against the #C0C0C0 squares (15 px).
     - 23 shackle-base boundary pixels sit at 1.97.
5. **Clean up arch pixels: PARTLY.**
   - Only 8 shackle pixels changed: (13,6) went from base to light, (22,7) and (22,8) from mid to base, and (23,9–13) from mid to base. The isolated base pixel at (13,6) is fixed.
   - Of the speckle the reviewers named, (10,7) light and (13,7), (18,7), (21,6) mid remain. (10,6) base, (12,8) mid and (19,8) mid are also still single-tone pixels.
   - New: the right crown mid rim stops abruptly at (21,6), next to the base pixel at (22,7). That is a 3-px dark fragment.

== 3. REGRESSIONS AND NEW RISKS ==
- **Paired leg and shoulder balance: should-fix (S1).**
  - The legs are not mirror-equivalent. The left leg reads base/light/base/mid (x8–11). The right leg reads mid/base/base/base (x20–23).
  - Together with the base right shoulder ((16–18,5), (18–20,6), (19–22,7), (20–22,8)), the right side forms one undivided base block about 3 px wide down the leg. The left leg is split by the light column at x9.
  - This re-creates the inherited "upper-right shoulder reads as one broad base mass / right fuller" objection, and my earlier N6. It also fails the adversarial acceptance criterion "paired legs and shoulders use mirror-equivalent value structure".
  - Firming the right leg's outer edge for the dark background traded away the fix that had closed N6.
  - Suggested fix:
    - Give both legs mirror structure that keeps the outer edges firm. For example, make the legs s-s-s-n on the left and n-s-s-s on the right: drop the x9 leg light, keep the light ring on the left crown and shoulder only.
    - Either continue the right crown rim through (22,7) and (22,8), or remove it so the crown is mirrored. Lighting can then be carried by the crown and the body.
- **Contrast on dark and checker:** see fix item 4. No outer pixel falls below 2.7 on dark, and none below 1.5 on checker. There is no regression from v1.
- **Remaining stripe-like runs (≥4 px, non-base):**
  - top row 14 light, x6–18 (13 px, abrupt end)
  - left face x5 light, rows 15–27 (13 tall), plus x6 light (8 tall)
  - right band x25–26 mid, 13–14 tall
  - bottom row 28 mid, x6–25 (20 px)
  - crown underside (14–17,6) mid
  - leg columns at x9 (light), x11 and x20 (mid)
  - Right band plus bottom row form a continuous mid L-frame. Nothing is darker than mid, so the "single black stripe" risk is low. The L-frame is the most bevel-like element.
- **Speckle:** reduced but not closed (fix item 5). The new (21,6) rim terminus counts as speckle.
- **Light direction: consistent upper-left.**
  - Body: lit top and left with a glint at top-left, mid on the right and bottom.
  - Shackle: light and highlight on the left and top ring only, with a crown highlight at (13–15,5).
  - The mid on both opening-facing leg edges is a symmetric convention, not a contradiction.

== 4. SOFT-ROUNDED IDENTITY vs DRIFT TO BEVEL: should-fix (S2) ==
Pixel role counts:

| Role | v1 | p1 | bevel |
|---|---|---|---|
| body-base | 197 | 225 | 244 |
| body-light | 48 | 34 | 31 |
| body-mid | 45 | 46 | 33 |
| body-low | 14 | 0 | 0 |
| body-highlight | 4 | 3 | 0 |
| shackle-base | 46 | 52 | 32 |
| shackle-light | 9 | 10 | 10 |
| shackle-mid | 28 | 21 | 44 |
| shackle-highlight | 3 | 3 | 0 |

Differing pixels:

| Pair | Body | Shackle |
|---|---|---|
| p1 vs bevel | 29/308 | 39/86 |
| v1 vs bevel | 73 | 31 |
| v1 vs p1 | 47 | 8 |

- The body has drifted strongly toward the bevel. It is now flat bands (light/base/mid) of uniform 2-px width with no graded ramp (body-low is gone), plus a small glint. Structurally it is a 2-px bevel frame.
- The shackle (tube ramp with left light ring) still separates the two studies.
- The polish authorization requires "keeps the soft-rounded look", so this is a scope-compliance risk.
- Suggested fix: restore some gradation on the body without re-widening the face. For example:
  - Taper the inner light column (x6) and the inner mid column (x25) at the top and bottom so the corners round off, rather than running full height.
  - Optionally make the top-row light fade through a short base or glint transition instead of a hard end at x18/19.
  - Stay within the 2 added tones per material.

== 5. BLOCKERS vs SHOULD-FIX ==
- **Blockers: none.** p1 can be produced as is.
- **Should-fix before dispatch:**
  - S1: leg and shoulder mirror balance, plus the crown rim terminus at (21,6).
  - S2: drift toward the bevel and loss of the soft gradient.
- **Notes for the post-pass reviews:**
  - body right and bottom edges at 2.85 and the crown rim at 2.72 on dark
  - body-light left edge at 1.50 on checker
  - abrupt top-row light end at x18/19
  - residual arch speckle at (10,7), (13,7), (18,7), (19,8), (12,8), (10,6)
  - the mid L-frame as a possible frame or stripe reading
- **Gate status:**
  - technicalValidation (recipe level): pass.
  - visualRecommendation: not assessed (the prior no-go of 56.25 stands until new evidence).
  - humanApproval: absent (direction selected only).


## Round 2 (revised p1, dispatched)

RE-AUDIT: revised soft-rounded p1 (polish-v1/p1-recipe-request.json, sha256 3213d0c6…294c; read-only, no MCP calls, no repo writes)

No blocker. Checks 1–3 pass, S1 is resolved and S2 is partly resolved. The p1 recipe can be dispatched.

== CHECKS 1–3: PASS ==
- **Mask fidelity: PASS.**
  - Body (308 px) and shackle (86 px) are identical to the pass3 masks, with 0 duplicates and 0 pixels outside the masks.
  - 59 spans are run-length merged and were expanded before comparison.
  - The keyhole region is byte-identical to pass3's.
  - The source is identical: dc00a000…, rev 0, fc6c21ca…a829.
  - All roles are flat with tone base, so the change is colour-only and alpha is unchanged.
  - recipeId 14f65e60…, expectedRevision 0 and the idempotency key are unchanged.
- **Palette rule: PASS.** Body adds 2 tones (light, hue +2.2°; mid, hue −1.5°). Shackle adds 2 tones (light, +0.0°; mid, +2.0°). All four lie componentwise between their material's shadow and highlight. body-low is not used.
- **maxColors: PASS.** 8 roles plus the keyhole make 9 distinct colours, and maxColors is 9. Theme roles, declared roles and used roles all match, with no duplicate RGB.

== S1 (leg and shoulder balance): RESOLVED ==
- **Legs:** both legs are now plain and mirror-exact: base/base/base/mid on the left (x8–11) and mid/base/base/base on the right (x20–23), with 0 mirror mismatches on rows 9–13.
- **Outer contour:** all 76 outer pixels are base or the body's edge tones. The shackle's outer contour is base on both sides, and the right crown rim is no longer mid.
- **Shoulders:** they differ from their mirror only by the intended lighting.
  - Left light ring: (11,6), (12,6), (13,6), (10,7), (10,8).
  - Right mid ring: (19,6), (20,6), (21,7), (21,8).
  - Crown highlight (13–15,5) on the left, base on the right.
  - The one non-mirror pixel is (13,6) light against (18,6) base, which is minor.
- **Right shoulder:** the mid ring now partitions it, so it no longer reads as one undivided base mass.

== S2 (soft-rounded identity vs drift toward the bevel): PARTLY RESOLVED, downgraded to a note for review ==
Pixel role counts:

| Role | v1 | p1 | bevel |
|---|---|---|---|
| body-base | 197 | 230 | 244 |
| body-light | 48 | 32 | 31 |
| body-mid | 45 | 43 | 33 |
| body-highlight | 4 | 3 | 0 |
| body-low | 14 | 0 | 0 |
| shackle-base | 46 | 56 | 32 |
| shackle-light | 9 | 5 | 10 |
| shackle-mid | 28 | 22 | 44 |
| shackle-highlight | 3 | 3 | 0 |

Pixels differing in role between each pair:

| Pair | Body | Shackle |
|---|---|---|
| p1 vs bevel | 26/308 (draft-a: 29; v1: 73) | 39/86 |
| p1 vs mostly-flat | 63 | 28 |
| v1 vs p1 | 52 | 20 |

- The body now differs from the bevel by the tapered inner columns: x6 light on rows 17–23 and x25 mid on rows 16–25. It also differs by the corner glint (6,15), (7,15), (6,16) and by the top-row light ending at x17 instead of x23.
- That gives rounded corners and a 2-tone edge, but no value ramp between light, base and mid.
- The shackle has lost its tube shading because the legs are plain. It is now closer to mostly-flat (28 px apart) than to the bevel (39 px apart).
- Much of this convergence follows directly from the authorized fixes (narrower lit face, 2-px right band, firm dark edges), so I don't treat it as a defect. The post-pass reviews must still judge explicitly whether p1 reads as soft-rounded.

== NEW RISKS (no blockers) ==
- **[note, review] Right-shoulder mid line.** The mid ring sits one pixel inside a base outer strip: (21,6), (22,7) and (22,8) are base outside the ring at (21,7) and (21,8). The pattern base/mid/base could read as a dark seam or groove, or as a detached outer strip, especially on dark at 8×. The left side has the same layout but uses light, which reads as a highlight.
- **[note] Speckle.** These single-tone pixels remain: (10,6) and (21,6) base on the outer steps, and (12,8), (13,7), (18,7), (19,8) mid on the opening-facing steps. Most are normal stair connections; the shoulder ones deserve a speckle check.

== UPDATED NOTES FOR POST-PASS REVIEW (native and 8×, on light, dark and checker) ==
1. **Paired legs and shoulders:** confirm neither side reads fuller now that the structure is mirrored. Check the right-shoulder mid line for a seam or detached-strip reading.
2. **Soft-rounded identity against the bevel and mostly-flat studies** (S2): the body is a 2-tone edge with rounded corners and the legs are plain.
3. **Dark background:** the lowest outer contrast is now 2.85, for the body-mid pixels on the right column x26 and bottom row 28. The shackle outer edge is all base at 4.55. Check whether the lower-right body edge still fades.
4. **Checker:** the body-light left edge (x5 and row 14, x6–17; 15 px) is at 1.50 against #C0C0C0, and 26 shackle-base outer pixels are at 1.97. This is the inherited checker objection, still only partly closed.
5. **Stripe-like runs:**
   - top row light x6–17 (12 px), which still ends abruptly at x17/18
   - left edge x5 light (13 tall)
   - right edge x26 mid (13 tall), plus x25 mid (10 tall)
   - bottom row 28 mid (20 px)
   - crown underside (14–17,6) mid
   - leg inner columns x11 and x20 mid
   - Nothing is darker than #875E2C, and the right side plus bottom form a mid L-frame.
6. **Arch speckle** at the pixels listed above.
7. **Light direction:** consistent upper-left throughout. Light is on the body's top and left plus the corner glint; the shackle crown and left shoulder are lit; the right shoulder ring and the right and bottom body edges are mid.

**Gate status:**
- technicalValidation (recipe level): pass.
- visualRecommendation: not assessed. The prior no-go stands until there is new evidence.
- humanApproval: absent.

