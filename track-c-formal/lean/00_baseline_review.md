# DeepMind Navier-Stokes Baseline Review

대상 파일: `refs/upstream/DeepMind_NavierStokes.lean`  
검토일: 2026-05-18 KST  
범위: 294 LOC 전체

## One-line Verdict

DeepMind PR #1457은 Clay 문제를 “풀었다”가 아니라, Clay의 4개 alternative를 Lean theorem statement로 올린 baseline이다. 우리 프로젝트에는 periodic statement (B)가 직접 출발점이며, 실제 연구 난점은 statement 이후의 PDE library와 proof infrastructure에 있다.

## 30-50 Line Block Notes

| Lines | 내용 | 한국어 주석 |
|---:|---|---|
| 1-17 | license/import | Apache-2.0 header와 `FormalConjectures.Util.ProblemImports` 단일 import. 실제 사용 API는 이 import에 감춰져 있어 Step 9에서 clone build가 가능해야 dependency surface를 확정할 수 있다. |
| 19-54 | module docstring | 파일 목적, 네 가지 Clay alternative, 변수 convention, `derivWithin` 시간 미분, pressure periodic errata 반영을 설명한다. 중요한 설계 선택은 `v x t` 순서와 `t >= 0` half-line 처리다. |
| 56-76 | namespace/open/divergence definition | `divergence`를 `fderiv`의 trace로 정의하고 `∇⬝` notation을 붙인다. 미분 불가능 지점에서 `fderiv`가 junk value가 될 수 있다는 사실을 docstring이 명시한다. |
| 78-106 | divergence API lemmas | not differentiable, zero, constant field의 divergence는 닫혀 있고, add/smul은 `sorry`다. statement repo라서 API lemma proof가 일부 비어 있다. 우리 Track C에서 바로 의존하면 안 된다. |
| 108-159 | periodicity and initial data conditions | `IsOnePeriodic`는 각 좌표 basis 방향으로 `x + e_i` periodic. `InitialVelocityCondition`은 divergence-free + smooth, Rn decay variant와 periodic variant를 분리한다. 우리 `T^3, f=0` target은 periodic variant에 해당한다. |
| 161-197 | force conditions | force의 smoothness, Rn decay, periodic/time-decay 조건을 따로 둔다. 최종 theorem (A/B)는 `f := 0`이므로 우리 1차 문제에서는 force condition 자체보다 breakdown statements (C/D) 해석에 중요하다. |
| 199-227 | core solution structure | `NavierStokesExistenceAndSmoothness`가 PDE, divergence-free, initial condition, velocity/pressure smoothness를 묶는다. convective term은 `fderiv R (v · t) x (v x t)`로 표현된다. |
| 229-245 | Rn solution extension | Rn case에는 finite-energy `MemLp`와 globally bounded energy가 추가된다. periodic target에는 이 extension이 직접 필요 없지만 energy diagnostics의 conceptual baseline이다. |
| 247-261 | periodic solution extension | velocity와 pressure 모두 spatially 1-periodic이어야 한다. Clay errata의 pressure periodicity 반영이 명시되어 있어, 우리 solver/Track C의 periodic gauge convention과 맞춰야 한다. |
| 264-276 | statements A/B | (A)는 R3 global existence, (B)는 periodic global existence. 둘 다 `nu > 0`, `f := 0`, smooth/div-free initial condition을 받으며 proof는 `sorry`. |
| 278-294 | statements C/D/end | (C)는 R3 breakdown alternative, (D)는 periodic breakdown alternative. breakdown은 force를 허용하고, 적절한 initial/force condition을 만족하면서 smooth solution이 존재하지 않는 경우를 말한다. |

## Four Clay Statements

| Label | Lean theorem | 한국어 요약 | 우리 프로젝트 관련성 |
|---|---|---|---|
| A | `navier_stokes_existence_and_smoothness_R3` | 임의의 smooth divergence-free rapidly decaying initial data와 `nu > 0`에 대해 R3 전공간 smooth global solution이 존재한다. | R3 track은 나중. 현재는 periodic 우선. |
| B | `navier_stokes_existence_and_smoothness_periodic` | 임의의 smooth divergence-free 1-periodic initial data와 `nu > 0`에 대해 periodic smooth global solution이 존재한다. | 1차 target과 가장 일치. |
| C | `navier_stokes_breakdown_R3` | R3에서 조건을 만족하는 initial data와 force가 존재해 smooth solution이 존재하지 않는 breakdown 시나리오가 있다. | blow-up/counterexample track의 R3 variant. |
| D | `navier_stokes_breakdown_periodic` | periodic setting에서 조건을 만족하는 initial data와 force가 존재해 smooth solution이 존재하지 않는 breakdown 시나리오가 있다. | Track B의 장기 negative route. 단 force 허용이라 `f=0` target과 다름. |

## PR #1457 Issue Notes

| PR issue | 우리 의견 |
|---|---|
| `fderiv R (v · t) x (v x t)`가 convective term이라는 게 곧장 명확하지 않음 | 수학적으로는 directional derivative `Dv(x,t)[v(x,t)]`라서 `(v · ∇)v`와 맞다. 다만 Lean reader에게는 좌표식 lemma가 별도로 있어야 한다. Track C gap으로 등록. |
| 성장 조건이 `‖iteratedFDeriv R n u0 x‖`인데 원문은 `|partial^alpha u(x,t)|`; 동치인가 | smooth finite-dimensional setting에서는 multi-index partial derivative bounds와 iterated Frechet derivative operator norm bounds가 서로 비교 가능해야 한다. 하지만 Lean에서는 이 동치가 큰 lemma 묶음이다. R3 decay target 전까지는 보류. |
| `t >= 0` vs `t > 0` 처리 | `derivWithin` on `Ici 0`는 closed half-line statement에 맞지만, `t=0`에서 PDE를 어떤 의미로 요구하는지 민감하다. Clay statement가 smooth on `[0,∞)`처럼 쓰이더라도 proof work에서는 interior `t>0`와 initial condition을 분리하는 편이 더 견고하다. |

## Statement (B) vs Our Fixed Variant

| 항목 | DeepMind statement (B) | 우리 고정 변형 | 판정 |
|---|---|---|---|
| 공간 | `R^3/Z^3`를 `IsOnePeriodic` 함수로 표현 | `T^3`, 구현상 periodic cube | 일치. 단 quotient torus가 아니라 periodic functions representation |
| viscosity | arbitrary `nu : R`, `nu > 0` | `nu = 1` 우선 | `nu=1`은 statement (B)의 특수한 경우 |
| force | theorem conclusion에서 `f := 0` | `f = 0` | 일치 |
| initial data | `InitialVelocityConditionPeriodic u0`: divergence-free, smooth, 1-periodic | smooth divergence-free periodic | 일치 |
| solution | exists `v p`, smooth, divergence-free, initial condition, periodic velocity/pressure | smooth periodic velocity/pressure expected | 일치 |
| pressure normalization | periodic pressure만 요구, 평균 0 gauge는 없음 | solver에서는 pressure gauge/mean-zero 필요 가능 | formal statement에는 gauge uniqueness가 없음. solver artifact에서 convention 명시 필요 |
| time domain | `t >= 0`, `derivWithin` | `t >= 0`, numerics는 `[0,T]` | 일치하지만 formal proof에서 `t=0` 처리 주의 |

## Immediate Track C Consequences

1. DeepMind file은 statement baseline이지 proof dependency로 그대로 신뢰할 수 없다. 내부 API lemma `divergence_add`, `divergence_smul`에도 `sorry`가 있다.
2. 우리 첫 formal artifact는 theorem (B) 증명이 아니라, statement (B)를 import하고 작은 compatible definition을 만드는 쪽이 맞다.
3. Convective term readability를 위해 좌표형 lemma skeleton이 필요하다: `fderiv R (v · t) x (v x t)` equals `sum_i v_i partial_i v`.
4. Periodic target은 quotient manifold formalization이 아니라 1-periodic function formalization으로 출발한다.
5. Pressure gauge는 Clay statement에는 없지만 numerical/analytic work에서는 mean-zero convention을 별도 문서화해야 한다.

## Acceptance Checklist

- [x] 294 LOC 전체 cover
- [x] 4 statement 한국어 요약
- [x] PR #1457 issue 3개 의견
- [x] DeepMind statement (B)와 우리 변형 비교 표
