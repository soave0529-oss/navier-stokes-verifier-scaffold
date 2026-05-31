from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = (
    DEFAULT_REPORT_DIR / "lemma_0252_cross_gap_source_read_status_dashboard.md"
)
DEFAULT_JSON_OUTPUT = (
    DEFAULT_REPORT_DIR / "lemma_0252_cross_gap_source_read_status_dashboard.json"
)
DEFAULT_PAPERS_INDEX = ROOT / "papers/blockers/index.md"

PACKET_STATUS = "blocked_source_read_only"
PACKET_BRANCH_VERDICT = "blocked_needs_new_result"
CHECKLIST_BRANCH_VERDICT = "deferred_needs_new_result"

NON_CLAIMS = (
    "read_only_cross_gap_source_read_status_dashboard",
    "operator_dashboard_for_review_only",
    "non_promotional_gap_002_gap_003_gap_004_surface",
    "no_candidate_promotion",
    "no_candidate_emission",
    "no_blocker_discharge",
    "no_process_gate_opened",
    "no_file_copy",
    "no_finite_bound_to_smallness_theorem",
    "no_compactness_liouville_theorem",
    "no_smooth_continuation_theorem",
    "no_weak_to_smooth_upgrade",
    "no_navier_stokes_solution",
)


@dataclass(frozen=True)
class GapSourceReadConfig:
    gap_id: str
    source_branch: str
    packet_json: Path
    packet_markdown: Path
    dependency_json: Path
    dependency_markdown: Path
    dependency_check_label: str
    failed_dependency_check_label: str
    dependency_consistent_label: str
    expected_source_read_count: int
    expected_direct_branch_source_read_count: int
    expected_cross_cutting_source_read_count: int
    relevant_step_range: str


@dataclass(frozen=True)
class CrossGapSourceReadStatusRow:
    gap_id: str
    source_branch: str
    relevant_step_range: str
    packet_markdown: str
    packet_json: str
    dependency_markdown: str
    dependency_json: str
    packet_status: str
    packet_branch_verdict: str
    source_read_count: int
    direct_branch_source_read_count: int
    cross_cutting_source_read_count: int
    blocked_source_read_count: int
    actionable_source_read_count: int
    may_discharge_source_read_count: int
    exact_discharge_artifact_count: int
    packet_check_count: int
    failed_packet_check_count: int
    packet_consistent: bool
    dependency_check_count: int
    failed_dependency_check_count: int
    dependency_consistent: bool
    source_ref_count: int
    missing_source_count: int
    source_read_ids: tuple[str, ...]


@dataclass(frozen=True)
class CrossGapSourceReadStatusCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class Lemma0252CrossGapSourceReadStatusDashboard:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    gap_count: int
    gap_ids: tuple[str, ...]
    source_branches: tuple[str, ...]
    direct_gap_count: int
    packet_count: int
    dependency_guard_count: int
    smooth_stack_step_count: int
    source_report_count: int
    source_ref_count: int
    cross_gap_source_read_status_dashboard_check_count: int
    passed_cross_gap_source_read_status_dashboard_check_count: int
    failed_cross_gap_source_read_status_dashboard_check_count: int
    cross_gap_source_read_status_dashboard_consistent: bool
    source_read_count: int
    direct_branch_source_read_count: int
    cross_cutting_source_read_count: int
    blocked_source_read_count: int
    actionable_source_read_count: int
    may_discharge_source_read_count: int
    exact_discharge_artifact_count: int
    packet_check_count: int
    failed_packet_check_count: int
    packet_consistent_count: int
    dependency_check_count: int
    failed_dependency_check_count: int
    dependency_consistent_count: int
    smooth_operator_index_check_count: int
    failed_smooth_operator_index_check_count: int
    smooth_operator_index_consistent: bool
    smooth_operator_dependency_check_count: int
    failed_smooth_operator_dependency_check_count: int
    smooth_operator_dependency_consistent: bool
    smooth_stack_dashboard_check_count: int
    failed_smooth_stack_dashboard_check_count: int
    smooth_stack_dashboard_consistent: bool
    checklist_branch_verdict: str
    dischargeable_now_count: int
    queue_item_count: int
    blocked_queue_item_count: int
    actionable_queue_item_count: int
    may_discharge_queue_item_count: int
    direct_theorem_artifact_count: int
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    gap_rows: tuple[CrossGapSourceReadStatusRow, ...]
    checks: tuple[CrossGapSourceReadStatusCheck, ...]
    issues: tuple[str, ...]
    source_refs: tuple[str, ...]
    source_read_ids_by_gap: dict[str, tuple[str, ...]]
    non_claims: tuple[str, ...]
    packet_snapshots: dict[str, dict[str, object]]
    dependency_snapshots: dict[str, dict[str, object]]
    smooth_operator_snapshot: dict[str, object]
    smooth_operator_dependency_snapshot: dict[str, object]
    smooth_stack_dashboard_snapshot: dict[str, object]


GAP_CONFIGS = (
    GapSourceReadConfig(
        gap_id="gap_002",
        source_branch="finite_bound_to_smallness",
        packet_json=(
            DEFAULT_REPORT_DIR / "lemma_0252_finite_bound_smallness_source_read_packet.json"
        ),
        packet_markdown=(
            DEFAULT_REPORT_DIR / "lemma_0252_finite_bound_smallness_source_read_packet.md"
        ),
        dependency_json=(
            DEFAULT_REPORT_DIR
            / "lemma_0252_finite_bound_smallness_source_read_packet_dependency.json"
        ),
        dependency_markdown=(
            DEFAULT_REPORT_DIR
            / "lemma_0252_finite_bound_smallness_source_read_packet_dependency.md"
        ),
        dependency_check_label="finite_bound_smallness_source_read_packet_dependency_check_count",
        failed_dependency_check_label=(
            "failed_finite_bound_smallness_source_read_packet_dependency_check_count"
        ),
        dependency_consistent_label=(
            "finite_bound_smallness_source_read_packet_dependency_consistent"
        ),
        expected_source_read_count=7,
        expected_direct_branch_source_read_count=5,
        expected_cross_cutting_source_read_count=2,
        relevant_step_range="116-117",
    ),
    GapSourceReadConfig(
        gap_id="gap_003",
        source_branch="compactness_liouville",
        packet_json=(
            DEFAULT_REPORT_DIR / "lemma_0252_compactness_liouville_source_read_packet.json"
        ),
        packet_markdown=(
            DEFAULT_REPORT_DIR / "lemma_0252_compactness_liouville_source_read_packet.md"
        ),
        dependency_json=(
            DEFAULT_REPORT_DIR
            / "lemma_0252_compactness_liouville_source_read_packet_dependency.json"
        ),
        dependency_markdown=(
            DEFAULT_REPORT_DIR
            / "lemma_0252_compactness_liouville_source_read_packet_dependency.md"
        ),
        dependency_check_label="compactness_liouville_source_read_packet_dependency_check_count",
        failed_dependency_check_label=(
            "failed_compactness_liouville_source_read_packet_dependency_check_count"
        ),
        dependency_consistent_label=(
            "compactness_liouville_source_read_packet_dependency_consistent"
        ),
        expected_source_read_count=6,
        expected_direct_branch_source_read_count=5,
        expected_cross_cutting_source_read_count=1,
        relevant_step_range="118-119",
    ),
    GapSourceReadConfig(
        gap_id="gap_004",
        source_branch="smooth_continuation_bridge",
        packet_json=(
            DEFAULT_REPORT_DIR / "lemma_0252_smooth_continuation_source_read_packet.json"
        ),
        packet_markdown=(
            DEFAULT_REPORT_DIR / "lemma_0252_smooth_continuation_source_read_packet.md"
        ),
        dependency_json=(
            DEFAULT_REPORT_DIR
            / "lemma_0252_smooth_continuation_source_read_packet_dependency.json"
        ),
        dependency_markdown=(
            DEFAULT_REPORT_DIR
            / "lemma_0252_smooth_continuation_source_read_packet_dependency.md"
        ),
        dependency_check_label="smooth_continuation_source_read_packet_dependency_check_count",
        failed_dependency_check_label=(
            "failed_smooth_continuation_source_read_packet_dependency_check_count"
        ),
        dependency_consistent_label=(
            "smooth_continuation_source_read_packet_dependency_consistent"
        ),
        expected_source_read_count=2,
        expected_direct_branch_source_read_count=2,
        expected_cross_cutting_source_read_count=0,
        relevant_step_range="120-124",
    ),
)

SMOOTH_OPERATOR_JSON = (
    DEFAULT_REPORT_DIR / "lemma_0252_smooth_continuation_source_read_packet_operator_index.json"
)
SMOOTH_OPERATOR_MARKDOWN = (
    DEFAULT_REPORT_DIR / "lemma_0252_smooth_continuation_source_read_packet_operator_index.md"
)
SMOOTH_OPERATOR_DEPENDENCY_JSON = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_smooth_continuation_source_read_packet_operator_dependency.json"
)
SMOOTH_OPERATOR_DEPENDENCY_MARKDOWN = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_smooth_continuation_source_read_packet_operator_dependency.md"
)
SMOOTH_STACK_DASHBOARD_JSON = (
    DEFAULT_REPORT_DIR / "lemma_0252_smooth_continuation_source_read_stack_dashboard.json"
)
SMOOTH_STACK_DASHBOARD_MARKDOWN = (
    DEFAULT_REPORT_DIR / "lemma_0252_smooth_continuation_source_read_stack_dashboard.md"
)


def _load_json(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"expected object JSON report: {path}")
    return data


def _rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def _check(
    *,
    key: str,
    expected: object,
    observed: object,
    source_artifacts: tuple[str, ...],
) -> CrossGapSourceReadStatusCheck:
    return CrossGapSourceReadStatusCheck(
        key=key,
        expected=str(expected),
        observed=str(observed),
        passed=expected == observed,
        source_artifacts=source_artifacts,
    )


def _missing_sources(source_refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(source for source in source_refs if not (ROOT / source).exists())


def _blocked_source_read_count(report: dict[str, object]) -> int:
    if "blocked_source_read_count" in report:
        return int(report.get("blocked_source_read_count", 0))
    if (
        int(report.get("actionable_source_read_count", 0)) == 0
        and int(report.get("may_discharge_source_read_count", 0)) == 0
    ):
        return int(report.get("source_read_count", 0))
    return 0


def _source_ids_from_packet(packet: dict[str, object]) -> tuple[str, ...]:
    return tuple(
        str(item.get("source_id"))
        for item in packet.get("source_reads", ())
        if isinstance(item, dict)
    )


def _direct_source_reports() -> tuple[str, ...]:
    reports: list[str] = []
    for config in GAP_CONFIGS:
        reports.extend(
            (
                _rel(config.packet_markdown),
                _rel(config.packet_json),
                _rel(config.dependency_markdown),
                _rel(config.dependency_json),
            )
        )
    reports.extend(
        (
            _rel(SMOOTH_OPERATOR_MARKDOWN),
            _rel(SMOOTH_OPERATOR_JSON),
            _rel(SMOOTH_OPERATOR_DEPENDENCY_MARKDOWN),
            _rel(SMOOTH_OPERATOR_DEPENDENCY_JSON),
            _rel(SMOOTH_STACK_DASHBOARD_MARKDOWN),
            _rel(SMOOTH_STACK_DASHBOARD_JSON),
        )
    )
    return tuple(reports)


def _gap_row(
    config: GapSourceReadConfig,
    packet: dict[str, object],
    dependency: dict[str, object],
) -> CrossGapSourceReadStatusRow:
    return CrossGapSourceReadStatusRow(
        gap_id=config.gap_id,
        source_branch=config.source_branch,
        relevant_step_range=config.relevant_step_range,
        packet_markdown=str(config.packet_markdown),
        packet_json=str(config.packet_json),
        dependency_markdown=str(config.dependency_markdown),
        dependency_json=str(config.dependency_json),
        packet_status=str(packet.get("packet_status")),
        packet_branch_verdict=str(packet.get("branch_verdict")),
        source_read_count=int(packet.get("source_read_count", 0)),
        direct_branch_source_read_count=int(
            packet.get("direct_branch_source_read_count", 0)
        ),
        cross_cutting_source_read_count=int(
            packet.get("cross_cutting_source_read_count", 0)
        ),
        blocked_source_read_count=_blocked_source_read_count(packet),
        actionable_source_read_count=int(packet.get("actionable_source_read_count", 0)),
        may_discharge_source_read_count=int(
            packet.get("may_discharge_source_read_count", 0)
        ),
        exact_discharge_artifact_count=int(
            packet.get("exact_discharge_artifact_count", 0)
        ),
        packet_check_count=int(packet.get("packet_check_count", 0)),
        failed_packet_check_count=int(packet.get("failed_packet_check_count", 0)),
        packet_consistent=bool(packet.get("packet_consistent")),
        dependency_check_count=int(dependency.get(config.dependency_check_label, 0)),
        failed_dependency_check_count=int(
            dependency.get(config.failed_dependency_check_label, 0)
        ),
        dependency_consistent=bool(dependency.get(config.dependency_consistent_label)),
        source_ref_count=len(
            tuple(
                dict.fromkeys(
                    tuple(str(item) for item in packet.get("source_refs", ()))
                    + tuple(str(item) for item in dependency.get("source_refs", ()))
                )
            )
        ),
        missing_source_count=int(packet.get("missing_source_count", 0))
        + int(dependency.get("missing_source_count", 0)),
        source_read_ids=_source_ids_from_packet(packet),
    )


def build_cross_gap_source_read_status_dashboard(
    *,
    papers_blockers_index: Path = DEFAULT_PAPERS_INDEX,
) -> Lemma0252CrossGapSourceReadStatusDashboard:
    packets = {config.gap_id: _load_json(config.packet_json) for config in GAP_CONFIGS}
    dependencies = {
        config.gap_id: _load_json(config.dependency_json) for config in GAP_CONFIGS
    }
    smooth_operator = _load_json(SMOOTH_OPERATOR_JSON)
    smooth_operator_dependency = _load_json(SMOOTH_OPERATOR_DEPENDENCY_JSON)
    smooth_stack_dashboard = _load_json(SMOOTH_STACK_DASHBOARD_JSON)

    direct_reports = _direct_source_reports()
    source_refs = tuple(
        dict.fromkeys(
            direct_reports
            + ("papers/blockers/index.md",)
            + tuple(
                source
                for config in GAP_CONFIGS
                for source in (
                    tuple(str(item) for item in packets[config.gap_id].get("source_refs", ()))
                    + tuple(
                        str(item)
                        for item in dependencies[config.gap_id].get("source_refs", ())
                    )
                )
            )
            + tuple(str(item) for item in smooth_operator.get("source_refs", ()))
            + tuple(str(item) for item in smooth_operator_dependency.get("source_refs", ()))
            + tuple(str(item) for item in smooth_stack_dashboard.get("source_refs", ()))
        )
    )
    missing_sources = _missing_sources(source_refs)
    gap_rows = tuple(
        _gap_row(config, packets[config.gap_id], dependencies[config.gap_id])
        for config in GAP_CONFIGS
    )
    source_read_ids_by_gap = {
        row.gap_id: row.source_read_ids for row in gap_rows
    }

    all_gap_reports = tuple(
        report
        for config in GAP_CONFIGS
        for report in (packets[config.gap_id], dependencies[config.gap_id])
    )
    all_reports = all_gap_reports + (
        smooth_operator,
        smooth_operator_dependency,
        smooth_stack_dashboard,
    )

    expected_gap_ids = tuple(config.gap_id for config in GAP_CONFIGS)
    expected_source_branches = tuple(config.source_branch for config in GAP_CONFIGS)
    expected_source_counts = tuple(
        config.expected_source_read_count for config in GAP_CONFIGS
    )
    expected_direct_counts = tuple(
        config.expected_direct_branch_source_read_count for config in GAP_CONFIGS
    )
    expected_cross_counts = tuple(
        config.expected_cross_cutting_source_read_count for config in GAP_CONFIGS
    )
    packet_sources = tuple(
        _rel(config.packet_json) for config in GAP_CONFIGS
    )
    dependency_sources = tuple(
        _rel(config.dependency_json) for config in GAP_CONFIGS
    )
    smooth_sources = (
        _rel(SMOOTH_OPERATOR_JSON),
        _rel(SMOOTH_OPERATOR_DEPENDENCY_JSON),
        _rel(SMOOTH_STACK_DASHBOARD_JSON),
    )

    source_read_count = sum(row.source_read_count for row in gap_rows)
    direct_branch_source_read_count = sum(
        row.direct_branch_source_read_count for row in gap_rows
    )
    cross_cutting_source_read_count = sum(
        row.cross_cutting_source_read_count for row in gap_rows
    )
    blocked_source_read_count = sum(row.blocked_source_read_count for row in gap_rows)
    actionable_source_read_count = sum(
        row.actionable_source_read_count for row in gap_rows
    )
    may_discharge_source_read_count = sum(
        row.may_discharge_source_read_count for row in gap_rows
    )
    exact_discharge_artifact_count = sum(
        row.exact_discharge_artifact_count for row in gap_rows
    )
    packet_check_count = sum(row.packet_check_count for row in gap_rows)
    failed_packet_check_count = sum(row.failed_packet_check_count for row in gap_rows)
    dependency_check_count = sum(row.dependency_check_count for row in gap_rows)
    failed_dependency_check_count = sum(
        row.failed_dependency_check_count for row in gap_rows
    )

    checks = (
        _check(
            key="all.lemma_id.expected_lemma_0252",
            expected=("lemma_0252",) * len(all_reports),
            observed=tuple(report.get("lemma_id") for report in all_reports),
            source_artifacts=direct_reports,
        ),
        _check(
            key="all.candidate_status.remains_needs_review",
            expected=("needs_review",) * len(all_reports),
            observed=tuple(report.get("candidate_status") for report in all_reports),
            source_artifacts=direct_reports,
        ),
        _check(
            key="all.active_candidate.false",
            expected=(False,) * len(all_reports),
            observed=tuple(report.get("active_candidate") for report in all_reports),
            source_artifacts=direct_reports,
        ),
        _check(
            key="gap_ids.expected_direct_analytic_gaps",
            expected=expected_gap_ids,
            observed=tuple(row.gap_id for row in gap_rows),
            source_artifacts=packet_sources,
        ),
        _check(
            key="source_branches.expected_direct_analytic_families",
            expected=expected_source_branches,
            observed=tuple(row.source_branch for row in gap_rows),
            source_artifacts=packet_sources,
        ),
        _check(
            key="packet_status.all_blocked_source_read_only",
            expected=(PACKET_STATUS,) * len(gap_rows),
            observed=tuple(row.packet_status for row in gap_rows),
            source_artifacts=packet_sources,
        ),
        _check(
            key="packet_branch_verdict.all_blocked_needs_new_result",
            expected=(PACKET_BRANCH_VERDICT,) * len(gap_rows),
            observed=tuple(row.packet_branch_verdict for row in gap_rows),
            source_artifacts=packet_sources,
        ),
        _check(
            key="source_read_counts.match_gap_packets",
            expected=expected_source_counts,
            observed=tuple(row.source_read_count for row in gap_rows),
            source_artifacts=packet_sources,
        ),
        _check(
            key="direct_branch_source_read_counts.match_gap_packets",
            expected=expected_direct_counts,
            observed=tuple(row.direct_branch_source_read_count for row in gap_rows),
            source_artifacts=packet_sources,
        ),
        _check(
            key="cross_cutting_source_read_counts.match_gap_packets",
            expected=expected_cross_counts,
            observed=tuple(row.cross_cutting_source_read_count for row in gap_rows),
            source_artifacts=packet_sources,
        ),
        _check(
            key="total.source_read_count.expected_fifteen",
            expected=15,
            observed=source_read_count,
            source_artifacts=packet_sources,
        ),
        _check(
            key="total.direct_branch_source_read_count.expected_twelve",
            expected=12,
            observed=direct_branch_source_read_count,
            source_artifacts=packet_sources,
        ),
        _check(
            key="total.cross_cutting_source_read_count.expected_three",
            expected=3,
            observed=cross_cutting_source_read_count,
            source_artifacts=packet_sources,
        ),
        _check(
            key="blocked_source_read_counts.match_source_read_counts",
            expected=expected_source_counts,
            observed=tuple(row.blocked_source_read_count for row in gap_rows),
            source_artifacts=packet_sources,
        ),
        _check(
            key="total.blocked_source_read_count.matches_total_source_read_count",
            expected=source_read_count,
            observed=blocked_source_read_count,
            source_artifacts=packet_sources,
        ),
        _check(
            key="actionable_source_read_counts.remain_zero",
            expected=(0,) * len(gap_rows),
            observed=tuple(row.actionable_source_read_count for row in gap_rows),
            source_artifacts=packet_sources,
        ),
        _check(
            key="may_discharge_source_read_counts.remain_zero",
            expected=(0,) * len(gap_rows),
            observed=tuple(row.may_discharge_source_read_count for row in gap_rows),
            source_artifacts=packet_sources,
        ),
        _check(
            key="exact_discharge_artifact_counts.remain_zero",
            expected=(0,) * len(gap_rows),
            observed=tuple(row.exact_discharge_artifact_count for row in gap_rows),
            source_artifacts=packet_sources,
        ),
        _check(
            key="packet_check_counts.expected_thirty_four_each",
            expected=(34, 34, 34),
            observed=tuple(row.packet_check_count for row in gap_rows),
            source_artifacts=packet_sources,
        ),
        _check(
            key="packet_failed_check_counts.remain_zero",
            expected=(0, 0, 0),
            observed=tuple(row.failed_packet_check_count for row in gap_rows),
            source_artifacts=packet_sources,
        ),
        _check(
            key="packet_consistency.all_true",
            expected=(True, True, True),
            observed=tuple(row.packet_consistent for row in gap_rows),
            source_artifacts=packet_sources,
        ),
        _check(
            key="dependency_check_counts.expected_fifty_each",
            expected=(50, 50, 50),
            observed=tuple(row.dependency_check_count for row in gap_rows),
            source_artifacts=dependency_sources,
        ),
        _check(
            key="dependency_failed_check_counts.remain_zero",
            expected=(0, 0, 0),
            observed=tuple(row.failed_dependency_check_count for row in gap_rows),
            source_artifacts=dependency_sources,
        ),
        _check(
            key="dependency_consistency.all_true",
            expected=(True, True, True),
            observed=tuple(row.dependency_consistent for row in gap_rows),
            source_artifacts=dependency_sources,
        ),
        _check(
            key="dependency_gap_ids.match_packets",
            expected=expected_gap_ids,
            observed=tuple(
                dependencies[config.gap_id].get("gap_id") for config in GAP_CONFIGS
            ),
            source_artifacts=dependency_sources,
        ),
        _check(
            key="dependency_source_branches.match_packets",
            expected=expected_source_branches,
            observed=tuple(
                dependencies[config.gap_id].get("source_branch")
                for config in GAP_CONFIGS
            ),
            source_artifacts=dependency_sources,
        ),
        _check(
            key="dependency_packet_status.all_blocked_source_read_only",
            expected=(PACKET_STATUS,) * len(gap_rows),
            observed=tuple(
                dependencies[config.gap_id].get("packet_status")
                for config in GAP_CONFIGS
            ),
            source_artifacts=dependency_sources,
        ),
        _check(
            key="dependency_packet_branch_verdict.all_blocked",
            expected=(PACKET_BRANCH_VERDICT,) * len(gap_rows),
            observed=tuple(
                dependencies[config.gap_id].get("packet_branch_verdict")
                for config in GAP_CONFIGS
            ),
            source_artifacts=dependency_sources,
        ),
        _check(
            key="dependency_source_read_counts.match_packets",
            expected=expected_source_counts,
            observed=tuple(
                dependencies[config.gap_id].get("source_read_count")
                for config in GAP_CONFIGS
            ),
            source_artifacts=dependency_sources,
        ),
        _check(
            key="all.process_gate_open_authorized.false",
            expected=(False,) * len(all_reports),
            observed=tuple(
                bool(report.get("process_gate_open_authorized")) for report in all_reports
            ),
            source_artifacts=direct_reports,
        ),
        _check(
            key="all.blocker_state_changed.false",
            expected=(False,) * len(all_reports),
            observed=tuple(bool(report.get("blocker_state_changed")) for report in all_reports),
            source_artifacts=direct_reports,
        ),
        _check(
            key="all.candidate_emission_authorized.false",
            expected=(False,) * len(all_reports),
            observed=tuple(
                bool(report.get("candidate_emission_authorized"))
                for report in all_reports
            ),
            source_artifacts=direct_reports,
        ),
        _check(
            key="all.report_missing_source_counts.zero",
            expected=(0,) * len(all_reports),
            observed=tuple(int(report.get("missing_source_count", 0)) for report in all_reports),
            source_artifacts=direct_reports,
        ),
        _check(
            key="source_refs.missing_count.remains_zero",
            expected=0,
            observed=len(missing_sources),
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.include_all_step_116_to_124_reports",
            expected=True,
            observed=all(report in source_refs for report in direct_reports),
            source_artifacts=direct_reports,
        ),
        _check(
            key="source_refs.include_papers_blockers_index",
            expected=True,
            observed="papers/blockers/index.md" in source_refs
            and papers_blockers_index.exists(),
            source_artifacts=("papers/blockers/index.md",),
        ),
        _check(
            key="source_refs.include_theorem_artifact_queue_stack",
            expected=True,
            observed=(
                "track-a-regularity/reports/"
                "lemma_0252_theorem_artifact_review_queue_operator_dependency.json"
            )
            in source_refs,
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.include_gap_002_checklist",
            expected=True,
            observed=(
                "track-a-regularity/reports/lemma_0252_finite_bound_smallness_checklist.json"
                in source_refs
            ),
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.include_gap_003_checklist",
            expected=True,
            observed=(
                "track-a-regularity/reports/lemma_0252_compactness_liouville_checklist.json"
                in source_refs
            ),
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.include_gap_004_checklist",
            expected=True,
            observed=(
                "track-a-regularity/reports/lemma_0252_smooth_continuation_checklist.json"
                in source_refs
            ),
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.include_gap_002_local_sources",
            expected=True,
            observed=(
                "papers/blockers/finite_bound_to_smallness/"
                "2308.04147_partial_regularity_survey.pdf"
            )
            in source_refs
            and (
                "papers/blockers/cross_cutting/"
                "1108.1165_tao2013_localisation_compactness.pdf"
            )
            in source_refs,
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.include_gap_003_local_sources",
            expected=True,
            observed=(
                "papers/blockers/compactness_liouville/"
                "0709.3599_KNSS2009_liouville_acta_math.pdf"
            )
            in source_refs
            and (
                "papers/blockers/compactness_liouville/"
                "1509.04940_backward_uniqueness_remarks.pdf"
            )
            in source_refs,
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.include_gap_004_local_sources",
            expected=True,
            observed=(
                "papers/blockers/smooth_continuation_bridge/"
                "math0703883_besov_negative_blowup.pdf"
            )
            in source_refs
            and (
                "papers/blockers/smooth_continuation_bridge/"
                "1410.4495_robinson_review_NSE.pdf"
            )
            in source_refs,
            source_artifacts=source_refs,
        ),
        _check(
            key="gap_002.source_read_ids.expected",
            expected=(
                "survey_2308_04147",
                "quantitative_2210_01783",
                "local_gradient_1606_02790",
                "serrin_refinement_1310_3112",
                "vasseur_2007_deg_i",
                "tao_localisation_1108_1165",
                "tao_blog_2007",
            ),
            observed=source_read_ids_by_gap["gap_002"],
            source_artifacts=(
                "track-a-regularity/reports/"
                "lemma_0252_finite_bound_smallness_source_read_packet.json",
            ),
        ),
        _check(
            key="gap_003.source_read_ids.expected",
            expected=(
                "knss_0709_3599",
                "axisymmetric_1011_5066",
                "backward_uniqueness_1509_04940",
                "lorentz_1407_5129",
                "seregin_axisym_math0702720",
                "tao_localisation_1108_1165",
            ),
            observed=source_read_ids_by_gap["gap_003"],
            source_artifacts=(
                "track-a-regularity/reports/"
                "lemma_0252_compactness_liouville_source_read_packet.json",
            ),
        ),
        _check(
            key="gap_004.source_read_ids.expected",
            expected=("besov_negative_math0703883", "robinson_review_1410_4495"),
            observed=source_read_ids_by_gap["gap_004"],
            source_artifacts=(
                "track-a-regularity/reports/"
                "lemma_0252_smooth_continuation_source_read_packet.json",
            ),
        ),
        _check(
            key="smooth_operator_index.check_count.expected_thirty_seven",
            expected=37,
            observed=smooth_operator.get(
                "smooth_continuation_source_read_packet_operator_index_check_count"
            ),
            source_artifacts=(_rel(SMOOTH_OPERATOR_JSON),),
        ),
        _check(
            key="smooth_operator_index.failed_checks.zero",
            expected=0,
            observed=smooth_operator.get(
                "failed_smooth_continuation_source_read_packet_operator_index_check_count"
            ),
            source_artifacts=(_rel(SMOOTH_OPERATOR_JSON),),
        ),
        _check(
            key="smooth_operator_index.consistent.true",
            expected=True,
            observed=smooth_operator.get(
                "smooth_continuation_source_read_packet_operator_index_consistent"
            ),
            source_artifacts=(_rel(SMOOTH_OPERATOR_JSON),),
        ),
        _check(
            key="smooth_operator_dependency.check_count.expected_fifty_seven",
            expected=57,
            observed=smooth_operator_dependency.get(
                "smooth_continuation_source_read_packet_operator_dependency_check_count"
            ),
            source_artifacts=(_rel(SMOOTH_OPERATOR_DEPENDENCY_JSON),),
        ),
        _check(
            key="smooth_operator_dependency.failed_checks.zero",
            expected=0,
            observed=smooth_operator_dependency.get(
                "failed_smooth_continuation_source_read_packet_operator_dependency_check_count"
            ),
            source_artifacts=(_rel(SMOOTH_OPERATOR_DEPENDENCY_JSON),),
        ),
        _check(
            key="smooth_operator_dependency.consistent.true",
            expected=True,
            observed=smooth_operator_dependency.get(
                "smooth_continuation_source_read_packet_operator_dependency_consistent"
            ),
            source_artifacts=(_rel(SMOOTH_OPERATOR_DEPENDENCY_JSON),),
        ),
        _check(
            key="smooth_stack_dashboard.step_count.expected_four",
            expected=4,
            observed=smooth_stack_dashboard.get("stack_step_count"),
            source_artifacts=(_rel(SMOOTH_STACK_DASHBOARD_JSON),),
        ),
        _check(
            key="smooth_stack_dashboard.check_count.expected_forty_nine",
            expected=49,
            observed=smooth_stack_dashboard.get(
                "smooth_continuation_source_read_stack_dashboard_check_count"
            ),
            source_artifacts=(_rel(SMOOTH_STACK_DASHBOARD_JSON),),
        ),
        _check(
            key="smooth_stack_dashboard.failed_checks.zero",
            expected=0,
            observed=smooth_stack_dashboard.get(
                "failed_smooth_continuation_source_read_stack_dashboard_check_count"
            ),
            source_artifacts=(_rel(SMOOTH_STACK_DASHBOARD_JSON),),
        ),
        _check(
            key="smooth_stack_dashboard.consistent.true",
            expected=True,
            observed=smooth_stack_dashboard.get(
                "smooth_continuation_source_read_stack_dashboard_consistent"
            ),
            source_artifacts=(_rel(SMOOTH_STACK_DASHBOARD_JSON),),
        ),
        _check(
            key="smooth_operator_dependency.checklist_branch_verdict.deferred",
            expected=CHECKLIST_BRANCH_VERDICT,
            observed=smooth_operator_dependency.get("checklist_branch_verdict"),
            source_artifacts=(_rel(SMOOTH_OPERATOR_DEPENDENCY_JSON),),
        ),
        _check(
            key="smooth_operator_dependency.dischargeable_now_count.zero",
            expected=0,
            observed=smooth_operator_dependency.get("dischargeable_now_count"),
            source_artifacts=(_rel(SMOOTH_OPERATOR_DEPENDENCY_JSON),),
        ),
        _check(
            key="queue_counts.remain_blocked",
            expected=(3, 3, 0, 0, 0),
            observed=(
                smooth_operator_dependency.get("queue_item_count"),
                smooth_operator_dependency.get("blocked_queue_item_count"),
                smooth_operator_dependency.get("actionable_queue_item_count"),
                smooth_operator_dependency.get("may_discharge_queue_item_count"),
                smooth_operator_dependency.get("direct_theorem_artifact_count"),
            ),
            source_artifacts=(_rel(SMOOTH_OPERATOR_DEPENDENCY_JSON),),
        ),
        _check(
            key="source_report_count.expected_eighteen",
            expected=18,
            observed=len(direct_reports),
            source_artifacts=direct_reports,
        ),
        _check(
            key="source_ref_count.expected_current_union",
            expected=len(source_refs),
            observed=len(source_refs),
            source_artifacts=source_refs,
        ),
    )
    issues = tuple(check.key for check in checks if not check.passed)

    return Lemma0252CrossGapSourceReadStatusDashboard(
        schema_version=1,
        lemma_id=str(packets["gap_002"].get("lemma_id")),
        candidate_status=str(packets["gap_002"].get("candidate_status")),
        active_candidate=bool(packets["gap_002"].get("active_candidate")),
        gap_count=len(gap_rows),
        gap_ids=expected_gap_ids,
        source_branches=expected_source_branches,
        direct_gap_count=len(gap_rows),
        packet_count=len(gap_rows),
        dependency_guard_count=len(gap_rows),
        smooth_stack_step_count=int(smooth_stack_dashboard.get("stack_step_count", 0)),
        source_report_count=len(direct_reports),
        source_ref_count=len(source_refs),
        cross_gap_source_read_status_dashboard_check_count=len(checks),
        passed_cross_gap_source_read_status_dashboard_check_count=sum(
            1 for check in checks if check.passed
        ),
        failed_cross_gap_source_read_status_dashboard_check_count=len(issues),
        cross_gap_source_read_status_dashboard_consistent=len(issues) == 0,
        source_read_count=source_read_count,
        direct_branch_source_read_count=direct_branch_source_read_count,
        cross_cutting_source_read_count=cross_cutting_source_read_count,
        blocked_source_read_count=blocked_source_read_count,
        actionable_source_read_count=actionable_source_read_count,
        may_discharge_source_read_count=may_discharge_source_read_count,
        exact_discharge_artifact_count=exact_discharge_artifact_count,
        packet_check_count=packet_check_count,
        failed_packet_check_count=failed_packet_check_count,
        packet_consistent_count=sum(1 for row in gap_rows if row.packet_consistent),
        dependency_check_count=dependency_check_count,
        failed_dependency_check_count=failed_dependency_check_count,
        dependency_consistent_count=sum(1 for row in gap_rows if row.dependency_consistent),
        smooth_operator_index_check_count=int(
            smooth_operator.get(
                "smooth_continuation_source_read_packet_operator_index_check_count", 0
            )
        ),
        failed_smooth_operator_index_check_count=int(
            smooth_operator.get(
                "failed_smooth_continuation_source_read_packet_operator_index_check_count",
                0,
            )
        ),
        smooth_operator_index_consistent=bool(
            smooth_operator.get(
                "smooth_continuation_source_read_packet_operator_index_consistent"
            )
        ),
        smooth_operator_dependency_check_count=int(
            smooth_operator_dependency.get(
                "smooth_continuation_source_read_packet_operator_dependency_check_count",
                0,
            )
        ),
        failed_smooth_operator_dependency_check_count=int(
            smooth_operator_dependency.get(
                "failed_smooth_continuation_source_read_packet_operator_dependency_check_count",
                0,
            )
        ),
        smooth_operator_dependency_consistent=bool(
            smooth_operator_dependency.get(
                "smooth_continuation_source_read_packet_operator_dependency_consistent"
            )
        ),
        smooth_stack_dashboard_check_count=int(
            smooth_stack_dashboard.get(
                "smooth_continuation_source_read_stack_dashboard_check_count", 0
            )
        ),
        failed_smooth_stack_dashboard_check_count=int(
            smooth_stack_dashboard.get(
                "failed_smooth_continuation_source_read_stack_dashboard_check_count", 0
            )
        ),
        smooth_stack_dashboard_consistent=bool(
            smooth_stack_dashboard.get(
                "smooth_continuation_source_read_stack_dashboard_consistent"
            )
        ),
        checklist_branch_verdict=str(
            smooth_operator_dependency.get("checklist_branch_verdict")
        ),
        dischargeable_now_count=int(
            smooth_operator_dependency.get("dischargeable_now_count", 0)
        ),
        queue_item_count=int(smooth_operator_dependency.get("queue_item_count", 0)),
        blocked_queue_item_count=int(
            smooth_operator_dependency.get("blocked_queue_item_count", 0)
        ),
        actionable_queue_item_count=int(
            smooth_operator_dependency.get("actionable_queue_item_count", 0)
        ),
        may_discharge_queue_item_count=int(
            smooth_operator_dependency.get("may_discharge_queue_item_count", 0)
        ),
        direct_theorem_artifact_count=int(
            smooth_operator_dependency.get("direct_theorem_artifact_count", 0)
        ),
        process_gate_open_authorized=any(
            bool(report.get("process_gate_open_authorized")) for report in all_reports
        ),
        blocker_state_changed=any(
            bool(report.get("blocker_state_changed")) for report in all_reports
        ),
        candidate_emission_authorized=any(
            bool(report.get("candidate_emission_authorized")) for report in all_reports
        ),
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        gap_rows=gap_rows,
        checks=checks,
        issues=issues,
        source_refs=source_refs,
        source_read_ids_by_gap=source_read_ids_by_gap,
        non_claims=NON_CLAIMS,
        packet_snapshots={config.gap_id: packets[config.gap_id] for config in GAP_CONFIGS},
        dependency_snapshots={
            config.gap_id: dependencies[config.gap_id] for config in GAP_CONFIGS
        },
        smooth_operator_snapshot=smooth_operator,
        smooth_operator_dependency_snapshot=smooth_operator_dependency,
        smooth_stack_dashboard_snapshot=smooth_stack_dashboard,
    )


def render_markdown(report: Lemma0252CrossGapSourceReadStatusDashboard) -> str:
    lines = [
        "# Lemma 0252 Cross-Gap Source Read Status Dashboard",
        "",
        "## Summary",
        "",
        f"- lemma_id: `{report.lemma_id}`",
        f"- candidate_status: `{report.candidate_status}`",
        f"- active_candidate: `{str(report.active_candidate).lower()}`",
        f"- gap_count: `{report.gap_count}`",
        f"- direct_gap_count: `{report.direct_gap_count}`",
        f"- packet_count: `{report.packet_count}`",
        f"- dependency_guard_count: `{report.dependency_guard_count}`",
        f"- smooth_stack_step_count: `{report.smooth_stack_step_count}`",
        f"- source_report_count: `{report.source_report_count}`",
        f"- source_ref_count: `{report.source_ref_count}`",
        (
            "- cross_gap_source_read_status_dashboard_check_count: "
            f"`{report.cross_gap_source_read_status_dashboard_check_count}`"
        ),
        (
            "- failed_cross_gap_source_read_status_dashboard_check_count: "
            f"`{report.failed_cross_gap_source_read_status_dashboard_check_count}`"
        ),
        (
            "- cross_gap_source_read_status_dashboard_consistent: "
            f"`{str(report.cross_gap_source_read_status_dashboard_consistent).lower()}`"
        ),
        f"- source_read_count: `{report.source_read_count}`",
        f"- direct_branch_source_read_count: `{report.direct_branch_source_read_count}`",
        f"- cross_cutting_source_read_count: `{report.cross_cutting_source_read_count}`",
        f"- blocked_source_read_count: `{report.blocked_source_read_count}`",
        f"- actionable_source_read_count: `{report.actionable_source_read_count}`",
        f"- may_discharge_source_read_count: `{report.may_discharge_source_read_count}`",
        f"- exact_discharge_artifact_count: `{report.exact_discharge_artifact_count}`",
        f"- packet_check_count: `{report.packet_check_count}`",
        f"- failed_packet_check_count: `{report.failed_packet_check_count}`",
        f"- dependency_check_count: `{report.dependency_check_count}`",
        f"- failed_dependency_check_count: `{report.failed_dependency_check_count}`",
        f"- smooth_operator_index_check_count: `{report.smooth_operator_index_check_count}`",
        (
            "- smooth_operator_dependency_check_count: "
            f"`{report.smooth_operator_dependency_check_count}`"
        ),
        f"- smooth_stack_dashboard_check_count: `{report.smooth_stack_dashboard_check_count}`",
        f"- checklist_branch_verdict: `{report.checklist_branch_verdict}`",
        f"- dischargeable_now_count: `{report.dischargeable_now_count}`",
        f"- queue_item_count: `{report.queue_item_count}`",
        f"- blocked_queue_item_count: `{report.blocked_queue_item_count}`",
        f"- direct_theorem_artifact_count: `{report.direct_theorem_artifact_count}`",
        f"- process_gate_open_authorized: `{str(report.process_gate_open_authorized).lower()}`",
        f"- blocker_state_changed: `{str(report.blocker_state_changed).lower()}`",
        f"- candidate_emission_authorized: `{str(report.candidate_emission_authorized).lower()}`",
        f"- missing_source_count: `{report.missing_source_count}`",
        "",
        "## Gap Status",
        "",
        (
            "| gap | family | steps | source reads | direct | cross-cutting | "
            "blocked | actionable | may discharge | exact artifacts | dep checks | dep failed |"
        ),
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in report.gap_rows:
        lines.append(
            f"| `{row.gap_id}` | `{row.source_branch}` | {row.relevant_step_range} | "
            f"{row.source_read_count} | {row.direct_branch_source_read_count} | "
            f"{row.cross_cutting_source_read_count} | {row.blocked_source_read_count} | "
            f"{row.actionable_source_read_count} | {row.may_discharge_source_read_count} | "
            f"{row.exact_discharge_artifact_count} | {row.dependency_check_count} | "
            f"{row.failed_dependency_check_count} |"
        )

    lines.extend(["", "## Source Reads", ""])
    for gap_id, source_ids in report.source_read_ids_by_gap.items():
        lines.append(f"### {gap_id}")
        lines.extend(f"- `{source_id}`" for source_id in source_ids)
        lines.append("")

    lines.extend(["## Checks", ""])
    lines.extend(["| key | expected | observed | passed |", "|---|---|---|---:|"])
    for check in report.checks:
        lines.append(
            f"| `{check.key}` | `{check.expected}` | `{check.observed}` | "
            f"{str(check.passed).lower()} |"
        )

    lines.extend(["", "## Source Refs", ""])
    lines.extend(f"- `{source}`" for source in report.source_refs)
    lines.extend(["", "## Non-Claims", ""])
    lines.extend(f"- `{claim}`" for claim in report.non_claims)
    lines.append("")
    return "\n".join(lines)


def render_json(report: Lemma0252CrossGapSourceReadStatusDashboard) -> str:
    return json.dumps(asdict(report), indent=2, sort_keys=True) + "\n"


def check_sources(report: Lemma0252CrossGapSourceReadStatusDashboard) -> tuple[bool, str]:
    if report.missing_source_count:
        return False, "missing source refs: " + ", ".join(report.missing_sources)
    return True, "all cross-gap source-read status dashboard sources exist"


def check_consistent(
    report: Lemma0252CrossGapSourceReadStatusDashboard,
) -> tuple[bool, str]:
    if not report.cross_gap_source_read_status_dashboard_consistent:
        return (
            False,
            "inconsistent cross-gap source-read status dashboard: "
            + ", ".join(report.issues),
        )
    return True, "cross-gap source-read status dashboard is consistent"


def check_blocked(report: Lemma0252CrossGapSourceReadStatusDashboard) -> tuple[bool, str]:
    if (
        report.gap_ids != ("gap_002", "gap_003", "gap_004")
        or report.source_read_count != 15
        or report.blocked_source_read_count != report.source_read_count
        or report.actionable_source_read_count != 0
        or report.may_discharge_source_read_count != 0
        or report.exact_discharge_artifact_count != 0
        or report.direct_theorem_artifact_count != 0
        or report.dischargeable_now_count != 0
        or report.process_gate_open_authorized
        or report.blocker_state_changed
        or report.candidate_emission_authorized
    ):
        return False, "cross-gap source-read status dashboard is not blocked"
    return True, "cross-gap source-read status dashboard remains blocked"


def check_output(
    output: Path,
    report: Lemma0252CrossGapSourceReadStatusDashboard,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_json(report) if output_format == "json" else render_markdown(report)
    if not output.exists():
        return False, f"missing cross-gap source-read status dashboard: {output}"
    observed = output.read_text(encoding="utf-8")
    if observed != expected:
        return False, f"stale cross-gap source-read status dashboard: {output}"
    return True, f"fresh cross-gap source-read status dashboard: {output}"


def _write_output(
    *,
    output: Path,
    report: Lemma0252CrossGapSourceReadStatusDashboard,
    output_format: str,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    text = render_json(report) if output_format == "json" else render_markdown(report)
    output.write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Render a read-only dashboard for lemma_0252 direct analytic "
            "source-read gaps gap_002, gap_003, and gap_004."
        )
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    parser.add_argument("--require-consistent", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    args = parser.parse_args(argv)

    report = build_cross_gap_source_read_status_dashboard()
    output = args.output
    if output is None:
        output = DEFAULT_JSON_OUTPUT if args.format == "json" else DEFAULT_MARKDOWN_OUTPUT

    if not args.check_output:
        _write_output(output=output, report=report, output_format=args.format)

    failures: list[str] = []
    if args.check_output:
        ok, message = check_output(output, report, args.format)
        print(message)
        if not ok:
            failures.append(message)
    if args.require_sources_exist:
        ok, message = check_sources(report)
        print(message)
        if not ok:
            failures.append(message)
    if args.require_consistent:
        ok, message = check_consistent(report)
        print(message)
        if not ok:
            failures.append(message)
    if args.require_blocked:
        ok, message = check_blocked(report)
        print(message)
        if not ok:
            failures.append(message)

    print(f"gap_count: {report.gap_count}")
    print(f"source_read_count: {report.source_read_count}")
    print(
        "cross_gap_source_read_status_dashboard_check_count: "
        f"{report.cross_gap_source_read_status_dashboard_check_count}"
    )
    print(
        "failed_cross_gap_source_read_status_dashboard_check_count: "
        f"{report.failed_cross_gap_source_read_status_dashboard_check_count}"
    )
    print(f"exact_discharge_artifact_count: {report.exact_discharge_artifact_count}")
    print(f"candidate_emission_authorized: {str(report.candidate_emission_authorized).lower()}")

    if failures:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
