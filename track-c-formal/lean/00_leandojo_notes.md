# lean-dojo LeanMillenniumPrizeProblems Baseline Notes

대상: `refs/upstream/leandojo_*.lean` 8 files  
검토일: 2026-05-18 KST  
라이선스: Apache-2.0 confirmed from cloned `LICENSE`

## One-line Verdict

lean-dojo baseline은 DeepMind보다 “statement 주변 정의”가 풍부하다. 다만 `Torus3`는 quotient torus가 아니라 `Euc R 3`에 periodic interpretation을 얹은 모델이고, weak/Leray-Hopf structures는 연구용 scaffold에 가깝다.

## File-by-file Summary

| File | LOC | 요약 | Track C 영향 |
|---|---:|---|---|
| `Imports.lean` | 17 | Mathlib calculus, matrix, inner product, Schwartz space, Lebesgue integral, normed module 등을 한꺼번에 import한다. 중복 import가 있으나 baseline 용도에는 문제 없음. | Lean dependency surface가 DeepMind보다 넓다. |
| `Definitions.lean` | 154 | `Euc K n = EuclideanSpace K (Fin n)`, standard basis, partial derivative, iterated partial derivative, generic PDE structures, divergence/laplacian examples를 정의한다. | 우리 작은 formal artifact는 이 좌표식 정의가 더 읽기 쉽다. |
| `Torus.lean` | 27 | `Torus3`를 실제 quotient가 아니라 `Euc R 3`로 두고, periodic interpretation이라고 문서화한다. Borel/volume instance를 붙인다. | 계산/statement bridge에는 편하지만 진짜 compact torus integration과는 차이가 있다. |
| `Millennium.lean` | 28 | Fefferman A-D disjunction을 `MillenniumNavierStokes.NavierStokesMillenniumProblem`로 re-export한다. | top-level statement wrapper. 직접 작업 대상은 아님. |
| `MillenniumRDomain.lean` | 119 | R3 case A/C를 Fefferman 조건 번호에 맞춰 formalize한다. decay condition, force decay, bounded energy, global smooth solution을 묶는다. | R3 decay/multi-index handling 참고. 현재 periodic target에는 보조 참고만. |
| `MillenniumBoundedDomain.lean` | 107 | periodic case B/D를 formalize한다. `IsPeriodic`는 모든 정수 shift에 대해 coordinate periodicity를 요구하고, pressure periodicity errata도 반영한다. | 우리 `T^3, f=0` target에 가장 가까운 lean-dojo statement. |
| `Navierstokes.lean` | 491 | velocity/pressure/force fields, material derivative, divergence, viscous term, pressure gradient, spacetime helpers, local/global/smooth/weak/Leray-Hopf solution structures, energy/enstrophy 정의를 포함한다. | Track C의 vocabulary source. 다만 많은 정의가 analysis theorem이 아니라 structure scaffold다. |
| `AdjointSpace.lean` | 547 | SciLean에서 가져온 `AdjointSpace` 계열. norm과 inner product가 정확히 유도 관계일 필요는 없고 topological equivalence를 요구한다. inner product algebra lemmas와 product/function instances가 핵심. | Step 17에서 정독. 약한 함수공간/dual/test function 쪽 기반 후보. |

## Nominal Signature List

### `Definitions.lean`

- `abbrev Euc (K) (n) := EuclideanSpace K (Fin n)`
- `Euc.ofFun`
- `standardBasis`
- `partialDeriv`
- `iteratedPartialDeriv`
- `DerivIndices`, `DerivIndices.zero/order/leq/eq`
- `structure GeneralPDE`
- `structure LinearPDE`
- `structure FullyNonlinearPDE`
- `divergence`, `laplacian`, `laplace_equation`

### `Navierstokes.lean`

- `VelocityField`, `PressureField`, `ForceField`
- `MaterialDerivative`
- `divergence`, `DivergenceFreeAt`
- `ViscousTerm`
- `PressureGradient`
- `pairToEuc`, `getTime`, `getSpace`
- `structure NavierStokesEquations`
- `TimeDomain`, `GlobalDomain`
- `structure Solution`
- `structure GlobalSolution`
- `structure GlobalSmoothSolution`
- `energyIntegral`, `kineticEnergy`, `enstrophy`
- `structure SmoothSolution`
- `structure WeakSolution`
- `structure LerayHopfSolution`

### `MillenniumRDomain.lean`

- `InitialVelocityR3`, `ForceFieldR3`
- `DivergenceFreeInitial`
- `spatialDerivVec`, `spaceTimeDerivVec`
- `FeffermanCond4`, `FeffermanCond5`, `FeffermanCond6`, `FeffermanCond7`
- `nseR3`
- `FeffermanA`, `FeffermanC`

### `MillenniumBoundedDomain.lean`

- `IsPeriodic`
- `IsSpatiallyPeriodicForce`
- `FeffermanCond8_initial`, `FeffermanCond8_force`
- `FeffermanCond9`, `FeffermanCond10`, `FeffermanCond11`
- `FeffermanB`, `FeffermanD`
- `FeffermanMillenniumProblem`

### `Torus.lean`

- `abbrev Torus3 := Euc R 3`
- `MeasurableSpace Torus3`
- `BorelSpace Torus3`
- `MeasureSpace Torus3`

### `Millennium.lean`

- `abbrev NavierStokesMillenniumProblem := MillenniumNS_BoundedDomain.FeffermanMillenniumProblem`

### `AdjointSpace.lean` signature groups

- Typeclass: `class AdjointSpace`
- Basic inner lemmas: `inner_conj_symm`, `real_inner_comm`, `inner_eq_zero_symm`, `inner_self_im`, `inner_add_left/right`, `inner_re_symm`, `inner_im_symm`, `inner_smul_left/right`
- Linear maps/forms: `sesqFormOfInner`, `inner_s_l`, `inner_l`
- Zero/nonnegativity/extensionality: `inner_zero_left/right`, `inner_self_nonneg`, `inner_self_eq_zero`, `ext_inner_left/right`
- Algebra expansions: `inner_add_add_self`, `real_inner_add_add_self`, `inner_sub_sub_self`, `real_inner_sub_sub_self`
- Instances: field, `Unit`, product, finite dependent functions
- Split lemmas: `inner_prod_split`, `inner_forall_split`

## DeepMind (B) vs lean-dojo `FeffermanB`

| 항목 | DeepMind statement (B) | lean-dojo `FeffermanB` | 비고 |
|---|---|---|---|
| 공간 표현 | functions on `R^3` with `IsOnePeriodic` | `Euc R 3` with `IsPeriodic`; `Torus3` is also `Euc R 3` | 둘 다 quotient torus를 직접 쓰지 않는다. |
| periodicity | shift by basis vector `+ e_i` | all integer shifts `+ n • e_i` | lean-dojo가 condition을 더 강하게/명시적으로 표현한다. |
| force | `f := 0` in theorem conclusion | `nseR3 ... (fun _ => 0)` | 일치 |
| smoothness | `ContDiffOn R ∞` on `univ x Ici 0` | `GlobalSmoothSolution` with `ContDiff R top u/p` | lean-dojo는 global function smoothness로 더 단순/강한 형태일 수 있다. |
| PDE encoding | `derivWithin` + `fderiv` directional derivative | coordinate `partialDeriv`, `MaterialDerivative` | DeepMind는 abstract calculus, lean-dojo는 coordinate readable. |
| pressure periodicity | required in periodic solution structure | `FeffermanCond10` includes pressure periodicity | errata 반영 일치 |

## Differences That Matter

1. DeepMind는 Clay statement를 간결하게 formalize하고, lean-dojo는 pedagogical/coordinate scaffold가 많다.
2. DeepMind의 convective term은 concise하지만 읽기 어렵다. lean-dojo `MaterialDerivative`는 좌표식이라 solver/문서와 연결하기 쉽다.
3. lean-dojo weak solution과 Leray-Hopf structure는 우리 guardrail 문서에 유용하지만, BV non-uniqueness와 직접 연결되는 theorem proof가 들어 있는 것은 아니다.
4. lean-dojo `Torus3`는 실제 compact quotient measure가 아니므로, 장기적으로 torus integration을 엄밀히 쓰려면 별도 gap으로 남는다.
5. Step 9에서 우리 Lean project를 만들 때 DeepMind statement import와 lean-dojo coordinate definitions 중 어느 쪽을 primary dependency로 삼을지 결정해야 한다. 현재 판단은 DeepMind = statement reference, lean-dojo = vocabulary reference.

## Acceptance Checklist

- [x] 8 files covered
- [x] nominal function/signature list included
- [x] `AdjointSpace.lean` treated as signature-level only
- [x] DeepMind statement (B) vs lean-dojo `FeffermanB` one-table comparison
- [ ] `docs/BASELINE.md` updated directly: blocked by project rule, see `docs/BASELINE_CODEX_REVIEW.md`
