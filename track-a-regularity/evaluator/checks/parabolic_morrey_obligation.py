from __future__ import annotations

from schema import CheckResult, LemmaCandidate


PARABOLIC_MORREY_EXACT_PATTERNS = (
    "parabolic morrey",
    "localized enstrophy concentration",
    "beta = 1",
    "sup_{x0,t0,r}",
)


def check(candidate: LemmaCandidate) -> CheckResult:
    text = candidate.normalized_text
    if candidate.id == "lemma_0252" and all(pattern in text for pattern in PARABOLIC_MORREY_EXACT_PATTERNS):
        return CheckResult(
            name="parabolic_morrey_obligation_check",
            status="review",
            reason=(
                "Proof-obligation memo found no finite-bound-to-smallness route; this exact "
                "parabolic Morrey statement needs a compactness/Liouville branch or a known-style "
                "epsilon/pressure rewrite before expert review."
            ),
            evidence={
                "family": "parabolic_morrey_enstrophy_exact",
                "audit": "docs/LEMMA_0252_PROOF_OBLIGATIONS.md",
                "formal_map": "docs/LEMMA_0252_LOCAL_ENERGY_FORMAL_MAP.md",
                "proof_obligation_graph": "docs/STEP64_PROOF_OBLIGATION_GRAPH.md",
                "lean_graph": "track-c-formal/lean/NavierStokesProgram/ProofObligationGraph.lean",
                "risk": "bounded critical local enstrophy does not by itself provide CKN epsilon smallness or pressure control",
            },
        )

    return CheckResult(
        name="parabolic_morrey_obligation_check",
        status="pass",
        reason="No exact parabolic Morrey proof-obligation marker detected.",
    )
