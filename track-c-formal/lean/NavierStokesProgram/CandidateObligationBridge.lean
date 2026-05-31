import NavierStokesProgram.ProofObligationGraph

/-!
# Candidate Gate to Proof-Obligation Graph Bridge

Small accessor layer connecting the v4 candidate-generation gate vocabulary to
the `lemma_0252` proof-obligation graph.

This file does not prove that any candidate is correct. It only records that a
candidate may need both ordinary v4 audit metadata and a graph-level discharge
of proof-route and solution-class blockers.
-/

namespace NavierStokesProgram
namespace CandidateObligationBridge

open CandidateGate
open ProofObligationGraph
open ParabolicMorrey

/--
A candidate shell paired with a local proof-obligation graph.

The `graphDischarges*` fields are propositions that must be supplied by a
future analytic route; this structure does not prove them.
-/
structure CandidateGraphAudit where
  candidate : CandidateShell
  graph : Lemma0252LocalEnergyGraph
  graphDischargesProofRoute : Prop
  graphDischargesSolutionClassBridge : Prop
  blockersDocumented : Prop

namespace CandidateGraphAudit

/-- The graph is ready only when it has no promotion blocker and its bridges are named. -/
def GraphReady (A : CandidateGraphAudit) : Prop :=
  ¬ A.graph.blocksPromotion ∧
    A.graphDischargesProofRoute ∧
    A.graphDischargesSolutionClassBridge

/-- Emit-ready with graph metadata requires the ordinary v4 gate plus graph readiness. -/
def EmitReadyWithGraph (A : CandidateGraphAudit) : Prop :=
  A.candidate.EmitReady ∧ A.GraphReady

theorem emitReadyWithGraph_has_candidate_emitReady
    (A : CandidateGraphAudit) (h : A.EmitReadyWithGraph) :
    A.candidate.EmitReady :=
  h.1

theorem emitReadyWithGraph_has_v4_proof_route
    (A : CandidateGraphAudit) (h : A.EmitReadyWithGraph) :
    A.candidate.audit.proofRoute :=
  CandidateShell.emitReady_has_proof_route A.candidate h.1

theorem emitReadyWithGraph_has_v4_solution_class_bridge
    (A : CandidateGraphAudit) (h : A.EmitReadyWithGraph) :
    A.candidate.audit.solutionClassBridge :=
  CandidateShell.emitReady_has_solution_class_bridge A.candidate h.1

theorem emitReadyWithGraph_not_graph_blocked
    (A : CandidateGraphAudit) (h : A.EmitReadyWithGraph) :
    ¬ A.graph.blocksPromotion :=
  h.2.1

theorem emitReadyWithGraph_has_graph_proof_route_discharge
    (A : CandidateGraphAudit) (h : A.EmitReadyWithGraph) :
    A.graphDischargesProofRoute :=
  h.2.2.1

theorem emitReadyWithGraph_has_graph_solution_class_discharge
    (A : CandidateGraphAudit) (h : A.EmitReadyWithGraph) :
    A.graphDischargesSolutionClassBridge :=
  h.2.2.2

end CandidateGraphAudit

/--
Step 67 bridge skeleton for the current `lemma_0252` graph state.

It deliberately uses the Step 64 graph skeleton and leaves graph-level proof
route and solution-class discharges as `False`.
-/
def step67GraphAudit
    (candidate : CandidateShell)
    (hypothesis : ParabolicMorreyHypothesis) : CandidateGraphAudit where
  candidate := candidate
  graph := step64GraphSkeleton hypothesis
  graphDischargesProofRoute := False
  graphDischargesSolutionClassBridge := False
  blockersDocumented := True

theorem step67GraphAudit_blocksPromotion
    (candidate : CandidateShell)
    (hypothesis : ParabolicMorreyHypothesis) :
    (step67GraphAudit candidate hypothesis).graph.blocksPromotion :=
  step64GraphSkeleton_blocksPromotion hypothesis

theorem step67GraphAudit_not_emitReadyWithGraph
    (candidate : CandidateShell)
    (hypothesis : ParabolicMorreyHypothesis) :
    ¬ (step67GraphAudit candidate hypothesis).EmitReadyWithGraph := by
  intro h
  exact h.2.1 (step67GraphAudit_blocksPromotion candidate hypothesis)

theorem step67GraphAudit_documents_blockers
    (candidate : CandidateShell)
    (hypothesis : ParabolicMorreyHypothesis) :
    (step67GraphAudit candidate hypothesis).blockersDocumented :=
  trivial

end CandidateObligationBridge
end NavierStokesProgram
