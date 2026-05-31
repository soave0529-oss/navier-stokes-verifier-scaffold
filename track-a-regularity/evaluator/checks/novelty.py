from __future__ import annotations

from schema import CheckResult, LemmaCandidate


KNOWN_CONTROL_MARKERS = (
    "bkm",
    "prodi",
    "serrin",
)


def check(candidate: LemmaCandidate) -> CheckResult:
    known = " ".join(candidate.related_known).lower()
    if any(marker in known for marker in KNOWN_CONTROL_MARKERS):
        return CheckResult(
            name="novelty_check",
            status="known_control",
            reason="Candidate is a direct restatement or near-restatement of a known control theorem.",
            evidence={"related_known": list(candidate.related_known)},
        )
    return CheckResult(
        name="novelty_check",
        status="pass",
        reason="No direct BKM/Prodi-Serrin known-control marker detected.",
        evidence={"related_known": list(candidate.related_known)},
    )
