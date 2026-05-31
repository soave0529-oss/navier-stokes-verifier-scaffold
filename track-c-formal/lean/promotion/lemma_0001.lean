import NavierStokesProgram.Basic

/-!
# Promotion skeleton for `lemma_0001`

Source candidate: `track-a-regularity/candidates/lemma_0001.yaml`

This file intentionally contains a type-checked statement-as-`Prop` skeleton, not
a proof. The predicates below are placeholders for future formalization of the
periodic 3D Navier-Stokes setting and the BKM continuation criterion.
-/

namespace NavierStokesProgram
namespace Promotion

/-- Lightweight periodic 3-torus model used in the current local skeleton. -/
abbrev Torus3Model : Type := Point3

/-- Placeholder for a smooth periodic Navier-Stokes solution on `T^3`. -/
structure SmoothPeriodicNSESolution where
  velocity : VectorField3
  viscosity : ℝ
  viscosity_pos : 0 < viscosity
  divergence_free : IsDivergenceFreeSmooth velocity
  mean_zero : Prop

/-- Placeholder vorticity field `ω(t,x) = curl u(t,x)`. -/
axiom VorticityField : SmoothPeriodicNSESolution → ℝ → Torus3Model → Point3

/-- Placeholder `L^∞(T^3)` norm for vector fields. -/
axiom LInfinityNormOnTorus3 : (Torus3Model → Point3) → ℝ

/-- Placeholder for finiteness of `∫_0^T f(t) dt`. -/
axiom TimeIntegralFinite : (ℝ → ℝ) → ℝ → Prop

/-- Placeholder continuation conclusion. -/
axiom ExtendsSmoothlyPast : SmoothPeriodicNSESolution → ℝ → Prop

/--
BKM-style continuation criterion, promoted from `lemma_0001`.

This is a statement skeleton only. It asserts the shape of the target proposition
without proving the criterion or claiming a new Navier-Stokes result.
-/
def lemma_0001_bkm_continuation_statement : Prop :=
  ∀ (u : SmoothPeriodicNSESolution) (T : ℝ),
    0 < T →
      TimeIntegralFinite
        (fun t => LInfinityNormOnTorus3 (VorticityField u t))
        T →
        ExtendsSmoothlyPast u T

end Promotion
end NavierStokesProgram
