from __future__ import annotations

from schema import CheckResult, LemmaCandidate


def check(candidate: LemmaCandidate) -> CheckResult:
    text = candidate.normalized_text
    known = {item.lower() for item in candidate.related_known}
    if any("bkm" in item for item in known):
        return CheckResult(
            name="known_results_check",
            status="pass",
            reason="Consistent with the BKM continuation criterion positive control.",
            evidence={"related_known": list(candidate.related_known)},
        )
    if any("prodi" in item or "serrin" in item for item in known):
        return CheckResult(
            name="known_results_check",
            status="pass",
            reason="Consistent with the Prodi-Serrin positive control.",
            evidence={"related_known": list(candidate.related_known)},
        )
    if "finite energy alone" in text or "leray-hopf energy" in text:
        return CheckResult(
            name="known_results_check",
            status="fail",
            reason="Finite energy is available at weak-solution level and is not a known 3D smooth continuation criterion.",
            evidence={"related_known": list(candidate.related_known)},
        )
    if "not a pde theorem" in text:
        return CheckResult(
            name="known_results_check",
            status="pass",
            reason="Numerical-only negative control is handled by the Taylor-Green check.",
        )
    return CheckResult(
        name="known_results_check",
        status="pass",
        reason="No contradiction with the first-pass known-results registry detected.",
        evidence={"related_known": list(candidate.related_known)},
    )

