# Known Local Enstrophy and Parabolic Morrey Criteria Registry

Date: 2026-05-19

Status: Step 49 comparison memo complete; Step 54 evaluator metadata added.

Scope: compare `lemma_0252`, the exact parabolic Morrey enstrophy candidate, against
CKN/ESS/local-enstrophy and local-Morrey regularity criteria. This is a known-result
comparison note, not a proof and not a publication-quality literature review.

## Bottom Line

Do not send `lemma_0252` to expert review yet.

Current call after Step 54: `lemma_0252` is non-failing evaluator `needs_review`, not an active
candidate and not a known-overlap failure. Step 53 refined the promotion gate to
`blocked_pending_compactness_or_smallness_mechanism`.

Reason:

- The candidate quantity
  `sup_{x0,t0,r} r^{-1} integral_{t0-r^2}^{t0} integral_{B_r(x0)} |omega|^2`
  is scale-critical and directly adjacent to CKN/local-energy vocabulary.
- Existing partial-regularity theory uses smallness, pressure, local energy inequality, and
  suitable weak-solution structure. The current candidate assumes only finite scale-critical
  local enstrophy for a smooth solution up to `T` and concludes smooth continuation.
- A finite critical envelope is not the same as an epsilon-regularity smallness hypothesis.
  If this statement is true, the missing theorem is a nontrivial blow-up obstruction:
  every finite-time singularity would have to make this local enstrophy envelope unbounded.

## Candidate Being Compared

`lemma_0252` states:

- domain: periodic `T^3`;
- solution class: smooth, divergence-free, mean-zero, zero-force NSE on `[0,T)`;
- cylinder: `Q_r(x0,t0) = B_r(x0) x (t0-r^2,t0)`;
- localized enstrophy concentration:
  `E_r(x0,t0) = r^{-1} integral_{Q_r(x0,t0)} |curl u|^2`;
- hypothesis: `sup E_r < infinity`;
- conclusion: smooth continuation past `T`.

Interpretation: this is a Type-I-like scale-critical local enstrophy continuation criterion.
It is not a CKN theorem as written, because it asks for boundedness rather than smallness.

## Known Result Anchors

| anchor | relevance to `lemma_0252` |
|---|---|
| Caffarelli-Kohn-Nirenberg 1982 | Partial regularity for suitable weak solutions; singular set has zero parabolic 1-dimensional Hausdorff measure. This supplies the main local-energy and parabolic-cylinder vocabulary, but not a global finite-envelope continuation theorem. |
| Lin 1998 | New proof of the CKN theorem; useful as a cleaner proof route if the project later formalizes local partial-regularity vocabulary. |
| Escauriaza-Seregin-Sverak 2003/2004 | Endpoint critical velocity criterion via backward uniqueness. This is a different critical norm family (`L^infty_t L^3_x` / `L_{3,infty}`-style vocabulary), so it is a comparison anchor rather than a direct match. |
| Seregin scale-invariant quantities / Type-I literature | Shows that bounded scale-invariant quantities are a recognized local-regularity theme. It also warns that bounded critical quantities alone need exact hypotheses and often do not automatically resolve the general problem. |
| Grujic-Xu 2019 | Local Morrey regularity with an epsilon smallness condition and dynamic lower scale. This is close in spirit, but the smallness and velocity/Morrey structure differ from `lemma_0252`. |
| Barker-Prange 2021 | Quantitative regularity via spatial concentration and Type-I bounds; relevant to what must concentrate near singularity, but not a direct proof of finite local-enstrophy envelope regularity. |

## Comparison to CKN-Type Epsilon Regularity

CKN-style criteria are local and smallness-based. A typical proof structure controls scaled local
velocity, pressure, and dissipation quantities on a parabolic cylinder; if the scale-normalized
quantity is below a universal threshold, the point is regular.

`lemma_0252` differs in four material ways:

1. It has boundedness, not smallness.
2. It uses local vorticity enstrophy only, not a full local pressure/velocity package.
3. It starts from smooth classical solutions on `[0,T)`, not suitable weak solutions with local
   energy inequality.
4. It asserts continuation past a terminal time, not partial regularity away from a small singular
   set.

Therefore the candidate should not be marked as a CKN restatement. It should remain blocked from
expert review until the missing finite-bound-to-regularity mechanism is isolated.

## Technical Gaps Before Promotion

`lemma_0252` needs at least the following proof obligations before it becomes expert-review ready:

- Local vorticity-to-gradient bridge: on periodic balls, specify exactly how local `|omega|^2`
  controls the local gradient energy used by CKN-style estimates, including cutoff and harmonic
  or lower-order errors.
- Pressure control: either add a pressure hypothesis or derive the local pressure quantity needed
  for epsilon regularity from the enstrophy envelope plus smooth periodic structure.
- Smallness mechanism: explain how finite `sup E_r <= M` yields a scale with epsilon-small CKN
  quantity near a hypothetical singular point, or prove a compactness/Liouville theorem for a
  bounded-envelope blow-up limit.
- Solution-class bridge: keep smooth classical, Leray-Hopf, and suitable weak conclusions
  separate. Do not use weak partial-regularity theorems as if they were smooth continuation
  theorems without an explicit bridge.

## Project Decision

For now after Step 54:

- keep `lemma_0252` as non-failing `needs_review`, not an active candidate;
- preserve the `candidate_substrate_high_risk` research note only as historical context;
- do not add an evaluator fail hook from this memo alone;
- do not contact experts with this statement yet;
- require a compactness/Liouville branch or epsilon/pressure/local-energy rewrite before
  promotion.

Step 53 update:

- `docs/LEMMA_0252_PROOF_OBLIGATIONS.md` found no bounded finite-to-smallness route.
- The candidate now needs either a compactness/Liouville branch or an epsilon-smallness rewrite
  with pressure/local-energy quantities.
- Step 54 encoded this as non-failing evaluator `needs_review`, not `fail`.

## Source Pointers

- Fefferman Clay problem statement, with CKN/partial-regularity summary:
  <https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf>
- Caffarelli, Kohn, and Nirenberg, "Partial regularity of suitable weak solutions of the
  Navier-Stokes equations", Comm. Pure Appl. Math. 35 (1982), 771-831:
  <https://doi.org/10.1002/cpa.3160350604>
- Lin, "A new proof of the Caffarelli-Kohn-Nirenberg theorem", Comm. Pure Appl. Math. 51
  (1998), 241-257:
  <https://doi.org/10.1002/(SICI)1097-0312(199803)51:3%3C241::AID-CPA1%3E3.0.CO;2-A>
- Escauriaza, Seregin, and Sverak, "On L 3,Infinity-solutions to the Navier-Stokes equations
  and backward uniqueness":
  <https://hdl.handle.net/11299/3858>
- Escauriaza, Seregin, and Sverak, "On Backward Uniqueness for Parabolic Equations":
  <https://doi.org/10.1023/B:JOTH.0000041475.11233.d8>
- Grujic and Xu, "A Regularity Criterion for Solutions to the 3D NSE in Dynamically Restricted
  Local Morrey Spaces":
  <https://arxiv.org/abs/1903.03833>
- Barker and Prange, "Quantitative Regularity for the Navier-Stokes Equations Via Spatial
  Concentration":
  <https://doi.org/10.1007/s00220-021-04122-x>
