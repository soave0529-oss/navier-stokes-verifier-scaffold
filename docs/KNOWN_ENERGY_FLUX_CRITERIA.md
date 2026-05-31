# Known Energy-Flux and Onsager-Adjacent Criteria Registry

Date: 2026-05-19

Status: Step 50 comparison memo complete; Step 52 supersedes the candidate-routing decision.

Scope: compare `lemma_0251`, the exact dyadic LES-flux candidate, against energy-flux,
Onsager, Besov, LES, and cascade-locality literature. This is a known-result comparison note,
not a proof and not a publication-quality literature review.

## Bottom Line

Do not send `lemma_0251` to expert review yet.

Current call after Step 52: `lemma_0251` is `needs_review`, not an active candidate substrate.
The Step 50 call was `candidate_substrate_high_risk` with an `automatic_finiteness_risk` blocker;
Step 51/52 tightened that into a sign/coercivity rewrite requirement.

Reason:

- Dyadic and LES-style energy flux is a heavily studied object in Onsager, anomalous dissipation,
  energy equality, and turbulence-cascade work.
- Existing results usually connect flux control to Besov/Onsager regularity, energy equality, or
  cascade locality, not directly to smooth continuation for 3D Navier-Stokes.
- The current condition controls only a weighted positive part,
  `sum_N N^{-1} integral max(Pi_N^LES,0) dt`. It does not control absolute flux, high-frequency
  energy, enstrophy, vorticity, or a critical Besov norm.
- There is a serious red flag: depending on the exact low-pass energy identity and sign convention,
  the positive-flux time integral may be bounded by already-known energy/dissipation quantities
  strongly enough that the `N^{-1}` dyadic sum is automatic. If automatic, the lemma would be an
  insufficient condition masquerading as a continuation criterion.

## Candidate Being Compared

`lemma_0251` states:

- domain: periodic `T^3`;
- solution class: smooth, divergence-free, mean-zero, zero-force NSE on `[0,T)`;
- low-pass projector: fixed smooth Littlewood-Paley `P_{<=N}`;
- LES stress: `P_{<=N}(u tensor u) - u_{<=N} tensor u_{<=N}`;
- flux:
  `Pi_N^LES(t) = integral grad u_{<=N} : (P_{<=N}(u tensor u) - u_{<=N} tensor u_{<=N}) dx`;
- hypothesis:
  `sum_{dyadic N} N^{-1} integral_0^T max(Pi_N^LES(t),0) dt < infinity`;
- conclusion: smooth continuation past `T`.

Interpretation: this is a frequency-cascade obstruction candidate. It says a singularity must
force enough positive forward flux through dyadic shells to make the weighted flux budget diverge.

## Known Result Anchors

| anchor | relevance to `lemma_0251` |
|---|---|
| Duchon-Robert 1999/2000 | Defines inertial/local energy dissipation defects for weak Euler and Navier-Stokes solutions. This is the local energy-defect side of the same flux vocabulary. |
| Cheskidov-Constantin-Friedlander-Shvydkoy 2008 | Littlewood-Paley energy flux, Onsager threshold, and flux locality for Euler. This is the main dyadic-flux/Besov anchor. |
| Cheskidov-Friedlander-Shvydkoy 2007/2010 | Energy equality for weak 3D NSE under functional-space assumptions. This is energy equality, not smooth continuation. |
| Cheskidov-Luo 2018 | Energy equality for NSE in weak-in-time Onsager spaces; again an energy equality criterion rather than a regularity theorem. |
| Dascaliuc-Grujic 2011 | Energy cascades and flux locality in physical scales for 3D NSE. Useful for cascade diagnostics, not a continuation criterion. |
| Drivas-Eyink 2017/2019 | Onsager singularity theorem for Leray solutions of incompressible NSE in the inviscid limit; relates anomalous dissipation to Besov roughness. This supports the idea that flux is a roughness detector, not automatically a smoothness proof. |
| Cheskidov-Dai 2015/2021 | Littlewood-Paley vorticity regularity criterion with smallness near blow-up time. This is closer to regularity, but it controls dyadic vorticity norms, not the positive LES energy flux budget. |

## Comparison to Onsager/Energy-Equality Criteria

Onsager-adjacent results usually prove one of:

- energy conservation/equality under Besov or fractional regularity;
- locality of energy flux in frequency or physical scales;
- nonzero anomalous dissipation requires roughness below an Onsager threshold;
- partial criteria using dyadic vorticity or velocity norms with smallness.

`lemma_0251` is different. It does not assume a Besov norm and it does not assert energy equality.
It attempts to use positive flux summability itself as a continuation condition.

That is not a known theorem from the anchors above. But the condition may be too weak:

1. Positive-part only: inverse transfer/backscatter and cancellations are discarded.
2. Weighted by `N^{-1}`: the high-frequency requirement may be too forgiving.
3. Flux is not coercive: energy flux can be small while high-frequency gradients or vorticity grow.
4. No pressure or strain/vorticity control is included.
5. If the low-pass energy balance bounds `integral Pi_N^+` uniformly or mildly in `N`, the dyadic
   `N^{-1}` sum is automatically finite and cannot imply smooth continuation by itself.

## Technical Gaps Before Promotion

`lemma_0251` needs an audit before it remains a serious candidate:

- Sign convention: fix whether positive `Pi_N^LES` means forward cascade or backscatter under the
  project definition. The Track B smoke run had zero positive flux under the current convention.
- Low-pass energy identity: derive the exact identity for
  `0.5 ||u_{<=N}||_2^2`, viscous dissipation, and `Pi_N^LES`.
- Automatic-finiteness check: prove or disprove whether
  `sum_N N^{-1} integral Pi_N^+ dt < infinity` follows from the standard energy inequality on
  `[0,T)`.
- Coercivity check: identify what norm or concentration quantity this flux budget actually
  controls. If it controls only energy transfer bookkeeping, downgrade the lemma.
- Known-result separation: state exactly how the condition is not just a weak form of a Besov
  `B^{1/3}_{3,*}` or energy-equality criterion.

## Project Decision

Step 51/52 update:

- `docs/LEMMA_0251_FLUX_BALANCE_AUDIT.md` derived the low-pass balance and sign convention.
- `track-a-regularity/evaluator/checks/flux_balance_risk.py` now marks `lemma_0251` as
  non-failing `needs_review`.
- Do not contact experts with this statement.
- Rewrite with sign-corrected forward flux and an explicit coercive bridge before any proof
  attempt or external review.

## Source Pointers

- Duchon and Robert, "Dissipation d'energie pour des solutions faibles des equations d'Euler et
  Navier-Stokes incompressibles":
  <https://www.numdam.org/item/SEDP_1999-2000____A13_0/>
- Cheskidov, Constantin, Friedlander, and Shvydkoy, "Energy conservation and Onsager's conjecture
  for the Euler equations":
  <https://arxiv.org/abs/0704.0759>
- Cheskidov, Friedlander, and Shvydkoy, "On the energy equality for weak solutions of the 3D
  Navier-Stokes equations":
  <https://arxiv.org/abs/0704.2089>
- Cheskidov and Luo, "Energy equality for the Navier-Stokes equations in weak-in-time Onsager
  spaces":
  <https://arxiv.org/abs/1802.05785>
- Dascaliuc and Grujic, "Energy cascades and flux locality in physical scales of the 3D
  Navier-Stokes equations":
  <https://arxiv.org/abs/1101.2193>
- Drivas and Eyink, "An Onsager Singularity Theorem for Leray Solutions of Incompressible
  Navier-Stokes":
  <https://arxiv.org/abs/1710.05205>
- Cheskidov and Dai, "Regularity criteria for the 3D Navier-Stokes and MHD equations":
  <https://arxiv.org/abs/1507.06611>
