from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from promotion_gate_analytic_discharge_gap_dependency import (
    DEFAULT_JSON_OUTPUT as DEFAULT_GAP_DEPENDENCY_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_GAP_DEPENDENCY_MARKDOWN_OUTPUT,
)
from promotion_gate_analytic_discharge_gap_index import (
    DEFAULT_JSON_OUTPUT as DEFAULT_GAP_INDEX_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_GAP_INDEX_MARKDOWN_OUTPUT,
)
from promotion_gate_analytic_discharge_gap_operator_index import (
    DEFAULT_JSON_OUTPUT as DEFAULT_GAP_OPERATOR_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_GAP_OPERATOR_MARKDOWN_OUTPUT,
)
from promotion_gate_analytic_discharge_operator_dashboard import (
    DEFAULT_JSON_OUTPUT as DEFAULT_OPERATOR_DASHBOARD_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_OPERATOR_DASHBOARD_MARKDOWN_OUTPUT,
)
from promotion_gate_regression import DEFAULT_CANDIDATE_DIR, DEFAULT_SMOKE_SUMMARY
from proof_obligation_blockers import DEFAULT_INPUT as DEFAULT_PROOF_GRAPH_JSON


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = (
    DEFAULT_REPORT_DIR
    / "promotion_gate_analytic_discharge_gap_operator_dependency.md"
)
DEFAULT_JSON_OUTPUT = (
    DEFAULT_REPORT_DIR
    / "promotion_gate_analytic_discharge_gap_operator_dependency.json"
)

NON_CLAIMS = (
    "analytic_discharge_gap_operator_dependency_guard_only",
    "read_only_source_index_bridge",
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
class GapOperatorDependencyCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class AnalyticDischargeGapOperatorDependencyReport:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    gap_operator_markdown: str
    gap_operator_json: str
    gap_dependency_markdown: str
    gap_dependency_json: str
    gap_index_markdown: str
    gap_index_json: str
    operator_dashboard_markdown: str
    operator_dashboard_json: str
    direct_source_report_count: int
    source_ref_count: int
    operator_dependency_check_count: int
    passed_operator_dependency_check_count: int
    failed_operator_dependency_check_count: int
    operator_dependency_consistent: bool
    gap_operator_index_check_count: int
    gap_operator_failed_check_count: int
    gap_operator_consistent: bool
    gap_dependency_check_count: int
    gap_dependency_failed_check_count: int
    gap_dependency_consistent: bool
    gap_index_stack_consistent: bool
    operator_dashboard_stack_consistent: bool
    gap_count: int
    blocked_gap_count: int
    actionable_gap_count: int
    may_discharge_gap_count: int
    missing_artifact_count: int
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    issues: tuple[str, ...]
    checks: tuple[GapOperatorDependencyCheck, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]
    gap_operator_snapshot: dict[str, object]
    gap_dependency_snapshot: dict[str, object]
    gap_index_snapshot: dict[str, object]
    operator_dashboard_snapshot: dict[str, object]


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
) -> GapOperatorDependencyCheck:
    return GapOperatorDependencyCheck(
        key=key,
        expected=str(expected),
        observed=str(observed),
        passed=expected == observed,
        source_artifacts=source_artifacts,
    )


def _missing_sources(source_refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(source for source in source_refs if not (ROOT / source).exists())


def build_analytic_discharge_gap_operator_dependency_report(
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
    smoke_summary: Path = DEFAULT_SMOKE_SUMMARY,
    proof_graph_json: Path = DEFAULT_PROOF_GRAPH_JSON,
) -> AnalyticDischargeGapOperatorDependencyReport:
    del candidate_dir, smoke_summary, proof_graph_json

    gap_operator = _load_json(DEFAULT_GAP_OPERATOR_JSON_OUTPUT)
    gap_dependency = _load_json(DEFAULT_GAP_DEPENDENCY_JSON_OUTPUT)
    gap_index = _load_json(DEFAULT_GAP_INDEX_JSON_OUTPUT)
    operator_dashboard = _load_json(DEFAULT_OPERATOR_DASHBOARD_JSON_OUTPUT)

    gap_operator_source = (
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_operator_index.md",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_operator_index.json",
    )
    gap_dependency_source = (
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_dependency.md",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_dependency.json",
    )
    gap_index_source = (
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.md",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.json",
    )
    operator_dashboard_source = (
        "track-a-regularity/reports/promotion_gate_analytic_discharge_operator_dashboard.md",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_operator_dashboard.json",
    )
    direct_sources = (
        gap_operator_source
        + gap_dependency_source
        + gap_index_source
        + operator_dashboard_source
    )
    source_refs = tuple(
        dict.fromkeys(
            direct_sources
            + tuple(str(item) for item in gap_operator.get("source_refs", ()))
            + tuple(str(item) for item in gap_dependency.get("source_refs", ()))
            + tuple(str(item) for item in gap_index.get("source_refs", ()))
            + tuple(str(item) for item in operator_dashboard.get("source_refs", ()))
        )
    )
    missing_sources = _missing_sources(source_refs)

    source_reports = (gap_operator, gap_dependency, gap_index, operator_dashboard)
    checks = (
        _check(
            key="operator.lemma_id.matches_gap_dependency",
            expected=gap_dependency.get("lemma_id"),
            observed=gap_operator.get("lemma_id"),
            source_artifacts=gap_operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.lemma_id.matches_gap_index",
            expected=gap_index.get("lemma_id"),
            observed=gap_operator.get("lemma_id"),
            source_artifacts=gap_operator_source + gap_index_source,
        ),
        _check(
            key="operator.lemma_id.matches_operator_dashboard",
            expected=operator_dashboard.get("lemma_id"),
            observed=gap_operator.get("lemma_id"),
            source_artifacts=gap_operator_source + operator_dashboard_source,
        ),
        _check(
            key="operator.candidate_status.matches_gap_dependency",
            expected=gap_dependency.get("candidate_status"),
            observed=gap_operator.get("candidate_status"),
            source_artifacts=gap_operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.candidate_status.matches_gap_index",
            expected=gap_index.get("candidate_status"),
            observed=gap_operator.get("candidate_status"),
            source_artifacts=gap_operator_source + gap_index_source,
        ),
        _check(
            key="operator.candidate_status.matches_operator_dashboard",
            expected=operator_dashboard.get("candidate_status"),
            observed=gap_operator.get("candidate_status"),
            source_artifacts=gap_operator_source + operator_dashboard_source,
        ),
        _check(
            key="operator.active_candidate.matches_gap_dependency",
            expected=gap_dependency.get("active_candidate"),
            observed=gap_operator.get("active_candidate"),
            source_artifacts=gap_operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.active_candidate.matches_gap_index",
            expected=gap_index.get("active_candidate"),
            observed=gap_operator.get("active_candidate"),
            source_artifacts=gap_operator_source + gap_index_source,
        ),
        _check(
            key="operator.active_candidate.matches_operator_dashboard",
            expected=operator_dashboard.get("active_candidate"),
            observed=gap_operator.get("active_candidate"),
            source_artifacts=gap_operator_source + operator_dashboard_source,
        ),
        _check(
            key="operator.gap_count.matches_gap_dependency",
            expected=gap_dependency.get("gap_count"),
            observed=gap_operator.get("gap_count"),
            source_artifacts=gap_operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.gap_count.matches_gap_index",
            expected=gap_index.get("gap_count"),
            observed=gap_operator.get("gap_count"),
            source_artifacts=gap_operator_source + gap_index_source,
        ),
        _check(
            key="operator.blocked_gap_count.matches_gap_dependency",
            expected=gap_dependency.get("blocked_gap_count"),
            observed=gap_operator.get("blocked_gap_count"),
            source_artifacts=gap_operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.blocked_gap_count.matches_gap_index",
            expected=gap_index.get("blocked_gap_count"),
            observed=gap_operator.get("blocked_gap_count"),
            source_artifacts=gap_operator_source + gap_index_source,
        ),
        _check(
            key="operator.actionable_gap_count.matches_gap_dependency",
            expected=gap_dependency.get("actionable_gap_count"),
            observed=gap_operator.get("actionable_gap_count"),
            source_artifacts=gap_operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.actionable_gap_count.matches_gap_index",
            expected=gap_index.get("actionable_gap_count"),
            observed=gap_operator.get("actionable_gap_count"),
            source_artifacts=gap_operator_source + gap_index_source,
        ),
        _check(
            key="operator.may_discharge_gap_count.matches_gap_dependency",
            expected=gap_dependency.get("may_discharge_gap_count"),
            observed=gap_operator.get("may_discharge_gap_count"),
            source_artifacts=gap_operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.may_discharge_gap_count.matches_gap_index",
            expected=gap_index.get("may_discharge_gap_count"),
            observed=gap_operator.get("may_discharge_gap_count"),
            source_artifacts=gap_operator_source + gap_index_source,
        ),
        _check(
            key="operator.missing_artifact_count.matches_gap_dependency",
            expected=gap_dependency.get("missing_artifact_count"),
            observed=gap_operator.get("missing_artifact_count"),
            source_artifacts=gap_operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.missing_artifact_count.matches_gap_index",
            expected=gap_index.get("missing_artifact_count"),
            observed=gap_operator.get("missing_artifact_count"),
            source_artifacts=gap_operator_source + gap_index_source,
        ),
        _check(
            key="operator.gap_dependency_check_count.matches_dependency",
            expected=gap_dependency.get("dependency_check_count"),
            observed=gap_operator.get("gap_dependency_check_count"),
            source_artifacts=gap_operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.gap_dependency_failed_check_count.matches_dependency",
            expected=gap_dependency.get("failed_dependency_check_count"),
            observed=gap_operator.get("gap_dependency_failed_check_count"),
            source_artifacts=gap_operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.gap_dependency_consistent.matches_dependency",
            expected=gap_dependency.get("dependency_consistent"),
            observed=gap_operator.get("gap_dependency_consistent"),
            source_artifacts=gap_operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.operator_stack_consistent.matches_gap_dependency",
            expected=gap_dependency.get("operator_stack_consistent"),
            observed=gap_operator.get("operator_stack_consistent"),
            source_artifacts=gap_operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.section_count.expected_two",
            expected=2,
            observed=gap_operator.get("section_count"),
            source_artifacts=gap_operator_source,
        ),
        _check(
            key="operator.source_report_count.expected_four",
            expected=4,
            observed=gap_operator.get("source_report_count"),
            source_artifacts=gap_operator_source,
        ),
        _check(
            key="operator.operator_index_check_count.expected_twenty",
            expected=20,
            observed=gap_operator.get("operator_index_check_count"),
            source_artifacts=gap_operator_source,
        ),
        _check(
            key="operator.failed_operator_index_check_count.remains_zero",
            expected=0,
            observed=gap_operator.get("failed_operator_index_check_count"),
            source_artifacts=gap_operator_source,
        ),
        _check(
            key="operator.operator_index_consistent.true",
            expected=True,
            observed=gap_operator.get("operator_index_consistent"),
            source_artifacts=gap_operator_source,
        ),
        _check(
            key="gap_dependency.dependency_consistent.true",
            expected=True,
            observed=gap_dependency.get("dependency_consistent"),
            source_artifacts=gap_dependency_source,
        ),
        _check(
            key="gap_dependency.failed_dependency_check_count.remains_zero",
            expected=0,
            observed=gap_dependency.get("failed_dependency_check_count"),
            source_artifacts=gap_dependency_source,
        ),
        _check(
            key="gap_dependency.missing_source_count.remains_zero",
            expected=0,
            observed=gap_dependency.get("missing_source_count"),
            source_artifacts=gap_dependency_source,
        ),
        _check(
            key="gap_index.stack_consistent.true",
            expected=True,
            observed=gap_index.get("stack_consistent"),
            source_artifacts=gap_index_source,
        ),
        _check(
            key="operator_dashboard.stack_consistent.true",
            expected=True,
            observed=operator_dashboard.get("stack_consistent"),
            source_artifacts=operator_dashboard_source,
        ),
        _check(
            key="operator_dashboard.failed_stack_consistency_check_count.remains_zero",
            expected=0,
            observed=operator_dashboard.get("failed_stack_consistency_check_count"),
            source_artifacts=operator_dashboard_source,
        ),
        _check(
            key="process_gate_open_authorized.all_false",
            expected=(False, False, False, False),
            observed=tuple(report.get("process_gate_open_authorized") for report in source_reports),
            source_artifacts=direct_sources,
        ),
        _check(
            key="blocker_state_changed.all_false",
            expected=(False, False, False, False),
            observed=tuple(report.get("blocker_state_changed") for report in source_reports),
            source_artifacts=direct_sources,
        ),
        _check(
            key="candidate_emission_authorized.all_false",
            expected=(False, False, False, False),
            observed=tuple(report.get("candidate_emission_authorized") for report in source_reports),
            source_artifacts=direct_sources,
        ),
        _check(
            key="source_reports.issues.all_empty",
            expected=((), (), (), ()),
            observed=tuple(tuple(report.get("issues", ())) for report in source_reports),
            source_artifacts=direct_sources,
        ),
        _check(
            key="direct_source_report_count.expected_eight",
            expected=8,
            observed=len(direct_sources),
            source_artifacts=direct_sources,
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
    operator_dependency_consistent = failed_count == 0 and not missing_sources

    return AnalyticDischargeGapOperatorDependencyReport(
        schema_version=1,
        lemma_id=str(gap_operator.get("lemma_id")),
        candidate_status=str(gap_operator.get("candidate_status")),
        active_candidate=bool(gap_operator.get("active_candidate")),
        gap_operator_markdown=str(DEFAULT_GAP_OPERATOR_MARKDOWN_OUTPUT),
        gap_operator_json=str(DEFAULT_GAP_OPERATOR_JSON_OUTPUT),
        gap_dependency_markdown=str(DEFAULT_GAP_DEPENDENCY_MARKDOWN_OUTPUT),
        gap_dependency_json=str(DEFAULT_GAP_DEPENDENCY_JSON_OUTPUT),
        gap_index_markdown=str(DEFAULT_GAP_INDEX_MARKDOWN_OUTPUT),
        gap_index_json=str(DEFAULT_GAP_INDEX_JSON_OUTPUT),
        operator_dashboard_markdown=str(DEFAULT_OPERATOR_DASHBOARD_MARKDOWN_OUTPUT),
        operator_dashboard_json=str(DEFAULT_OPERATOR_DASHBOARD_JSON_OUTPUT),
        direct_source_report_count=len(direct_sources),
        source_ref_count=len(source_refs),
        operator_dependency_check_count=len(checks),
        passed_operator_dependency_check_count=len(checks) - failed_count,
        failed_operator_dependency_check_count=failed_count,
        operator_dependency_consistent=operator_dependency_consistent,
        gap_operator_index_check_count=int(gap_operator.get("operator_index_check_count", 0)),
        gap_operator_failed_check_count=int(
            gap_operator.get("failed_operator_index_check_count", 0)
        ),
        gap_operator_consistent=bool(gap_operator.get("operator_index_consistent")),
        gap_dependency_check_count=int(gap_dependency.get("dependency_check_count", 0)),
        gap_dependency_failed_check_count=int(
            gap_dependency.get("failed_dependency_check_count", 0)
        ),
        gap_dependency_consistent=bool(gap_dependency.get("dependency_consistent")),
        gap_index_stack_consistent=bool(gap_index.get("stack_consistent")),
        operator_dashboard_stack_consistent=bool(operator_dashboard.get("stack_consistent")),
        gap_count=int(gap_operator.get("gap_count", 0)),
        blocked_gap_count=int(gap_operator.get("blocked_gap_count", 0)),
        actionable_gap_count=int(gap_operator.get("actionable_gap_count", 0)),
        may_discharge_gap_count=int(gap_operator.get("may_discharge_gap_count", 0)),
        missing_artifact_count=int(gap_operator.get("missing_artifact_count", 0)),
        process_gate_open_authorized=any(
            bool(report.get("process_gate_open_authorized")) for report in source_reports
        ),
        blocker_state_changed=any(
            bool(report.get("blocker_state_changed")) for report in source_reports
        ),
        candidate_emission_authorized=any(
            bool(report.get("candidate_emission_authorized")) for report in source_reports
        ),
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        issues=issues,
        checks=checks,
        source_refs=source_refs,
        non_claims=NON_CLAIMS,
        gap_operator_snapshot=gap_operator,
        gap_dependency_snapshot=gap_dependency,
        gap_index_snapshot=gap_index,
        operator_dashboard_snapshot=operator_dashboard,
    )


def gap_operator_dependency_to_dict(
    report: AnalyticDischargeGapOperatorDependencyReport,
) -> dict[str, object]:
    return {
        "schema_version": report.schema_version,
        "lemma_id": report.lemma_id,
        "candidate_status": report.candidate_status,
        "active_candidate": report.active_candidate,
        "gap_operator_markdown": report.gap_operator_markdown,
        "gap_operator_json": report.gap_operator_json,
        "gap_dependency_markdown": report.gap_dependency_markdown,
        "gap_dependency_json": report.gap_dependency_json,
        "gap_index_markdown": report.gap_index_markdown,
        "gap_index_json": report.gap_index_json,
        "operator_dashboard_markdown": report.operator_dashboard_markdown,
        "operator_dashboard_json": report.operator_dashboard_json,
        "direct_source_report_count": report.direct_source_report_count,
        "source_ref_count": report.source_ref_count,
        "operator_dependency_check_count": report.operator_dependency_check_count,
        "passed_operator_dependency_check_count": (
            report.passed_operator_dependency_check_count
        ),
        "failed_operator_dependency_check_count": (
            report.failed_operator_dependency_check_count
        ),
        "operator_dependency_consistent": report.operator_dependency_consistent,
        "gap_operator_index_check_count": report.gap_operator_index_check_count,
        "gap_operator_failed_check_count": report.gap_operator_failed_check_count,
        "gap_operator_consistent": report.gap_operator_consistent,
        "gap_dependency_check_count": report.gap_dependency_check_count,
        "gap_dependency_failed_check_count": report.gap_dependency_failed_check_count,
        "gap_dependency_consistent": report.gap_dependency_consistent,
        "gap_index_stack_consistent": report.gap_index_stack_consistent,
        "operator_dashboard_stack_consistent": report.operator_dashboard_stack_consistent,
        "gap_count": report.gap_count,
        "blocked_gap_count": report.blocked_gap_count,
        "actionable_gap_count": report.actionable_gap_count,
        "may_discharge_gap_count": report.may_discharge_gap_count,
        "missing_artifact_count": report.missing_artifact_count,
        "process_gate_open_authorized": report.process_gate_open_authorized,
        "blocker_state_changed": report.blocker_state_changed,
        "candidate_emission_authorized": report.candidate_emission_authorized,
        "missing_source_count": report.missing_source_count,
        "missing_sources": list(report.missing_sources),
        "issues": list(report.issues),
        "checks": [asdict(check) for check in report.checks],
        "source_refs": list(report.source_refs),
        "non_claims": list(report.non_claims),
        "gap_operator_snapshot": report.gap_operator_snapshot,
        "gap_dependency_snapshot": report.gap_dependency_snapshot,
        "gap_index_snapshot": report.gap_index_snapshot,
        "operator_dashboard_snapshot": report.operator_dashboard_snapshot,
        "docs": {
            "gap_index_doc": "docs/STEP102_PROMOTION_GATE_ANALYTIC_DISCHARGE_GAP_INDEX.md",
            "gap_dependency_doc": (
                "docs/STEP103_PROMOTION_GATE_ANALYTIC_DISCHARGE_GAP_DEPENDENCY.md"
            ),
            "gap_operator_index_doc": (
                "docs/STEP104_PROMOTION_GATE_ANALYTIC_DISCHARGE_GAP_OPERATOR_INDEX.md"
            ),
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _source_rows(report: AnalyticDischargeGapOperatorDependencyReport) -> list[str]:
    rows = [
        "| step | report | markdown | json |",
        "|---:|---|---|---|",
        "| 104 | `gap_operator_index` | "
        f"`{report.gap_operator_markdown}` | `{report.gap_operator_json}` |",
        "| 103 | `gap_dependency` | "
        f"`{report.gap_dependency_markdown}` | `{report.gap_dependency_json}` |",
        "| 102 | `gap_index` | "
        f"`{report.gap_index_markdown}` | `{report.gap_index_json}` |",
        "| 101 | `operator_dashboard` | "
        f"`{report.operator_dashboard_markdown}` | "
        f"`{report.operator_dashboard_json}` |",
    ]
    return rows


def _check_rows(report: AnalyticDischargeGapOperatorDependencyReport) -> list[str]:
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


def render_markdown(report: AnalyticDischargeGapOperatorDependencyReport) -> str:
    return "\n".join(
        (
            "# Promotion Gate Analytic Discharge Gap Operator Dependency",
            "",
            "Generated by `track-a-regularity/evaluator/promotion_gate_analytic_discharge_gap_operator_dependency.py`.",
            "",
            "This read-only guard bridges the Step 104 gap operator/source index back to",
            "the Step 102 gap index, Step 103 gap-dependency guard, and Step 101 analytic",
            "discharge operator dashboard. It prevents source-index drift without changing",
            "blocker state or authorizing process gates.",
            "",
            "## Summary",
            "",
            f"- lemma_id: `{report.lemma_id}`",
            f"- candidate_status: `{report.candidate_status}`",
            f"- active_candidate: `{str(report.active_candidate).lower()}`",
            f"- direct_source_report_count: `{report.direct_source_report_count}`",
            f"- source_ref_count: `{report.source_ref_count}`",
            f"- operator_dependency_check_count: `{report.operator_dependency_check_count}`",
            f"- passed_operator_dependency_check_count: `{report.passed_operator_dependency_check_count}`",
            f"- failed_operator_dependency_check_count: `{report.failed_operator_dependency_check_count}`",
            f"- operator_dependency_consistent: `{str(report.operator_dependency_consistent).lower()}`",
            f"- gap_operator_index_check_count: `{report.gap_operator_index_check_count}`",
            f"- gap_operator_failed_check_count: `{report.gap_operator_failed_check_count}`",
            f"- gap_operator_consistent: `{str(report.gap_operator_consistent).lower()}`",
            f"- gap_dependency_check_count: `{report.gap_dependency_check_count}`",
            f"- gap_dependency_failed_check_count: `{report.gap_dependency_failed_check_count}`",
            f"- gap_dependency_consistent: `{str(report.gap_dependency_consistent).lower()}`",
            f"- gap_index_stack_consistent: `{str(report.gap_index_stack_consistent).lower()}`",
            f"- operator_dashboard_stack_consistent: `{str(report.operator_dashboard_stack_consistent).lower()}`",
            f"- gap_count: `{report.gap_count}`",
            f"- blocked_gap_count: `{report.blocked_gap_count}`",
            f"- actionable_gap_count: `{report.actionable_gap_count}`",
            f"- may_discharge_gap_count: `{report.may_discharge_gap_count}`",
            f"- missing_artifact_count: `{report.missing_artifact_count}`",
            f"- process_gate_open_authorized: `{str(report.process_gate_open_authorized).lower()}`",
            f"- blocker_state_changed: `{str(report.blocker_state_changed).lower()}`",
            f"- candidate_emission_authorized: `{str(report.candidate_emission_authorized).lower()}`",
            f"- missing_source_count: `{report.missing_source_count}`",
            f"- issues: `{', '.join(report.issues) or 'none'}`",
            "",
            "## Source Reports",
            "",
            *_source_rows(report),
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


def render_json(report: AnalyticDischargeGapOperatorDependencyReport) -> str:
    return json.dumps(
        gap_operator_dependency_to_dict(report),
        indent=2,
        sort_keys=True,
    ) + "\n"


def render_output(
    report: AnalyticDischargeGapOperatorDependencyReport,
    output_format: str,
) -> str:
    if output_format == "markdown":
        return render_markdown(report)
    if output_format == "json":
        return render_json(report)
    raise ValueError(f"unknown analytic discharge gap operator dependency format: {output_format}")


def write_output(
    output: Path,
    report: AnalyticDischargeGapOperatorDependencyReport,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(report, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    report: AnalyticDischargeGapOperatorDependencyReport,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(report, output_format)
    if not output.exists():
        return False, f"missing promotion gate analytic discharge gap operator dependency: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale promotion gate analytic discharge gap operator dependency: {output}"
    return True, f"fresh promotion gate analytic discharge gap operator dependency: {output}"


def check_consistent(
    report: AnalyticDischargeGapOperatorDependencyReport,
) -> tuple[bool, str]:
    if not report.operator_dependency_consistent:
        return False, (
            "analytic discharge gap operator dependency inconsistent: "
            + ", ".join(report.issues)
        )
    return True, "analytic discharge gap operator dependency is consistent"


def check_sources(report: AnalyticDischargeGapOperatorDependencyReport) -> tuple[bool, str]:
    if report.missing_source_count:
        return False, (
            "missing analytic discharge gap operator dependency sources: "
            + ", ".join(report.missing_sources)
        )
    return True, "all analytic discharge gap operator dependency sources exist"


def check_blocked(report: AnalyticDischargeGapOperatorDependencyReport) -> tuple[bool, str]:
    if report.process_gate_open_authorized:
        return False, "process gate open became authorized"
    if report.blocker_state_changed:
        return False, "gap operator dependency changed blocker state"
    if report.candidate_emission_authorized:
        return False, "gap operator dependency authorized candidate emission"
    if report.actionable_gap_count:
        return False, "gap operator dependency found actionable gaps"
    if report.may_discharge_gap_count:
        return False, "gap operator dependency found blocker-discharge-capable gaps"
    if report.blocked_gap_count != report.gap_count:
        return False, "not all gaps remain blocked"
    return True, "analytic discharge gap operator dependency keeps gaps blocked"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown analytic discharge gap operator dependency format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check Step 104 analytic discharge gap operator dependencies."
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
        report = build_analytic_discharge_gap_operator_dependency_report(
            candidate_dir=args.candidate_dir,
            smoke_summary=args.smoke_summary,
            proof_graph_json=args.proof_graph_json,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report setup failures.
        print(
            f"failed to build analytic discharge gap operator dependency: {exc}",
            file=sys.stderr,
        )
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, report, args.format)
        print(message)
        if not ok:
            print(
                "run without --check-output to regenerate the analytic discharge gap operator dependency",
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

    print(f"operator_dependency_check_count: {report.operator_dependency_check_count}")
    print(
        "passed_operator_dependency_check_count: "
        f"{report.passed_operator_dependency_check_count}"
    )
    print(
        "failed_operator_dependency_check_count: "
        f"{report.failed_operator_dependency_check_count}"
    )
    print(
        "operator_dependency_consistent: "
        f"{str(report.operator_dependency_consistent).lower()}"
    )
    print(f"process_gate_open_authorized: {str(report.process_gate_open_authorized).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
