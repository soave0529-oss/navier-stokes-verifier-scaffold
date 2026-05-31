from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from promotion_gate_analytic_prerequisite_dependency import (
    DEFAULT_JSON_OUTPUT as DEFAULT_DEPENDENCY_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_DEPENDENCY_MARKDOWN_OUTPUT,
    build_analytic_prerequisite_dependency_report,
    dependency_report_to_dict,
)
from promotion_gate_analytic_prerequisites import (
    DEFAULT_JSON_OUTPUT as DEFAULT_PACKET_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_PACKET_MARKDOWN_OUTPUT,
    EXPECTED_FAMILIES,
    AnalyticPrerequisite,
    build_analytic_prerequisite_packet,
    packet_to_dict,
)
from promotion_gate_regression import DEFAULT_CANDIDATE_DIR, DEFAULT_SMOKE_SUMMARY
from proof_obligation_blockers import DEFAULT_INPUT as DEFAULT_PROOF_GRAPH_JSON


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "promotion_gate_analytic_work_order_matrix.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "promotion_gate_analytic_work_order_matrix.json"

SOURCE_BRANCH_BY_PREREQUISITE = {
    "proof_obligation.zero_promotion_blockers": "proof_obligation_graph",
    "proof_obligation.finite_bound_to_smallness.discharge_artifact": "finite_bound_to_smallness",
    "proof_obligation.compactness_liouville.discharge_artifact": "compactness_liouville",
    "proof_obligation.smooth_continuation_bridge.discharge_artifact": "smooth_continuation_bridge",
    "closure.verdict_not_blocked": "closure_dashboard",
    "closure.no_unresolved_branches": "closure_branch_resolution",
    "closure.all_substantive_blockers_discharged": "closure_substantive_blockers",
    "closure.candidate_emission_authorized": "closure_candidate_authorization",
}

ARTIFACT_TYPE_BY_PREREQUISITE = {
    "proof_obligation.zero_promotion_blockers": "zero_blocker_proof_graph_update",
    "proof_obligation.finite_bound_to_smallness.discharge_artifact": (
        "finite_bound_to_smallness_discharge_bundle"
    ),
    "proof_obligation.compactness_liouville.discharge_artifact": (
        "compactness_liouville_discharge_bundle"
    ),
    "proof_obligation.smooth_continuation_bridge.discharge_artifact": (
        "smooth_continuation_discharge_bundle"
    ),
    "closure.verdict_not_blocked": "closure_dashboard_refresh",
    "closure.no_unresolved_branches": "branch_resolution_artifact_set",
    "closure.all_substantive_blockers_discharged": "substantive_blocker_discharge_bundle",
    "closure.candidate_emission_authorized": "candidate_emission_authorization_record",
}

DEPENDENCY_KEYS_BY_PREREQUISITE = {
    "proof_obligation.zero_promotion_blockers": (
        "packet.promotion_blocker_count.matches_proof_graph",
        "packet.proof_prerequisite_keys.match_proof_blockers",
    ),
    "proof_obligation.finite_bound_to_smallness.discharge_artifact": (
        "packet.proof_prerequisite_keys.match_proof_blockers",
    ),
    "proof_obligation.compactness_liouville.discharge_artifact": (
        "packet.proof_prerequisite_keys.match_proof_blockers",
    ),
    "proof_obligation.smooth_continuation_bridge.discharge_artifact": (
        "packet.proof_prerequisite_keys.match_proof_blockers",
    ),
    "closure.verdict_not_blocked": (
        "packet.closure_verdict.matches_closure_dashboard",
        "packet.closure_prerequisite_keys.match_expected_closure_keys",
    ),
    "closure.no_unresolved_branches": (
        "packet.closure_unresolved_branch_count.matches_closure_dashboard",
        "packet.closure_prerequisite_keys.match_expected_closure_keys",
    ),
    "closure.all_substantive_blockers_discharged": (
        "packet.closure_discharged_blocker_count.matches_closure_dashboard",
        "packet.closure_prerequisite_keys.match_expected_closure_keys",
    ),
    "closure.candidate_emission_authorized": (
        "packet.closure_prerequisite_keys.match_expected_closure_keys",
        "packet.process_gate_open_authorized.remains_false",
    ),
}

NON_CLAIMS = (
    "analytic_work_order_matrix_only",
    "read_only_discharge_planning",
    "no_process_gate_opened",
    "no_file_copy",
    "no_candidate_emission",
    "no_candidate_promotion",
    "no_blocker_discharge",
    "no_navier_stokes_solution",
    "no_epsilon_regularity_theorem",
    "no_compactness_or_liouville_theorem",
    "no_weak_to_smooth_upgrade",
)


@dataclass(frozen=True)
class AnalyticWorkOrder:
    work_order_id: str
    family: str
    source_branch: str
    prerequisite_key: str
    required_artifact_type: str
    current_state: str
    required_state: str
    status: str
    actionable_now: bool
    blocks_process_gate_open: bool
    dependency_guard_keys: tuple[str, ...]
    source_artifact: str
    operator_instruction: str


@dataclass(frozen=True)
class SourceBranchSummary:
    source_branch: str
    work_order_count: int
    artifact_types: tuple[str, ...]
    families: tuple[str, ...]
    actionable_count: int
    blocked_count: int


@dataclass(frozen=True)
class ArtifactTypeSummary:
    required_artifact_type: str
    work_order_count: int
    source_branches: tuple[str, ...]
    families: tuple[str, ...]


@dataclass(frozen=True)
class AnalyticWorkOrderMatrix:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    analytic_families: tuple[str, ...]
    work_order_count: int
    blocked_work_order_count: int
    actionable_work_order_count: int
    artifact_type_count: int
    source_branch_count: int
    dependency_consistent: bool
    process_gate_open_authorized: bool
    process_gate_open_blocked_by: tuple[str, ...]
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    issues: tuple[str, ...]
    work_orders: tuple[AnalyticWorkOrder, ...]
    source_branch_summaries: tuple[SourceBranchSummary, ...]
    artifact_type_summaries: tuple[ArtifactTypeSummary, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]


def _operator_instruction(item: AnalyticPrerequisite, artifact_type: str) -> str:
    if item.family == "proof_obligation":
        return (
            f"Produce a reviewed `{artifact_type}` for `{item.prerequisite_key}` before "
            "editing blocker status or reopening process gates."
        )
    return (
        f"Produce `{artifact_type}` before refreshing closure evidence; the cited analytic "
        "branches must already have real discharge artifacts."
    )


def _work_orders(prerequisites: tuple[AnalyticPrerequisite, ...]) -> tuple[AnalyticWorkOrder, ...]:
    orders: list[AnalyticWorkOrder] = []
    for index, item in enumerate(prerequisites, start=1):
        source_branch = SOURCE_BRANCH_BY_PREREQUISITE.get(item.prerequisite_key, "unknown")
        artifact_type = ARTIFACT_TYPE_BY_PREREQUISITE.get(
            item.prerequisite_key, "reviewed_discharge_artifact"
        )
        status = "satisfied" if item.satisfied else "blocked_pending_discharge"
        orders.append(
            AnalyticWorkOrder(
                work_order_id=f"wo_{index:03d}",
                family=item.family,
                source_branch=source_branch,
                prerequisite_key=item.prerequisite_key,
                required_artifact_type=artifact_type,
                current_state=item.current_state,
                required_state=item.required_state,
                status=status,
                actionable_now=False,
                blocks_process_gate_open=item.blocks_process_gate_open,
                dependency_guard_keys=DEPENDENCY_KEYS_BY_PREREQUISITE.get(
                    item.prerequisite_key, ()
                ),
                source_artifact=item.source_artifact,
                operator_instruction=_operator_instruction(item, artifact_type),
            )
        )
    return tuple(orders)


def _source_branch_summaries(
    work_orders: tuple[AnalyticWorkOrder, ...]
) -> tuple[SourceBranchSummary, ...]:
    summaries: list[SourceBranchSummary] = []
    for branch in sorted({order.source_branch for order in work_orders}):
        branch_orders = tuple(order for order in work_orders if order.source_branch == branch)
        summaries.append(
            SourceBranchSummary(
                source_branch=branch,
                work_order_count=len(branch_orders),
                artifact_types=tuple(sorted({order.required_artifact_type for order in branch_orders})),
                families=tuple(sorted({order.family for order in branch_orders})),
                actionable_count=sum(1 for order in branch_orders if order.actionable_now),
                blocked_count=sum(
                    1 for order in branch_orders if order.status == "blocked_pending_discharge"
                ),
            )
        )
    return tuple(summaries)


def _artifact_type_summaries(
    work_orders: tuple[AnalyticWorkOrder, ...]
) -> tuple[ArtifactTypeSummary, ...]:
    summaries: list[ArtifactTypeSummary] = []
    for artifact_type in sorted({order.required_artifact_type for order in work_orders}):
        artifact_orders = tuple(
            order for order in work_orders if order.required_artifact_type == artifact_type
        )
        summaries.append(
            ArtifactTypeSummary(
                required_artifact_type=artifact_type,
                work_order_count=len(artifact_orders),
                source_branches=tuple(sorted({order.source_branch for order in artifact_orders})),
                families=tuple(sorted({order.family for order in artifact_orders})),
            )
        )
    return tuple(summaries)


def _missing_sources(source_refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(source for source in source_refs if not (ROOT / source).exists())


def build_analytic_work_order_matrix(
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
    smoke_summary: Path = DEFAULT_SMOKE_SUMMARY,
    proof_graph_json: Path = DEFAULT_PROOF_GRAPH_JSON,
) -> AnalyticWorkOrderMatrix:
    packet = build_analytic_prerequisite_packet(
        candidate_dir=candidate_dir,
        smoke_summary=smoke_summary,
        proof_graph_json=proof_graph_json,
    )
    dependency = build_analytic_prerequisite_dependency_report(
        candidate_dir=candidate_dir,
        smoke_summary=smoke_summary,
        proof_graph_json=proof_graph_json,
    )
    work_orders = _work_orders(packet.prerequisites)
    source_refs = tuple(
        dict.fromkeys(
            (
                "track-a-regularity/reports/promotion_gate_analytic_prerequisites.md",
                "track-a-regularity/reports/promotion_gate_analytic_prerequisites.json",
                "track-a-regularity/reports/promotion_gate_analytic_prerequisite_dependency.md",
                "track-a-regularity/reports/promotion_gate_analytic_prerequisite_dependency.json",
                *(order.source_artifact for order in work_orders),
            )
        )
    )
    missing_sources = _missing_sources(source_refs)
    blocked_count = sum(1 for order in work_orders if order.status == "blocked_pending_discharge")
    actionable_count = sum(1 for order in work_orders if order.actionable_now)
    issues: list[str] = []
    if len(work_orders) != packet.prerequisite_count:
        issues.append("work_order_count_mismatch")
    if not dependency.dependency_consistent:
        issues.append("dependency_inconsistent")
    if missing_sources:
        issues.append("missing_sources")
    if actionable_count:
        issues.append("unexpected_actionable_work_orders")
    if packet.process_gate_open_authorized:
        issues.append("process_gate_open_authorized")

    return AnalyticWorkOrderMatrix(
        schema_version=1,
        lemma_id=packet.lemma_id,
        candidate_status=packet.candidate_status,
        active_candidate=packet.active_candidate,
        analytic_families=EXPECTED_FAMILIES,
        work_order_count=len(work_orders),
        blocked_work_order_count=blocked_count,
        actionable_work_order_count=actionable_count,
        artifact_type_count=len({order.required_artifact_type for order in work_orders}),
        source_branch_count=len({order.source_branch for order in work_orders}),
        dependency_consistent=dependency.dependency_consistent,
        process_gate_open_authorized=packet.process_gate_open_authorized,
        process_gate_open_blocked_by=packet.process_gate_open_blocked_by,
        blocker_state_changed=False,
        candidate_emission_authorized=False,
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        issues=tuple(issues),
        work_orders=work_orders,
        source_branch_summaries=_source_branch_summaries(work_orders),
        artifact_type_summaries=_artifact_type_summaries(work_orders),
        source_refs=source_refs,
        non_claims=NON_CLAIMS,
    )


def matrix_to_dict(matrix: AnalyticWorkOrderMatrix) -> dict[str, object]:
    return {
        "schema_version": matrix.schema_version,
        "lemma_id": matrix.lemma_id,
        "candidate_status": matrix.candidate_status,
        "active_candidate": matrix.active_candidate,
        "analytic_families": list(matrix.analytic_families),
        "work_order_count": matrix.work_order_count,
        "blocked_work_order_count": matrix.blocked_work_order_count,
        "actionable_work_order_count": matrix.actionable_work_order_count,
        "artifact_type_count": matrix.artifact_type_count,
        "source_branch_count": matrix.source_branch_count,
        "dependency_consistent": matrix.dependency_consistent,
        "process_gate_open_authorized": matrix.process_gate_open_authorized,
        "process_gate_open_blocked_by": list(matrix.process_gate_open_blocked_by),
        "blocker_state_changed": matrix.blocker_state_changed,
        "candidate_emission_authorized": matrix.candidate_emission_authorized,
        "missing_source_count": matrix.missing_source_count,
        "missing_sources": list(matrix.missing_sources),
        "issues": list(matrix.issues),
        "work_orders": [asdict(order) for order in matrix.work_orders],
        "source_branch_summaries": [
            asdict(summary) for summary in matrix.source_branch_summaries
        ],
        "artifact_type_summaries": [
            asdict(summary) for summary in matrix.artifact_type_summaries
        ],
        "source_refs": list(matrix.source_refs),
        "non_claims": list(matrix.non_claims),
        "packet_snapshot": packet_to_dict(build_analytic_prerequisite_packet()),
        "dependency_snapshot": dependency_report_to_dict(
            build_analytic_prerequisite_dependency_report()
        ),
        "docs": {
            "analytic_prerequisites_doc": "docs/STEP96_PROMOTION_GATE_ANALYTIC_PREREQUISITES.md",
            "analytic_dependency_doc": (
                "docs/STEP97_PROMOTION_GATE_ANALYTIC_PREREQUISITE_DEPENDENCY.md"
            ),
        },
        "canonical_reports": {
            "analytic_prerequisites_markdown": str(DEFAULT_PACKET_MARKDOWN_OUTPUT),
            "analytic_prerequisites_json": str(DEFAULT_PACKET_JSON_OUTPUT),
            "analytic_dependency_markdown": str(DEFAULT_DEPENDENCY_MARKDOWN_OUTPUT),
            "analytic_dependency_json": str(DEFAULT_DEPENDENCY_JSON_OUTPUT),
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _branch_rows(matrix: AnalyticWorkOrderMatrix) -> list[str]:
    rows = [
        "| source branch | work orders | artifact types | families | actionable | blocked |",
        "|---|---:|---|---|---:|---:|",
    ]
    for summary in matrix.source_branch_summaries:
        rows.append(
            "| "
            f"`{summary.source_branch}` | "
            f"{summary.work_order_count} | "
            f"{'<br>'.join(f'`{item}`' for item in summary.artifact_types)} | "
            f"{', '.join(f'`{item}`' for item in summary.families)} | "
            f"{summary.actionable_count} | "
            f"{summary.blocked_count} |"
        )
    return rows


def _artifact_rows(matrix: AnalyticWorkOrderMatrix) -> list[str]:
    rows = [
        "| artifact type | work orders | source branches | families |",
        "|---|---:|---|---|",
    ]
    for summary in matrix.artifact_type_summaries:
        rows.append(
            "| "
            f"`{summary.required_artifact_type}` | "
            f"{summary.work_order_count} | "
            f"{'<br>'.join(f'`{item}`' for item in summary.source_branches)} | "
            f"{', '.join(f'`{item}`' for item in summary.families)} |"
        )
    return rows


def _work_order_rows(matrix: AnalyticWorkOrderMatrix) -> list[str]:
    rows = [
        "| id | family | branch | prerequisite | artifact type | status | actionable | guard keys | instruction |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for order in matrix.work_orders:
        rows.append(
            "| "
            f"`{order.work_order_id}` | "
            f"`{order.family}` | "
            f"`{order.source_branch}` | "
            f"`{order.prerequisite_key}` | "
            f"`{order.required_artifact_type}` | "
            f"`{order.status}` | "
            f"`{str(order.actionable_now).lower()}` | "
            f"{'<br>'.join(f'`{key}`' for key in order.dependency_guard_keys) or '`none`'} | "
            f"{_format(order.operator_instruction)} |"
        )
    return rows


def render_markdown(matrix: AnalyticWorkOrderMatrix) -> str:
    return "\n".join(
        (
            "# Promotion Gate Analytic Work-Order Matrix",
            "",
            "Generated by `track-a-regularity/evaluator/promotion_gate_analytic_work_order_matrix.py`.",
            "",
            "This read-only matrix groups the Step 96 analytic prerequisites by required",
            "artifact type and source branch. It does not discharge blockers, open process",
            "gates, copy YAML, or emit a candidate.",
            "",
            "## Summary",
            "",
            f"- lemma_id: `{matrix.lemma_id}`",
            f"- candidate_status: `{matrix.candidate_status}`",
            f"- active_candidate: `{str(matrix.active_candidate).lower()}`",
            f"- work_order_count: `{matrix.work_order_count}`",
            f"- blocked_work_order_count: `{matrix.blocked_work_order_count}`",
            f"- actionable_work_order_count: `{matrix.actionable_work_order_count}`",
            f"- artifact_type_count: `{matrix.artifact_type_count}`",
            f"- source_branch_count: `{matrix.source_branch_count}`",
            f"- dependency_consistent: `{str(matrix.dependency_consistent).lower()}`",
            f"- process_gate_open_authorized: `{str(matrix.process_gate_open_authorized).lower()}`",
            f"- process_gate_open_blocked_by: `{', '.join(matrix.process_gate_open_blocked_by) or 'none'}`",
            f"- blocker_state_changed: `{str(matrix.blocker_state_changed).lower()}`",
            f"- candidate_emission_authorized: `{str(matrix.candidate_emission_authorized).lower()}`",
            f"- missing_source_count: `{matrix.missing_source_count}`",
            f"- issues: `{', '.join(matrix.issues) or 'none'}`",
            "",
            "## Source Branch Summary",
            "",
            *_branch_rows(matrix),
            "",
            "## Artifact Type Summary",
            "",
            *_artifact_rows(matrix),
            "",
            "## Work Orders",
            "",
            *_work_order_rows(matrix),
            "",
            "## Non-Claims",
            "",
            *(f"- `{item}`" for item in matrix.non_claims),
            "",
        )
    )


def render_json(matrix: AnalyticWorkOrderMatrix) -> str:
    return json.dumps(matrix_to_dict(matrix), indent=2, sort_keys=True) + "\n"


def render_output(matrix: AnalyticWorkOrderMatrix, output_format: str) -> str:
    if output_format == "markdown":
        return render_markdown(matrix)
    if output_format == "json":
        return render_json(matrix)
    raise ValueError(f"unknown analytic work-order matrix format: {output_format}")


def write_output(
    output: Path,
    matrix: AnalyticWorkOrderMatrix,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(matrix, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    matrix: AnalyticWorkOrderMatrix,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(matrix, output_format)
    if not output.exists():
        return False, f"missing promotion gate analytic work-order matrix: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale promotion gate analytic work-order matrix: {output}"
    return True, f"fresh promotion gate analytic work-order matrix: {output}"


def check_blocked(matrix: AnalyticWorkOrderMatrix) -> tuple[bool, str]:
    if matrix.process_gate_open_authorized:
        return False, "process gate open became authorized"
    if matrix.blocker_state_changed:
        return False, "matrix changed blocker state"
    if matrix.candidate_emission_authorized:
        return False, "candidate emission became authorized"
    if matrix.actionable_work_order_count:
        return False, "work orders became actionable without analytic discharge"
    if matrix.blocked_work_order_count != matrix.work_order_count:
        return False, "not all work orders remain blocked pending discharge"
    if tuple(matrix.process_gate_open_blocked_by) != EXPECTED_FAMILIES:
        return False, "process gate open is not blocked by both expected analytic families"
    return True, "analytic work-order matrix remains blocked and read-only"


def check_dependency_consistent(matrix: AnalyticWorkOrderMatrix) -> tuple[bool, str]:
    if not matrix.dependency_consistent:
        return False, "analytic work-order matrix dependency inconsistent"
    if matrix.issues:
        return False, "analytic work-order matrix has issues: " + ", ".join(matrix.issues)
    return True, "analytic work-order matrix dependencies are consistent"


def check_sources(matrix: AnalyticWorkOrderMatrix) -> tuple[bool, str]:
    if matrix.missing_source_count:
        return False, "missing analytic work-order matrix sources: " + ", ".join(
            matrix.missing_sources
        )
    return True, "all analytic work-order matrix sources exist"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown analytic work-order matrix format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a read-only work-order matrix for analytic blocker discharge prerequisites."
    )
    parser.add_argument("--candidate-dir", type=Path, default=DEFAULT_CANDIDATE_DIR)
    parser.add_argument("--smoke-summary", type=Path, default=DEFAULT_SMOKE_SUMMARY)
    parser.add_argument("--proof-graph-json", type=Path, default=DEFAULT_PROOF_GRAPH_JSON)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    parser.add_argument("--require-dependency-consistent", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    args = parser.parse_args(argv)

    try:
        matrix = build_analytic_work_order_matrix(
            candidate_dir=args.candidate_dir,
            smoke_summary=args.smoke_summary,
            proof_graph_json=args.proof_graph_json,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report setup failures.
        print(f"failed to build analytic work-order matrix: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, matrix, args.format)
        print(message)
        if not ok:
            print(
                "run without --check-output to regenerate the analytic work-order matrix",
                file=sys.stderr,
            )
            return 1
    else:
        written = write_output(output, matrix, args.format)
        print(f"wrote {written}")

    if args.require_blocked:
        ok, message = check_blocked(matrix)
        print(message)
        if not ok:
            return 1
    if args.require_dependency_consistent:
        ok, message = check_dependency_consistent(matrix)
        print(message)
        if not ok:
            return 1
    if args.require_sources_exist:
        ok, message = check_sources(matrix)
        print(message)
        if not ok:
            return 1

    print(f"work_order_count: {matrix.work_order_count}")
    print(f"blocked_work_order_count: {matrix.blocked_work_order_count}")
    print(f"actionable_work_order_count: {matrix.actionable_work_order_count}")
    print(f"dependency_consistent: {str(matrix.dependency_consistent).lower()}")
    print(f"process_gate_open_authorized: {str(matrix.process_gate_open_authorized).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
