import NavierStokesProgram.SolutionClasses
import Mathlib.Data.Finset.Basic

/-!
# Parabolic Cylinder Vocabulary

Placeholder vocabulary for the definition-tightened parabolic Morrey enstrophy
candidate `lemma_0252`.

This file records the geometry and scale-normalized local enstrophy envelope as
typed data. It does not formalize balls on the quotient torus, does not define
curl, and does not state a Navier-Stokes continuation theorem.
-/

namespace NavierStokesProgram
namespace ParabolicMorrey

open SolutionClasses

/-- A backward parabolic cylinder `B_r(x0) x (t0 - r^2, t0)` placeholder. -/
structure ParabolicCylinder where
  center : Point3
  topTime : Time
  radius : ℝ
  radius_pos : 0 < radius
  radius_le_one : radius ≤ 1
  periodic_lift_convention : Prop

namespace ParabolicCylinder

/-- Lower time endpoint `t0 - r^2`. -/
noncomputable def lowerTime (Q : ParabolicCylinder) : Time :=
  Q.topTime - Q.radius ^ 2

/-- Radius inverse used by the beta=1 normalized enstrophy quantity. -/
noncomputable def betaOneScale (Q : ParabolicCylinder) : ℝ :=
  Q.radius⁻¹

theorem betaOneScale_nonneg (Q : ParabolicCylinder) :
    0 ≤ Q.betaOneScale := by
  unfold betaOneScale
  exact inv_nonneg.mpr (le_of_lt Q.radius_pos)

end ParabolicCylinder

/-- A local vorticity L2 spacetime integral attached to one cylinder. -/
structure LocalEnstrophySample where
  cylinder : ParabolicCylinder
  vorticityL2Integral : ℝ
  integral_nonneg : 0 ≤ vorticityL2Integral

namespace LocalEnstrophySample

/-- The beta=1 normalized localized enstrophy `r^{-1} integral |omega|^2`. -/
noncomputable def normalizedEnstrophy (s : LocalEnstrophySample) : ℝ :=
  s.cylinder.betaOneScale * s.vorticityL2Integral

theorem normalizedEnstrophy_nonneg (s : LocalEnstrophySample) :
    0 ≤ s.normalizedEnstrophy := by
  unfold normalizedEnstrophy
  exact mul_nonneg s.cylinder.betaOneScale_nonneg s.integral_nonneg

end LocalEnstrophySample

/--
Finite placeholder for a parabolic Morrey envelope with beta fixed to one.

The true candidate uses a supremum over centers, top times, and radii. This
record deliberately covers only finite samples so the vocabulary stays buildable
and does not assert compactness, measurability, or a regularity implication.
-/
structure FiniteParabolicMorreyEnvelope where
  indices : Finset ℕ
  sample : ℕ → LocalEnstrophySample
  bound : ℝ
  bound_nonneg : 0 ≤ bound
  beta : ℝ
  beta_eq_one : beta = 1
  normalized_le_bound :
    ∀ i, i ∈ indices → (sample i).normalizedEnstrophy ≤ bound

namespace FiniteParabolicMorreyEnvelope

theorem sample_nonneg (E : FiniteParabolicMorreyEnvelope) {i : ℕ} :
    0 ≤ (E.sample i).normalizedEnstrophy :=
  (E.sample i).normalizedEnstrophy_nonneg

theorem sample_le_bound (E : FiniteParabolicMorreyEnvelope) {i : ℕ}
    (hi : i ∈ E.indices) :
    (E.sample i).normalizedEnstrophy ≤ E.bound :=
  E.normalized_le_bound i hi

end FiniteParabolicMorreyEnvelope

/--
Typed hypothesis shell for `lemma_0252`.

This keeps the smooth classical solution class explicit while avoiding any
claim that the finite placeholder envelope implies smooth continuation.
-/
structure ParabolicMorreyHypothesis where
  solution : SmoothClassicalSolution
  terminalTime : Time
  envelope : FiniteParabolicMorreyEnvelope

end ParabolicMorrey
end NavierStokesProgram
