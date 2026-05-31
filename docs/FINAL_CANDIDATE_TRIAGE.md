# Final Candidate Triage Before Expert Review

Date: 2026-05-19

Status: Step 55 Duhamel formal-only evaluator metadata added.

Scope: classify the remaining candidates after Step 55. This is not an expert-review
packet and not a proof.

## Current Remaining Candidates

After Step 55:

| id/family | count | current call |
|---|---:|---|
| critical Duhamel bilinear variants `0209/0219/0229/0239/0249` | 5 | needs review, formal-only |
| exact parabolic Morrey `0252` | 1 | needs review, blocked pending compactness/smallness mechanism |
| exact dyadic flux `0251` | 1 | needs rewrite before review, not active candidate |

Distribution:

| status | count |
|---|---:|
| `falsified` | 227 |
| `known_control` | 12 |
| `known_control_with_extra_assumption` | 6 |
| `needs_review` | 7 |
| `candidate` | 0 |

## Calls

### Critical Duhamel Bilinear Variants

Representative ids: `0209/0219/0229/0239/0249`.

Call: `needs_review`, `formal_only`.

Reason:

- The current statement says only "mild Duhamel bilinear term stays bounded in a critical
  space-time norm".
- Without exact bilinear operator, Leray projection, time integral, target space, and critical
  indices, this is too broad to be a candidate theorem.
- Step 46 already extracted the useful part into `NavierStokesProgram/DuhamelBilinear.lean`.
- Step 55 marks the five variants as evaluator `needs_review`.

Next action:

- Do not send to experts.
- Keep as Track C vocabulary until exact function spaces are selected.
- If promoted later, require a statement closer to a known mild-solution estimate, not a bare
  continuation criterion.

### Exact Dyadic Flux Candidate

Representative id: `lemma_0251`.

Call: `needs_rewrite_before_review`.

Reason:

- This is one of the few exact rewrites: shell projector, LES flux, positive part, alpha=1, dyadic
  summability, and time norm are specified.
- It has Track B diagnostic support and Track C finite shell vocabulary.
- Step 51 derived `Pi_N^project = dE_N/dt + nu D_N`; under this convention positive flux feeds
  resolved low-pass energy, while the usual forward subgrid flux has the opposite sign.
- The signed time integral is energy-controlled, but the positive-part dyadic budget is not a
  coercive bridge to enstrophy, BKM, pressure, or a critical Besov norm.

Next action:

- Step 50 added `docs/KNOWN_ENERGY_FLUX_CRITERIA.md`.
- Step 51 added `docs/LEMMA_0251_FLUX_BALANCE_AUDIT.md`.
- Step 52 marks `lemma_0251` as evaluator `needs_review`.
- Rewrite with sign-corrected forward flux and an explicit coercive bridge before expert review.
- Use Track B `Pi_N^LES` diagnostics only as falsifier pressure, never as proof.

### Exact Parabolic Morrey Candidate

Representative id: `lemma_0252`.

Call: `needs_review`, blocked from expert review.

Reason:

- This is an exact rewrite: periodic cylinder, beta=1, localized enstrophy, supremum domain, and
  smooth solution class are specified.
- It has Track C finite parabolic-cylinder vocabulary.
- But beta=1 local enstrophy concentration is close to CKN/ESS/local-energy partial-regularity
  vocabulary. Current project has not separated it from known criteria.

Next action:

- Step 49 added `docs/KNOWN_LOCAL_ENSTROPHY_CRITERIA.md`.
- Step 53 added `docs/LEMMA_0252_PROOF_OBLIGATIONS.md`.
- Step 54 marks `lemma_0252` as evaluator `needs_review`.
- Keep blocked from expert review until a finite-bound-to-smallness or compactness/Liouville
  mechanism is isolated. No such route is currently identified.
- Do not pitch it as a smooth continuation theorem until weak/suitable-weak and smooth-class
  implications are explicitly separated.

## Expert Review Gate

Do not contact experts yet.

Minimum gate for expert contact:

1. `lemma_0251` is removed from expert routing until a sign-corrected coercive rewrite exists.
2. `lemma_0252` is removed from expert routing until the Step 53 compactness/smallness blocker is
   resolved or the statement is rewritten.
3. Critical Duhamel family is removed from active candidate status; rewrite only with exact
   function spaces and a known mild-estimate route.

## Next Step

No candidate is expert-ready. Step 56 should decide the next generation path: exact mild-estimate
rewrite, new candidate round with stricter generator constraints, or Track C infrastructure.
