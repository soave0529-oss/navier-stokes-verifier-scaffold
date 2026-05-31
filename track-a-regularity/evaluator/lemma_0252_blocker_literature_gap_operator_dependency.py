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
from lemma_0252_blocker_literature_gap_dependency import (
    DEFAULT_JSON_OUTPUT as DEFAULT_GAP_DEPENDENCY_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_GAP_DEPENDENCY_MARKDOWN,
)
from lemma_0252_blocker_literature_gap_matrix import (
    DEFAULT_JSON_OUTPUT as DEFAULT_GAP_MATRIX_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_GAP_MATRIX_MARKDOWN,
)
from lemma_0252_blocker_literature_gap_operator_index import (
    DEFAULT_JSON_OUTPUT as DEFAULT_GAP_OPERATOR_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_GAP_OPERATOR_MARKDOWN,
)
from lemma_0252_blocker_literature_index import (
    DEFAULT_JSON_OUTPUT as DEFAULT_LITERATURE_INDEX_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_LITERATURE_INDEX_MARKDOWN,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_blocker_literature_gap_operator_dependency.md"
)
DEFAULT_JSON_OUTPUT = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_blocker_literature_gap_operator_dependency.json"
)

NON_CLAIMS = (
    "read_only_literature_gap_operator_dependency_guard",
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
class LiteratureGapOperatorDependencyCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class Lemma0252BlockerLiteratureGapOperatorDependency:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    literature_gap_operator_markdown: str
    literature_gap_operator_json: str
    literature_gap_matrix_markdown: str
    literature_gap_matrix_json: str
    literature_gap_dependency_markdown: str
    literature_gap_dependency_json: str
    literature_index_markdown: str
    literature_index_json: str
    literature_dependency_markdown: str
    literature_dependency_json: str
    direct_source_report_count: int
    source_ref_count: int
    literature_gap_operator_dependency_check_count: int
    passed_literature_gap_operator_dependency_check_count: int
    failed_literature_gap_operator_dependency_check_count: int
    literature_gap_operator_dependency_consistent: bool
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
    literature_gap_dependency_check_count: int
    failed_literature_gap_dependency_check_count: int
    literature_gap_operator_index_check_count: int
    failed_literature_gap_operator_index_check_count: int
    literature_dependency_consistent: bool
    literature_gap_dependency_consistent: bool
    literature_gap_operator_index_consistent: bool
    analytic_gap_stack_consistent: bool
    operator_stack_consistent: bool
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    issues: tuple[str, ...]
    checks: tuple[LiteratureGapOperatorDependencyCheck, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]
    literature_gap_operator_snapshot: dict[str, object]
    literature_gap_matrix_snapshot: dict[str, object]
    literature_gap_dependency_snapshot: dict[str, object]
    literature_index_snapshot: dict[str, object]
    literature_dependency_snapshot: dict[str, object]


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
) -> LiteratureGapOperatorDependencyCheck:
    return LiteratureGapOperatorDependencyCheck(
        key=key,
        expected=str(expected),
        observed=str(observed),
        passed=expected == observed,
        source_artifacts=source_artifacts,
    )


def _missing_sources(source_refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(source for source in source_refs if not (ROOT / source).exists())


def _direct_sources() -> tuple[str, ...]:
    return (
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_operator_index.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_operator_index.json",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.json",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_dependency.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_dependency.json",
        "track-a-regularity/reports/lemma_0252_blocker_literature_index.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_index.json",
        "track-a-regularity/reports/lemma_0252_blocker_literature_dependency.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_dependency.json",
    )


def build_blocker_literature_gap_operator_dependency(
    *,
    literature_gap_operator_json: Path = DEFAULT_GAP_OPERATOR_JSON,
    literature_gap_matrix_json: Path = DEFAULT_GAP_MATRIX_JSON,
    literature_gap_dependency_json: Path = DEFAULT_GAP_DEPENDENCY_JSON,
    literature_index_json: Path = DEFAULT_LITERATURE_INDEX_JSON,
    literature_dependency_json: Path = DEFAULT_LITERATURE_DEPENDENCY_JSON,
) -> Lemma0252BlockerLiteratureGapOperatorDependency:
    operator = _load_json(literature_gap_operator_json)
    matrix = _load_json(literature_gap_matrix_json)
    gap_dependency = _load_json(literature_gap_dependency_json)
    literature = _load_json(literature_index_json)
    literature_dependency = _load_json(literature_dependency_json)

    operator_source = (
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_operator_index.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_operator_index.json",
    )
    matrix_source = (
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.json",
    )
    gap_dependency_source = (
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_dependency.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_dependency.json",
    )
    literature_source = (
        "track-a-regularity/reports/lemma_0252_blocker_literature_index.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_index.json",
    )
    literature_dependency_source = (
        "track-a-regularity/reports/lemma_0252_blocker_literature_dependency.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_dependency.json",
    )
    source_refs = tuple(
        dict.fromkeys(
            _direct_sources()
            + tuple(str(item) for item in operator.get("source_refs", ()))
            + tuple(str(item) for item in matrix.get("source_refs", ()))
            + tuple(str(item) for item in gap_dependency.get("source_refs", ()))
            + tuple(str(item) for item in literature.get("source_refs", ()))
            + tuple(str(item) for item in literature_dependency.get("source_refs", ()))
        )
    )
    missing_sources = _missing_sources(source_refs)

    checks = (
        _check(
            key="operator.lemma_id.matches_matrix",
            expected=matrix.get("lemma_id"),
            observed=operator.get("lemma_id"),
            source_artifacts=operator_source + matrix_source,
        ),
        _check(
            key="operator.lemma_id.matches_gap_dependency",
            expected=gap_dependency.get("lemma_id"),
            observed=operator.get("lemma_id"),
            source_artifacts=operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.lemma_id.matches_literature_index",
            expected=literature.get("lemma_id"),
            observed=operator.get("lemma_id"),
            source_artifacts=operator_source + literature_source,
        ),
        _check(
            key="operator.lemma_id.matches_literature_dependency",
            expected=literature_dependency.get("lemma_id"),
            observed=operator.get("lemma_id"),
            source_artifacts=operator_source + literature_dependency_source,
        ),
        _check(
            key="operator.candidate_status.matches_matrix",
            expected=matrix.get("candidate_status"),
            observed=operator.get("candidate_status"),
            source_artifacts=operator_source + matrix_source,
        ),
        _check(
            key="operator.candidate_status.matches_literature_index",
            expected=literature.get("candidate_status"),
            observed=operator.get("candidate_status"),
            source_artifacts=operator_source + literature_source,
        ),
        _check(
            key="operator.active_candidate.matches_matrix",
            expected=matrix.get("active_candidate"),
            observed=operator.get("active_candidate"),
            source_artifacts=operator_source + matrix_source,
        ),
        _check(
            key="operator.active_candidate.matches_literature_index",
            expected=literature.get("active_candidate"),
            observed=operator.get("active_candidate"),
            source_artifacts=operator_source + literature_source,
        ),
        _check(
            key="operator.literature_source_count.matches_matrix",
            expected=matrix.get("literature_source_count"),
            observed=operator.get("literature_source_count"),
            source_artifacts=operator_source + matrix_source,
        ),
        _check(
            key="operator.literature_source_count.matches_literature_index",
            expected=literature.get("literature_source_count"),
            observed=operator.get("literature_source_count"),
            source_artifacts=operator_source + literature_source,
        ),
        _check(
            key="operator.literature_source_count.matches_literature_dependency",
            expected=literature_dependency.get("literature_source_count"),
            observed=operator.get("literature_source_count"),
            source_artifacts=operator_source + literature_dependency_source,
        ),
        _check(
            key="operator.gap_count.matches_matrix",
            expected=matrix.get("gap_count"),
            observed=operator.get("gap_count"),
            source_artifacts=operator_source + matrix_source,
        ),
        _check(
            key="operator.gap_count.matches_gap_dependency",
            expected=gap_dependency.get("gap_count"),
            observed=operator.get("gap_count"),
            source_artifacts=operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.source_gap_edge_count.matches_matrix",
            expected=matrix.get("source_gap_edge_count"),
            observed=operator.get("source_gap_edge_count"),
            source_artifacts=operator_source + matrix_source,
        ),
        _check(
            key="operator.source_gap_edge_count.matches_gap_dependency",
            expected=gap_dependency.get("source_gap_edge_count"),
            observed=operator.get("source_gap_edge_count"),
            source_artifacts=operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.source_with_gap_count.matches_matrix",
            expected=matrix.get("source_with_gap_count"),
            observed=operator.get("source_with_gap_count"),
            source_artifacts=operator_source + matrix_source,
        ),
        _check(
            key="operator.unmapped_source_count.remains_zero",
            expected=0,
            observed=operator.get("unmapped_source_count"),
            source_artifacts=operator_source,
        ),
        _check(
            key="operator.gap_with_literature_source_count.matches_matrix",
            expected=matrix.get("gap_with_literature_source_count"),
            observed=operator.get("gap_with_literature_source_count"),
            source_artifacts=operator_source + matrix_source,
        ),
        _check(
            key="operator.gap_without_literature_source_count.matches_matrix",
            expected=matrix.get("gap_without_literature_source_count"),
            observed=operator.get("gap_without_literature_source_count"),
            source_artifacts=operator_source + matrix_source,
        ),
        _check(
            key="operator.direct_branch_edge_count.matches_gap_dependency",
            expected=gap_dependency.get("direct_branch_edge_count"),
            observed=operator.get("direct_branch_edge_count"),
            source_artifacts=operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.closure_bundle_edge_count.matches_gap_dependency",
            expected=gap_dependency.get("closure_bundle_edge_count"),
            observed=operator.get("closure_bundle_edge_count"),
            source_artifacts=operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.blocked_gap_count.matches_gap_dependency",
            expected=gap_dependency.get("blocked_gap_count"),
            observed=operator.get("blocked_gap_count"),
            source_artifacts=operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.actionable_gap_count.remains_zero",
            expected=0,
            observed=operator.get("actionable_gap_count"),
            source_artifacts=operator_source,
        ),
        _check(
            key="operator.may_discharge_gap_count.remains_zero",
            expected=0,
            observed=operator.get("may_discharge_gap_count"),
            source_artifacts=operator_source,
        ),
        _check(
            key="operator.direct_discharge_source_count.matches_literature_index",
            expected=literature.get("direct_discharge_source_count"),
            observed=operator.get("direct_discharge_source_count"),
            source_artifacts=operator_source + literature_source,
        ),
        _check(
            key="operator.literature_gap_dependency_check_count.matches_gap_dependency",
            expected=gap_dependency.get("literature_gap_dependency_check_count"),
            observed=operator.get("literature_gap_dependency_check_count"),
            source_artifacts=operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.failed_literature_gap_dependency_check_count.matches_gap_dependency",
            expected=gap_dependency.get("failed_literature_gap_dependency_check_count"),
            observed=operator.get("failed_literature_gap_dependency_check_count"),
            source_artifacts=operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.literature_gap_dependency_consistent.matches_gap_dependency",
            expected=gap_dependency.get("literature_gap_dependency_consistent"),
            observed=operator.get("literature_gap_dependency_consistent"),
            source_artifacts=operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.analytic_gap_stack_consistent.matches_gap_dependency",
            expected=gap_dependency.get("analytic_gap_stack_consistent"),
            observed=operator.get("analytic_gap_stack_consistent"),
            source_artifacts=operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.operator_stack_consistent.matches_gap_dependency",
            expected=gap_dependency.get("operator_stack_consistent"),
            observed=operator.get("operator_stack_consistent"),
            source_artifacts=operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.literature_gap_operator_index_check_count.expected_thirty",
            expected=30,
            observed=operator.get("literature_gap_operator_index_check_count"),
            source_artifacts=operator_source,
        ),
        _check(
            key="operator.failed_literature_gap_operator_index_check_count.remains_zero",
            expected=0,
            observed=operator.get("failed_literature_gap_operator_index_check_count"),
            source_artifacts=operator_source,
        ),
        _check(
            key="operator.literature_gap_operator_index_consistent.true",
            expected=True,
            observed=operator.get("literature_gap_operator_index_consistent"),
            source_artifacts=operator_source,
        ),
        _check(
            key="literature_dependency.literature_dependency_consistent.true",
            expected=True,
            observed=literature_dependency.get("literature_dependency_consistent"),
            source_artifacts=literature_dependency_source,
        ),
        _check(
            key="gap_dependency.literature_gap_dependency_consistent.true",
            expected=True,
            observed=gap_dependency.get("literature_gap_dependency_consistent"),
            source_artifacts=gap_dependency_source,
        ),
        _check(
            key="matrix.literature_dependency_consistent.true",
            expected=True,
            observed=matrix.get("literature_dependency_consistent"),
            source_artifacts=matrix_source,
        ),
        _check(
            key="source_reports.issues.all_empty",
            expected=((), (), (), (), ()),
            observed=(
                tuple(operator.get("issues", ())),
                tuple(matrix.get("issues", ())),
                tuple(gap_dependency.get("issues", ())),
                tuple(literature.get("issues", ())),
                tuple(literature_dependency.get("issues", ())),
            ),
            source_artifacts=(
                operator_source
                + matrix_source
                + gap_dependency_source
                + literature_source
                + literature_dependency_source
            ),
        ),
        _check(
            key="source_report_count.matches_direct_sources",
            expected=len(_direct_sources()),
            observed=len(_direct_sources()),
            source_artifacts=_direct_sources(),
        ),
        _check(
            key="all.process_gate_open_authorized.false",
            expected=(False, False, False, False, False),
            observed=(
                operator.get("process_gate_open_authorized"),
                matrix.get("process_gate_open_authorized"),
                gap_dependency.get("process_gate_open_authorized"),
                literature.get("process_gate_open_authorized"),
                literature_dependency.get("process_gate_open_authorized"),
            ),
            source_artifacts=_direct_sources(),
        ),
        _check(
            key="all.blocker_state_changed.false",
            expected=(False, False, False, False, False),
            observed=(
                operator.get("blocker_state_changed"),
                matrix.get("blocker_state_changed"),
                gap_dependency.get("blocker_state_changed"),
                literature.get("blocker_state_changed"),
                literature_dependency.get("blocker_state_changed"),
            ),
            source_artifacts=_direct_sources(),
        ),
        _check(
            key="all.candidate_emission_authorized.false",
            expected=(False, False, False, False, False),
            observed=(
                operator.get("candidate_emission_authorized"),
                matrix.get("candidate_emission_authorized"),
                gap_dependency.get("candidate_emission_authorized"),
                literature.get("candidate_emission_authorized"),
                literature_dependency.get("candidate_emission_authorized"),
            ),
            source_artifacts=_direct_sources(),
        ),
        _check(
            key="source_refs.missing_count.remains_zero",
            expected=0,
            observed=len(missing_sources),
            source_artifacts=source_refs,
        ),
    )
    issues = tuple(check.key for check in checks if not check.passed)

    process_gate_open_authorized = any(
        bool(report.get("process_gate_open_authorized"))
        for report in (operator, matrix, gap_dependency, literature, literature_dependency)
    )
    blocker_state_changed = any(
        bool(report.get("blocker_state_changed"))
        for report in (operator, matrix, gap_dependency, literature, literature_dependency)
    )
    candidate_emission_authorized = any(
        bool(report.get("candidate_emission_authorized"))
        for report in (operator, matrix, gap_dependency, literature, literature_dependency)
    )

    return Lemma0252BlockerLiteratureGapOperatorDependency(
        schema_version=1,
        lemma_id=str(operator.get("lemma_id")),
        candidate_status=str(operator.get("candidate_status")),
        active_candidate=bool(operator.get("active_candidate")),
        literature_gap_operator_markdown=str(DEFAULT_GAP_OPERATOR_MARKDOWN),
        literature_gap_operator_json=str(DEFAULT_GAP_OPERATOR_JSON),
        literature_gap_matrix_markdown=str(DEFAULT_GAP_MATRIX_MARKDOWN),
        literature_gap_matrix_json=str(DEFAULT_GAP_MATRIX_JSON),
        literature_gap_dependency_markdown=str(DEFAULT_GAP_DEPENDENCY_MARKDOWN),
        literature_gap_dependency_json=str(DEFAULT_GAP_DEPENDENCY_JSON),
        literature_index_markdown=str(DEFAULT_LITERATURE_INDEX_MARKDOWN),
        literature_index_json=str(DEFAULT_LITERATURE_INDEX_JSON),
        literature_dependency_markdown=str(DEFAULT_LITERATURE_DEPENDENCY_MARKDOWN),
        literature_dependency_json=str(DEFAULT_LITERATURE_DEPENDENCY_JSON),
        direct_source_report_count=len(_direct_sources()),
        source_ref_count=len(source_refs),
        literature_gap_operator_dependency_check_count=len(checks),
        passed_literature_gap_operator_dependency_check_count=sum(
            1 for check in checks if check.passed
        ),
        failed_literature_gap_operator_dependency_check_count=len(issues),
        literature_gap_operator_dependency_consistent=not issues and not missing_sources,
        literature_source_count=int(operator.get("literature_source_count", 0)),
        gap_count=int(operator.get("gap_count", 0)),
        source_gap_edge_count=int(operator.get("source_gap_edge_count", 0)),
        source_with_gap_count=int(operator.get("source_with_gap_count", 0)),
        unmapped_source_count=int(operator.get("unmapped_source_count", 0)),
        gap_with_literature_source_count=int(
            operator.get("gap_with_literature_source_count", 0)
        ),
        gap_without_literature_source_count=int(
            operator.get("gap_without_literature_source_count", 0)
        ),
        direct_branch_edge_count=int(operator.get("direct_branch_edge_count", 0)),
        closure_bundle_edge_count=int(operator.get("closure_bundle_edge_count", 0)),
        blocked_gap_count=int(operator.get("blocked_gap_count", 0)),
        actionable_gap_count=int(operator.get("actionable_gap_count", 0)),
        may_discharge_gap_count=int(operator.get("may_discharge_gap_count", 0)),
        direct_discharge_source_count=int(operator.get("direct_discharge_source_count", 0)),
        literature_dependency_check_count=int(
            literature_dependency.get("literature_dependency_check_count", 0)
        ),
        literature_gap_dependency_check_count=int(
            gap_dependency.get("literature_gap_dependency_check_count", 0)
        ),
        failed_literature_gap_dependency_check_count=int(
            gap_dependency.get("failed_literature_gap_dependency_check_count", 0)
        ),
        literature_gap_operator_index_check_count=int(
            operator.get("literature_gap_operator_index_check_count", 0)
        ),
        failed_literature_gap_operator_index_check_count=int(
            operator.get("failed_literature_gap_operator_index_check_count", 0)
        ),
        literature_dependency_consistent=bool(
            literature_dependency.get("literature_dependency_consistent")
        ),
        literature_gap_dependency_consistent=bool(
            gap_dependency.get("literature_gap_dependency_consistent")
        ),
        literature_gap_operator_index_consistent=bool(
            operator.get("literature_gap_operator_index_consistent")
        ),
        analytic_gap_stack_consistent=bool(
            operator.get("analytic_gap_stack_consistent")
        ),
        operator_stack_consistent=bool(operator.get("operator_stack_consistent")),
        process_gate_open_authorized=process_gate_open_authorized,
        blocker_state_changed=blocker_state_changed,
        candidate_emission_authorized=candidate_emission_authorized,
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        issues=issues,
        checks=checks,
        source_refs=source_refs,
        non_claims=NON_CLAIMS,
        literature_gap_operator_snapshot=operator,
        literature_gap_matrix_snapshot=matrix,
        literature_gap_dependency_snapshot=gap_dependency,
        literature_index_snapshot=literature,
        literature_dependency_snapshot=literature_dependency,
    )


def literature_gap_operator_dependency_to_dict(
    report: Lemma0252BlockerLiteratureGapOperatorDependency,
) -> dict[str, object]:
    return {
        "schema_version": report.schema_version,
        "lemma_id": report.lemma_id,
        "candidate_status": report.candidate_status,
        "active_candidate": report.active_candidate,
        "literature_gap_operator_markdown": report.literature_gap_operator_markdown,
        "literature_gap_operator_json": report.literature_gap_operator_json,
        "literature_gap_matrix_markdown": report.literature_gap_matrix_markdown,
        "literature_gap_matrix_json": report.literature_gap_matrix_json,
        "literature_gap_dependency_markdown": report.literature_gap_dependency_markdown,
        "literature_gap_dependency_json": report.literature_gap_dependency_json,
        "literature_index_markdown": report.literature_index_markdown,
        "literature_index_json": report.literature_index_json,
        "literature_dependency_markdown": report.literature_dependency_markdown,
        "literature_dependency_json": report.literature_dependency_json,
        "direct_source_report_count": report.direct_source_report_count,
        "source_ref_count": report.source_ref_count,
        "literature_gap_operator_dependency_check_count": (
            report.literature_gap_operator_dependency_check_count
        ),
        "passed_literature_gap_operator_dependency_check_count": (
            report.passed_literature_gap_operator_dependency_check_count
        ),
        "failed_literature_gap_operator_dependency_check_count": (
            report.failed_literature_gap_operator_dependency_check_count
        ),
        "literature_gap_operator_dependency_consistent": (
            report.literature_gap_operator_dependency_consistent
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
        "literature_gap_dependency_check_count": (
            report.literature_gap_dependency_check_count
        ),
        "failed_literature_gap_dependency_check_count": (
            report.failed_literature_gap_dependency_check_count
        ),
        "literature_gap_operator_index_check_count": (
            report.literature_gap_operator_index_check_count
        ),
        "failed_literature_gap_operator_index_check_count": (
            report.failed_literature_gap_operator_index_check_count
        ),
        "literature_dependency_consistent": report.literature_dependency_consistent,
        "literature_gap_dependency_consistent": (
            report.literature_gap_dependency_consistent
        ),
        "literature_gap_operator_index_consistent": (
            report.literature_gap_operator_index_consistent
        ),
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
        "literature_gap_operator_snapshot": report.literature_gap_operator_snapshot,
        "literature_gap_matrix_snapshot": report.literature_gap_matrix_snapshot,
        "literature_gap_dependency_snapshot": report.literature_gap_dependency_snapshot,
        "literature_index_snapshot": report.literature_index_snapshot,
        "literature_dependency_snapshot": report.literature_dependency_snapshot,
        "docs": {
            "step_doc": (
                "docs/STEP111_LEMMA_0252_BLOCKER_LITERATURE_GAP_OPERATOR_DEPENDENCY.md"
            ),
            "gap_operator_doc": (
                "docs/STEP110_LEMMA_0252_BLOCKER_LITERATURE_GAP_OPERATOR_INDEX.md"
            ),
            "gap_dependency_doc": (
                "docs/STEP109_LEMMA_0252_BLOCKER_LITERATURE_GAP_DEPENDENCY.md"
            ),
            "gap_matrix_doc": (
                "docs/STEP108_LEMMA_0252_BLOCKER_LITERATURE_GAP_MATRIX.md"
            ),
            "literature_dependency_doc": (
                "docs/STEP107_LEMMA_0252_BLOCKER_LITERATURE_DEPENDENCY.md"
            ),
            "literature_index_doc": (
                "docs/STEP106_LEMMA_0252_BLOCKER_LITERATURE_INDEX.md"
            ),
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _summary_lines(
    report: Lemma0252BlockerLiteratureGapOperatorDependency,
) -> tuple[str, ...]:
    keys = (
        "lemma_id",
        "candidate_status",
        "active_candidate",
        "direct_source_report_count",
        "source_ref_count",
        "literature_gap_operator_dependency_check_count",
        "passed_literature_gap_operator_dependency_check_count",
        "failed_literature_gap_operator_dependency_check_count",
        "literature_gap_operator_dependency_consistent",
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
        "literature_gap_dependency_check_count",
        "failed_literature_gap_dependency_check_count",
        "literature_gap_operator_index_check_count",
        "failed_literature_gap_operator_index_check_count",
        "literature_dependency_consistent",
        "literature_gap_dependency_consistent",
        "literature_gap_operator_index_consistent",
        "analytic_gap_stack_consistent",
        "operator_stack_consistent",
        "process_gate_open_authorized",
        "blocker_state_changed",
        "candidate_emission_authorized",
        "missing_source_count",
    )
    data = literature_gap_operator_dependency_to_dict(report)
    return tuple(f"- {key}: `{str(data[key]).lower()}`" for key in keys)


def _check_rows(
    report: Lemma0252BlockerLiteratureGapOperatorDependency,
) -> list[str]:
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


def render_markdown(
    report: Lemma0252BlockerLiteratureGapOperatorDependency,
) -> str:
    return "\n".join(
        (
            "# Lemma 0252 Blocker Literature Gap Operator Dependency",
            "",
            "Generated by `track-a-regularity/evaluator/lemma_0252_blocker_literature_gap_operator_dependency.py`.",
            "",
            "This read-only dependency/freshness guard keeps the Step 110 literature-gap",
            "operator/source index synchronized with the Step 108 gap matrix, the Step 109",
            "gap-dependency guard, and the broader Step 106-107 literature stack. It is",
            "an audit surface only; it does not discharge blockers or authorize process",
            "gates.",
            "",
            "## Summary",
            "",
            *_summary_lines(report),
            f"- issues: `{', '.join(report.issues) or 'none'}`",
            "",
            "## Source Reports",
            "",
            f"- gap_operator_markdown: `{report.literature_gap_operator_markdown}`",
            f"- gap_operator_json: `{report.literature_gap_operator_json}`",
            f"- gap_matrix_markdown: `{report.literature_gap_matrix_markdown}`",
            f"- gap_matrix_json: `{report.literature_gap_matrix_json}`",
            f"- gap_dependency_markdown: `{report.literature_gap_dependency_markdown}`",
            f"- gap_dependency_json: `{report.literature_gap_dependency_json}`",
            f"- literature_index_markdown: `{report.literature_index_markdown}`",
            f"- literature_index_json: `{report.literature_index_json}`",
            f"- literature_dependency_markdown: `{report.literature_dependency_markdown}`",
            f"- literature_dependency_json: `{report.literature_dependency_json}`",
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


def render_json(report: Lemma0252BlockerLiteratureGapOperatorDependency) -> str:
    return json.dumps(
        literature_gap_operator_dependency_to_dict(report),
        indent=2,
        sort_keys=True,
    ) + "\n"


def render_output(
    report: Lemma0252BlockerLiteratureGapOperatorDependency,
    output_format: str,
) -> str:
    if output_format == "markdown":
        return render_markdown(report)
    if output_format == "json":
        return render_json(report)
    raise ValueError(f"unknown literature gap operator dependency format: {output_format}")


def write_output(
    output: Path,
    report: Lemma0252BlockerLiteratureGapOperatorDependency,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(report, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    report: Lemma0252BlockerLiteratureGapOperatorDependency,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(report, output_format)
    if not output.exists():
        return False, f"missing lemma_0252 blocker literature gap operator dependency: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale lemma_0252 blocker literature gap operator dependency: {output}"
    return True, f"fresh lemma_0252 blocker literature gap operator dependency: {output}"


def check_consistent(
    report: Lemma0252BlockerLiteratureGapOperatorDependency,
) -> tuple[bool, str]:
    if not report.literature_gap_operator_dependency_consistent:
        return (
            False,
            "lemma_0252 blocker literature gap operator dependency inconsistent: "
            + ", ".join(report.issues),
        )
    return True, "lemma_0252 blocker literature gap operator dependency is consistent"


def check_sources(
    report: Lemma0252BlockerLiteratureGapOperatorDependency,
) -> tuple[bool, str]:
    if report.missing_source_count:
        return (
            False,
            "missing lemma_0252 blocker literature gap operator dependency sources: "
            + ", ".join(report.missing_sources),
        )
    return True, "all lemma_0252 blocker literature gap operator dependency sources exist"


def check_blocked(
    report: Lemma0252BlockerLiteratureGapOperatorDependency,
) -> tuple[bool, str]:
    if report.process_gate_open_authorized:
        return False, "process gate open became authorized"
    if report.blocker_state_changed:
        return False, "literature gap operator dependency changed blocker state"
    if report.candidate_emission_authorized:
        return False, "literature gap operator dependency authorized candidate emission"
    if report.actionable_gap_count:
        return False, "literature gap operator dependency found actionable gaps"
    if report.may_discharge_gap_count:
        return False, "literature gap operator dependency found discharge-capable gaps"
    if report.direct_discharge_source_count:
        return False, "literature gap operator dependency found direct discharge sources"
    if report.blocked_gap_count != report.gap_count:
        return False, "not all literature-linked gaps remain blocked"
    return True, "lemma_0252 blocker literature gap operator dependency keeps gaps blocked"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown literature gap operator dependency format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check Step 110 lemma_0252 literature-gap operator index against its "
            "canonical upstream sources."
        )
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-consistent", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    args = parser.parse_args(argv)

    try:
        report = build_blocker_literature_gap_operator_dependency()
    except Exception as exc:  # noqa: BLE001 - CLI should report setup failures.
        print(
            f"failed to build lemma_0252 blocker literature gap operator dependency: {exc}",
            file=sys.stderr,
        )
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, report, args.format)
        print(message)
        if not ok:
            print(
                "run without --check-output to regenerate the literature gap operator dependency",
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

    print(
        "literature_gap_operator_dependency_check_count: "
        f"{report.literature_gap_operator_dependency_check_count}"
    )
    print(
        "passed_literature_gap_operator_dependency_check_count: "
        f"{report.passed_literature_gap_operator_dependency_check_count}"
    )
    print(
        "failed_literature_gap_operator_dependency_check_count: "
        f"{report.failed_literature_gap_operator_dependency_check_count}"
    )
    print(
        "literature_gap_operator_dependency_consistent: "
        f"{str(report.literature_gap_operator_dependency_consistent).lower()}"
    )
    print(
        "process_gate_open_authorized: "
        f"{str(report.process_gate_open_authorized).lower()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
