import NavierStokesProgram.LocalEnergy
import NavierStokesProgram.CandidateGate

/-!
# Proof Obligation Graph Vocabulary

Finite vocabulary for tracking which `lemma_0252` proof obligations are only
named, which are partial, and which remain analytic blockers.

This file does not prove epsilon regularity, compactness, a pressure estimate,
or smooth continuation. It is an audit graph for future review.
-/

namespace NavierStokesProgram
namespace ProofObligationGraph

open ParabolicMorrey
open LocalEnergy

/-- Coarse proof obligations for the parabolic-Morrey `lemma_0252` route. -/
inductive Lemma0252Obligation where
  | cylinderAdmissibility
  | enstrophyToLocalEnergy
  | pressureControl
  | finiteBoundToSmallness
  | compactnessLiouville
  | smoothContinuationBridge
deriving DecidableEq

/-- Status of one obligation inside the current formal artifact set. -/
inductive ObligationStatus where
  | partialVocabulary
  | vocabularyOnly
  | guardrailOnly
  | missingMechanism
deriving DecidableEq

/-- One node in the finite obligation graph. -/
structure ObligationNode where
  obligation : Lemma0252Obligation
  status : ObligationStatus
  suppliedAsAssumption : Prop
  provedInCurrentArtifact : Prop

/--
Graph shell connecting a parabolic-Morrey hypothesis to local-energy metadata.

The mechanism fields are deliberately propositions rather than proofs. A graph
can name a missing route without converting it into a theorem.
-/
structure Lemma0252LocalEnergyGraph where
  hypothesis : ParabolicMorreyHypothesis
  localEnergy : Option FiniteLocalEnergyInequality
  pressureDataNamed : Prop
  cutoffDataNamed : Prop
  finiteBoundToSmallnessMechanism : Prop
  compactnessLiouvilleMechanism : Prop
  smoothContinuationBridge : Prop
  noEpsilonRegularityClaim : Prop
  noWeakToSmoothUpgradeClaim : Prop
  node : Lemma0252Obligation → ObligationNode
  node_matches : ∀ o, (node o).obligation = o

namespace Lemma0252LocalEnergyGraph

/-- The Step 64 promotion blocker: at least one analytic mechanism is absent. -/
def blocksPromotion (G : Lemma0252LocalEnergyGraph) : Prop :=
  ¬ G.finiteBoundToSmallnessMechanism ∨
    ¬ G.compactnessLiouvilleMechanism ∨
    ¬ G.smoothContinuationBridge

theorem node_obligation_eq (G : Lemma0252LocalEnergyGraph)
    (o : Lemma0252Obligation) :
    (G.node o).obligation = o :=
  G.node_matches o

/-- Named accessor for the no-epsilon-regularity guardrail proposition. -/
def noEpsilonRegularizationClaimProp
    (G : Lemma0252LocalEnergyGraph) : Prop :=
  G.noEpsilonRegularityClaim

/-- Named accessor for the no-weak-to-smooth-upgrade guardrail proposition. -/
def noWeakToSmoothUpgradeClaimProp
    (G : Lemma0252LocalEnergyGraph) : Prop :=
  G.noWeakToSmoothUpgradeClaim

theorem noEpsilonRegularizationClaimProp_eq
    (G : Lemma0252LocalEnergyGraph) :
    G.noEpsilonRegularizationClaimProp = G.noEpsilonRegularityClaim :=
  rfl

theorem noWeakToSmoothUpgradeClaimProp_eq
    (G : Lemma0252LocalEnergyGraph) :
    G.noWeakToSmoothUpgradeClaimProp = G.noWeakToSmoothUpgradeClaim :=
  rfl

end Lemma0252LocalEnergyGraph

/-- Step 64's conservative status map for `lemma_0252`. -/
def step64Node : Lemma0252Obligation → ObligationNode
  | .cylinderAdmissibility =>
      { obligation := .cylinderAdmissibility
        status := .partialVocabulary
        suppliedAsAssumption := True
        provedInCurrentArtifact := False }
  | .enstrophyToLocalEnergy =>
      { obligation := .enstrophyToLocalEnergy
        status := .vocabularyOnly
        suppliedAsAssumption := True
        provedInCurrentArtifact := False }
  | .pressureControl =>
      { obligation := .pressureControl
        status := .vocabularyOnly
        suppliedAsAssumption := True
        provedInCurrentArtifact := False }
  | .finiteBoundToSmallness =>
      { obligation := .finiteBoundToSmallness
        status := .missingMechanism
        suppliedAsAssumption := False
        provedInCurrentArtifact := False }
  | .compactnessLiouville =>
      { obligation := .compactnessLiouville
        status := .missingMechanism
        suppliedAsAssumption := False
        provedInCurrentArtifact := False }
  | .smoothContinuationBridge =>
      { obligation := .smoothContinuationBridge
        status := .guardrailOnly
        suppliedAsAssumption := False
        provedInCurrentArtifact := False }

theorem step64Node_matches (o : Lemma0252Obligation) :
    (step64Node o).obligation = o := by
  cases o <;> rfl

/--
Canonical Step 64 graph skeleton.

It deliberately leaves local-energy records optional and sets the analytic
mechanism propositions to `False`, so downstream code cannot mistake the map
for a proof route.
-/
def step64GraphSkeleton
    (hypothesis : ParabolicMorreyHypothesis) : Lemma0252LocalEnergyGraph where
  hypothesis := hypothesis
  localEnergy := none
  pressureDataNamed := True
  cutoffDataNamed := True
  finiteBoundToSmallnessMechanism := False
  compactnessLiouvilleMechanism := False
  smoothContinuationBridge := False
  noEpsilonRegularityClaim := True
  noWeakToSmoothUpgradeClaim := True
  node := step64Node
  node_matches := step64Node_matches

theorem step64GraphSkeleton_blocksPromotion
    (hypothesis : ParabolicMorreyHypothesis) :
    (step64GraphSkeleton hypothesis).blocksPromotion := by
  left
  intro h
  exact h

theorem step64GraphSkeleton_localEnergy_none
    (hypothesis : ParabolicMorreyHypothesis) :
    (step64GraphSkeleton hypothesis).localEnergy = none :=
  rfl

theorem step64GraphSkeleton_finiteBound_missing
    (hypothesis : ParabolicMorreyHypothesis) :
    ((step64GraphSkeleton hypothesis).node
      .finiteBoundToSmallness).status = .missingMechanism :=
  rfl

theorem step64GraphSkeleton_compactness_missing
    (hypothesis : ParabolicMorreyHypothesis) :
    ((step64GraphSkeleton hypothesis).node
      .compactnessLiouville).status = .missingMechanism :=
  rfl

theorem step64GraphSkeleton_no_epsilon_claim
    (hypothesis : ParabolicMorreyHypothesis) :
    (step64GraphSkeleton hypothesis).noEpsilonRegularityClaim :=
  trivial

theorem step64GraphSkeleton_no_weak_to_smooth_claim
    (hypothesis : ParabolicMorreyHypothesis) :
    (step64GraphSkeleton hypothesis).noWeakToSmoothUpgradeClaim :=
  trivial

end ProofObligationGraph
end NavierStokesProgram
