from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from promotion_gate_analytic_discharge_gap_index import (
    DEFAULT_JSON_OUTPUT as DEFAULT_GAP_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_GAP_MARKDOWN_OUTPUT,
)
from promotion_gate_analytic_discharge_operator_dashboard import (
    DEFAULT_JSON_OUTPUT as DEFAULT_OPERATOR_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_OPERATOR_MARKDOWN_OUTPUT,
)
from promotion_gate_analytic_discharge_template_dependency import (
    DEFAULT_JSON_OUTPUT as DEFAULT_TEMPLATE_DEPENDENCY_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_TEMPLATE_DEPENDENCY_MARKDOWN_OUTPUT,
)
from promotion_gate_analytic_discharge_templates import (
    DEFAULT_JSON_OUTPUT as DEFAULT_TEMPLATE_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_TEMPLATE_MARKDOWN_OUTPUT,
    FORBIDDEN_MUTATIONS,
    REQUIRED_EVIDENCE_KEYS,
)
from promotion_gate_analytic_work_order_matrix import (
    DEFAULT_JSON_OUTPUT as DEFAULT_MATRIX_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_MATRIX_MARKDOWN_OUTPUT,
)
from promotion_gate_regression import DEFAULT_CANDIDATE_DIR, DEFAULT_SMOKE_SUMMARY
from proof_obligation_blockers import DEFAULT_INPUT as DEFAULT_PROOF_GRAPH_JSON


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = (
    DEFAULT_REPORT_DIR / "promotion_gate_analytic_discharge_gap_dependency.md"
)
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "promotion_gate_analytic_discharge_gap_dependency.json"

NON_CLAIMS = (
    "analytic_discharge_gap_dependency_guard_only",
    "read_only_consistency_check",
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
class GapDependencyCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class AnalyticDischargeGapDependencyReport:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    gap_index_markdown: str
    gap_index_json: str
    operator_dashboard_markdown: str
    operator_dashboard_json: str
    template_markdown: str
    template_json: str
    matrix_markdown: str
    matrix_json: str
    template_dependency_markdown: str
    template_dependency_json: str
    dependency_check_count: int
    passed_dependency_check_count: int
    failed_dependency_check_count: int
    dependency_consistent: bool
    gap_count: int
    blocked_gap_count: int
    actionable_gap_count: int
    may_discharge_gap_count: int
    missing_artifact_count: int
    template_count: int
    matrix_work_order_count: int
    template_dependency_check_count: int
    operator_stack_consistent: bool
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    issues: tuple[str, ...]
    checks: tuple[GapDependencyCheck, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]
    gap_index_snapshot: dict[str, object]
    operator_dashboard_snapshot: dict[str, object]
    template_snapshot: dict[str, object]
    matrix_snapshot: dict[str, object]
    template_dependency_snapshot: dict[str, object]


def _load_json(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"expected object JSON report: {path}")
    return data


def _check(
    *,
    key: str,
    expected: object,
    observed: object,
    source_artifacts: tuple[str, ...],
) -> GapDependencyCheck:
    return GapDependencyCheck(
        key=key,
        expected=str(expected),
        observed=str(observed),
        passed=expected == observed,
        source_artifacts=source_artifacts,
    )


def _missing_sources(source_refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(source for source in source_refs if not (ROOT / source).exists())


def _items(data: dict[str, object], key: str) -> tuple[dict[str, object], ...]:
    value = data.get(key)
    if not isinstance(value, list):
        raise ValueError(f"expected list field `{key}` in source report")
    return tuple(item for item in value if isinstance(item, dict))


def _values(items: tuple[dict[str, object], ...], key: str) -> tuple[object, ...]:
    return tuple(item.get(key) for item in items)


def _unexpected_tuple_values(
    items: tuple[dict[str, object], ...],
    field: str,
    expected: tuple[str, ...],
) -> tuple[tuple[str, tuple[str, ...]], ...]:
    unexpected: list[tuple[str, tuple[str, ...]]] = []
    for item in items:
        observed = tuple(str(value) for value in item.get(field, ()))
        if observed != expected:
            unexpected.append((str(item.get("gap_id")), observed))
    return tuple(unexpected)


def build_analytic_discharge_gap_dependency_report(
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
    smoke_summary: Path = DEFAULT_SMOKE_SUMMARY,
    proof_graph_json: Path = DEFAULT_PROOF_GRAPH_JSON,
) -> AnalyticDischargeGapDependencyReport:
    del candidate_dir, smoke_summary, proof_graph_json

    gap_index = _load_json(DEFAULT_GAP_JSON_OUTPUT)
    dashboard = _load_json(DEFAULT_OPERATOR_JSON_OUTPUT)
    template_audit = _load_json(DEFAULT_TEMPLATE_JSON_OUTPUT)
    matrix = _load_json(DEFAULT_MATRIX_JSON_OUTPUT)
    template_dependency = _load_json(DEFAULT_TEMPLATE_DEPENDENCY_JSON_OUTPUT)

    gap_source = (
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.md",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.json",
    )
    operator_source = (
        "track-a-regularity/reports/promotion_gate_analytic_discharge_operator_dashboard.md",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_operator_dashboard.json",
    )
    template_source = (
        "track-a-regularity/reports/promotion_gate_analytic_discharge_templates.md",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_templates.json",
    )
    matrix_source = (
        "track-a-regularity/reports/promotion_gate_analytic_work_order_matrix.md",
        "track-a-regularity/reports/promotion_gate_analytic_work_order_matrix.json",
    )
    template_dependency_source = (
        "track-a-regularity/reports/promotion_gate_analytic_discharge_template_dependency.md",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_template_dependency.json",
    )
    source_refs = tuple(
        dict.fromkeys(
            gap_source
            + operator_source
            + template_source
            + matrix_source
            + template_dependency_source
            + tuple(str(item) for item in gap_index.get("source_refs", ()))
        )
    )
    missing_sources = _missing_sources(source_refs)

    gaps = _items(gap_index, "gaps")
    templates = _items(template_audit, "templates")
    work_orders = _items(matrix, "work_orders")
    checks = (
        _check(
            key="gap.lemma_id.matches_operator_dashboard",
            expected=dashboard.get("lemma_id"),
            observed=gap_index.get("lemma_id"),
            source_artifacts=operator_source + gap_source,
        ),
        _check(
            key="gap.lemma_id.matches_template_audit",
            expected=template_audit.get("lemma_id"),
            observed=gap_index.get("lemma_id"),
            source_artifacts=template_source + gap_source,
        ),
        _check(
            key="gap.lemma_id.matches_matrix",
            expected=matrix.get("lemma_id"),
            observed=gap_index.get("lemma_id"),
            source_artifacts=matrix_source + gap_source,
        ),
        _check(
            key="gap.lemma_id.matches_template_dependency",
            expected=template_dependency.get("lemma_id"),
            observed=gap_index.get("lemma_id"),
            source_artifacts=template_dependency_source + gap_source,
        ),
        _check(
            key="gap.candidate_status.matches_operator_dashboard",
            expected=dashboard.get("candidate_status"),
            observed=gap_index.get("candidate_status"),
            source_artifacts=operator_source + gap_source,
        ),
        _check(
            key="gap.candidate_status.matches_template_dependency",
            expected=template_dependency.get("candidate_status"),
            observed=gap_index.get("candidate_status"),
            source_artifacts=template_dependency_source + gap_source,
        ),
        _check(
            key="gap.active_candidate.matches_operator_dashboard",
            expected=dashboard.get("active_candidate"),
            observed=gap_index.get("active_candidate"),
            source_artifacts=operator_source + gap_source,
        ),
        _check(
            key="gap.active_candidate.matches_template_dependency",
            expected=template_dependency.get("active_candidate"),
            observed=gap_index.get("active_candidate"),
            source_artifacts=template_dependency_source + gap_source,
        ),
        _check(
            key="gap.gap_count.matches_template_count",
            expected=template_audit.get("template_count"),
            observed=gap_index.get("gap_count"),
            source_artifacts=template_source + gap_source,
        ),
        _check(
            key="gap.gap_count.matches_matrix_work_order_count",
            expected=matrix.get("work_order_count"),
            observed=gap_index.get("gap_count"),
            source_artifacts=matrix_source + gap_source,
        ),
        _check(
            key="gap.gap_count.matches_template_dependency_template_count",
            expected=template_dependency.get("template_count"),
            observed=gap_index.get("gap_count"),
            source_artifacts=template_dependency_source + gap_source,
        ),
        _check(
            key="gap.blocked_gap_count.matches_template_blocked_count",
            expected=template_audit.get("blocked_template_count"),
            observed=gap_index.get("blocked_gap_count"),
            source_artifacts=template_source + gap_source,
        ),
        _check(
            key="gap.blocked_gap_count.matches_gap_count",
            expected=gap_index.get("gap_count"),
            observed=gap_index.get("blocked_gap_count"),
            source_artifacts=gap_source,
        ),
        _check(
            key="gap.actionable_gap_count.remains_zero",
            expected=0,
            observed=gap_index.get("actionable_gap_count"),
            source_artifacts=gap_source,
        ),
        _check(
            key="gap.may_discharge_gap_count.remains_zero",
            expected=0,
            observed=gap_index.get("may_discharge_gap_count"),
            source_artifacts=gap_source,
        ),
        _check(
            key="gap.missing_artifact_count.matches_gap_count",
            expected=gap_index.get("gap_count"),
            observed=gap_index.get("missing_artifact_count"),
            source_artifacts=gap_source,
        ),
        _check(
            key="gap.required_review_evidence_key_count.matches_template_required_keys",
            expected=len(REQUIRED_EVIDENCE_KEYS),
            observed=gap_index.get("required_review_evidence_key_count"),
            source_artifacts=template_source + gap_source,
        ),
        _check(
            key="gap.minimum_acceptance_check_count.has_three_per_gap",
            expected=int(gap_index.get("gap_count", 0)) * 3,
            observed=gap_index.get("minimum_acceptance_check_count"),
            source_artifacts=gap_source,
        ),
        _check(
            key="gap.source_branch_count.matches_template",
            expected=template_audit.get("source_branch_count"),
            observed=gap_index.get("source_branch_count"),
            source_artifacts=template_source + gap_source,
        ),
        _check(
            key="gap.source_branch_count.matches_matrix",
            expected=matrix.get("source_branch_count"),
            observed=gap_index.get("source_branch_count"),
            source_artifacts=matrix_source + gap_source,
        ),
        _check(
            key="gap.artifact_type_count.matches_template",
            expected=template_audit.get("artifact_type_count"),
            observed=gap_index.get("artifact_type_count"),
            source_artifacts=template_source + gap_source,
        ),
        _check(
            key="gap.artifact_type_count.matches_matrix",
            expected=matrix.get("artifact_type_count"),
            observed=gap_index.get("artifact_type_count"),
            source_artifacts=matrix_source + gap_source,
        ),
        _check(
            key="gap.stack_consistent.matches_operator_dashboard",
            expected=dashboard.get("stack_consistent"),
            observed=gap_index.get("stack_consistent"),
            source_artifacts=operator_source + gap_source,
        ),
        _check(
            key="operator_dashboard.stack_consistent.true",
            expected=True,
            observed=dashboard.get("stack_consistent"),
            source_artifacts=operator_source,
        ),
        _check(
            key="template_dependency.dependency_consistent.true",
            expected=True,
            observed=template_dependency.get("dependency_consistent"),
            source_artifacts=template_dependency_source,
        ),
        _check(
            key="template_dependency.failed_dependency_check_count.remains_zero",
            expected=0,
            observed=template_dependency.get("failed_dependency_check_count"),
            source_artifacts=template_dependency_source,
        ),
        _check(
            key="gap.work_order_ids.match_template_work_order_ids",
            expected=_values(templates, "work_order_id"),
            observed=_values(gaps, "work_order_id"),
            source_artifacts=template_source + gap_source,
        ),
        _check(
            key="gap.work_order_ids.match_matrix_work_order_ids",
            expected=_values(work_orders, "work_order_id"),
            observed=_values(gaps, "work_order_id"),
            source_artifacts=matrix_source + gap_source,
        ),
        _check(
            key="gap.prerequisite_keys.match_template",
            expected=_values(templates, "prerequisite_key"),
            observed=_values(gaps, "prerequisite_key"),
            source_artifacts=template_source + gap_source,
        ),
        _check(
            key="gap.required_artifact_types.match_template",
            expected=_values(templates, "required_artifact_type"),
            observed=_values(gaps, "required_artifact_type"),
            source_artifacts=template_source + gap_source,
        ),
        _check(
            key="gap.required_artifact_types.match_matrix",
            expected=_values(work_orders, "required_artifact_type"),
            observed=_values(gaps, "required_artifact_type"),
            source_artifacts=matrix_source + gap_source,
        ),
        _check(
            key="gap.source_branches.match_template",
            expected=_values(templates, "source_branch"),
            observed=_values(gaps, "source_branch"),
            source_artifacts=template_source + gap_source,
        ),
        _check(
            key="gap.dependency_guard_keys.match_template",
            expected=_values(templates, "dependency_guard_keys"),
            observed=_values(gaps, "dependency_guard_keys"),
            source_artifacts=template_source + gap_source,
        ),
        _check(
            key="gap.source_artifacts.match_template",
            expected=_values(templates, "source_artifact"),
            observed=_values(gaps, "source_artifact"),
            source_artifacts=template_source + gap_source,
        ),
        _check(
            key="gap.required_review_evidence.all_expected",
            expected=(),
            observed=_unexpected_tuple_values(
                gaps,
                "required_review_evidence",
                REQUIRED_EVIDENCE_KEYS,
            ),
            source_artifacts=template_source + gap_source,
        ),
        _check(
            key="gap.forbidden_mutations.all_expected",
            expected=(),
            observed=_unexpected_tuple_values(
                gaps,
                "forbidden_mutations",
                FORBIDDEN_MUTATIONS,
            ),
            source_artifacts=template_source + gap_source,
        ),
        _check(
            key="process_gate_open_authorized.all_false",
            expected=(False, False, False, False, False),
            observed=(
                dashboard.get("process_gate_open_authorized"),
                template_dependency.get("process_gate_open_authorized"),
                template_audit.get("process_gate_open_authorized"),
                matrix.get("process_gate_open_authorized"),
                gap_index.get("process_gate_open_authorized"),
            ),
            source_artifacts=operator_source
            + template_dependency_source
            + template_source
            + matrix_source
            + gap_source,
        ),
        _check(
            key="blocker_state_changed.all_false",
            expected=(False, False, False, False, False),
            observed=(
                dashboard.get("blocker_state_changed"),
                template_dependency.get("blocker_state_changed"),
                template_audit.get("blocker_state_changed"),
                matrix.get("blocker_state_changed"),
                gap_index.get("blocker_state_changed"),
            ),
            source_artifacts=operator_source
            + template_dependency_source
            + template_source
            + matrix_source
            + gap_source,
        ),
        _check(
            key="candidate_emission_authorized.all_false",
            expected=(False, False, False, False, False),
            observed=(
                dashboard.get("candidate_emission_authorized"),
                template_dependency.get("candidate_emission_authorized"),
                template_audit.get("candidate_emission_authorized"),
                matrix.get("candidate_emission_authorized"),
                gap_index.get("candidate_emission_authorized"),
            ),
            source_artifacts=operator_source
            + template_dependency_source
            + template_source
            + matrix_source
            + gap_source,
        ),
        _check(
            key="source_reports.issues.all_empty",
            expected=((), (), (), ()),
            observed=(
                tuple(dashboard.get("issues", ())),
                tuple(template_dependency.get("issues", ())),
                tuple(template_audit.get("issues", ())),
                tuple(matrix.get("issues", ())),
            ),
            source_artifacts=operator_source + template_dependency_source + template_source + matrix_source,
        ),
        _check(
            key="gap_index.issues.empty",
            expected=(),
            observed=tuple(gap_index.get("issues", ())),
            source_artifacts=gap_source,
        ),
        _check(
            key="source_refs.missing_count.remains_zero",
            expected=0,
            observed=len(missing_sources),
            source_artifacts=source_refs,
        ),
    )

    issues = tuple(check.key for check in checks if not check.passed)
    failed_count = len(issues)
    dependency_consistent = failed_count == 0 and not missing_sources

    return AnalyticDischargeGapDependencyReport(
        schema_version=1,
        lemma_id=str(gap_index.get("lemma_id")),
        candidate_status=str(gap_index.get("candidate_status")),
        active_candidate=bool(gap_index.get("active_candidate")),
        gap_index_markdown=str(DEFAULT_GAP_MARKDOWN_OUTPUT),
        gap_index_json=str(DEFAULT_GAP_JSON_OUTPUT),
        operator_dashboard_markdown=str(DEFAULT_OPERATOR_MARKDOWN_OUTPUT),
        operator_dashboard_json=str(DEFAULT_OPERATOR_JSON_OUTPUT),
        template_markdown=str(DEFAULT_TEMPLATE_MARKDOWN_OUTPUT),
        template_json=str(DEFAULT_TEMPLATE_JSON_OUTPUT),
        matrix_markdown=str(DEFAULT_MATRIX_MARKDOWN_OUTPUT),
        matrix_json=str(DEFAULT_MATRIX_JSON_OUTPUT),
        template_dependency_markdown=str(DEFAULT_TEMPLATE_DEPENDENCY_MARKDOWN_OUTPUT),
        template_dependency_json=str(DEFAULT_TEMPLATE_DEPENDENCY_JSON_OUTPUT),
        dependency_check_count=len(checks),
        passed_dependency_check_count=len(checks) - failed_count,
        failed_dependency_check_count=failed_count,
        dependency_consistent=dependency_consistent,
        gap_count=int(gap_index.get("gap_count", 0)),
        blocked_gap_count=int(gap_index.get("blocked_gap_count", 0)),
        actionable_gap_count=int(gap_index.get("actionable_gap_count", 0)),
        may_discharge_gap_count=int(gap_index.get("may_discharge_gap_count", 0)),
        missing_artifact_count=int(gap_index.get("missing_artifact_count", 0)),
        template_count=int(template_audit.get("template_count", 0)),
        matrix_work_order_count=int(matrix.get("work_order_count", 0)),
        template_dependency_check_count=int(template_dependency.get("dependency_check_count", 0)),
        operator_stack_consistent=bool(dashboard.get("stack_consistent")),
        process_gate_open_authorized=bool(gap_index.get("process_gate_open_authorized")),
        blocker_state_changed=bool(gap_index.get("blocker_state_changed")),
        candidate_emission_authorized=bool(gap_index.get("candidate_emission_authorized")),
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        issues=issues,
        checks=checks,
        source_refs=source_refs,
        non_claims=NON_CLAIMS,
        gap_index_snapshot=gap_index,
        operator_dashboard_snapshot=dashboard,
        template_snapshot=template_audit,
        matrix_snapshot=matrix,
        template_dependency_snapshot=template_dependency,
    )


def gap_dependency_report_to_dict(
    report: AnalyticDischargeGapDependencyReport,
) -> dict[str, object]:
    return {
        "schema_version": report.schema_version,
        "lemma_id": report.lemma_id,
        "candidate_status": report.candidate_status,
        "active_candidate": report.active_candidate,
        "gap_index_markdown": report.gap_index_markdown,
        "gap_index_json": report.gap_index_json,
        "operator_dashboard_markdown": report.operator_dashboard_markdown,
        "operator_dashboard_json": report.operator_dashboard_json,
        "template_markdown": report.template_markdown,
        "template_json": report.template_json,
        "matrix_markdown": report.matrix_markdown,
        "matrix_json": report.matrix_json,
        "template_dependency_markdown": report.template_dependency_markdown,
        "template_dependency_json": report.template_dependency_json,
        "dependency_check_count": report.dependency_check_count,
        "passed_dependency_check_count": report.passed_dependency_check_count,
        "failed_dependency_check_count": report.failed_dependency_check_count,
        "dependency_consistent": report.dependency_consistent,
        "gap_count": report.gap_count,
        "blocked_gap_count": report.blocked_gap_count,
        "actionable_gap_count": report.actionable_gap_count,
        "may_discharge_gap_count": report.may_discharge_gap_count,
        "missing_artifact_count": report.missing_artifact_count,
        "template_count": report.template_count,
        "matrix_work_order_count": report.matrix_work_order_count,
        "template_dependency_check_count": report.template_dependency_check_count,
        "operator_stack_consistent": report.operator_stack_consistent,
        "process_gate_open_authorized": report.process_gate_open_authorized,
        "blocker_state_changed": report.blocker_state_changed,
        "candidate_emission_authorized": report.candidate_emission_authorized,
        "missing_source_count": report.missing_source_count,
        "missing_sources": list(report.missing_sources),
        "issues": list(report.issues),
        "checks": [asdict(check) for check in report.checks],
        "source_refs": list(report.source_refs),
        "non_claims": list(report.non_claims),
        "gap_index_snapshot": report.gap_index_snapshot,
        "operator_dashboard_snapshot": report.operator_dashboard_snapshot,
        "template_snapshot": report.template_snapshot,
        "matrix_snapshot": report.matrix_snapshot,
        "template_dependency_snapshot": report.template_dependency_snapshot,
        "docs": {
            "gap_index_doc": "docs/STEP102_PROMOTION_GATE_ANALYTIC_DISCHARGE_GAP_INDEX.md",
            "operator_dashboard_doc": (
                "docs/STEP101_PROMOTION_GATE_ANALYTIC_DISCHARGE_OPERATOR_DASHBOARD.md"
            ),
            "template_dependency_doc": (
                "docs/STEP100_PROMOTION_GATE_ANALYTIC_DISCHARGE_TEMPLATE_DEPENDENCY.md"
            ),
            "analytic_discharge_templates_doc": (
                "docs/STEP99_PROMOTION_GATE_ANALYTIC_DISCHARGE_TEMPLATES.md"
            ),
            "analytic_work_order_matrix_doc": (
                "docs/STEP98_PROMOTION_GATE_ANALYTIC_WORK_ORDER_MATRIX.md"
            ),
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _check_rows(report: AnalyticDischargeGapDependencyReport) -> list[str]:
    rows = [
        "| check | expected | observed | passed | sources |",
        "|---|---|---|---|---|",
    ]
    for check in report.checks:
        sources = "<br>".join(f"`{source}`" for source in check.source_artifacts)
        rows.append(
            "| "
            f"`{check.key}` | "
            f"`{_format(check.expected)}` | "
            f"`{_format(check.observed)}` | "
            f"`{str(check.passed).lower()}` | "
            f"{sources} |"
        )
    return rows


def render_markdown(report: AnalyticDischargeGapDependencyReport) -> str:
    return "\n".join(
        (
            "# Promotion Gate Analytic Discharge Gap Dependency",
            "",
            "Generated by `track-a-regularity/evaluator/promotion_gate_analytic_discharge_gap_dependency.py`.",
            "",
            "This read-only report checks that the Step 102 gap index cannot drift from",
            "the Step 101 operator dashboard, Step 100 template-dependency guard, Step 99",
            "template audit, or Step 98 work-order matrix it depends on.",
            "",
            "## Summary",
            "",
            f"- lemma_id: `{report.lemma_id}`",
            f"- candidate_status: `{report.candidate_status}`",
            f"- active_candidate: `{str(report.active_candidate).lower()}`",
            f"- dependency_check_count: `{report.dependency_check_count}`",
            f"- passed_dependency_check_count: `{report.passed_dependency_check_count}`",
            f"- failed_dependency_check_count: `{report.failed_dependency_check_count}`",
            f"- dependency_consistent: `{str(report.dependency_consistent).lower()}`",
            f"- gap_count: `{report.gap_count}`",
            f"- blocked_gap_count: `{report.blocked_gap_count}`",
            f"- actionable_gap_count: `{report.actionable_gap_count}`",
            f"- may_discharge_gap_count: `{report.may_discharge_gap_count}`",
            f"- missing_artifact_count: `{report.missing_artifact_count}`",
            f"- template_count: `{report.template_count}`",
            f"- matrix_work_order_count: `{report.matrix_work_order_count}`",
            f"- template_dependency_check_count: `{report.template_dependency_check_count}`",
            f"- operator_stack_consistent: `{str(report.operator_stack_consistent).lower()}`",
            f"- process_gate_open_authorized: `{str(report.process_gate_open_authorized).lower()}`",
            f"- blocker_state_changed: `{str(report.blocker_state_changed).lower()}`",
            f"- candidate_emission_authorized: `{str(report.candidate_emission_authorized).lower()}`",
            f"- missing_source_count: `{report.missing_source_count}`",
            f"- issues: `{', '.join(report.issues) or 'none'}`",
            "",
            "## Source Reports",
            "",
            f"- gap_index_markdown: `{report.gap_index_markdown}`",
            f"- gap_index_json: `{report.gap_index_json}`",
            f"- operator_dashboard_markdown: `{report.operator_dashboard_markdown}`",
            f"- operator_dashboard_json: `{report.operator_dashboard_json}`",
            f"- template_dependency_markdown: `{report.template_dependency_markdown}`",
            f"- template_dependency_json: `{report.template_dependency_json}`",
            f"- template_markdown: `{report.template_markdown}`",
            f"- template_json: `{report.template_json}`",
            f"- matrix_markdown: `{report.matrix_markdown}`",
            f"- matrix_json: `{report.matrix_json}`",
            "",
            "## Dependency Checks",
            "",
            *_check_rows(report),
            "",
            "## Non-Claims",
            "",
            *(f"- `{item}`" for item in report.non_claims),
            "",
        )
    )


def render_json(report: AnalyticDischargeGapDependencyReport) -> str:
    return json.dumps(
        gap_dependency_report_to_dict(report),
        indent=2,
        sort_keys=True,
    ) + "\n"


def render_output(
    report: AnalyticDischargeGapDependencyReport,
    output_format: str,
) -> str:
    if output_format == "markdown":
        return render_markdown(report)
    if output_format == "json":
        return render_json(report)
    raise ValueError(f"unknown analytic discharge gap dependency format: {output_format}")


def write_output(
    output: Path,
    report: AnalyticDischargeGapDependencyReport,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(report, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    report: AnalyticDischargeGapDependencyReport,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(report, output_format)
    if not output.exists():
        return False, f"missing promotion gate analytic discharge gap dependency: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale promotion gate analytic discharge gap dependency: {output}"
    return True, f"fresh promotion gate analytic discharge gap dependency: {output}"


def check_consistent(
    report: AnalyticDischargeGapDependencyReport,
) -> tuple[bool, str]:
    if not report.dependency_consistent:
        return False, "analytic discharge gap dependency inconsistent: " + ", ".join(
            report.issues
        )
    return True, "analytic discharge gap dependency is consistent"


def check_sources(report: AnalyticDischargeGapDependencyReport) -> tuple[bool, str]:
    if report.missing_source_count:
        return False, "missing analytic discharge gap dependency sources: " + ", ".join(
            report.missing_sources
        )
    return True, "all analytic discharge gap dependency sources exist"


def check_blocked(report: AnalyticDischargeGapDependencyReport) -> tuple[bool, str]:
    if report.process_gate_open_authorized:
        return False, "process gate open became authorized"
    if report.blocker_state_changed:
        return False, "gap dependency changed blocker state"
    if report.candidate_emission_authorized:
        return False, "gap dependency authorized candidate emission"
    if report.actionable_gap_count:
        return False, "gap dependency found actionable gaps"
    if report.may_discharge_gap_count:
        return False, "gap dependency found blocker-discharge-capable gaps"
    if report.blocked_gap_count != report.gap_count:
        return False, "not all gaps remain blocked"
    return True, "analytic discharge gap dependency keeps gaps blocked"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown analytic discharge gap dependency format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check Step 102 analytic discharge gap index dependencies."
    )
    parser.add_argument("--candidate-dir", type=Path, default=DEFAULT_CANDIDATE_DIR)
    parser.add_argument("--smoke-summary", type=Path, default=DEFAULT_SMOKE_SUMMARY)
    parser.add_argument("--proof-graph-json", type=Path, default=DEFAULT_PROOF_GRAPH_JSON)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-consistent", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    args = parser.parse_args(argv)

    try:
        report = build_analytic_discharge_gap_dependency_report(
            candidate_dir=args.candidate_dir,
            smoke_summary=args.smoke_summary,
            proof_graph_json=args.proof_graph_json,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report setup failures.
        print(f"failed to build analytic discharge gap dependency: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, report, args.format)
        print(message)
        if not ok:
            print(
                "run without --check-output to regenerate the analytic discharge gap dependency",
                file=sys.stderr,
            )
            return 1
    else:
        written = write_output(output, report, args.format)
        print(f"wrote {written}")

    if args.require_consistent:
        ok, message = check_consistent(report)
        print(message)
        if not ok:
            return 1
    if args.require_sources_exist:
        ok, message = check_sources(report)
        print(message)
        if not ok:
            return 1
    if args.require_blocked:
        ok, message = check_blocked(report)
        print(message)
        if not ok:
            return 1

    print(f"dependency_check_count: {report.dependency_check_count}")
    print(f"passed_dependency_check_count: {report.passed_dependency_check_count}")
    print(f"failed_dependency_check_count: {report.failed_dependency_check_count}")
    print(f"dependency_consistent: {str(report.dependency_consistent).lower()}")
    print(f"process_gate_open_authorized: {str(report.process_gate_open_authorized).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
