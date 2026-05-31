# Round 3 Selected Definitions

Date: 2026-05-19

Status: Step 34 draft complete.

Scope: definition tightening for five selected Track A round-3 candidate families.

This file defines quantities for evaluator and formalization planning. It does not assert that
any quantity gives a valid Navier-Stokes regularity criterion.

## Common Setting

Unless stated otherwise:

- domain: periodic `T^3 = R^3 / Z^3`;
- velocity: `u : T^3 x [0,T) -> R^3`;
- solution class: smooth classical, divergence-free, mean-zero;
- viscosity: `nu > 0`;
- force: `0`;
- vorticity: `omega = curl u`;
- strain tensor: `S = (grad u + (grad u)^T) / 2`;
- Littlewood-Paley shell: `P_N`, where `N` ranges over dyadic integers.

Any future candidate using these quantities must specify whether it is a smooth continuation
criterion, a diagnostic bound, or a known-result registry item.

## 1. Dyadic Nonlinear Energy Flux

Representative candidates: `lemma_0204`, `0214`, `0224`, `0234`, `0244`.

### Quantity

Let `u_{<=N} = P_{<=N} u`. Define a shell energy-flux proxy:

```text
Pi_N(u)(t) = - integral_{T^3} ((u(t) · grad) u(t)) · u_{<=N}(t) dx
```

Alternative LES-style flux may use:

```text
Pi_N^LES(u)(t) = integral_{T^3} grad u_{<=N}(t) : tau_N(u,u)(t) dx
tau_N(u,u) = P_{<=N}(u tensor u) - u_{<=N} tensor u_{<=N}
```

The evaluator must reject a statement unless it declares which convention is used.

### Scaling

Energy flux has units of energy per time. A scale-invariant statement should not just bound
`Pi_N` absolutely. It should specify a normalized envelope such as:

```text
F_N(t) = N^{-alpha} max(Pi_N(u)(t), 0)
```

with explicit `alpha`, summability over dyadic `N`, and time norm.

### Known-Result Risk

High. Flux bounds often encode regularity already present in Besov or Onsager-style conditions.
Before treating as a candidate theorem, compare against energy flux criteria in turbulence and
Onsager-adjacent literature.

### Evaluator Rule

Fail if:

- no shell projector convention is stated;
- no normalization exponent is stated;
- no dyadic summability and time norm are stated;
- the conclusion is smooth continuation but the hypothesis is only a diagnostic phrase.

## 2. Parabolic Morrey Enstrophy Concentration

Representative candidates: `lemma_0205`, `0215`, `0225`, `0235`, `0245`.

### Quantity

For a parabolic cylinder centered at `(x0,t0)`:

```text
Q_r(x0,t0) = B_r(x0) x (t0 - r^2, t0)
```

on `T^3`, interpret `B_r` periodically for small `r`, or lift to `R^3` locally.

Define localized enstrophy concentration:

```text
E_r(x0,t0) = r^{-beta} integral_{t0-r^2}^{t0} integral_{B_r(x0)} |omega(x,t)|^2 dx dt
```

The exponent `beta` must be selected to match the intended scaling. A candidate is not precise
until `beta`, the supremum domain, and the time boundary convention are fixed.

### Scaling

Under NSE scaling, `omega` scales like length^{-2}; `|omega|^2 dx dt` in 3D scales like
length^{-4} * length^3 * length^2 = length. Thus `beta = 1` makes `E_r` scale-invariant.

### Known-Result Risk

Medium to high. CKN partial regularity already uses scale-invariant local quantities for suitable
weak solutions. A smooth continuation statement must be separated from CKN-type partial
regularity and ESS endpoint results.

### Evaluator Rule

Fail if:

- the solution class is weak/suitable weak but the conclusion is smooth continuation;
- `beta` is missing;
- the cylinder geometry or periodic interpretation is missing;
- the statement does not specify `sup_{x0,t0,r}` or an equivalent envelope.

## 3. Localized Vortex-Stretching Control

Representative candidates: `lemma_0202`, `0212`, `0222`, `0232`, `0242`.

### Quantity

Vortex-stretching density:

```text
VS(x,t) = ((omega(x,t) · grad) u(x,t)) · omega(x,t)
        = omega(x,t) · S(x,t) omega(x,t)
```

For a threshold `lambda(t)` and localization scale `r`, define high-vorticity region:

```text
H_lambda(t) = { x in T^3 : |omega(x,t)| >= lambda(t) }
```

A localized positive stretching envelope may be:

```text
V_r^+(t) = sup_{x0} integral_{B_r(x0) cap H_lambda(t)} max(VS(x,t), 0) dx
```

### Scaling

`VS` scales like length^{-6}; integrating over space gives length^{-3}. Any time-integrated
criterion needs a compensating scale factor and explicit relation between `r` and `lambda`.

### Known-Result Risk

Medium. This targets the nonlinear obstruction directly, but many geometric depletion and
vorticity direction criteria already exist. It needs literature comparison before promotion.

Step 40 update: the risk is now high. `docs/KNOWN_GEOMETRIC_CRITERIA.md` identifies strong overlap
with Constantin-Fefferman vorticity-direction criteria, Beirao da Veiga-Berselli direction
regularization, Chae direction-magnitude criteria, and strain-eigenvalue criteria. Do not rewrite
this family as a new candidate until a `geometric_known_result_check` is added.

### Evaluator Rule

Fail if:

- vortex-stretching density is not explicitly defined;
- high-vorticity threshold is missing;
- positive/negative part convention is missing;
- scale/time normalization is missing.

## 4. Strain Eigenvalue Contribution

Representative candidates: `lemma_0203`, `0213`, `0223`, `0233`, `0243`.

### Quantity

Let `S(x,t)` be the symmetric strain tensor with eigenvalues:

```text
lambda_1(x,t) <= lambda_2(x,t) <= lambda_3(x,t)
```

For incompressible flow, `trace S = 0`. Define vorticity direction where nonzero:

```text
xi = omega / |omega|
```

The stretching contribution can be written:

```text
omega · S omega = |omega|^2 (xi · S xi)
```

A candidate eigenvalue proxy might bound:

```text
SE^+(t) = integral_{T^3} max(xi · S xi, 0) |omega|^2 dx
```

or a variant involving `lambda_3^+ |omega|^2`. The exact version must be fixed.

### Scaling

`S` scales like `length^{-2}`, `|omega|^2` scales like `length^{-4}`, so the integrand scales like
`length^{-6}` and the spatial integral like `length^{-3}`. Time and scale normalization must be
specified for criticality.

### Known-Result Risk

Medium. Strain/vorticity alignment criteria are real, but the eigenvalue proxy may be too strong
or equivalent to existing controls.

### Evaluator Rule

Fail if:

- eigenvalue ordering is missing;
- `xi` at vorticity zeros is not handled;
- the candidate does not choose between `xi · S xi` and `lambda_3^+`;
- scale/time norm is missing.

## 5. Vorticity Direction on High-Vorticity Superlevel Sets

Representative candidates: `lemma_0207`, `0217`, `0227`, `0237`, `0247`.

### Quantity

Define:

```text
xi(x,t) = omega(x,t) / |omega(x,t)|
```

only on:

```text
H_lambda(t) = { x : |omega(x,t)| >= lambda(t) > 0 }
```

A direction modulus on high-vorticity sets may be:

```text
M_r(t) = sup {
  |xi(x,t) - xi(y,t)| / |x-y|^gamma :
  x,y in H_lambda(t), 0 < |x-y| <= r
}
```

The candidate must specify `gamma`, `r`, `lambda(t)`, and the time norm.

### Scaling

`xi` is dimensionless, while `M_r` scales like `length^{-gamma}`. A critical statement must pair
the modulus with a scale or threshold relation.

### Known-Result Risk

High. Vorticity-direction coherence is a known Navier-Stokes regularity theme. The next step is
to compare against Constantin-Fefferman-type criteria and add known-result registry entries.

### Evaluator Rule

Fail if:

- the statement defines vorticity direction where `omega = 0`;
- high-vorticity superlevel set is missing;
- Hölder/Lipschitz exponent is missing;
- time norm and scale are missing.

## Step 34 Output Contract

Selected families can move forward only after each candidate rewrite includes:

1. exact quantity definition;
2. scaling exponent or declared non-critical status;
3. solution class;
4. known-result overlap note;
5. evaluator rule.

No selected family is ready for theorem promotion yet.
