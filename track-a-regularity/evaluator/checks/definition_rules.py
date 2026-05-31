from __future__ import annotations

from schema import CheckResult, LemmaCandidate


def _has_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(pattern in text for pattern in patterns)


def check(candidate: LemmaCandidate) -> CheckResult:
    text = candidate.normalized_text

    if "dyadic nonlinear energy-flux" in text or "dyadic nonlinear energy flux" in text:
        if not _has_any(text, ("p_<=", "p_{<=n}", "pi_n", "shell projector", "normalization exponent")):
            return CheckResult(
                name="definition_rule_check",
                status="fail",
                reason="Dyadic flux candidates must specify shell projector convention and normalization exponent.",
                evidence={"family": "dyadic_flux"},
            )

    if "parabolic morrey" in text or "localized enstrophy concentration" in text:
        if not _has_any(text, ("q_r", "beta =", "r^{-1}", "parabolic cylinder", "sup_{x0,t0,r}")):
            return CheckResult(
                name="definition_rule_check",
                status="fail",
                reason="Parabolic Morrey enstrophy candidates must specify cylinder geometry and scaling exponent.",
                evidence={"family": "parabolic_morrey_enstrophy"},
            )

    if "vortex-stretching contribution" in text or "vortex stretching contribution" in text:
        if not _has_any(text, ("omega · s omega", "omega dot s omega", "h_lambda", "high-vorticity threshold")):
            return CheckResult(
                name="definition_rule_check",
                status="fail",
                reason="Vortex-stretching candidates must define stretching density and high-vorticity threshold.",
                evidence={"family": "localized_vortex_stretching"},
            )

    if "strain eigenvalue contribution" in text:
        if not _has_any(text, ("lambda_1", "lambda_3", "eigenvalue ordering", "xi · s xi")):
            return CheckResult(
                name="definition_rule_check",
                status="fail",
                reason="Strain eigenvalue candidates must specify eigenvalue ordering and the chosen strain proxy.",
                evidence={"family": "strain_eigenvalue"},
            )

    if "vorticity direction" in text and "superlevel" in text:
        if not _has_any(text, ("h_lambda", "gamma", "holder", "hölder", "lipschitz exponent")):
            return CheckResult(
                name="definition_rule_check",
                status="fail",
                reason="Vorticity-direction candidates must specify superlevel set, exponent, scale, and time norm.",
                evidence={"family": "vorticity_direction"},
            )

    return CheckResult(
        name="definition_rule_check",
        status="pass",
        reason="No selected-family definition-rule violation detected.",
    )
