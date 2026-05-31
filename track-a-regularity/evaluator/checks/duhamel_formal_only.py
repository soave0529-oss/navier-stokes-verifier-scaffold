from __future__ import annotations

from schema import CheckResult, LemmaCandidate


DUHAMEL_FORMAL_ONLY_IDS = {
    "lemma_0209",
    "lemma_0219",
    "lemma_0229",
    "lemma_0239",
    "lemma_0249",
}


def check(candidate: LemmaCandidate) -> CheckResult:
    text = candidate.normalized_text
    if candidate.id in DUHAMEL_FORMAL_ONLY_IDS and "mild duhamel bilinear term" in text:
        return CheckResult(
            name="duhamel_formal_only_check",
            status="review",
            reason=(
                "Critical Duhamel bilinear family is formal vocabulary only until the real NSE "
                "bilinear operator, Leray projection, time integral, target space, and critical "
                "indices are specified."
            ),
            evidence={
                "family": "critical_duhamel_bilinear_formal_only",
                "artifact": "track-c-formal/lean/NavierStokesProgram/DuhamelBilinear.lean",
                "representatives": sorted(DUHAMEL_FORMAL_ONLY_IDS),
            },
        )

    return CheckResult(
        name="duhamel_formal_only_check",
        status="pass",
        reason="No critical Duhamel formal-only marker detected.",
    )
