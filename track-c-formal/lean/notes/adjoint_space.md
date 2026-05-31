# Step 17 - lean-dojo `AdjointSpace.lean` 정독

Date: 2026-05-19 KST  
Source: `refs/upstream/leandojo_AdjointSpace.lean`  
Size: 547 LOC

## 결론

`AdjointSpace`는 Navier-Stokes 해석학 전체를 담은 기반이 아니라, `InnerProductSpace`와 비슷한
내적 대수를 Lean에서 더 느슨한 norm 조건으로 쓰기 위한 보조 클래스다. 특히 `X × Y`와 finite
dependent function space `(i : ι) → E i`에 componentwise inner product를 주고, 그 split lemma를
제공하는 점이 Step 18에서 가장 유용하다.

Step 18에서는 full Leray-Hopf energy inequality를 바로 증명하려 하지 말고, finite-dimensional
inner-product algebra 또는 heat semigroup toy artifact처럼 작고 빌드 가능한 조각을 먼저 만드는
것이 맞다.

## `AdjointSpace` 클래스

```lean
class AdjointSpace (𝕜 : Type*) (E : Type*) [RCLike 𝕜] [NormedAddCommGroup E] extends
  NormedSpace 𝕜 E, Inner 𝕜 E where
  inner_top_equiv_norm : ∃ c d : ℝ, c > 0 ∧ d > 0 ∧
    ∀ x : E, c • ‖x‖^2 ≤ re (inner x x) ∧ re (inner x x) ≤ d • ‖x‖^2
  conj_symm : ∀ x y, conj (inner y x) = inner x y
  add_left : ∀ x y z, inner (x + y) z = inner x z + inner y z
  smul_left : ∀ x y r, inner (r • x) y = conj r * inner x y
```

핵심 차이는 `InnerProductSpace`처럼 norm이 inner product에서 정확히 유도된다고 요구하지 않는다는
점이다. 대신 inner-induced quadratic form과 기존 norm 사이에 양의 상수 `c,d`를 둔 topological
equivalence만 요구한다. 파일 주석상 이유는 `ℝ × ℝ`, `ι → ℝ` 같은 타입이 기본적으로 max norm을
갖기 때문에 표준 Euclidean inner product와 norm이 definitional하게 맞지 않는 문제를 피하려는
것이다.

우리 프로젝트 관점에서 이 선택은 장점과 위험이 동시에 있다. 장점은 finite product/function
space 대수를 빠르게 얻는 것이고, 위험은 analytic theorem을 옮길 때 mathlib의 표준
`InnerProductSpace` 정리와 직접 호환되지 않는 부분이 생긴다는 점이다.

## 기본 내적 대수

| 선언 | 역할 | Step 18 재사용성 |
| --- | --- | --- |
| `inner_conj_symm` | `⟪y,x⟫† = ⟪x,y⟫` | 복소/실수 inner symmetry 정리 전개 |
| `real_inner_comm` | 실수 내적 대칭성 | `ℝ` 기반 에너지 항 정리 |
| `inner_eq_zero_symm` | 직교 조건의 대칭성 | projector/orthogonality skeleton |
| `inner_self_im` | self-inner의 imaginary part가 0 | 복소 Fourier mode energy에서 필요 |
| `inner_add_left`, `inner_add_right` | 양쪽 덧셈 전개 | 에너지 확장/차이 전개 |
| `inner_smul_left`, `inner_smul_right` | scalar multiplication 전개 | heat multiplier, Fourier multiplier 대수 |
| `inner_smul_real_left`, `inner_smul_real_right` | real scalar 특수화 | viscosity/real coefficient 처리 |
| `sum_inner`, `inner_sum` | finite sum 안팎 교환 | finite mode energy sum |
| `inner_zero_left`, `inner_zero_right` | zero vector inner 정리 | trivial controls |
| `inner_self_nonneg`, `real_inner_self_nonneg` | self-inner nonnegative | energy nonnegativity |
| `inner_self_eq_zero`, `inner_self_ne_zero` | self-inner zero iff vector zero | coercive check |
| `inner_neg_left`, `inner_neg_right`, `inner_neg_neg` | 부호 처리 | difference energy |
| `inner_sub_left`, `inner_sub_right` | subtraction 전개 | stability/energy difference |
| `inner_add_add_self`, `real_inner_add_add_self` | `‖x+y‖²`형 전개 | finite-dimensional energy algebra |
| `inner_sub_sub_self`, `real_inner_sub_sub_self` | `‖x-y‖²`형 전개 | error energy algebra |
| `ext_inner_left`, `ext_inner_right` | inner product로 extensionality | weak form equality skeleton |

이 중 Step 18에 바로 쓰기 좋은 것은 `inner_smul_*`, `sum_inner`, `inner_sum`,
`real_inner_add_add_self`, `real_inner_sub_sub_self`다. 다만 현재 로컬 Lean project는 lean-dojo를
dependency로 연결하지 않았으므로, 이 선언들을 직접 import해서 쓰는 상태는 아니다. 우선은 이
파일의 구조를 참고해 우리 쪽에서 mathlib가 이미 제공하는 작은 정리만 쓰는 방식이 안전하다.

## 선형/반선형 형태

`sesqFormOfInner`, `innerₛₗ`, `innerₗ`, `flip_innerₗ`는 inner product를 Lean의 `LinearMap` 계층에
올리는 장치다.

- `sesqFormOfInner`: 첫 인자는 linear map, 둘째 인자는 conjugate-linear map 형태로 포장한다.
- `innerₛₗ`: `E →ₗ⋆[𝕜] E →ₗ[𝕜] 𝕜`; 첫 인자 conjugate-linear, 둘째 인자 linear.
- `innerₗ`: `𝕜 = ℝ`에서 bilinear map으로 특수화한다.
- `flip_innerₗ`: 실수 내적의 flip이 자기 자신임을 보여준다.

PDE weak formulation을 Lean에서 다룰 때는 이런 linear-map 포장이 유용하지만, 현재 프로젝트의
Step 18에서 바로 weak solution theorem으로 들어가면 measure/integration/regularity 의존성이 너무
커진다. 따라서 지금은 linear-map 계층을 "후속 promote 후보"로 기록하고, 첫 artifact에는 쓰지
않는 편이 낫다.

## 인스턴스와 split lemma

파일 하단은 네 가지 주요 인스턴스를 제공한다.

| 인스턴스 | inner product | 의미 |
| --- | --- | --- |
| `AdjointSpace 𝕜 𝕜` | `conj x * y` | base field 자체 |
| `AdjointSpace 𝕜 Unit` | `0` | trivial space |
| `AdjointSpace 𝕜 (X × Y)` | component inner의 합 | product vector space |
| `AdjointSpace 𝕜 ((i : ι) → E i)` | finite sum of component inners | finite coordinate/function space |

마지막 두 인스턴스가 우리에게 중요하다. lean-dojo는 아래 split lemma를 제공한다.

```lean
theorem inner_prod_split (x y : X×Y) :
  ⟪x,y⟫_𝕜 = ⟪x.1,y.1⟫_𝕜 + ⟪x.2,y.2⟫_𝕜 := by rfl

theorem inner_forall_split (f g : (i : ι) → E i) :
  ⟪f,g⟫_𝕜 = ∑ i, ⟪f i, g i⟫_𝕜 := by rfl
```

이 lemma들은 `Euc ℝ n`, velocity component, finite Fourier-mode proxy 같은 finite-dimensional
대상에서 에너지 합을 componentwise로 쪼개는 데 유용하다.

## `Definitions.lean` / `Navierstokes.lean` 연결

`Definitions.lean`은 `Euc 𝕜 n := EuclideanSpace 𝕜 (Fin n)`를 기본 finite-dimensional 공간으로
쓴다. `standardBasis`, `partialDeriv`, `iteratedPartialDeriv`, `divergence`, `laplacian` 같은 PDE
scaffold도 이 위에 올라간다.

`Navierstokes.lean`은 다음 구조를 둔다.

- `VelocityField n := Euc ℝ (n+1) → Euc ℝ n`
- `PressureField`, `ForceField`
- `DivergenceFreeAt`, `MaterialDerivative`, `ViscousTerm`, `PressureGradient`
- `Solution`, `GlobalSolution`, `GlobalSmoothSolution`, `SmoothSolution`
- `energyIntegral`, `kineticEnergy`, `enstrophy`
- `WeakSolution`, `LerayHopfSolution`

특히 `LerayHopfSolution`에는 kinetic energy와 enstrophy를 묶는 energy inequality 필드가 있지만,
그 자체가 proof-rich foundation은 아니다. weak formulation, integration, measure-theoretic
regularity가 모두 scaffold 형태라서, Step 18에서 이 구조를 그대로 증명 대상으로 잡는 것은
범위가 크다.

`Torus.lean`도 확인했다. `Torus3`는 실제 quotient torus가 아니라 `Euc ℝ 3`에 periodic 해석을 붙인
lightweight model이다. 따라서 periodic bounded-domain formalization을 사용할 때도 quotient
geometry가 해결된 것으로 보면 안 된다.

## Step 18 사용 후보

낮은 위험:

- finite-dimensional energy algebra helper
- real scalar heat multiplier의 positivity/semigroup algebra
- `Euc ℝ 3` 또는 `(Fin n → ℝ)` 수준의 componentwise norm/energy identity

중간 위험:

- `NavierStokesEquations`의 `kineticEnergy`/`enstrophy` 정의를 import한 뒤, statement skeleton만
  만들고 막힌 의존성을 `PROGRESS.md`에 적는 작업
- Leray projector statement skeleton

높은 위험:

- full Leray-Hopf energy inequality proof
- weak solution uniqueness/regularity 관련 자연어 증명을 Lean으로 직접 옮기는 작업
- periodic torus quotient geometry가 필요한 정리

## Step 18 권장안

첫 artifact는 `02_heat_semigroup` 계열로 진행하는 것이 가장 안전하다. 다만 Lean module name은
숫자로 시작할 수 없으므로 실제 빌드 파일은 `NavierStokesProgram/HeatSemigroup.lean`처럼
Lean-valid name을 써야 한다. `PROGRESS.md`에는 이것을 roadmap의 `02_heat_semigroup.lean`에
대응하는 artifact라고 명시한다.

권장 acceptance:

1. `NavierStokesProgram/HeatSemigroup.lean` 추가.
2. heat multiplier 또는 finite-mode toy semigroup 정의.
3. `sorry` 없이 닫히는 작은 lemma 2-4개.
4. `NavierStokesProgram.lean`에서 import.
5. `PATH="$HOME/.elan/bin:$PATH" lake build` 통과.
6. `track-c-formal/lean/PROGRESS.md`에 이번 artifact의 범위와 막힌 의존성 기록.

## 남은 리스크

- lean-dojo `AdjointSpace`는 local Lean project dependency가 아니다.
- `AdjointSpace`의 norm 조건은 exact inner-product norm equality가 아니다.
- lean-dojo Navier-Stokes files는 Clay statement scaffold에 가깝고, theorem library가 아니다.
- `WeakSolution`/`LerayHopfSolution` 계층은 statement에는 좋지만 proof search에는 아직 무겁다.
- Step 18은 "NSE 해결"이 아니라 formal artifact bootstrap이어야 한다.

## Acceptance 체크

- [x] `AdjointSpace.lean` 547 LOC 구조 확인.
- [x] class axioms와 topological norm equivalence 해석.
- [x] 주요 theorem/definition을 Step 18 재사용성 기준으로 분류.
- [x] product/function-space instance와 split lemma 확인.
- [x] `Definitions.lean`, `Navierstokes.lean`, `Torus.lean` 연결점 확인.
- [x] Step 18 권장 artifact 방향 결정.
