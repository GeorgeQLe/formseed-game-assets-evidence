# Independent authored rear-grille review

Reviewed r35 checkpoint `03fadf3c65771dd87786c008db2a9a327696ca553622b0e2d5548f084f8030f2`, actual review GLB SHA-256 `bfb4388f9601f010adf7d30e9ca70c089d02387ad09e643ddd8fe01899fce0f3`. Read-only producer review; no source mutation. All six native image hashes match `candidate-render.json`, which binds revision 35 and this checkpoint.

## Observations recorded before geometry/recipe checks

- Rear: two rectangular panels of repeated vertical slats now occupy the formerly blank lower rear face. A substantial center web divides them, an upper bar caps them, and their edges read as attached to the body rather than floating strips. Slats remain individually legible in the supplied native view.
- Front: broad simplified hull, sloping turret shoulders, central gun opening and basket edge remain visible; no new protrusion appears around the front silhouette.
- Physical left: rising aft turret underside and long open basket rail remain distinct. The rear grille presents only a thin aft edge. No return of the rejected lower aft shelf is visible.
- Physical right: the same rising underside persists. Basket rails remain low contrast against the armor, as in the prior candidate; the rear extension is thin.
- Top: open rear/side basket and existing turret/roof contours remain apparent. The grille has no conspicuous new plan footprint beyond a thin rear edge.
- Three-quarter: open basket, turret, gun and hull retain their existing relationships. This forward viewpoint largely hides the new grille and therefore does not independently establish rear detail quality.

These observations were sent to the parent before comparing the authored export to the recipe.

## Reference and prior-candidate challenge

Directly inspected retained USMC `crop-20.png` and the native r34 rear image. The reference supports a broad, divided grille footprint, vertical rhythm, center division and upper horizontal boundary. r34 lacked that readable feature; r35 supplies it without changing the accepted basket/turret direction. The simplified twelve slats per half, 22 mm slat width, shallow backing and frame construction are declared design choices, not historical measurements. The diagram's detailed hinges, fasteners and other fittings are not reproduced by this bounded correction. No retained rear photograph is claimed as corroboration.

The added panels are visually modest relative to the whole tank and readable at this native render scale. No obvious z-fighting, detached slat, broken center join or new underside/roof regression is visible. The lower outer approximately 80 mm overhang beyond the narrower lower hull remains an intentional supported panel extension; the continuous backing and upper attachment provide support. This is not evidence of exact engine hardware or working ventilation. Flat neutral rendering limits assessment of fine relief and finish.

## Independent authored checks

- Loaded the actual exported GLB and verified its bytes against the receipt SHA-256.
- All 57 pre-existing r34 meshes have exactly equal reconstructed world-coordinate vertices, faces and face materials. This includes all five basket parts, complete rising floor, gun and hull; no geometric sibling regression was found.
- Exactly two meshes were added: `rear-grille-l` and `rear-grille-r`, both parented to `hull`, each with 204 triangles. Their float32 vertex sets exactly match the prepared proposal.
- Actual combined bounds are X−7.9498000 to−7.9148002, Y±1.1000000, Z0.83999997 to1.38999999 m. This implements the approximately 25 mm aft relief and 10 mm mounting-plane overlap, rather than an unchanged overall X bound.
- Actual total is 16,752 triangles, including the 408 added triangles, below the 20,000 limit. Independent proposal topology/overlap checks are retained in `recipe-review.md`; complete native isolation and motion validation remain the parent's separate checks.

## Recommendation and gate separation

**Recommend scoped retention of r35's rear-grille correction**, conditional on the separate native validation, isolation and motion checks passing. No visual defect found here warrants restoration. This recommendation covers the approved missing-feature correction only; it does not close the remaining cross-view trace uncertainty or establish a qualified finished Abrams model.

- **technicalValidation:** independent image/GLB hash checks, actual vertex-set correspondence, exact preservation of 57 existing meshes, parent mapping and triangle budget passed. Complete native validation and moving-clearance results are separate evidence.
- **visualRecommendation:** retain this bounded reference-informed addition; whole-model visual recommendation remains **no-go** pending the complete required dimension/style/rubric evidence and unresolved broader targets. No numerical score or overall visual go is inferred.
- **humanApproval:** requester authorization to make the rear-grille correction was reported by the parent. No approval of the resulting r35 model, finishing, promotion or integration is inferred from that authorization or this independent review.
