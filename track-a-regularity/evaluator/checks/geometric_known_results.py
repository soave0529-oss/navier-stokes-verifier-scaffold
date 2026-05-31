from __future__ import annotations

from schema import CheckResult, LemmaCandidate


GEOMETRIC_ANCHORS = {
    "localized_vortex_stretching": [
        "ConstantinFefferman1993",
        "BeiraoDaVeigaBerselli2002",
        "Chae2007",
    ],
    "depleted_vortex_stretching": [
        "ConstantinFefferman1993",
        "BeiraoDaVeigaBerselli2002",
        "Chae2007",
        "Miller2021AnisotropicVorticity",
    ],
    "strain_eigenvalue": [
        "NeustupaPenel2005",
        "Miller2020MiddleEigenvalue",
        "Wu2021MiddleEigenvalue",
    ],
    "strain_vorticity_alignment": [
        "ConstantinFefferman1993",
        "Chae2007",
        "Miller2020MiddleEigenvalue",
        "Miller2021AnisotropicVorticity",
    ],
    "vorticity_direction": [
        "ConstantinFefferman1993",
        "BeiraoDaVeigaBerselli2002",
        "Miller2021AnisotropicVorticity",
    ],
}


def _fail(family: str, reason: str) -> CheckResult:
    return CheckResult(
        name="geometric_known_result_check",
        status="fail",
        reason=reason,
        evidence={
            "family": family,
            "anchors": GEOMETRIC_ANCHORS[family],
            "registry": "docs/KNOWN_GEOMETRIC_CRITERIA.md",
        },
    )


def check(candidate: LemmaCandidate) -> CheckResult:
    text = candidate.normalized_text

    if "vortex-stretching contribution" in text or "vortex stretching contribution" in text:
        return _fail(
            "localized_vortex_stretching",
            "Localized vortex-stretching candidates overlap known vorticity-direction/geometric depletion criteria before they are novel candidates.",
        )

    if "depleted vortex stretching" in text or "depleted_vortex_stretching" in text:
        return _fail(
            "depleted_vortex_stretching",
            "Depleted vortex-stretching candidates overlap known vorticity-direction and geometric depletion criteria until they specify a genuinely new critical norm.",
        )

    if "strain eigenvalue contribution" in text or "vorticity-weighted strain eigenvalue" in text:
        return _fail(
            "strain_eigenvalue",
            "Strain-eigenvalue candidates must be compared to middle-eigenvalue/deformation-tensor regularity criteria before promotion.",
        )

    if "strain-vorticity alignment defect" in text or "strain vorticity alignment defect" in text:
        return _fail(
            "strain_vorticity_alignment",
            "Strain-vorticity alignment-defect candidates overlap vorticity-direction and strain-eigenvalue criteria until the defect quantity and novelty gap are exact.",
        )

    if "vorticity direction" in text and "superlevel" in text:
        return _fail(
            "vorticity_direction",
            "Vorticity-direction candidates overlap Constantin-Fefferman and follow-up direction criteria before they are novel candidates.",
        )

    return CheckResult(
        name="geometric_known_result_check",
        status="pass",
        reason="No geometric known-result overlap trigger detected.",
    )
