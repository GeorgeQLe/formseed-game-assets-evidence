# Independent shoulder-cleanup whole-form review — r38

Checkpoint `d2236645f11cf33a2847ee59475e40df8ba93f7b6585e313991f6fc6954427b4`; actual GLB SHA-256 `a57611bc734b8e4e46501886988fee8ebe77bbdfd0cc9802c07c07178365abee`; native render-set receipt hash `46013a5aa33137a5559a99831775c6988249fb194fc860abf947eb7be00b468d`. Read-only review; inspected six clean native frames before comparison annotations or numerical junction evidence.

## Neutral observations

- Top: the shoulder perimeter looks cleaner; the small pale protruding strip seen in r37 is reduced. The broad roof and descending oblique forward correction retain their shape.
- Three-quarter: the broad roof-to-shoulder relationship remains coherent. No conspicuous new shelf, detached strip or open gap appears at the native viewing scale.
- Front: gun opening, cheek shoulders and outer silhouette retain their prior relationship, with no new high projection.
- Rear: basket, rear armor and divided grille retain their appearance.
- Physical left: rising floor/underside, upper slope, basket and hull ramp remain intact; no new lower shelf is visible.
- Physical right: silhouette and accepted aft relationships remain intact. Some basket rails remain low contrast against armor, as before.

## Comparison and limitations

Relative to r37, this is a small local cleanup rather than a redesign. The prior approximately8.835 mm protruding shoulder lip is no longer apparent as a raised strip. The checked junction evidence reports its removal; native appearance supports retaining that improvement.

This does **not** establish a uniformly flush roof/armor join. The pre-existing negative-side roof-edge drop deepens by approximately13.412 mm near X−3.92,Y−1.247 and10.922 mm near X−3.8,Y−1.226, as identified by the independent local geometry audit. At the supplied native scale this does not read as a new major shelf or gap, but it remains an explicit local surface tradeoff. It must not be described as all seams being repaired or all adjacent surfaces now being continuous. Flat neutral lighting limits fine seam assessment.

The comparison correctly distinguishes gray uncertainty/unassessed spans, green assessed lateral agreement and blue actual model boundaries. The entire roof is unchanged, so the earlier sampled lateral trace result is preserved; central gun-adjacent and stowage correspondence remain unassessed. The local lip check does not grant broader contour closure or whole-model qualification.

Inspected the updated semantic comparison after its visible tradeoff caption was added. The11–13 mm deeper existing edge is now disclosed directly on the sheet; the red defect marker appears only in the r37 row. Green is explicitly limited to sampled lateral agreement, while the central continuation stays unassessed. No semantic blocker found for this comparison. The parent separately reports native verification and actual motion validation passed; their records remain authoritative for those checks.

## Independent identity and preservation checks

All six PNG byte hashes match `candidate-render.json`, whose checkpoint matches the reviewed r38 pin. The actual GLB bytes match the export receipt. Comparing reconstructed world vertices, faces and face materials to r37 finds changes only in `redo-cheek-l`, `redo-cheek-r` and `redo-turret-bustle`; the other56 meshes are exact, including the entire roof, floor, gun, basket and grille. Actual mesh count remains59 and triangle count16,788.

Verified native image SHA-256 values:

| View | SHA-256 |
| --- | --- |
| physical-left | `4b0e50de28eb7473e0e319e81d8608eb6a9a633a068acc9140de05d19fc8eaa8` |
| physical-right | `72acb7e3d90fd97b9772b2137542a99cce3ba0db3fcd70bb96e04a66c206df86` |
| front | `d2fd88464b5167318d0d42a8810604abd1df59cabce2dbc91102adfa389f8561` |
| rear | `75162d44318d4bf1b5343201fc61b36e1944dc56543162ed59868c4ee474bd9f` |
| top | `b7ea30c439e176039da32d21ee882f5a6af30c11e496826333809b8966689851` |
| three-quarter | `792cb5c428233f7fc420da0fd52f84c2a9c48562acca8de8514cd0dda3078ba6` |

## Recommendation

**Recommend scoped retention of r38's shoulder cleanup**, conditional on separate current-checkpoint technical validation, native isolation and motion checks passing. The visible local lip improves, the accepted roof and assembly relationships remain, and no new major regression in the six native views warrants restoration. The deeper pre-existing negative roof-edge drop remains disclosed above; retention is appropriate for this stage of approximate form development, not a claim of zero defects.

- **technicalValidation:** independent PNG/GLB identity,56-mesh preservation and counts passed. Full recipe realization, junction, native isolation and motion checks remain separate evidence.
- **visualRecommendation:** retain the bounded cleanup; whole-model final visual recommendation remains **no-go/unqualified** pending complete required evidence and remaining broader targets. No numerical visual score is assigned.
- **humanApproval:** task authorization does not imply approval of the resulting r38 model, finishing, promotion or integration.
