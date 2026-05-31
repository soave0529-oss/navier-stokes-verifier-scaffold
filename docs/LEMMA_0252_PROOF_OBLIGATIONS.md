# Lemma 0252 Proof-Obligation Breakdown

Date: 2026-05-19

Status: Step 53 proof-obligation memo complete; Step 54 evaluator metadata added.

Scope: decompose what would be required to promote `lemma_0252`, the exact parabolic Morrey
localized-enstrophy candidate, beyond a high-risk substrate. This is not a proof and not a
Navier-Stokes solution claim.

## Candidate

`lemma_0252` assumes a smooth divergence-free mean-zero zero-force 3D periodic NSE solution on
`[0,T)` and defines

```text
Q_r(x0,t0) = B_r(x0) x (t0 - r^2, t0),
E_r(x0,t0) = r^{-1} integral_{Q_r(x0,t0)} |curl u|^2 dx dt.
```

It claims:

```text
sup_{x0,t0,r} E_r(x0,t0) < infinity -> u extends smoothly past T.
```

The quantity is scale-critical. Finite boundedness is materially different from the epsilon
smallness conditions used in CKN-type regularity criteria.

## Bottom Line

No bounded finite-to-smallness route is currently identified.

`lemma_0252` should stay blocked from expert review unless the project can supply one of two
missing mechanisms:

1. a compactness/Liouville theorem excluding finite-time singular blow-up limits with bounded
   scale-critical local enstrophy, or
2. an added smallness/pressure/velocity package that turns the statement into a precise known-style
   epsilon-regularity criterion.

The first route would be genuinely hard and may be close to the original problem. The second route
is likely known/redundant. Therefore the current statement is not expert-ready as a continuation
criterion.

## Obligation 0 — Cylinder Admissibility

The statement currently says `0 < r <= 1` and `0 < t0 < T`, then integrates over
`(t0 - r^2, t0)`.

Before proof work, the candidate must choose one convention:

- require `r^2 <= t0`, so the backward cylinder lies inside the time domain;
- use an initial-time truncated cylinder and prove the scaling change is harmless;
- restrict the supremum to terminal cylinders near `T`, if the goal is only blow-up exclusion.

Without this, the statement is under-specified near `t=0`.

## Obligation 1 — Local Vorticity to CKN Quantities

CKN-style epsilon criteria use localized velocity, pressure, and dissipation quantities. A local
vorticity enstrophy envelope alone does not directly give those quantities on a ball.

Needed bridge:

```text
r^{-1} integral_{Q_r} |omega|^2
  -> local gradient/dissipation control with cutoffs
  -> local velocity and pressure quantities used by epsilon regularity
```

Obstacles:

- Localizing `||grad u||_2` from `||curl u||_2` introduces cutoff and lower-order terms.
- On balls, the divergence-free/curl identity has boundary and harmonic-part terms.
- Periodic global structure helps globally, but the CKN mechanism is local.

## Obligation 2 — Pressure Control

The candidate has no pressure hypothesis.

For NSE,

```text
-Delta p = partial_i partial_j (u_i u_j)
```

so local pressure estimates are nonlocal and normally require velocity control, Calderon-Zygmund
decomposition, or explicit pressure terms. A proof must either:

- derive the required pressure quantity from the local enstrophy envelope plus a velocity/local
  energy bound, or
- add a pressure/local-energy hypothesis and accept that the result becomes a known-style
  epsilon-regularity statement rather than a new finite-envelope criterion.

## Obligation 3 — Finite Bound to Smallness

The main gap is:

```text
sup E_r <= M
```

does not imply that any particular cylinder has

```text
E_r < epsilon_CKN
```

near a hypothetical singular point. Boundedness allows the same non-small critical mass to persist
across every dyadic scale.

A valid proof route must show one of:

- a monotonicity or decay mechanism that converts finite critical local enstrophy into smallness at
  sufficiently small scales;
- an improved integrability/self-improvement result that lowers the effective critical quantity;
- a contradiction if a singular point has uniformly bounded but non-small local enstrophy.

No such mechanism is present in the current candidate.

## Obligation 4 — Blow-Up Compactness and Liouville Branch

The non-smallness route would likely require rescaling at a terminal singular point. The invariant
bound would pass to a limit:

```text
u_k(x,t) = lambda_k u(x0 + lambda_k x, T + lambda_k^2 t)
```

and the limit would be an ancient suitable object with bounded scale-critical local enstrophy.

To finish the proof, the project would need a Liouville/backward-uniqueness theorem of the form:

```text
nonzero ancient NSE profile
  + bounded local enstrophy Morrey envelope
  + suitable/local-energy structure
  -> impossible or smooth enough to contradict singular rescaling
```

This is the hard branch. ESS-type backward uniqueness results are a comparison anchor, but the
current candidate does not supply the same hypotheses.

## Obligation 5 — Smooth Continuation Bridge

Even if all terminal points are regular in a partial-regularity sense, the target conclusion is
smooth continuation past `T` for a classical solution.

Needed bridge:

```text
no singular point at time T
  -> uniform local regularity up to T
  -> bounded high Sobolev norm or Serrin/BKM control near T
  -> classical continuation past T
```

The proof must keep these classes distinct:

- smooth classical solution on `[0,T)`;
- Leray-Hopf weak solution;
- suitable weak solution satisfying local energy inequality;
- ancient blow-up limit.

No weak-to-smooth upgrade can be used without naming the exact theorem and hypotheses.

## Obligation 6 — Formalization Target

The current Lean file `NavierStokesProgram/ParabolicCylinder.lean` is finite vocabulary only. It
does not formalize:

- balls on the periodic quotient;
- curl/vorticity;
- local pressure;
- local energy inequality;
- supremum over all centers, times, and radii;
- compactness or continuation.

The next formal target should stay small: encode the admissible-cylinder convention and a record of
the proof-obligation graph, not the CKN theorem.

## Decision

Project call:

```text
lemma_0252:
  current: candidate_substrate_high_risk
  promotion gate: blocked_pending_compactness_or_smallness_mechanism
```

Do not send `lemma_0252` to experts as a possible continuation theorem.

Acceptable next moves:

1. Downgrade to evaluator `needs_review` until a compactness/Liouville branch is supplied.
2. Rewrite the lemma with epsilon smallness plus pressure/local-energy quantities, knowing it is
   likely a known-result restatement.
3. Keep the current statement only as a research-question substrate and build a separate
   compactness/Liouville checklist.

## Next Action

Step 54 encoded this decision in the public registries and evaluator metadata using non-failing
`review` status, not `fail`, because this memo identifies missing proof mechanisms rather than a
contradiction.

Evaluator hook: `track-a-regularity/evaluator/checks/parabolic_morrey_obligation.py` now marks
`lemma_0252` as evaluator `needs_review`.
