from __future__ import annotations

from schema import CheckResult, LemmaCandidate


DUPLICATE_OF = {
    "lemma_0196": "lemma_0191",
    "lemma_0197": "lemma_0192",
    "lemma_0198": "lemma_0193",
    "lemma_0199": "lemma_0194",
    "lemma_0200": "lemma_0195",
}


def check(candidate: LemmaCandidate) -> CheckResult:
    primary = DUPLICATE_OF.get(candidate.id)
    if primary is None:
        return CheckResult(
            name="duplicate_family_check",
            status="pass",
            reason="No known duplicate-family marker detected.",
        )
    return CheckResult(
        name="duplicate_family_check",
        status="review",
        reason="Candidate duplicates an earlier survivor-family template and should not increase novelty count.",
        evidence={"primary": primary, "duplicate": candidate.id},
    )
