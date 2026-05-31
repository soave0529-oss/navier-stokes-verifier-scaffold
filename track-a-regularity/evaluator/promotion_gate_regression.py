from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from active_pool_ingress_audit import build_ingress_audit
from generation_spec_v4 import assess_candidate
from lemma_0252_blocker_closure_dashboard import build_blocker_closure_dashboard
from manual_promotion_packet import build_manual_promotion_report
from needs_review_blocker_sources import build_source_index, check_sources_exist
from promotion_dry_run_fixture import build_promotion_dry_run_report
from promotion_lifecycle_dashboard import build_lifecycle_dashboard
from proof_obligation_blockers import DEFAULT_INPUT as DEFAULT_PROOF_OBLIGATION_JSON
from proof_obligation_blockers import load_blocker_summary
from proposed_candidate_staging import DEFAULT_CANDIDATE_DIR, build_staging_audit
from run_all import evaluate
from schema import load_candidate
from v4_metadata_checklist import build_checklist


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "promotion_gate_regression.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "promotion_gate_regression.json"
DEFAULT_SMOKE_SUMMARY = ROOT / "logs/repro_20260520_182021/summary.md"
BLOCKER_CLOSURE_GATE_KEY = "lemma_0252_blocker_closure_not_blocked"
BLOCKER_CLOSURE_ARTIFACT = "track-a-regularity/reports/lemma_0252_blocker_closure_dashboard.json"
NON_CLAIMS = (
    "promotion_gate_regression_only",
    "read_only_dashboard",
    "temporary_dry_run_not_real_emission",
    "no_file_copy",
    "no_candidate_emission",
    "no_candidate_promotion",
    "no_navier_stokes_solution",
    "no_epsilon_regularity_theorem",
    "no_blocker_closure_discharge",
    "no_weak_to_smooth_upgrade",
)


@dataclass(frozen=True)
class GateCheck:
    gate_key: str
    artifact: str
    current_state: str
    required_for_real_emission: str
    status: str
    blocks_real_emission: bool
    dry_run_insufficient_reason: str


@dataclass(frozen=True)
class ClosureDependencyCheck:
    gate_key: str
    closure_artifact: str
    lemma_id: str
    closure_verdict: str
    unresolved_branch_count: int
    discharged_blocker_count: int
    candidate_emission_authorized: bool
    gate_present: bool
    gate_status: str
    gate_blocks_real_emission: bool
    gate_artifact_matches: bool
    gate_current_state_matches_closure: bool
    gate_blocks_when_closure_blocked: bool
    consistent: bool
    issues: tuple[str, ...]


@dataclass(frozen=True)
class PromotionGateRegression:
    schema_version: int
    candidate_dir: str
    dry_run_passed: bool
    dry_run_sufficient_for_real_emission: bool
    real_emission_ready: bool
    gate_count: int
    blocking_gate_count: int
    protective_gate_count: int
    passing_gate_count: int
    failure_gate_count: int
    closure_dependency: ClosureDependencyCheck
    gates: tuple[GateCheck, ...]
    non_claims: tuple[str, ...]


def _relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return str(path)


def _candidate_paths(candidate_dir: Path) -> tuple[Path, ...]:
    if not candidate_dir.exists():
        return ()
    return tuple(sorted(candidate_dir.glob("lemma_*.yaml")))


def _gate(
    *,
    gate_key: str,
    artifact: str,
    current_state: str,
    required_for_real_emission: str,
    status: str,
    blocks_real_emission: bool,
    dry_run_insufficient_reason: str,
) -> GateCheck:
    return GateCheck(
        gate_key=gate_key,
        artifact=artifact,
        current_state=current_state,
        required_for_real_emission=required_for_real_emission,
        status=status,
        blocks_real_emission=blocks_real_emission,
        dry_run_insufficient_reason=dry_run_insufficient_reason,
    )


def _preflight_counts(candidate_dir: Path) -> dict[str, int]:
    checked = 0
    skipped = 0
    blocked = 0
    for path in _candidate_paths(candidate_dir):
        candidate = load_candidate(path)
        if candidate.expected_evaluator.get("status") != "candidate":
            skipped += 1
            continue
        checked += 1
        if not assess_candidate(candidate).emit_ready:
            blocked += 1
    return {"checked": checked, "skipped": skipped, "blocked": blocked}


def _evaluation_summary(candidate_dir: Path) -> dict[str, Any]:
    status_counts: dict[str, int] = {}
    mismatch_ids: list[str] = []
    paths = _candidate_paths(candidate_dir)
    for path in paths:
        report = evaluate(load_candidate(path))
        status_counts[report.final_status] = status_counts.get(report.final_status, 0) + 1
        if not report.matches_expected:
            mismatch_ids.append(report.candidate.id)
    return {
        "candidate_count": len(paths),
        "matches_expected": not mismatch_ids,
        "mismatch_count": len(mismatch_ids),
        "mismatch_ids": mismatch_ids,
        "status_counts": status_counts,
    }


def _smoke_passed(path: Path) -> bool:
    if not path.exists():
        return False
    return "PASS: reproducibility smoke check completed." in path.read_text(
        encoding="utf-8",
        errors="replace",
    )


def _closure_state_string(closure_dashboard: Any) -> str:
    return (
        f"lemma_id={closure_dashboard.lemma_id}, "
        f"closure_verdict={closure_dashboard.closure_verdict}, "
        f"unresolved_branch_count={closure_dashboard.unresolved_branch_count}, "
        f"discharged_blocker_count={closure_dashboard.discharged_blocker_count}, "
        f"candidate_emission_authorized="
        f"{str(closure_dashboard.candidate_emission_authorized).lower()}"
    )


def _expected_closure_gate_blocks(closure_dashboard: Any) -> bool:
    return (
        closure_dashboard.closure_verdict == "blocked_no_discharge"
        or not closure_dashboard.candidate_emission_authorized
    )


def _expected_closure_gate_status(closure_dashboard: Any) -> str:
    if not _expected_closure_gate_blocks(closure_dashboard):
        return "pass"
    return "blocked"


def _build_closure_dependency(
    *,
    closure_dashboard: Any,
    gates: tuple[GateCheck, ...],
) -> ClosureDependencyCheck:
    gate = next((item for item in gates if item.gate_key == BLOCKER_CLOSURE_GATE_KEY), None)
    expected_state = _closure_state_string(closure_dashboard)
    expected_blocks = _expected_closure_gate_blocks(closure_dashboard)
    expected_status = _expected_closure_gate_status(closure_dashboard)
    issues: list[str] = []

    gate_present = gate is not None
    gate_status = gate.status if gate else "missing"
    gate_blocks_real_emission = gate.blocks_real_emission if gate else False
    gate_artifact_matches = gate.artifact == BLOCKER_CLOSURE_ARTIFACT if gate else False
    gate_current_state_matches_closure = gate.current_state == expected_state if gate else False
    gate_blocks_when_closure_blocked = (
        gate_present
        and gate_status == expected_status
        and gate_blocks_real_emission == expected_blocks
    )

    if not gate_present:
        issues.append("missing_closure_dependency_gate")
    if gate_present and not gate_artifact_matches:
        issues.append("closure_gate_artifact_mismatch")
    if gate_present and not gate_current_state_matches_closure:
        issues.append("closure_gate_current_state_mismatch")
    if gate_present and not gate_blocks_when_closure_blocked:
        issues.append("closure_gate_blocking_semantics_mismatch")

    return ClosureDependencyCheck(
        gate_key=BLOCKER_CLOSURE_GATE_KEY,
        closure_artifact=BLOCKER_CLOSURE_ARTIFACT,
        lemma_id=closure_dashboard.lemma_id,
        closure_verdict=closure_dashboard.closure_verdict,
        unresolved_branch_count=closure_dashboard.unresolved_branch_count,
        discharged_blocker_count=closure_dashboard.discharged_blocker_count,
        candidate_emission_authorized=closure_dashboard.candidate_emission_authorized,
        gate_present=gate_present,
        gate_status=gate_status,
        gate_blocks_real_emission=gate_blocks_real_emission,
        gate_artifact_matches=gate_artifact_matches,
        gate_current_state_matches_closure=gate_current_state_matches_closure,
        gate_blocks_when_closure_blocked=gate_blocks_when_closure_blocked,
        consistent=not issues,
        issues=tuple(issues),
    )


def build_gate_regression(
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
    smoke_summary: Path = DEFAULT_SMOKE_SUMMARY,
) -> PromotionGateRegression:
    staging = build_staging_audit(candidate_dir=candidate_dir)
    packet = build_manual_promotion_report(candidate_dir=candidate_dir)
    ingress = build_ingress_audit(candidate_dir=candidate_dir)
    lifecycle = build_lifecycle_dashboard(candidate_dir=candidate_dir)
    dry_run = build_promotion_dry_run_report()
    checklist = build_checklist()
    proof_summary = load_blocker_summary(DEFAULT_PROOF_OBLIGATION_JSON)
    closure_dashboard = build_blocker_closure_dashboard(
        proof_obligation_json=DEFAULT_PROOF_OBLIGATION_JSON,
    )
    source_index = build_source_index()
    sources_exist, sources_message = check_sources_exist(source_index)
    preflight = _preflight_counts(candidate_dir)
    evaluation = _evaluation_summary(candidate_dir)
    smoke_passed = _smoke_passed(smoke_summary)

    gates = (
        _gate(
            gate_key="temporary_promotion_dry_run",
            artifact="track-a-regularity/reports/promotion_dry_run_fixture.json",
            current_state=(
                f"dry_run_passed={str(dry_run.dry_run_passed).lower()}, "
                f"real_candidate_pool_untouched={str(dry_run.real_candidate_pool_untouched).lower()}, "
                f"phase_count={len(dry_run.phases)}"
            ),
            required_for_real_emission="synthetic lifecycle fixture must keep the real candidate pool untouched",
            status="pass" if dry_run.dry_run_passed and dry_run.real_candidate_pool_untouched else "fail",
            blocks_real_emission=not (dry_run.dry_run_passed and dry_run.real_candidate_pool_untouched),
            dry_run_insufficient_reason=(
                "This only proves the plumbing can accept a synthetic zero-blocker record in a "
                "temporary directory; it does not discharge any real candidate proof obligation."
            ),
        ),
        _gate(
            gate_key="staged_candidate_ready",
            artifact="track-a-regularity/reports/proposed_candidate_staging_audit.json",
            current_state=(
                f"proposal_count={staging.proposal_count}, ready_count={staging.ready_count}, "
                f"blocked_count={staging.blocked_count}, rejected_count={staging.rejected_count}"
            ),
            required_for_real_emission="at least one real staged candidate must be ready_for_manual_copy",
            status="pass" if staging.ready_count > 0 else "blocked",
            blocks_real_emission=staging.ready_count == 0,
            dry_run_insufficient_reason=(
                "The canonical staged object is still the blocked template; the temporary dry-run "
                "does not create a real staged candidate."
            ),
        ),
        _gate(
            gate_key="manual_promotion_packet_ready",
            artifact="track-a-regularity/reports/manual_promotion_packet.json",
            current_state=(
                f"packet_count={packet.packet_count}, ready_packet_count={packet.ready_packet_count}, "
                f"blocked_packet_count={packet.blocked_packet_count}, rejected_packet_count={packet.rejected_packet_count}"
            ),
            required_for_real_emission="a real staged candidate must have a ready no-copy manual packet",
            status="pass" if packet.ready_packet_count > 0 else "blocked",
            blocks_real_emission=packet.ready_packet_count == 0,
            dry_run_insufficient_reason=(
                "The dry-run packet is built under a temporary root and is intentionally not a real "
                "manual-copy authorization."
            ),
        ),
        _gate(
            gate_key="promotion_lifecycle_ready_or_authorized",
            artifact="track-a-regularity/reports/promotion_lifecycle_dashboard.json",
            current_state=(
                f"lifecycle_ready_count={lifecycle.lifecycle_ready_count}, "
                f"lifecycle_authorized_count={lifecycle.lifecycle_authorized_count}, "
                f"lifecycle_blocked_count={lifecycle.lifecycle_blocked_count}, "
                f"lifecycle_violation_count={lifecycle.lifecycle_violation_count}"
            ),
            required_for_real_emission="a real lifecycle entry must be ready or already authorized",
            status=(
                "pass"
                if lifecycle.lifecycle_ready_count > 0 or lifecycle.lifecycle_authorized_count > 0
                else "blocked"
            ),
            blocks_real_emission=(
                lifecycle.lifecycle_ready_count == 0 and lifecycle.lifecycle_authorized_count == 0
            ),
            dry_run_insufficient_reason=(
                "The canonical lifecycle remains blocked_in_staging even though the temporary "
                "fixture exercises the ready and authorized paths."
            ),
        ),
        _gate(
            gate_key="active_pool_ingress_clean",
            artifact="track-a-regularity/reports/active_pool_ingress_audit.json",
            current_state=(
                f"active_candidate_file_count={ingress.active_candidate_file_count}, "
                f"legacy_skipped_count={ingress.legacy_skipped_count}, "
                f"authorized_ingress_count={ingress.authorized_ingress_count}, "
                f"violation_count={ingress.violation_count}"
            ),
            required_for_real_emission="active pool must have no unauthorized v4/template-like ingress",
            status="protective_pass" if ingress.violation_count == 0 else "fail",
            blocks_real_emission=ingress.violation_count > 0,
            dry_run_insufficient_reason=(
                "A clean active pool is necessary, but it does not identify a real zero-blocker "
                "candidate to promote."
            ),
        ),
        _gate(
            gate_key="v4_metadata_checklist_template_safe",
            artifact="track-a-regularity/reports/v4_candidate_metadata_checklist.json",
            current_state=(
                f"marker_count={checklist.marker_count}, "
                f"expected_evaluator_key_count={checklist.expected_evaluator_key_count}, "
                f"template_safe={str(not checklist.template_safety.issues).lower()}"
            ),
            required_for_real_emission="future YAML must include every v4 marker and expected_evaluator sidecar",
            status="protective_pass" if not checklist.template_safety.issues else "fail",
            blocks_real_emission=bool(checklist.template_safety.issues),
            dry_run_insufficient_reason=(
                "The checklist describes required metadata; it is not a mathematical proof route."
            ),
        ),
        _gate(
            gate_key="proof_obligation_zero_blocker_real_candidate",
            artifact="track-a-regularity/reports/lemma_0252_proof_obligation_graph.json",
            current_state=(
                f"lemma_id={proof_summary.lemma_id}, candidate_status={proof_summary.candidate_status}, "
                f"active_candidate={str(proof_summary.active_candidate).lower()}, "
                f"promotion_blocker_count={proof_summary.promotion_blocker_count}"
            ),
            required_for_real_emission="candidate-specific proof-obligation report must have zero promotion blockers",
            status="pass" if proof_summary.promotion_blocker_count == 0 and proof_summary.active_candidate else "blocked",
            blocks_real_emission=not (
                proof_summary.promotion_blocker_count == 0 and proof_summary.active_candidate
            ),
            dry_run_insufficient_reason=(
                "The temporary dry-run uses synthetic discharged obligations; lemma_0252 still records "
                "real promotion blockers."
            ),
        ),
        _gate(
            gate_key=BLOCKER_CLOSURE_GATE_KEY,
            artifact=BLOCKER_CLOSURE_ARTIFACT,
            current_state=_closure_state_string(closure_dashboard),
            required_for_real_emission=(
                "closure dashboard must no longer report blocked_no_discharge and must authorize "
                "candidate emission after genuine blocker discharge"
            ),
            status=_expected_closure_gate_status(closure_dashboard),
            blocks_real_emission=_expected_closure_gate_blocks(closure_dashboard),
            dry_run_insufficient_reason=(
                "The closure dashboard joins the known-theorem mapping and all three branch "
                "checklists; while it reports blocked_no_discharge, plumbing-level dry-runs and "
                "older blocker counts cannot authorize real emission."
            ),
        ),
        _gate(
            gate_key="blocker_source_index_fresh",
            artifact="track-a-regularity/reports/needs_review_blocker_sources.json",
            current_state=(
                f"source_count={source_index.source_count}, "
                f"missing_source_count={source_index.missing_source_count}, "
                f"sources_exist={str(sources_exist).lower()}"
            ),
            required_for_real_emission="blocker provenance source index must be fresh and all source refs must exist",
            status="protective_pass" if sources_exist else "fail",
            blocks_real_emission=not sources_exist,
            dry_run_insufficient_reason=(
                f"{sources_message}; provenance freshness is still separate from proof discharge."
            ),
        ),
        _gate(
            gate_key="v4_preflight_current_pool",
            artifact="track-a-regularity/evaluator/preflight_v4.py",
            current_state=(
                f"checked={preflight['checked']}, skipped={preflight['skipped']}, "
                f"blocked={preflight['blocked']}"
            ),
            required_for_real_emission="at least one current-pool candidate-status YAML must pass v4 preflight",
            status="pass" if preflight["checked"] > 0 and preflight["blocked"] == 0 else "blocked",
            blocks_real_emission=preflight["checked"] == 0 or preflight["blocked"] > 0,
            dry_run_insufficient_reason=(
                "Current preflight checks no active candidate-status YAML; the synthetic dry-run is "
                "outside the real active pool."
            ),
        ),
        _gate(
            gate_key="evaluator_expected_check_current_pool",
            artifact="track-a-regularity/evaluator/run_all.py --check-expected",
            current_state=(
                f"candidate_count={evaluation['candidate_count']}, "
                f"matches_expected={str(evaluation['matches_expected']).lower()}, "
                f"mismatch_count={evaluation['mismatch_count']}, "
                f"status_counts={evaluation['status_counts']}"
            ),
            required_for_real_emission="current evaluator expectations must remain coherent",
            status="protective_pass" if evaluation["matches_expected"] else "fail",
            blocks_real_emission=not evaluation["matches_expected"],
            dry_run_insufficient_reason=(
                "Evaluator coherence prevents regressions but does not make a blocked record an "
                "active candidate."
            ),
        ),
        _gate(
            gate_key="full_reproducibility_smoke_reference",
            artifact=_relative(smoke_summary),
            current_state=f"exists={str(smoke_summary.exists()).lower()}, pass={str(smoke_passed).lower()}",
            required_for_real_emission="a full reproducibility smoke must be available and passing",
            status="protective_pass" if smoke_passed else "fail",
            blocks_real_emission=not smoke_passed,
            dry_run_insufficient_reason=(
                "A passing smoke test is a regression guard; it does not prove the analytic bridge."
            ),
        ),
    )

    blocking = sum(1 for gate in gates if gate.status == "blocked" or gate.blocks_real_emission)
    protective = sum(1 for gate in gates if gate.status == "protective_pass")
    passing = sum(1 for gate in gates if gate.status == "pass")
    failures = sum(1 for gate in gates if gate.status == "fail")
    closure_dependency = _build_closure_dependency(
        closure_dashboard=closure_dashboard,
        gates=gates,
    )
    real_ready = blocking == 0 and failures == 0 and dry_run.dry_run_passed
    return PromotionGateRegression(
        schema_version=1,
        candidate_dir=_relative(candidate_dir),
        dry_run_passed=dry_run.dry_run_passed,
        dry_run_sufficient_for_real_emission=False,
        real_emission_ready=real_ready,
        gate_count=len(gates),
        blocking_gate_count=blocking,
        protective_gate_count=protective,
        passing_gate_count=passing,
        failure_gate_count=failures,
        closure_dependency=closure_dependency,
        gates=gates,
        non_claims=NON_CLAIMS,
    )


def gate_regression_to_dict(regression: PromotionGateRegression) -> dict[str, object]:
    return {
        "schema_version": regression.schema_version,
        "candidate_dir": regression.candidate_dir,
        "dry_run_passed": regression.dry_run_passed,
        "dry_run_sufficient_for_real_emission": regression.dry_run_sufficient_for_real_emission,
        "real_emission_ready": regression.real_emission_ready,
        "gate_count": regression.gate_count,
        "blocking_gate_count": regression.blocking_gate_count,
        "protective_gate_count": regression.protective_gate_count,
        "passing_gate_count": regression.passing_gate_count,
        "failure_gate_count": regression.failure_gate_count,
        "closure_dependency": asdict(regression.closure_dependency),
        "gates": [asdict(gate) for gate in regression.gates],
        "non_claims": list(regression.non_claims),
        "docs": {
            "staging_doc": "docs/STEP81_PROPOSED_CANDIDATE_STAGING.md",
            "manual_packet_doc": "docs/STEP82_MANUAL_PROMOTION_PACKET.md",
            "ingress_doc": "docs/STEP83_ACTIVE_POOL_INGRESS_AUDIT.md",
            "lifecycle_doc": "docs/STEP84_PROMOTION_LIFECYCLE_DASHBOARD.md",
            "dry_run_doc": "docs/STEP85_PROMOTION_DRY_RUN_FIXTURE.md",
            "gate_regression_doc": "docs/STEP86_PROMOTION_GATE_REGRESSION.md",
            "blocker_closure_doc": "docs/STEP91_BLOCKER_CLOSURE_DASHBOARD.md",
            "v4_spec": "docs/CANDIDATE_GENERATION_SPEC_V4.md",
            "freeze_doc": "docs/CANDIDATE_GENERATION_FREEZE.md",
        },
    }


def _format_reason(text: str) -> str:
    return text.replace("|", "\\|")


def _gate_rows(regression: PromotionGateRegression) -> list[str]:
    rows = [
        "| gate | status | blocks real emission | current state | required state | why dry-run is insufficient |",
        "|---|---|---|---|---|---|",
    ]
    for gate in regression.gates:
        rows.append(
            "| "
            f"`{gate.gate_key}` | "
            f"`{gate.status}` | "
            f"`{str(gate.blocks_real_emission).lower()}` | "
            f"`{_format_reason(gate.current_state)}` | "
            f"{_format_reason(gate.required_for_real_emission)} | "
            f"{_format_reason(gate.dry_run_insufficient_reason)} |"
        )
    return rows


def _closure_dependency_rows(regression: PromotionGateRegression) -> list[str]:
    dependency = regression.closure_dependency
    return [
        "| field | value |",
        "|---|---:|",
        f"| gate_key | `{dependency.gate_key}` |",
        f"| closure_artifact | `{dependency.closure_artifact}` |",
        f"| closure_verdict | `{dependency.closure_verdict}` |",
        f"| unresolved_branch_count | {dependency.unresolved_branch_count} |",
        f"| discharged_blocker_count | {dependency.discharged_blocker_count} |",
        f"| candidate_emission_authorized | `{str(dependency.candidate_emission_authorized).lower()}` |",
        f"| gate_present | `{str(dependency.gate_present).lower()}` |",
        f"| gate_artifact_matches | `{str(dependency.gate_artifact_matches).lower()}` |",
        f"| gate_current_state_matches_closure | `{str(dependency.gate_current_state_matches_closure).lower()}` |",
        f"| gate_blocks_when_closure_blocked | `{str(dependency.gate_blocks_when_closure_blocked).lower()}` |",
        f"| consistent | `{str(dependency.consistent).lower()}` |",
        f"| issues | `{', '.join(dependency.issues) or 'none'}` |",
    ]


def render_markdown(regression: PromotionGateRegression) -> str:
    return "\n".join(
        (
            "# Promotion Gate Regression",
            "",
            "Generated by `track-a-regularity/evaluator/promotion_gate_regression.py`.",
            "",
            "This read-only dashboard explains why the temporary promotion dry-run is necessary",
            "but not sufficient for real candidate emission. It ties real-emission readiness to",
            "the staging, manual packet, lifecycle, ingress, v4 preflight, proof-obligation,",
            "blocker-closure, source-index, evaluator, and full-smoke gates.",
            "",
            "## Summary",
            "",
            f"- candidate_dir: `{regression.candidate_dir}`",
            f"- dry_run_passed: `{str(regression.dry_run_passed).lower()}`",
            "- dry_run_sufficient_for_real_emission: "
            f"`{str(regression.dry_run_sufficient_for_real_emission).lower()}`",
            f"- real_emission_ready: `{str(regression.real_emission_ready).lower()}`",
            f"- gate_count: `{regression.gate_count}`",
            f"- blocking_gate_count: `{regression.blocking_gate_count}`",
            f"- protective_gate_count: `{regression.protective_gate_count}`",
            f"- passing_gate_count: `{regression.passing_gate_count}`",
            f"- failure_gate_count: `{regression.failure_gate_count}`",
            "",
            "## Closure Dependency",
            "",
            "This section checks that the promotion gate is still reading the Step 91",
            "`lemma_0252` blocker-closure dashboard and has not drifted into an independent",
            "or stale interpretation of the closure state.",
            "",
            *_closure_dependency_rows(regression),
            "",
            "## Gate Checks",
            "",
            *_gate_rows(regression),
            "",
            "## Non-Claims",
            "",
            *(f"- `{item}`" for item in regression.non_claims),
            "",
        )
    )


def render_json(regression: PromotionGateRegression) -> str:
    return json.dumps(gate_regression_to_dict(regression), indent=2, sort_keys=True) + "\n"


def render_output(regression: PromotionGateRegression, output_format: str) -> str:
    if output_format == "markdown":
        return render_markdown(regression)
    if output_format == "json":
        return render_json(regression)
    raise ValueError(f"unknown promotion gate regression format: {output_format}")


def write_output(output: Path, regression: PromotionGateRegression, output_format: str) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(regression, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    regression: PromotionGateRegression,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(regression, output_format)
    if not output.exists():
        return False, f"missing promotion gate regression dashboard: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale promotion gate regression dashboard: {output}"
    return True, f"fresh promotion gate regression dashboard: {output}"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown promotion gate regression format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a read-only regression dashboard for real candidate promotion gates."
    )
    parser.add_argument("--candidate-dir", type=Path, default=DEFAULT_CANDIDATE_DIR)
    parser.add_argument("--smoke-summary", type=Path, default=DEFAULT_SMOKE_SUMMARY)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--check-output",
        action="store_true",
        help="Check that --output already matches the rendered dashboard.",
    )
    parser.add_argument(
        "--require-not-ready",
        action="store_true",
        help="Fail if the real-emission gate unexpectedly reports ready.",
    )
    parser.add_argument(
        "--require-clean",
        action="store_true",
        help="Fail on any hard regression failure such as stale smoke, source, or ingress violations.",
    )
    parser.add_argument(
        "--require-closure-dependency",
        action="store_true",
        help="Fail if the closure gate no longer matches the Step 91 blocker-closure dashboard.",
    )
    args = parser.parse_args(argv)

    try:
        regression = build_gate_regression(
            candidate_dir=args.candidate_dir,
            smoke_summary=args.smoke_summary,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report dashboard setup failures.
        print(f"failed to build promotion gate regression dashboard: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, regression, args.format)
        print(message)
        if not ok:
            print("run without --check-output to regenerate the promotion gate regression dashboard", file=sys.stderr)
            return 1
    else:
        written = write_output(output, regression, args.format)
        print(f"wrote {written}")

    if args.require_not_ready and regression.real_emission_ready:
        print("real candidate emission unexpectedly reports ready", file=sys.stderr)
        return 1
    if args.require_clean and regression.failure_gate_count:
        print("promotion gate regression contains hard failures", file=sys.stderr)
        return 1
    if args.require_closure_dependency and not regression.closure_dependency.consistent:
        print(
            "promotion gate regression closure dependency is inconsistent: "
            f"{', '.join(regression.closure_dependency.issues)}",
            file=sys.stderr,
        )
        return 1

    print(f"dry_run_passed: {str(regression.dry_run_passed).lower()}")
    print(
        "dry_run_sufficient_for_real_emission: "
        f"{str(regression.dry_run_sufficient_for_real_emission).lower()}"
    )
    print(f"real_emission_ready: {str(regression.real_emission_ready).lower()}")
    print(f"gate_count: {regression.gate_count}")
    print(f"blocking_gate_count: {regression.blocking_gate_count}")
    print(f"failure_gate_count: {regression.failure_gate_count}")
    print(f"closure_dependency_consistent: {str(regression.closure_dependency.consistent).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
