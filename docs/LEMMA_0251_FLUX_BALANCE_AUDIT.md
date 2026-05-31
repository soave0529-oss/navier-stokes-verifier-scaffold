# Lemma 0251 Flux-Balance Audit

Date: 2026-05-19

Status: Step 51 audit complete.

Scope: audit the low-pass energy identity behind `lemma_0251` and decide whether the weighted
positive-flux hypothesis is automatic, sign-correct, and potentially coercive. This is not a proof
of regularity.

## Bottom Line

`lemma_0251` should be downgraded from active expert-review substrate to
`needs_rewrite_before_review`.

Decision:

- The hypothesis is not obviously automatic from the standard global energy inequality alone.
- But the current sign convention is backwards for the usual forward-cascade interpretation.
- Even after correcting the sign, the weighted positive-flux budget is noncoercive: it does not
  directly control high-frequency energy, enstrophy, vorticity, or a critical Besov norm.
- Therefore `lemma_0251` should not be treated as a plausible continuation criterion until it is
  rewritten with a sign-corrected flux and an explicit coercive bridge.

This keeps the Track B/Track C flux vocabulary useful as diagnostics, but blocks the current
candidate statement from expert review.

## Setup

Let `P = P_{<=N}` be a self-adjoint Fourier low-pass projector on `T^3` that commutes with spatial
derivatives and preserves divergence-free vector fields.

Define:

```text
u_N = P u
tau_N = P(u tensor u) - u_N tensor u_N
Pi_N^project = integral_{T^3} grad u_N : tau_N dx
```

The project candidate `lemma_0251` uses `Pi_N^project` and assumes:

```text
sum_{dyadic N} N^{-1} integral_0^T max(Pi_N^project(t), 0) dt < infinity.
```

## Low-Pass Energy Identity

Start from periodic incompressible NSE in divergence form:

```text
partial_t u + div(u tensor u) + grad p = nu Delta u,
div u = 0.
```

Apply `P`:

```text
partial_t u_N + div P(u tensor u) + grad Pp = nu Delta u_N.
```

Using `P(u tensor u) = u_N tensor u_N + tau_N`:

```text
partial_t u_N + div(u_N tensor u_N) + grad Pp
  = nu Delta u_N - div tau_N.
```

Dot with `u_N` and integrate over the torus. The low-low transport term and pressure term vanish
by periodicity and `div u_N = 0`. The remaining identity is:

```text
d/dt (1/2 ||u_N||_2^2)
  = - nu ||grad u_N||_2^2 + integral grad u_N : tau_N dx.
```

Thus:

```text
Pi_N^project(t)
  = d/dt E_N(t) + nu D_N(t),

where
E_N(t) = 1/2 ||u_N(t)||_2^2,
D_N(t) = ||grad u_N(t)||_2^2.
```

## Sign Convention

Under the identity above, positive `Pi_N^project` feeds the resolved low-pass energy after
viscous loss:

```text
dE_N/dt + nu D_N = Pi_N^project.
```

In common LES/Onsager language, the forward subgrid flux from resolved modes to unresolved modes is
usually the opposite sign:

```text
Pi_N^forward = - integral grad u_N : tau_N dx
             = - Pi_N^project.
```

Therefore the current candidate's positive part,

```text
max(Pi_N^project, 0),
```

is naturally a positive backscatter or low-mode-feeding envelope, not a forward-cascade envelope.
The Step 37 Track B smoke diagnostic also recorded zero positive flux under this convention, which
is consistent with a sign-convention ambiguity rather than evidence for regularity.

## Automatic-Finiteness Check

The standard energy inequality gives:

```text
E(t) + nu integral_0^t ||grad u||_2^2 ds <= E(0).
```

Because `P` is an `L^2` contraction:

```text
0 <= E_N(t) <= E(t),
D_N(t) <= ||grad u(t)||_2^2.
```

This yields a signed integral bound:

```text
integral_0^t Pi_N^project ds
  = E_N(t) - E_N(0) + nu integral_0^t D_N ds
  <= E(0) + nu integral_0^t ||grad u||_2^2 ds
  <= 2 E(0).
```

However, this is a bound on the signed time integral. It does not bound

```text
integral_0^t max(Pi_N^project, 0) ds
```

because positive and negative flux oscillations can cancel in the signed identity.

For each fixed finite `N`, smoothness on compact subintervals gives finite flux integrals, and
basic Bernstein estimates can give `N`-dependent bounds. But those bounds grow with `N`; they do
not imply:

```text
sum_{dyadic N} N^{-1} integral_0^T max(Pi_N^project, 0) dt < infinity.
```

Conclusion: the condition is not currently proven automatic from the standard energy inequality
alone. The automatic-finiteness risk remains open in the strong form, but the signed identity
shows that the candidate is mainly energy-transfer bookkeeping unless it controls a coercive
quantity.

## Coercivity Failure

Even if the weighted positive part is finite and nonautomatic, it does not by itself give an
obvious route to smooth continuation.

Missing coercive bridges:

- No bound on `sum_N N^2 ||Delta_N u||_2^2` or enstrophy.
- No bound on a critical Besov norm such as `L^3_t B^{1/3}_{3,*}`.
- No BKM-type control of `integral ||omega||_infty dt`.
- No pressure or strain/vorticity control.
- No monotonicity: flux can be small because transfer cancels or because the chosen sign sees
  backscatter, while high-frequency gradients still grow.

The identity

```text
Pi_N^project = dE_N/dt + nu D_N
```

does contain `D_N`, but only after subtracting the time derivative of low-pass energy. The positive
part of `Pi_N^project` does not isolate `D_N` and cannot be used as an enstrophy bound without
additional variation control on `E_N`.

## Decision for Project State

Update the project classification:

```text
lemma_0251:
  previous: candidate_substrate_high_risk
  new call: needs_rewrite_before_review
```

This is not a falsifying evaluator failure. Step 52 adds a non-failing evaluator metadata check
that reports `lemma_0251` as `needs_review` because it has exact definitions but carries the
sign/coercivity risk documented here.

Human-facing docs should no longer list `lemma_0251` as expert-review-ready substrate. It is a
diagnostic/formal vocabulary item until rewritten.

## Rewrite Requirements

A future replacement should:

1. Choose sign explicitly:

   ```text
   Pi_N^forward = - integral grad u_N : tau_N dx.
   ```

2. Decide positive part:

   ```text
   max(Pi_N^forward, 0)
   ```

   if the intent is forward cascade, or use absolute flux if cancellations are the obstruction.

3. Replace the weak `N^{-1}` weighted budget with a quantity tied to a known coercive norm, such as
   a precise Besov, vorticity, spectral-tail, or dissipation-wavenumber envelope.

4. Prove a bridge:

   ```text
   flux hypothesis -> critical norm control or BKM-style control -> smooth continuation
   ```

   or explicitly state it as a diagnostic-only falsifier, not a theorem candidate.

## Next Action

Step 52 updated the public candidate registries and evaluator metadata so `lemma_0251` is no
longer treated as a serious candidate without this rewrite.

Recommended bounded implementation:

- `track-a-regularity/PASSED.md`;
- `docs/FINAL_CANDIDATE_TRIAGE.md` and `docs/REMAINING_CANDIDATE_REGISTRY.md`;
- `track-a-regularity/evaluator/checks/flux_balance_risk.py`, a small review-status check for
  flux-sign/coercivity risk, without pretending to prove mathematical falsehood.
