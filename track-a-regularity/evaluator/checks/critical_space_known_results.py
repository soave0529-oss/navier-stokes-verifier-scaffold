from __future__ import annotations

from schema import CheckResult, LemmaCandidate


ANCHORS = {
    "critical_besov": [
        "Kato1984",
        "Planchon1996",
        "KochTataru2001",
        "CheskidovShvydkoy2007",
        "CheminPlanchon2011",
        "KochPlanchon2014",
    ],
    "critical_morrey": [
        "Kato1984",
        "KozonoYamazaki1994",
        "KochTataru2001",
    ],
}


def _fail(family: str, reason: str) -> CheckResult:
    return CheckResult(
        name="critical_space_known_result_check",
        status="fail",
        reason=reason,
        evidence={
            "family": family,
            "anchors": ANCHORS[family],
            "registry": "docs/KNOWN_CRITICAL_SPACE_CRITERIA.md",
        },
    )


def check(candidate: LemmaCandidate) -> CheckResult:
    text = candidate.normalized_text

    if "scale-critical besov-type norm" in text or "critical besov-type control" in text:
        return _fail(
            "critical_besov",
            "Broad critical Besov candidates overlap established Kato/Planchon/Koch-Tataru/Chemin-Planchon critical-space criteria until exact indices and novelty are supplied.",
        )

    if "scale-critical morrey norm" in text or "critical velocity morrey" in text:
        return _fail(
            "critical_morrey",
            "Broad critical velocity Morrey candidates overlap Morrey/Besov-Morrey and BMO^{-1} critical-space criteria until exact indices and novelty are supplied.",
        )

    return CheckResult(
        name="critical_space_known_result_check",
        status="pass",
        reason="No broad critical Besov/Morrey known-result trigger detected.",
    )
