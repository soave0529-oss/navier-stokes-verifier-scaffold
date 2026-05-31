from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from lemma_0252_blocker_literature_dependency import (
    DEFAULT_JSON_OUTPUT as DEFAULT_LITERATURE_DEPENDENCY_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_LITERATURE_DEPENDENCY_MARKDOWN,
)
from lemma_0252_blocker_literature_gap_matrix import (
    DEFAULT_JSON_OUTPUT as DEFAULT_GAP_MATRIX_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_GAP_MATRIX_MARKDOWN,
)
from lemma_0252_blocker_literature_index import (
    DEFAULT_JSON_OUTPUT as DEFAULT_LITERATURE_INDEX_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_LITERATURE_INDEX_MARKDOWN,
)
from promotion_gate_analytic_discharge_gap_index import (
    DEFAULT_JSON_OUTPUT as DEFAULT_ANALYTIC_GAP_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_ANALYTIC_GAP_MARKDOWN,
)
from promotion_gate_analytic_discharge_operator_dashboard import (
    DEFAULT_JSON_OUTPUT as DEFAULT_OPERATOR_DASHBOARD_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_OPERATOR_DASHBOARD_MARKDOWN,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = (
    DEFAULT_REPORT_DIR / "lemma_0252_blocker_literature_gap_dependency.md"
)
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "lemma_0252_blocker_literature_gap_dependency.json"

NON_CLAIMS = (
    "read_only_literature_gap_dependency_guard",
    "canonical_report_freshness_only",
    "no_candidate_promotion",
    "no_candidate_emission",
    "no_blocker_discharge",
    "no_process_gate_opened",
    "no_epsilon_regularity_theorem",
    "no_compactness_or_liouville_theorem",
    "no_bkm_or_serrin_or_high_sobolev_bound",
    "no_weak_to_smooth_upgrade",
    "no_navier_stokes_solution",
)


@dataclass(frozen=True)
class LiteratureGapDependencyCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class Lemma0252BlockerLiteratureGapDependency:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    literature_gap_matrix_markdown: str
    literature_gap_matrix_json: str
    literature_index_markdown: str
    literature_index_json: str
    literature_dependency_markdown: str
    literature_dependency_json: str
    analytic_gap_index_markdown: str
    analytic_gap_index_json: str
    operator_dashboard_markdown: str
    operator_dashboard_json: str
    direct_source_report_count: int
    source_ref_count: int
    literature_gap_dependency_check_count: int
    passed_literature_gap_dependency_check_count: int
    failed_literature_gap_dependency_check_count: int
    literature_gap_dependency_consistent: bool
    literature_source_count: int
    gap_count: int
    source_gap_edge_count: int
    source_with_gap_count: int
    unmapped_source_count: int
    gap_with_literature_source_count: int
    gap_without_literature_source_count: int
    direct_branch_edge_count: int
    closure_bundle_edge_count: int
    blocked_gap_count: int
    actionable_gap_count: int
    may_discharge_gap_count: int
    direct_discharge_source_count: int
    literature_dependency_check_count: int
    analytic_gap_stack_consistent: bool
    operator_stack_consistent: bool
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    issues: tuple[str, ...]
    checks: tuple[LiteratureGapDependencyCheck, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]
    literature_gap_matrix_snapshot: dict[str, object]
    literature_index_snapshot: dict[str, object]
    literature_dependency_snapshot: dict[str, object]
    analytic_gap_index_snapshot: dict[str, object]
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
) -> LiteratureGapDependencyCheck:
    return LiteratureGapDependencyCheck(
        key=key,
        expected=str(expected),
        observed=str(observed),
        passed=expected == observed,
        source_artifacts=source_artifacts,
    )


def _missing_sources(source_refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(source for source in source_refs if not (ROOT / source).exists())


def _items(report: dict[str, object], key: str) -> tuple[dict[str, object], ...]:
    value = report.get(key)
    if not isinstance(value, list):
        raise ValueError(f"expected list field `{key}`")
    return tuple(item for item in value if isinstance(item, dict))


def _values(items: tuple[dict[str, object], ...], key: str) -> tuple[object, ...]:
    return tuple(item.get(key) for item in items)


def _expected_edge_count(source_summaries: tuple[dict[str, object], ...]) -> int:
    return sum(
        len(summary.get("target_gap_ids", ()))
        for summary in source_summaries
        if isinstance(summary.get("target_gap_ids", ()), list)
    )


def _direct_sources() -> tuple[str, ...]:
    return (
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.json",
        "track-a-regularity/reports/lemma_0252_blocker_literature_index.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_index.json",
        "track-a-regularity/reports/lemma_0252_blocker_literature_dependency.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_dependency.json",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.md",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.json",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_operator_dashboard.md",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_operator_dashboard.json",
    )


def build_blocker_literature_gap_dependency(
    *,
    literature_gap_matrix_json: Path = DEFAULT_GAP_MATRIX_JSON,
    literature_index_json: Path = DEFAULT_LITERATURE_INDEX_JSON,
    literature_dependency_json: Path = DEFAULT_LITERATURE_DEPENDENCY_JSON,
    analytic_gap_json: Path = DEFAULT_ANALYTIC_GAP_JSON,
    operator_dashboard_json: Path = DEFAULT_OPERATOR_DASHBOARD_JSON,
) -> Lemma0252BlockerLiteratureGapDependency:
    matrix = _load_json(literature_gap_matrix_json)
    literature = _load_json(literature_index_json)
    dependency = _load_json(literature_dependency_json)
    analytic_gap = _load_json(analytic_gap_json)
    operator = _load_json(operator_dashboard_json)

    matrix_source = (
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.json",
    )
    literature_source = (
        "track-a-regularity/reports/lemma_0252_blocker_literature_index.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_index.json",
    )
    dependency_source = (
        "track-a-regularity/reports/lemma_0252_blocker_literature_dependency.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_dependency.json",
    )
    analytic_gap_source = (
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.md",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.json",
    )
    operator_source = (
        "track-a-regularity/reports/promotion_gate_analytic_discharge_operator_dashboard.md",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_operator_dashboard.json",
    )
    source_refs = tuple(
        dict.fromkeys(
            _direct_sources()
            + tuple(str(item) for item in matrix.get("source_refs", ()))
            + tuple(str(item) for item in dependency.get("source_refs", ()))
            + tuple(str(item) for item in analytic_gap.get("source_refs", ()))
            + tuple(str(item) for item in operator.get("source_refs", ()))
        )
    )
    missing_sources = _missing_sources(source_refs)

    literature_sources = _items(literature, "sources")
    matrix_summaries = _items(matrix, "source_summaries")
    matrix_edges = _items(matrix, "edges")
    matrix_coverages = _items(matrix, "gap_coverages")
    analytic_gaps = _items(analytic_gap, "gaps")

    literature_source_ids = tuple(str(item.get("source_id")) for item in literature_sources)
    matrix_source_ids = tuple(str(item.get("source_id")) for item in matrix_summaries)
    analytic_gap_ids = tuple(sorted(str(item.get("gap_id")) for item in analytic_gaps))
    matrix_gap_ids = tuple(sorted(str(item.get("gap_id")) for item in matrix_coverages))
    analytic_gap_by_id = {str(item.get("gap_id")): item for item in analytic_gaps}
    matrix_gap_by_id = {str(item.get("gap_id")): item for item in matrix_coverages}
    analytic_gap_artifact_types = tuple(
        str(analytic_gap_by_id[gap_id].get("required_artifact_type"))
        for gap_id in analytic_gap_ids
    )
    matrix_gap_artifact_types = tuple(
        str(matrix_gap_by_id[gap_id].get("required_artifact_type"))
        for gap_id in analytic_gap_ids
    )
    analytic_gap_source_branches = tuple(
        str(analytic_gap_by_id[gap_id].get("source_branch"))
        for gap_id in analytic_gap_ids
    )
    matrix_gap_source_branches = tuple(
        str(matrix_gap_by_id[gap_id].get("source_branch"))
        for gap_id in analytic_gap_ids
    )
    expected_edge_count = _expected_edge_count(matrix_summaries)

    checks = (
        _check(
            key="matrix.lemma_id.matches_literature_index",
            expected=literature.get("lemma_id"),
            observed=matrix.get("lemma_id"),
            source_artifacts=matrix_source + literature_source,
        ),
        _check(
            key="matrix.lemma_id.matches_literature_dependency",
            expected=dependency.get("lemma_id"),
            observed=matrix.get("lemma_id"),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="matrix.lemma_id.matches_analytic_gap_index",
            expected=analytic_gap.get("lemma_id"),
            observed=matrix.get("lemma_id"),
            source_artifacts=matrix_source + analytic_gap_source,
        ),
        _check(
            key="matrix.lemma_id.matches_operator_dashboard",
            expected=operator.get("lemma_id"),
            observed=matrix.get("lemma_id"),
            source_artifacts=matrix_source + operator_source,
        ),
        _check(
            key="matrix.candidate_status.matches_literature_index",
            expected=literature.get("candidate_status"),
            observed=matrix.get("candidate_status"),
            source_artifacts=matrix_source + literature_source,
        ),
        _check(
            key="matrix.candidate_status.matches_analytic_gap_index",
            expected=analytic_gap.get("candidate_status"),
            observed=matrix.get("candidate_status"),
            source_artifacts=matrix_source + analytic_gap_source,
        ),
        _check(
            key="matrix.active_candidate.matches_literature_index",
            expected=literature.get("active_candidate"),
            observed=matrix.get("active_candidate"),
            source_artifacts=matrix_source + literature_source,
        ),
        _check(
            key="matrix.active_candidate.matches_analytic_gap_index",
            expected=analytic_gap.get("active_candidate"),
            observed=matrix.get("active_candidate"),
            source_artifacts=matrix_source + analytic_gap_source,
        ),
        _check(
            key="matrix.literature_source_count.matches_index",
            expected=literature.get("literature_source_count"),
            observed=matrix.get("literature_source_count"),
            source_artifacts=matrix_source + literature_source,
        ),
        _check(
            key="matrix.literature_source_count.matches_dependency",
            expected=dependency.get("literature_source_count"),
            observed=matrix.get("literature_source_count"),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="matrix.source_ids.match_literature_sources",
            expected=literature_source_ids,
            observed=matrix_source_ids,
            source_artifacts=matrix_source + literature_source,
        ),
        _check(
            key="matrix.source_with_gap_count.matches_literature_sources",
            expected=literature.get("literature_source_count"),
            observed=matrix.get("source_with_gap_count"),
            source_artifacts=matrix_source + literature_source,
        ),
        _check(
            key="matrix.unmapped_source_count.remains_zero",
            expected=0,
            observed=matrix.get("unmapped_source_count"),
            source_artifacts=matrix_source,
        ),
        _check(
            key="matrix.source_gap_edge_count.matches_edges",
            expected=len(matrix_edges),
            observed=matrix.get("source_gap_edge_count"),
            source_artifacts=matrix_source,
        ),
        _check(
            key="matrix.source_gap_edge_count.matches_summary_targets",
            expected=expected_edge_count,
            observed=matrix.get("source_gap_edge_count"),
            source_artifacts=matrix_source,
        ),
        _check(
            key="matrix.gap_count.matches_analytic_gap_index",
            expected=analytic_gap.get("gap_count"),
            observed=matrix.get("gap_count"),
            source_artifacts=matrix_source + analytic_gap_source,
        ),
        _check(
            key="matrix.gap_ids.match_analytic_gap_index",
            expected=analytic_gap_ids,
            observed=matrix_gap_ids,
            source_artifacts=matrix_source + analytic_gap_source,
        ),
        _check(
            key="matrix.gap_artifact_types.match_analytic_gap_index",
            expected=analytic_gap_artifact_types,
            observed=matrix_gap_artifact_types,
            source_artifacts=matrix_source + analytic_gap_source,
        ),
        _check(
            key="matrix.gap_source_branches.match_analytic_gap_index",
            expected=analytic_gap_source_branches,
            observed=matrix_gap_source_branches,
            source_artifacts=matrix_source + analytic_gap_source,
        ),
        _check(
            key="matrix.blocked_gap_count.matches_analytic_gap_index",
            expected=analytic_gap.get("blocked_gap_count"),
            observed=matrix.get("blocked_gap_count"),
            source_artifacts=matrix_source + analytic_gap_source,
        ),
        _check(
            key="matrix.actionable_gap_count.matches_analytic_gap_index",
            expected=analytic_gap.get("actionable_gap_count"),
            observed=matrix.get("actionable_gap_count"),
            source_artifacts=matrix_source + analytic_gap_source,
        ),
        _check(
            key="matrix.may_discharge_gap_count.matches_analytic_gap_index",
            expected=analytic_gap.get("may_discharge_gap_count"),
            observed=matrix.get("may_discharge_gap_count"),
            source_artifacts=matrix_source + analytic_gap_source,
        ),
        _check(
            key="matrix.gap_stack_consistent.matches_analytic_gap_index",
            expected=analytic_gap.get("stack_consistent"),
            observed=matrix.get("gap_stack_consistent"),
            source_artifacts=matrix_source + analytic_gap_source,
        ),
        _check(
            key="matrix.gap_stack_consistent.matches_operator_dashboard",
            expected=operator.get("stack_consistent"),
            observed=matrix.get("gap_stack_consistent"),
            source_artifacts=matrix_source + operator_source,
        ),
        _check(
            key="matrix.literature_dependency_consistent.matches_dependency_guard",
            expected=dependency.get("literature_dependency_consistent"),
            observed=matrix.get("literature_dependency_consistent"),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="dependency.failed_literature_dependency_check_count.remains_zero",
            expected=0,
            observed=dependency.get("failed_literature_dependency_check_count"),
            source_artifacts=dependency_source,
        ),
        _check(
            key="matrix.direct_discharge_source_count.matches_literature_index",
            expected=literature.get("direct_discharge_source_count"),
            observed=matrix.get("direct_discharge_source_count"),
            source_artifacts=matrix_source + literature_source,
        ),
        _check(
            key="matrix.direct_discharge_source_count.matches_dependency_guard",
            expected=dependency.get("direct_discharge_source_count"),
            observed=matrix.get("direct_discharge_source_count"),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="matrix.gap_with_literature_source_count.expected_five",
            expected=5,
            observed=matrix.get("gap_with_literature_source_count"),
            source_artifacts=matrix_source,
        ),
        _check(
            key="matrix.gap_without_literature_source_count.expected_three",
            expected=3,
            observed=matrix.get("gap_without_literature_source_count"),
            source_artifacts=matrix_source,
        ),
        _check(
            key="matrix.direct_branch_edge_count.expected_twelve",
            expected=12,
            observed=matrix.get("direct_branch_edge_count"),
            source_artifacts=matrix_source,
        ),
        _check(
            key="matrix.closure_bundle_edge_count.expected_thirty",
            expected=30,
            observed=matrix.get("closure_bundle_edge_count"),
            source_artifacts=matrix_source,
        ),
        _check(
            key="matrix.checks.all_passed",
            expected=True,
            observed=all(
                bool(check.get("passed"))
                for check in _items(matrix, "checks")
            ),
            source_artifacts=matrix_source,
        ),
        _check(
            key="operator.stack_consistent.true",
            expected=True,
            observed=operator.get("stack_consistent"),
            source_artifacts=operator_source,
        ),
        _check(
            key="all.process_gate_open_authorized.false",
            expected=(False, False, False, False, False),
            observed=(
                matrix.get("process_gate_open_authorized"),
                literature.get("process_gate_open_authorized"),
                dependency.get("process_gate_open_authorized"),
                analytic_gap.get("process_gate_open_authorized"),
                operator.get("process_gate_open_authorized"),
            ),
            source_artifacts=(
                matrix_source
                + literature_source
                + dependency_source
                + analytic_gap_source
                + operator_source
            ),
        ),
        _check(
            key="all.blocker_state_changed.false",
            expected=(False, False, False, False, False),
            observed=(
                matrix.get("blocker_state_changed"),
                literature.get("blocker_state_changed"),
                dependency.get("blocker_state_changed"),
                analytic_gap.get("blocker_state_changed"),
                operator.get("blocker_state_changed"),
            ),
            source_artifacts=(
                matrix_source
                + literature_source
                + dependency_source
                + analytic_gap_source
                + operator_source
            ),
        ),
        _check(
            key="all.candidate_emission_authorized.false",
            expected=(False, False, False, False, False),
            observed=(
                matrix.get("candidate_emission_authorized"),
                literature.get("candidate_emission_authorized"),
                dependency.get("candidate_emission_authorized"),
                analytic_gap.get("candidate_emission_authorized"),
                operator.get("candidate_emission_authorized"),
            ),
            source_artifacts=(
                matrix_source
                + literature_source
                + dependency_source
                + analytic_gap_source
                + operator_source
            ),
        ),
        _check(
            key="source_refs.missing_count.remains_zero",
            expected=0,
            observed=len(missing_sources),
            source_artifacts=source_refs,
        ),
    )
    issues = tuple(check.key for check in checks if not check.passed)

    return Lemma0252BlockerLiteratureGapDependency(
        schema_version=1,
        lemma_id=str(matrix.get("lemma_id")),
        candidate_status=str(matrix.get("candidate_status")),
        active_candidate=bool(matrix.get("active_candidate")),
        literature_gap_matrix_markdown=str(DEFAULT_GAP_MATRIX_MARKDOWN),
        literature_gap_matrix_json=str(DEFAULT_GAP_MATRIX_JSON),
        literature_index_markdown=str(DEFAULT_LITERATURE_INDEX_MARKDOWN),
        literature_index_json=str(DEFAULT_LITERATURE_INDEX_JSON),
        literature_dependency_markdown=str(DEFAULT_LITERATURE_DEPENDENCY_MARKDOWN),
        literature_dependency_json=str(DEFAULT_LITERATURE_DEPENDENCY_JSON),
        analytic_gap_index_markdown=str(DEFAULT_ANALYTIC_GAP_MARKDOWN),
        analytic_gap_index_json=str(DEFAULT_ANALYTIC_GAP_JSON),
        operator_dashboard_markdown=str(DEFAULT_OPERATOR_DASHBOARD_MARKDOWN),
        operator_dashboard_json=str(DEFAULT_OPERATOR_DASHBOARD_JSON),
        direct_source_report_count=len(_direct_sources()),
        source_ref_count=len(source_refs),
        literature_gap_dependency_check_count=len(checks),
        passed_literature_gap_dependency_check_count=sum(
            1 for check in checks if check.passed
        ),
        failed_literature_gap_dependency_check_count=len(issues),
        literature_gap_dependency_consistent=not issues,
        literature_source_count=int(matrix.get("literature_source_count", 0)),
        gap_count=int(matrix.get("gap_count", 0)),
        source_gap_edge_count=int(matrix.get("source_gap_edge_count", 0)),
        source_with_gap_count=int(matrix.get("source_with_gap_count", 0)),
        unmapped_source_count=int(matrix.get("unmapped_source_count", 0)),
        gap_with_literature_source_count=int(
            matrix.get("gap_with_literature_source_count", 0)
        ),
        gap_without_literature_source_count=int(
            matrix.get("gap_without_literature_source_count", 0)
        ),
        direct_branch_edge_count=int(matrix.get("direct_branch_edge_count", 0)),
        closure_bundle_edge_count=int(matrix.get("closure_bundle_edge_count", 0)),
        blocked_gap_count=int(matrix.get("blocked_gap_count", 0)),
        actionable_gap_count=int(matrix.get("actionable_gap_count", 0)),
        may_discharge_gap_count=int(matrix.get("may_discharge_gap_count", 0)),
        direct_discharge_source_count=int(matrix.get("direct_discharge_source_count", 0)),
        literature_dependency_check_count=int(
            dependency.get("literature_dependency_check_count", 0)
        ),
        analytic_gap_stack_consistent=bool(analytic_gap.get("stack_consistent")),
        operator_stack_consistent=bool(operator.get("stack_consistent")),
        process_gate_open_authorized=False,
        blocker_state_changed=False,
        candidate_emission_authorized=False,
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        issues=issues,
        checks=checks,
        source_refs=source_refs,
        non_claims=NON_CLAIMS,
        literature_gap_matrix_snapshot=matrix,
        literature_index_snapshot=literature,
        literature_dependency_snapshot=dependency,
        analytic_gap_index_snapshot=analytic_gap,
        operator_dashboard_snapshot=operator,
    )


def literature_gap_dependency_to_dict(
    report: Lemma0252BlockerLiteratureGapDependency,
) -> dict[str, object]:
    return {
        "schema_version": report.schema_version,
        "lemma_id": report.lemma_id,
        "candidate_status": report.candidate_status,
        "active_candidate": report.active_candidate,
        "literature_gap_matrix_markdown": report.literature_gap_matrix_markdown,
        "literature_gap_matrix_json": report.literature_gap_matrix_json,
        "literature_index_markdown": report.literature_index_markdown,
        "literature_index_json": report.literature_index_json,
        "literature_dependency_markdown": report.literature_dependency_markdown,
        "literature_dependency_json": report.literature_dependency_json,
        "analytic_gap_index_markdown": report.analytic_gap_index_markdown,
        "analytic_gap_index_json": report.analytic_gap_index_json,
        "operator_dashboard_markdown": report.operator_dashboard_markdown,
        "operator_dashboard_json": report.operator_dashboard_json,
        "direct_source_report_count": report.direct_source_report_count,
        "source_ref_count": report.source_ref_count,
        "literature_gap_dependency_check_count": report.literature_gap_dependency_check_count,
        "passed_literature_gap_dependency_check_count": (
            report.passed_literature_gap_dependency_check_count
        ),
        "failed_literature_gap_dependency_check_count": (
            report.failed_literature_gap_dependency_check_count
        ),
        "literature_gap_dependency_consistent": (
            report.literature_gap_dependency_consistent
        ),
        "literature_source_count": report.literature_source_count,
        "gap_count": report.gap_count,
        "source_gap_edge_count": report.source_gap_edge_count,
        "source_with_gap_count": report.source_with_gap_count,
        "unmapped_source_count": report.unmapped_source_count,
        "gap_with_literature_source_count": report.gap_with_literature_source_count,
        "gap_without_literature_source_count": report.gap_without_literature_source_count,
        "direct_branch_edge_count": report.direct_branch_edge_count,
        "closure_bundle_edge_count": report.closure_bundle_edge_count,
        "blocked_gap_count": report.blocked_gap_count,
        "actionable_gap_count": report.actionable_gap_count,
        "may_discharge_gap_count": report.may_discharge_gap_count,
        "direct_discharge_source_count": report.direct_discharge_source_count,
        "literature_dependency_check_count": report.literature_dependency_check_count,
        "analytic_gap_stack_consistent": report.analytic_gap_stack_consistent,
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
        "literature_gap_matrix_snapshot": report.literature_gap_matrix_snapshot,
        "literature_index_snapshot": report.literature_index_snapshot,
        "literature_dependency_snapshot": report.literature_dependency_snapshot,
        "analytic_gap_index_snapshot": report.analytic_gap_index_snapshot,
        "operator_dashboard_snapshot": report.operator_dashboard_snapshot,
        "docs": {
            "step_doc": (
                "docs/STEP109_LEMMA_0252_BLOCKER_LITERATURE_GAP_DEPENDENCY.md"
            ),
            "gap_matrix_doc": (
                "docs/STEP108_LEMMA_0252_BLOCKER_LITERATURE_GAP_MATRIX.md"
            ),
            "literature_index_doc": (
                "docs/STEP106_LEMMA_0252_BLOCKER_LITERATURE_INDEX.md"
            ),
            "literature_dependency_doc": (
                "docs/STEP107_LEMMA_0252_BLOCKER_LITERATURE_DEPENDENCY.md"
            ),
            "analytic_gap_index_doc": (
                "docs/STEP102_PROMOTION_GATE_ANALYTIC_DISCHARGE_GAP_INDEX.md"
            ),
            "operator_dashboard_doc": (
                "docs/STEP101_PROMOTION_GATE_ANALYTIC_DISCHARGE_OPERATOR_DASHBOARD.md"
            ),
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _summary_lines(report: Lemma0252BlockerLiteratureGapDependency) -> tuple[str, ...]:
    keys = (
        "lemma_id",
        "candidate_status",
        "active_candidate",
        "direct_source_report_count",
        "source_ref_count",
        "literature_gap_dependency_check_count",
        "passed_literature_gap_dependency_check_count",
        "failed_literature_gap_dependency_check_count",
        "literature_gap_dependency_consistent",
        "literature_source_count",
        "gap_count",
        "source_gap_edge_count",
        "source_with_gap_count",
        "unmapped_source_count",
        "gap_with_literature_source_count",
        "gap_without_literature_source_count",
        "direct_branch_edge_count",
        "closure_bundle_edge_count",
        "blocked_gap_count",
        "actionable_gap_count",
        "may_discharge_gap_count",
        "direct_discharge_source_count",
        "literature_dependency_check_count",
        "analytic_gap_stack_consistent",
        "operator_stack_consistent",
        "process_gate_open_authorized",
        "blocker_state_changed",
        "candidate_emission_authorized",
        "missing_source_count",
    )
    data = literature_gap_dependency_to_dict(report)
    return tuple(f"- {key}: `{str(data[key]).lower()}`" for key in keys)


def _check_rows(report: Lemma0252BlockerLiteratureGapDependency) -> list[str]:
    rows = [
        "| check | expected | observed | passed |",
        "|---|---|---|---|",
    ]
    for check in report.checks:
        rows.append(
            "| "
            f"`{check.key}` | "
            f"`{_format(check.expected)}` | "
            f"`{_format(check.observed)}` | "
            f"`{str(check.passed).lower()}` |"
        )
    return rows


def render_markdown(report: Lemma0252BlockerLiteratureGapDependency) -> str:
    return "\n".join(
        (
            "# Lemma 0252 Blocker Literature Gap Dependency",
            "",
            "Generated by `track-a-regularity/evaluator/lemma_0252_blocker_literature_gap_dependency.py`.",
            "",
            "This read-only dependency guard prevents the Step 108 blocker-literature gap matrix",
            "from drifting away from the Step 106 literature index, Step 107 literature dependency",
            "guard, Step 102 analytic-discharge gap index, and Step 101 analytic-discharge operator",
            "dashboard. It is a freshness and consistency surface only.",
            "",
            "## Summary",
            "",
            *_summary_lines(report),
            f"- issues: `{', '.join(report.issues) or 'none'}`",
            "",
            "## Consistency Checks",
            "",
            *_check_rows(report),
            "",
            "## Source Reports",
            "",
            "- `track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.md`",
            "- `track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.json`",
            "- `track-a-regularity/reports/lemma_0252_blocker_literature_index.md`",
            "- `track-a-regularity/reports/lemma_0252_blocker_literature_index.json`",
            "- `track-a-regularity/reports/lemma_0252_blocker_literature_dependency.md`",
            "- `track-a-regularity/reports/lemma_0252_blocker_literature_dependency.json`",
            "- `track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.md`",
            "- `track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.json`",
            "- `track-a-regularity/reports/promotion_gate_analytic_discharge_operator_dashboard.md`",
            "- `track-a-regularity/reports/promotion_gate_analytic_discharge_operator_dashboard.json`",
            "",
            "## Non-Claims",
            "",
            *(f"- `{item}`" for item in report.non_claims),
            "",
        )
    )


def render_json(report: Lemma0252BlockerLiteratureGapDependency) -> str:
    return json.dumps(literature_gap_dependency_to_dict(report), indent=2, sort_keys=True) + "\n"


def render_output(
    report: Lemma0252BlockerLiteratureGapDependency,
    output_format: str,
) -> str:
    if output_format == "markdown":
        return render_markdown(report)
    if output_format == "json":
        return render_json(report)
    raise ValueError(f"unknown blocker literature gap dependency format: {output_format}")


def write_output(
    output: Path,
    report: Lemma0252BlockerLiteratureGapDependency,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(report, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    report: Lemma0252BlockerLiteratureGapDependency,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(report, output_format)
    if not output.exists():
        return False, f"missing lemma_0252 blocker literature gap dependency: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale lemma_0252 blocker literature gap dependency: {output}"
    return True, f"fresh lemma_0252 blocker literature gap dependency: {output}"


def check_sources(report: Lemma0252BlockerLiteratureGapDependency) -> tuple[bool, str]:
    if report.missing_source_count:
        return False, "missing blocker literature gap dependency sources: " + ", ".join(
            report.missing_sources
        )
    return True, "all blocker literature gap dependency sources exist"


def check_consistent(report: Lemma0252BlockerLiteratureGapDependency) -> tuple[bool, str]:
    if report.issues:
        return False, "blocker literature gap dependency has issues: " + ", ".join(
            report.issues
        )
    if not report.literature_gap_dependency_consistent:
        return False, "blocker literature gap dependency is inconsistent"
    if not report.analytic_gap_stack_consistent:
        return False, "analytic gap stack is inconsistent"
    if not report.operator_stack_consistent:
        return False, "operator dashboard stack is inconsistent"
    return True, "blocker literature gap dependency is consistent"


def check_blocked(report: Lemma0252BlockerLiteratureGapDependency) -> tuple[bool, str]:
    if report.process_gate_open_authorized:
        return False, "process gate open became authorized"
    if report.blocker_state_changed:
        return False, "literature gap dependency changed blocker state"
    if report.candidate_emission_authorized:
        return False, "literature gap dependency authorized candidate emission"
    if report.actionable_gap_count:
        return False, "literature gap dependency marked a gap actionable"
    if report.may_discharge_gap_count:
        return False, "literature gap dependency marked a gap as discharge-capable"
    if report.direct_discharge_source_count:
        return False, "literature gap dependency found a direct discharge source"
    return True, "blocker literature gap dependency keeps every gap blocked"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown blocker literature gap dependency format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a dependency guard for the lemma_0252 blocker-literature gap matrix."
    )
    parser.add_argument("--literature-gap-matrix-json", type=Path, default=DEFAULT_GAP_MATRIX_JSON)
    parser.add_argument("--literature-index-json", type=Path, default=DEFAULT_LITERATURE_INDEX_JSON)
    parser.add_argument(
        "--literature-dependency-json",
        type=Path,
        default=DEFAULT_LITERATURE_DEPENDENCY_JSON,
    )
    parser.add_argument("--analytic-gap-json", type=Path, default=DEFAULT_ANALYTIC_GAP_JSON)
    parser.add_argument(
        "--operator-dashboard-json",
        type=Path,
        default=DEFAULT_OPERATOR_DASHBOARD_JSON,
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    parser.add_argument("--require-consistent", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    args = parser.parse_args(argv)

    try:
        report = build_blocker_literature_gap_dependency(
            literature_gap_matrix_json=args.literature_gap_matrix_json,
            literature_index_json=args.literature_index_json,
            literature_dependency_json=args.literature_dependency_json,
            analytic_gap_json=args.analytic_gap_json,
            operator_dashboard_json=args.operator_dashboard_json,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report setup failures.
        print(f"failed to build blocker literature gap dependency: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, report, args.format)
        print(message)
        if not ok:
            print(
                "run without --check-output to regenerate the blocker literature gap dependency",
                file=sys.stderr,
            )
            return 1
    else:
        written = write_output(output, report, args.format)
        print(f"wrote {written}")

    if args.require_sources_exist:
        ok, message = check_sources(report)
        print(message)
        if not ok:
            return 1
    if args.require_consistent:
        ok, message = check_consistent(report)
        print(message)
        if not ok:
            return 1
    if args.require_blocked:
        ok, message = check_blocked(report)
        print(message)
        if not ok:
            return 1

    print(f"literature_gap_dependency_check_count: {report.literature_gap_dependency_check_count}")
    print(
        "failed_literature_gap_dependency_check_count: "
        f"{report.failed_literature_gap_dependency_check_count}"
    )
    print(f"source_ref_count: {report.source_ref_count}")
    print(f"literature_source_count: {report.literature_source_count}")
    print(f"gap_count: {report.gap_count}")
    print(f"source_gap_edge_count: {report.source_gap_edge_count}")
    print(f"candidate_emission_authorized: {str(report.candidate_emission_authorized).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
