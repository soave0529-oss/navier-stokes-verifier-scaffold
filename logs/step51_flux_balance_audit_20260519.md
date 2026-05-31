# Step 51 — Flux-Balance Audit for `lemma_0251`

Date: 2026-05-19

Status: complete.

## Artifact

- `docs/LEMMA_0251_FLUX_BALANCE_AUDIT.md`

## Main Identity

For `u_N = P_{<=N}u` and
`tau_N = P_{<=N}(u tensor u) - u_N tensor u_N`, the project flux convention satisfies:

```text
d/dt (1/2 ||u_N||_2^2)
  = -nu ||grad u_N||_2^2 + integral grad u_N : tau_N dx.
```

So:

```text
Pi_N^project = dE_N/dt + nu D_N.
```

## Decision

`lemma_0251` should be downgraded to `needs_rewrite_before_review`.

Reasons:

- current positive `Pi_N^project` is low-mode feeding/backscatter under the usual forward-cascade
  sign convention;
- signed integral is energy-controlled, but positive-part summability is not proven automatic from
  the global energy inequality alone;
- the hypothesis is noncoercive and gives no direct bound on enstrophy, BKM, pressure, Besov
  regularity, or high-frequency spectral tail.

## Verification

No code changed in this step. Latest verification from Step 50:

- Python tests: `30 passed`.
- Evaluator expected-check matched all 252 candidates.
- Distribution: `falsified 227`, `known_control 12`, `known_control_with_extra_assumption 6`,
  `candidate 7`.

## Next

Step 52 should propagate the downgrade into candidate registries and, if useful, add evaluator
metadata for flux sign/coercivity risk.
