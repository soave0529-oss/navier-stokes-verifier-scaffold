from __future__ import annotations

from schema import CheckResult, LemmaCandidate


REQUIRED_HINTS = {
    "domain": ("t^3", "torus", "r^3", "whole space", "periodic"),
    "equation": ("navier-stokes", "nse"),
    "solution_class": ("smooth", "weak", "leray-hopf"),
    "time_interval": ("[0,t", "0 <= t", "0≤t", "past time t", "(0,t"),
    "viscosity": ("viscosity", "nu > 0", "ν > 0", "ν>0"),
}


def _missing_hints(text: str) -> list[str]:
    missing: list[str] = []
    for name, options in REQUIRED_HINTS.items():
        if not any(option in text for option in options):
            missing.append(name)
    return missing


def _is_known_control(candidate: LemmaCandidate) -> bool:
    known = " ".join(candidate.related_known).lower()
    return any(marker in known for marker in ("bkm", "prodi", "serrin"))


def check(candidate: LemmaCandidate) -> CheckResult:
    missing = _missing_hints(candidate.normalized_text)
    if not missing:
        return CheckResult(
            name="hypothesis_completeness_check",
            status="pass",
            reason="Domain, equation, solution class, time interval, and viscosity are syntactically explicit.",
        )
    if _is_known_control(candidate):
        return CheckResult(
            name="hypothesis_completeness_check",
            status="review",
            reason="Known-control candidate has missing or implicit hypotheses that must be made explicit before promotion.",
            evidence={"missing": missing},
        )
    return CheckResult(
        name="hypothesis_completeness_check",
        status="fail",
        reason="Candidate omits required PDE hypotheses.",
        evidence={"missing": missing},
    )
