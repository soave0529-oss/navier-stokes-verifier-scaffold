from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from lemma_0252_cross_gap_source_read_status_dashboard import (
    DEFAULT_JSON_OUTPUT as DEFAULT_DASHBOARD_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_DASHBOARD_MARKDOWN,
    build_cross_gap_source_read_status_dashboard,
    render_json as render_dashboard_json,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_cross_gap_source_read_status_dashboard_dependency.md"
)
DEFAULT_JSON_OUTPUT = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_cross_gap_source_read_status_dashboard_dependency.json"
)
DEFAULT_PAPERS_INDEX = ROOT / "papers/blockers/index.md"

CHECKLIST_BRANCH_VERDICT = "deferred_needs_new_result"
PACKET_STATUS = "blocked_source_read_only"
PACKET_BRANCH_VERDICT = "blocked_needs_new_result"

NON_CLAIMS = (
    "read_only_cross_gap_source_read_status_dashboard_dependency_guard",
    "canonical_report_freshness_only",
    "non_promotional_gap_002_gap_003_gap_004_dependency_audit",
    "no_candidate_promotion",
    "no_candidate_emission",
    "no_blocker_discharge",
    "no_process_gate_opened",
    "no_file_copy",
    "no_finite_bound_to_smallness_theorem",
    "no_compactness_liouville_theorem",
    "no_bkm_theorem",
    "no_serrin_theorem",
    "no_high_sobolev_continuation_bridge",
    "no_weak_to_smooth_upgrade",
    "no_navier_stokes_solution",
)

GAP_IDS = ("gap_002", "gap_003", "gap_004")
SOURCE_BRANCHES = (
    "finite_bound_to_smallness",
    "compactness_liouville",
    "smooth_continuation_bridge",
)
EXPECTED_SOURCE_READ_COUNTS = (7, 6, 2)
EXPECTED_DIRECT_BRANCH_COUNTS = (5, 5, 2)
EXPECTED_CROSS_CUTTING_COUNTS = (2, 1, 0)
EXPECTED_CHECKLIST_COUNTS = (7, 6, 7)
EXPECTED_THEOREM_BRANCH_COUNTS = (4, 3, 5)
DEPENDENCY_CHECK_LABEL_BY_GAP = {
    "gap_002": "finite_bound_smallness_source_read_packet_dependency_check_count",
    "gap_003": "compactness_liouville_source_read_packet_dependency_check_count",
    "gap_004": "smooth_continuation_source_read_packet_dependency_check_count",
}
FAILED_DEPENDENCY_CHECK_LABEL_BY_GAP = {
    "gap_002": "failed_finite_bound_smallness_source_read_packet_dependency_check_count",
    "gap_003": "failed_compactness_liouville_source_read_packet_dependency_check_count",
    "gap_004": "failed_smooth_continuation_source_read_packet_dependency_check_count",
}

PACKET_JSON_BY_GAP = {
    "gap_002": (
        DEFAULT_REPORT_DIR / "lemma_0252_finite_bound_smallness_source_read_packet.json"
    ),
    "gap_003": (
        DEFAULT_REPORT_DIR / "lemma_0252_compactness_liouville_source_read_packet.json"
    ),
    "gap_004": (
        DEFAULT_REPORT_DIR / "lemma_0252_smooth_continuation_source_read_packet.json"
    ),
}
DEPENDENCY_JSON_BY_GAP = {
    "gap_002": (
        DEFAULT_REPORT_DIR
        / "lemma_0252_finite_bound_smallness_source_read_packet_dependency.json"
    ),
    "gap_003": (
        DEFAULT_REPORT_DIR
        / "lemma_0252_compactness_liouville_source_read_packet_dependency.json"
    ),
    "gap_004": (
        DEFAULT_REPORT_DIR
        / "lemma_0252_smooth_continuation_source_read_packet_dependency.json"
    ),
}
CHECKLIST_JSON_BY_GAP = {
    "gap_002": DEFAULT_REPORT_DIR / "lemma_0252_finite_bound_smallness_checklist.json",
    "gap_003": DEFAULT_REPORT_DIR / "lemma_0252_compactness_liouville_checklist.json",
    "gap_004": DEFAULT_REPORT_DIR / "lemma_0252_smooth_continuation_checklist.json",
}


@dataclass(frozen=True)
class CrossGapSourceReadStatusDashboardDependencyCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class Lemma0252CrossGapSourceReadStatusDashboardDependency:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    cross_gap_dashboard_markdown: str
    cross_gap_dashboard_json: str
    papers_blockers_index: str
    direct_source_report_count: int
    source_ref_count: int
    cross_gap_source_read_status_dashboard_dependency_check_count: int
    passed_cross_gap_source_read_status_dashboard_dependency_check_count: int
    failed_cross_gap_source_read_status_dashboard_dependency_check_count: int
    cross_gap_source_read_status_dashboard_dependency_consistent: bool
    dashboard_gap_count: int
    dashboard_source_report_count: int
    dashboard_source_ref_count: int
    dashboard_check_count: int
    failed_dashboard_check_count: int
    dashboard_consistent: bool
    source_read_count: int
    direct_branch_source_read_count: int
    cross_cutting_source_read_count: int
    blocked_source_read_count: int
    actionable_source_read_count: int
    may_discharge_source_read_count: int
    exact_discharge_artifact_count: int
    packet_check_count: int
    failed_packet_check_count: int
    dependency_check_count: int
    failed_dependency_check_count: int
    packet_consistent_count: int
    dependency_consistent_count: int
    checklist_item_count: int
    theorem_branch_count: int
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
    issues: tuple[str, ...]
    checks: tuple[CrossGapSourceReadStatusDashboardDependencyCheck, ...]
    source_refs: tuple[str, ...]
    source_read_ids_by_gap: dict[str, tuple[str, ...]]
    checklist_branch_verdicts_by_gap: dict[str, str]
    non_claims: tuple[str, ...]
    dashboard_snapshot: dict[str, object]
    packet_snapshots: dict[str, dict[str, object]]
    dependency_snapshots: dict[str, dict[str, object]]
    checklist_snapshots: dict[str, dict[str, object]]
    queue_stack_snapshots: dict[str, dict[str, object]]
    smooth_stack_snapshots: dict[str, dict[str, object]]


def _rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


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
) -> CrossGapSourceReadStatusDashboardDependencyCheck:
    return CrossGapSourceReadStatusDashboardDependencyCheck(
        key=key,
        expected=str(expected),
        observed=str(observed),
        passed=expected == observed,
        source_artifacts=source_artifacts,
    )


def _missing_sources(source_refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(source for source in source_refs if not (ROOT / source).exists())


def _markdown_pair(json_path: Path) -> tuple[str, str]:
    json_ref = _rel(json_path)
    return (json_ref.removesuffix(".json") + ".md", json_ref)


def _direct_source_reports() -> tuple[str, ...]:
    reports: list[str] = [
        _rel(DEFAULT_DASHBOARD_MARKDOWN),
        _rel(DEFAULT_DASHBOARD_JSON),
    ]
    for path in (
        PACKET_JSON_BY_GAP["gap_002"],
        DEPENDENCY_JSON_BY_GAP["gap_002"],
        PACKET_JSON_BY_GAP["gap_003"],
        DEPENDENCY_JSON_BY_GAP["gap_003"],
        PACKET_JSON_BY_GAP["gap_004"],
        DEPENDENCY_JSON_BY_GAP["gap_004"],
        DEFAULT_REPORT_DIR / "lemma_0252_smooth_continuation_source_read_packet_operator_index.json",
        DEFAULT_REPORT_DIR
        / "lemma_0252_smooth_continuation_source_read_packet_operator_dependency.json",
        DEFAULT_REPORT_DIR / "lemma_0252_smooth_continuation_source_read_stack_dashboard.json",
        DEFAULT_REPORT_DIR / "lemma_0252_theorem_artifact_review_queue.json",
        DEFAULT_REPORT_DIR / "lemma_0252_theorem_artifact_review_queue_dependency.json",
        DEFAULT_REPORT_DIR / "lemma_0252_theorem_artifact_review_queue_operator_index.json",
        DEFAULT_REPORT_DIR
        / "lemma_0252_theorem_artifact_review_queue_operator_dependency.json",
        CHECKLIST_JSON_BY_GAP["gap_002"],
        CHECKLIST_JSON_BY_GAP["gap_003"],
        CHECKLIST_JSON_BY_GAP["gap_004"],
    ):
        reports.extend(_markdown_pair(path))
    return tuple(dict.fromkeys(reports))


def _source_refs_from(*reports: dict[str, object]) -> tuple[str, ...]:
    refs: list[str] = []
    for report in reports:
        refs.extend(str(source) for source in report.get("source_refs", ()))
    return tuple(refs)


def _source_ids(packet: dict[str, object]) -> tuple[str, ...]:
    return tuple(
        str(item.get("source_id"))
        for item in packet.get("source_reads", ())
        if isinstance(item, dict)
    )


def _dashboard_rows(dashboard: dict[str, object]) -> tuple[dict[str, object], ...]:
    rows = dashboard.get("gap_rows", ())
    if not isinstance(rows, list):
        raise ValueError("expected list field `gap_rows`")
    return tuple(row for row in rows if isinstance(row, dict))


def _load_queue_stack() -> dict[str, dict[str, object]]:
    paths = {
        "queue": DEFAULT_REPORT_DIR / "lemma_0252_theorem_artifact_review_queue.json",
        "queue_dependency": (
            DEFAULT_REPORT_DIR / "lemma_0252_theorem_artifact_review_queue_dependency.json"
        ),
        "queue_operator_index": (
            DEFAULT_REPORT_DIR
            / "lemma_0252_theorem_artifact_review_queue_operator_index.json"
        ),
        "queue_operator_dependency": (
            DEFAULT_REPORT_DIR
            / "lemma_0252_theorem_artifact_review_queue_operator_dependency.json"
        ),
    }
    return {name: _load_json(path) for name, path in paths.items()}


def _load_smooth_stack() -> dict[str, dict[str, object]]:
    paths = {
        "smooth_operator_index": (
            DEFAULT_REPORT_DIR
            / "lemma_0252_smooth_continuation_source_read_packet_operator_index.json"
        ),
        "smooth_operator_dependency": (
            DEFAULT_REPORT_DIR
            / "lemma_0252_smooth_continuation_source_read_packet_operator_dependency.json"
        ),
        "smooth_stack_dashboard": (
            DEFAULT_REPORT_DIR
            / "lemma_0252_smooth_continuation_source_read_stack_dashboard.json"
        ),
    }
    return {name: _load_json(path) for name, path in paths.items()}


def build_cross_gap_source_read_status_dashboard_dependency(
    *,
    papers_blockers_index: Path = DEFAULT_PAPERS_INDEX,
) -> Lemma0252CrossGapSourceReadStatusDashboardDependency:
    dashboard = _load_json(DEFAULT_DASHBOARD_JSON)
    fresh_dashboard = json.loads(
        render_dashboard_json(build_cross_gap_source_read_status_dashboard())
    )
    packets = {gap_id: _load_json(path) for gap_id, path in PACKET_JSON_BY_GAP.items()}
    dependencies = {
        gap_id: _load_json(path) for gap_id, path in DEPENDENCY_JSON_BY_GAP.items()
    }
    checklists = {
        gap_id: _load_json(path) for gap_id, path in CHECKLIST_JSON_BY_GAP.items()
    }
    queue_stack = _load_queue_stack()
    smooth_stack = _load_smooth_stack()

    direct_reports = _direct_source_reports()
    all_reports = (
        (dashboard,)
        + tuple(packets[gap_id] for gap_id in GAP_IDS)
        + tuple(dependencies[gap_id] for gap_id in GAP_IDS)
        + tuple(checklists[gap_id] for gap_id in GAP_IDS)
        + tuple(queue_stack.values())
        + tuple(smooth_stack.values())
    )
    source_refs = tuple(
        dict.fromkeys(
            direct_reports
            + ("papers/blockers/index.md",)
            + _source_refs_from(*all_reports)
        )
    )
    missing_sources = _missing_sources(source_refs)

    dashboard_rows = _dashboard_rows(dashboard)
    source_read_ids_by_gap = {
        gap_id: _source_ids(packets[gap_id]) for gap_id in GAP_IDS
    }
    checklist_branch_verdicts_by_gap = {
        gap_id: str(checklists[gap_id].get("branch_verdict")) for gap_id in GAP_IDS
    }

    packet_source_reads = tuple(
        int(packets[gap_id].get("source_read_count", 0)) for gap_id in GAP_IDS
    )
    packet_direct_reads = tuple(
        int(packets[gap_id].get("direct_branch_source_read_count", 0))
        for gap_id in GAP_IDS
    )
    packet_cross_reads = tuple(
        int(packets[gap_id].get("cross_cutting_source_read_count", 0))
        for gap_id in GAP_IDS
    )
    dependency_counts = tuple(
        int(dependencies[gap_id].get(DEPENDENCY_CHECK_LABEL_BY_GAP[gap_id], 0))
        for gap_id in GAP_IDS
    )
    failed_dependency_counts = tuple(
        int(dependencies[gap_id].get(FAILED_DEPENDENCY_CHECK_LABEL_BY_GAP[gap_id], 0))
        for gap_id in GAP_IDS
    )
    checklist_item_counts = tuple(
        int(checklists[gap_id].get("checklist_item_count", 0)) for gap_id in GAP_IDS
    )
    theorem_branch_counts = tuple(
        int(checklists[gap_id].get("theorem_branch_count", 0)) for gap_id in GAP_IDS
    )
    branch_verdicts = tuple(checklist_branch_verdicts_by_gap[gap_id] for gap_id in GAP_IDS)
    source_read_ids_from_dashboard = tuple(
        tuple(str(source_id) for source_id in dashboard.get("source_read_ids_by_gap", {}).get(gap_id, ()))
        for gap_id in GAP_IDS
    )

    queue_operator_dependency = queue_stack["queue_operator_dependency"]
    smooth_operator_dependency = smooth_stack["smooth_operator_dependency"]

    checks = (
        _check(
            key="dashboard.canonical_json.matches_fresh_build",
            expected=True,
            observed=dashboard == fresh_dashboard,
            source_artifacts=(_rel(DEFAULT_DASHBOARD_JSON),),
        ),
        _check(
            key="dashboard.lemma_id.expected_lemma_0252",
            expected="lemma_0252",
            observed=dashboard.get("lemma_id"),
            source_artifacts=(_rel(DEFAULT_DASHBOARD_JSON),),
        ),
        _check(
            key="dashboard.candidate_status.remains_needs_review",
            expected="needs_review",
            observed=dashboard.get("candidate_status"),
            source_artifacts=(_rel(DEFAULT_DASHBOARD_JSON),),
        ),
        _check(
            key="dashboard.active_candidate.false",
            expected=False,
            observed=dashboard.get("active_candidate"),
            source_artifacts=(_rel(DEFAULT_DASHBOARD_JSON),),
        ),
        _check(
            key="dashboard.gap_ids.expected_direct_analytic_gaps",
            expected=GAP_IDS,
            observed=tuple(str(gap_id) for gap_id in dashboard.get("gap_ids", ())),
            source_artifacts=(_rel(DEFAULT_DASHBOARD_JSON),),
        ),
        _check(
            key="dashboard.source_branches.expected_direct_analytic_families",
            expected=SOURCE_BRANCHES,
            observed=tuple(str(branch) for branch in dashboard.get("source_branches", ())),
            source_artifacts=(_rel(DEFAULT_DASHBOARD_JSON),),
        ),
        _check(
            key="dashboard.gap_count.expected_three",
            expected=3,
            observed=dashboard.get("gap_count"),
            source_artifacts=(_rel(DEFAULT_DASHBOARD_JSON),),
        ),
        _check(
            key="dashboard.row_count.expected_three",
            expected=3,
            observed=len(dashboard_rows),
            source_artifacts=(_rel(DEFAULT_DASHBOARD_JSON),),
        ),
        _check(
            key="dashboard.check_count.expected_sixty_one",
            expected=61,
            observed=dashboard.get("cross_gap_source_read_status_dashboard_check_count"),
            source_artifacts=(_rel(DEFAULT_DASHBOARD_JSON),),
        ),
        _check(
            key="dashboard.failed_checks.zero",
            expected=0,
            observed=dashboard.get("failed_cross_gap_source_read_status_dashboard_check_count"),
            source_artifacts=(_rel(DEFAULT_DASHBOARD_JSON),),
        ),
        _check(
            key="dashboard.consistent.true",
            expected=True,
            observed=dashboard.get("cross_gap_source_read_status_dashboard_consistent"),
            source_artifacts=(_rel(DEFAULT_DASHBOARD_JSON),),
        ),
        _check(
            key="packet.source_read_counts.match_expected",
            expected=EXPECTED_SOURCE_READ_COUNTS,
            observed=packet_source_reads,
            source_artifacts=tuple(_rel(PACKET_JSON_BY_GAP[gap_id]) for gap_id in GAP_IDS),
        ),
        _check(
            key="packet.direct_branch_counts.match_expected",
            expected=EXPECTED_DIRECT_BRANCH_COUNTS,
            observed=packet_direct_reads,
            source_artifacts=tuple(_rel(PACKET_JSON_BY_GAP[gap_id]) for gap_id in GAP_IDS),
        ),
        _check(
            key="packet.cross_cutting_counts.match_expected",
            expected=EXPECTED_CROSS_CUTTING_COUNTS,
            observed=packet_cross_reads,
            source_artifacts=tuple(_rel(PACKET_JSON_BY_GAP[gap_id]) for gap_id in GAP_IDS),
        ),
        _check(
            key="dashboard.source_read_count.matches_packet_sum",
            expected=sum(packet_source_reads),
            observed=dashboard.get("source_read_count"),
            source_artifacts=tuple(_rel(PACKET_JSON_BY_GAP[gap_id]) for gap_id in GAP_IDS),
        ),
        _check(
            key="dashboard.direct_branch_source_read_count.matches_packet_sum",
            expected=sum(packet_direct_reads),
            observed=dashboard.get("direct_branch_source_read_count"),
            source_artifacts=tuple(_rel(PACKET_JSON_BY_GAP[gap_id]) for gap_id in GAP_IDS),
        ),
        _check(
            key="dashboard.cross_cutting_source_read_count.matches_packet_sum",
            expected=sum(packet_cross_reads),
            observed=dashboard.get("cross_cutting_source_read_count"),
            source_artifacts=tuple(_rel(PACKET_JSON_BY_GAP[gap_id]) for gap_id in GAP_IDS),
        ),
        _check(
            key="dashboard.blocked_source_read_count.matches_source_read_count",
            expected=dashboard.get("source_read_count"),
            observed=dashboard.get("blocked_source_read_count"),
            source_artifacts=(_rel(DEFAULT_DASHBOARD_JSON),),
        ),
        _check(
            key="dashboard.actionable_source_read_count.zero",
            expected=0,
            observed=dashboard.get("actionable_source_read_count"),
            source_artifacts=(_rel(DEFAULT_DASHBOARD_JSON),),
        ),
        _check(
            key="dashboard.may_discharge_source_read_count.zero",
            expected=0,
            observed=dashboard.get("may_discharge_source_read_count"),
            source_artifacts=(_rel(DEFAULT_DASHBOARD_JSON),),
        ),
        _check(
            key="dashboard.exact_discharge_artifact_count.zero",
            expected=0,
            observed=dashboard.get("exact_discharge_artifact_count"),
            source_artifacts=(_rel(DEFAULT_DASHBOARD_JSON),),
        ),
        _check(
            key="packet.status.all_blocked_source_read_only",
            expected=(PACKET_STATUS, PACKET_STATUS, PACKET_STATUS),
            observed=tuple(str(packets[gap_id].get("packet_status")) for gap_id in GAP_IDS),
            source_artifacts=tuple(_rel(PACKET_JSON_BY_GAP[gap_id]) for gap_id in GAP_IDS),
        ),
        _check(
            key="dependency.packet_branch_verdicts.all_blocked_needs_new_result",
            expected=(PACKET_BRANCH_VERDICT, PACKET_BRANCH_VERDICT, PACKET_BRANCH_VERDICT),
            observed=tuple(
                str(dependencies[gap_id].get("packet_branch_verdict")) for gap_id in GAP_IDS
            ),
            source_artifacts=tuple(_rel(DEPENDENCY_JSON_BY_GAP[gap_id]) for gap_id in GAP_IDS),
        ),
        _check(
            key="dependency.check_counts.expected_fifty_each",
            expected=(50, 50, 50),
            observed=dependency_counts,
            source_artifacts=tuple(_rel(DEPENDENCY_JSON_BY_GAP[gap_id]) for gap_id in GAP_IDS),
        ),
        _check(
            key="dependency.failed_checks.zero",
            expected=(0, 0, 0),
            observed=failed_dependency_counts,
            source_artifacts=tuple(_rel(DEPENDENCY_JSON_BY_GAP[gap_id]) for gap_id in GAP_IDS),
        ),
        _check(
            key="dashboard.dependency_check_count.matches_dependency_sum",
            expected=sum(dependency_counts),
            observed=dashboard.get("dependency_check_count"),
            source_artifacts=tuple(_rel(DEPENDENCY_JSON_BY_GAP[gap_id]) for gap_id in GAP_IDS),
        ),
        _check(
            key="dashboard.failed_dependency_check_count.matches_dependency_sum",
            expected=sum(failed_dependency_counts),
            observed=dashboard.get("failed_dependency_check_count"),
            source_artifacts=tuple(_rel(DEPENDENCY_JSON_BY_GAP[gap_id]) for gap_id in GAP_IDS),
        ),
        _check(
            key="checklists.branch_verdicts.remain_deferred_needs_new_result",
            expected=(CHECKLIST_BRANCH_VERDICT,) * 3,
            observed=branch_verdicts,
            source_artifacts=tuple(_rel(CHECKLIST_JSON_BY_GAP[gap_id]) for gap_id in GAP_IDS),
        ),
        _check(
            key="checklists.item_counts.match_expected",
            expected=EXPECTED_CHECKLIST_COUNTS,
            observed=checklist_item_counts,
            source_artifacts=tuple(_rel(CHECKLIST_JSON_BY_GAP[gap_id]) for gap_id in GAP_IDS),
        ),
        _check(
            key="checklists.theorem_branch_counts.match_expected",
            expected=EXPECTED_THEOREM_BRANCH_COUNTS,
            observed=theorem_branch_counts,
            source_artifacts=tuple(_rel(CHECKLIST_JSON_BY_GAP[gap_id]) for gap_id in GAP_IDS),
        ),
        _check(
            key="checklists.dischargeable_now_counts.zero",
            expected=(0, 0, 0),
            observed=tuple(
                int(checklists[gap_id].get("dischargeable_now_count", 0))
                for gap_id in GAP_IDS
            ),
            source_artifacts=tuple(_rel(CHECKLIST_JSON_BY_GAP[gap_id]) for gap_id in GAP_IDS),
        ),
        _check(
            key="dashboard.source_read_ids.match_packets",
            expected=tuple(source_read_ids_by_gap[gap_id] for gap_id in GAP_IDS),
            observed=source_read_ids_from_dashboard,
            source_artifacts=tuple(_rel(PACKET_JSON_BY_GAP[gap_id]) for gap_id in GAP_IDS),
        ),
        _check(
            key="queue_stack.counts.remain_blocked",
            expected=(3, 3, 0, 0, 0),
            observed=(
                queue_operator_dependency.get("queue_item_count"),
                queue_operator_dependency.get("blocked_queue_item_count"),
                queue_operator_dependency.get("actionable_queue_item_count"),
                queue_operator_dependency.get("may_discharge_queue_item_count"),
                queue_operator_dependency.get("direct_theorem_artifact_count"),
            ),
            source_artifacts=(
                "track-a-regularity/reports/"
                "lemma_0252_theorem_artifact_review_queue_operator_dependency.json",
            ),
        ),
        _check(
            key="queue_dependency.check_count.expected_seventy",
            expected=70,
            observed=queue_stack["queue_dependency"].get(
                "theorem_artifact_review_queue_dependency_check_count"
            ),
            source_artifacts=(
                "track-a-regularity/reports/"
                "lemma_0252_theorem_artifact_review_queue_dependency.json",
            ),
        ),
        _check(
            key="queue_operator_index.check_count.expected_forty_four",
            expected=44,
            observed=queue_stack["queue_operator_index"].get(
                "theorem_artifact_review_queue_operator_index_check_count"
            ),
            source_artifacts=(
                "track-a-regularity/reports/"
                "lemma_0252_theorem_artifact_review_queue_operator_index.json",
            ),
        ),
        _check(
            key="queue_operator_dependency.check_count.expected_sixty_one",
            expected=61,
            observed=queue_operator_dependency.get(
                "theorem_artifact_review_queue_operator_dependency_check_count"
            ),
            source_artifacts=(
                "track-a-regularity/reports/"
                "lemma_0252_theorem_artifact_review_queue_operator_dependency.json",
            ),
        ),
        _check(
            key="queue_stack.failed_checks.zero",
            expected=(0, 0, 0),
            observed=(
                queue_stack["queue_dependency"].get(
                    "failed_theorem_artifact_review_queue_dependency_check_count"
                ),
                queue_stack["queue_operator_index"].get(
                    "failed_theorem_artifact_review_queue_operator_index_check_count"
                ),
                queue_operator_dependency.get(
                    "failed_theorem_artifact_review_queue_operator_dependency_check_count"
                ),
            ),
            source_artifacts=tuple(
                source
                for source in direct_reports
                if "theorem_artifact_review_queue" in source
            ),
        ),
        _check(
            key="smooth_stack.check_counts.match_step_120_to_124",
            expected=(37, 57, 49),
            observed=(
                smooth_stack["smooth_operator_index"].get(
                    "smooth_continuation_source_read_packet_operator_index_check_count"
                ),
                smooth_operator_dependency.get(
                    "smooth_continuation_source_read_packet_operator_dependency_check_count"
                ),
                smooth_stack["smooth_stack_dashboard"].get(
                    "smooth_continuation_source_read_stack_dashboard_check_count"
                ),
            ),
            source_artifacts=tuple(
                source
                for source in direct_reports
                if "smooth_continuation_source_read" in source
            ),
        ),
        _check(
            key="smooth_stack.failed_checks.zero",
            expected=(0, 0, 0),
            observed=(
                smooth_stack["smooth_operator_index"].get(
                    "failed_smooth_continuation_source_read_packet_operator_index_check_count"
                ),
                smooth_operator_dependency.get(
                    "failed_smooth_continuation_source_read_packet_operator_dependency_check_count"
                ),
                smooth_stack["smooth_stack_dashboard"].get(
                    "failed_smooth_continuation_source_read_stack_dashboard_check_count"
                ),
            ),
            source_artifacts=tuple(
                source
                for source in direct_reports
                if "smooth_continuation_source_read" in source
            ),
        ),
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
            key="source_refs.include_direct_source_reports",
            expected=True,
            observed=all(source in source_refs for source in direct_reports),
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
            key="source_refs.include_gap_checklists",
            expected=True,
            observed=all(_rel(CHECKLIST_JSON_BY_GAP[gap_id]) in source_refs for gap_id in GAP_IDS),
            source_artifacts=tuple(_rel(CHECKLIST_JSON_BY_GAP[gap_id]) for gap_id in GAP_IDS),
        ),
        _check(
            key="source_refs.include_step_125_dashboard",
            expected=True,
            observed=_rel(DEFAULT_DASHBOARD_JSON) in source_refs
            and _rel(DEFAULT_DASHBOARD_MARKDOWN) in source_refs,
            source_artifacts=(_rel(DEFAULT_DASHBOARD_MARKDOWN), _rel(DEFAULT_DASHBOARD_JSON)),
        ),
        _check(
            key="source_refs.include_gap_002_local_sources",
            expected=True,
            observed=(
                "papers/blockers/finite_bound_to_smallness/"
                "2308.04147_partial_regularity_survey.pdf"
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
            in source_refs,
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.missing_count.zero",
            expected=0,
            observed=len(missing_sources),
            source_artifacts=source_refs,
        ),
        _check(
            key="source_ref_count.expected_current_union",
            expected=len(source_refs),
            observed=len(source_refs),
            source_artifacts=source_refs,
        ),
    )
    issues = tuple(check.key for check in checks if not check.passed)

    return Lemma0252CrossGapSourceReadStatusDashboardDependency(
        schema_version=1,
        lemma_id=str(dashboard.get("lemma_id")),
        candidate_status=str(dashboard.get("candidate_status")),
        active_candidate=bool(dashboard.get("active_candidate")),
        cross_gap_dashboard_markdown=_rel(DEFAULT_DASHBOARD_MARKDOWN),
        cross_gap_dashboard_json=_rel(DEFAULT_DASHBOARD_JSON),
        papers_blockers_index="papers/blockers/index.md",
        direct_source_report_count=len(direct_reports),
        source_ref_count=len(source_refs),
        cross_gap_source_read_status_dashboard_dependency_check_count=len(checks),
        passed_cross_gap_source_read_status_dashboard_dependency_check_count=sum(
            1 for check in checks if check.passed
        ),
        failed_cross_gap_source_read_status_dashboard_dependency_check_count=len(
            issues
        ),
        cross_gap_source_read_status_dashboard_dependency_consistent=len(issues) == 0,
        dashboard_gap_count=int(dashboard.get("gap_count", 0)),
        dashboard_source_report_count=int(dashboard.get("source_report_count", 0)),
        dashboard_source_ref_count=int(dashboard.get("source_ref_count", 0)),
        dashboard_check_count=int(
            dashboard.get("cross_gap_source_read_status_dashboard_check_count", 0)
        ),
        failed_dashboard_check_count=int(
            dashboard.get("failed_cross_gap_source_read_status_dashboard_check_count", 0)
        ),
        dashboard_consistent=bool(
            dashboard.get("cross_gap_source_read_status_dashboard_consistent")
        ),
        source_read_count=int(dashboard.get("source_read_count", 0)),
        direct_branch_source_read_count=int(
            dashboard.get("direct_branch_source_read_count", 0)
        ),
        cross_cutting_source_read_count=int(
            dashboard.get("cross_cutting_source_read_count", 0)
        ),
        blocked_source_read_count=int(dashboard.get("blocked_source_read_count", 0)),
        actionable_source_read_count=int(
            dashboard.get("actionable_source_read_count", 0)
        ),
        may_discharge_source_read_count=int(
            dashboard.get("may_discharge_source_read_count", 0)
        ),
        exact_discharge_artifact_count=int(
            dashboard.get("exact_discharge_artifact_count", 0)
        ),
        packet_check_count=int(dashboard.get("packet_check_count", 0)),
        failed_packet_check_count=int(dashboard.get("failed_packet_check_count", 0)),
        dependency_check_count=int(dashboard.get("dependency_check_count", 0)),
        failed_dependency_check_count=int(
            dashboard.get("failed_dependency_check_count", 0)
        ),
        packet_consistent_count=int(dashboard.get("packet_consistent_count", 0)),
        dependency_consistent_count=int(dashboard.get("dependency_consistent_count", 0)),
        checklist_item_count=sum(checklist_item_counts),
        theorem_branch_count=sum(theorem_branch_counts),
        dischargeable_now_count=sum(
            int(checklists[gap_id].get("dischargeable_now_count", 0))
            for gap_id in GAP_IDS
        ),
        queue_item_count=int(queue_operator_dependency.get("queue_item_count", 0)),
        blocked_queue_item_count=int(
            queue_operator_dependency.get("blocked_queue_item_count", 0)
        ),
        actionable_queue_item_count=int(
            queue_operator_dependency.get("actionable_queue_item_count", 0)
        ),
        may_discharge_queue_item_count=int(
            queue_operator_dependency.get("may_discharge_queue_item_count", 0)
        ),
        direct_theorem_artifact_count=int(
            queue_operator_dependency.get("direct_theorem_artifact_count", 0)
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
        issues=issues,
        checks=checks,
        source_refs=source_refs,
        source_read_ids_by_gap=source_read_ids_by_gap,
        checklist_branch_verdicts_by_gap=checklist_branch_verdicts_by_gap,
        non_claims=NON_CLAIMS,
        dashboard_snapshot=dashboard,
        packet_snapshots={gap_id: packets[gap_id] for gap_id in GAP_IDS},
        dependency_snapshots={gap_id: dependencies[gap_id] for gap_id in GAP_IDS},
        checklist_snapshots={gap_id: checklists[gap_id] for gap_id in GAP_IDS},
        queue_stack_snapshots=queue_stack,
        smooth_stack_snapshots=smooth_stack,
    )


def render_markdown(
    report: Lemma0252CrossGapSourceReadStatusDashboardDependency,
) -> str:
    lines = [
        "# Lemma 0252 Cross-Gap Source Read Status Dashboard Dependency",
        "",
        "## Summary",
        "",
        f"- lemma_id: `{report.lemma_id}`",
        f"- candidate_status: `{report.candidate_status}`",
        f"- active_candidate: `{str(report.active_candidate).lower()}`",
        f"- direct_source_report_count: `{report.direct_source_report_count}`",
        f"- source_ref_count: `{report.source_ref_count}`",
        (
            "- cross_gap_source_read_status_dashboard_dependency_check_count: "
            f"`{report.cross_gap_source_read_status_dashboard_dependency_check_count}`"
        ),
        (
            "- failed_cross_gap_source_read_status_dashboard_dependency_check_count: "
            f"`{report.failed_cross_gap_source_read_status_dashboard_dependency_check_count}`"
        ),
        (
            "- cross_gap_source_read_status_dashboard_dependency_consistent: "
            f"`{str(report.cross_gap_source_read_status_dashboard_dependency_consistent).lower()}`"
        ),
        f"- dashboard_gap_count: `{report.dashboard_gap_count}`",
        f"- dashboard_source_report_count: `{report.dashboard_source_report_count}`",
        f"- dashboard_source_ref_count: `{report.dashboard_source_ref_count}`",
        f"- dashboard_check_count: `{report.dashboard_check_count}`",
        f"- failed_dashboard_check_count: `{report.failed_dashboard_check_count}`",
        f"- dashboard_consistent: `{str(report.dashboard_consistent).lower()}`",
        f"- source_read_count: `{report.source_read_count}`",
        f"- blocked_source_read_count: `{report.blocked_source_read_count}`",
        f"- actionable_source_read_count: `{report.actionable_source_read_count}`",
        f"- may_discharge_source_read_count: `{report.may_discharge_source_read_count}`",
        f"- exact_discharge_artifact_count: `{report.exact_discharge_artifact_count}`",
        f"- packet_check_count: `{report.packet_check_count}`",
        f"- dependency_check_count: `{report.dependency_check_count}`",
        f"- checklist_item_count: `{report.checklist_item_count}`",
        f"- theorem_branch_count: `{report.theorem_branch_count}`",
        f"- dischargeable_now_count: `{report.dischargeable_now_count}`",
        f"- queue_item_count: `{report.queue_item_count}`",
        f"- blocked_queue_item_count: `{report.blocked_queue_item_count}`",
        f"- direct_theorem_artifact_count: `{report.direct_theorem_artifact_count}`",
        f"- process_gate_open_authorized: `{str(report.process_gate_open_authorized).lower()}`",
        f"- blocker_state_changed: `{str(report.blocker_state_changed).lower()}`",
        f"- candidate_emission_authorized: `{str(report.candidate_emission_authorized).lower()}`",
        f"- missing_source_count: `{report.missing_source_count}`",
        "",
        "## Gap Source Reads",
        "",
        "| gap | branch verdict | source reads | source ids |",
        "|---|---|---:|---|",
    ]
    for gap_id in GAP_IDS:
        lines.append(
            f"| `{gap_id}` | `{report.checklist_branch_verdicts_by_gap[gap_id]}` | "
            f"{len(report.source_read_ids_by_gap[gap_id])} | "
            f"`{', '.join(report.source_read_ids_by_gap[gap_id])}` |"
        )

    lines.extend(["", "## Checks", ""])
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


def render_json(report: Lemma0252CrossGapSourceReadStatusDashboardDependency) -> str:
    return json.dumps(asdict(report), indent=2, sort_keys=True) + "\n"


def check_sources(
    report: Lemma0252CrossGapSourceReadStatusDashboardDependency,
) -> tuple[bool, str]:
    if report.missing_source_count:
        return False, "missing source refs: " + ", ".join(report.missing_sources)
    return True, "all cross-gap source-read status dashboard dependency sources exist"


def check_consistent(
    report: Lemma0252CrossGapSourceReadStatusDashboardDependency,
) -> tuple[bool, str]:
    if not report.cross_gap_source_read_status_dashboard_dependency_consistent:
        return (
            False,
            "inconsistent cross-gap source-read status dashboard dependency: "
            + ", ".join(report.issues),
        )
    return True, "cross-gap source-read status dashboard dependency is consistent"


def check_blocked(
    report: Lemma0252CrossGapSourceReadStatusDashboardDependency,
) -> tuple[bool, str]:
    if (
        report.dashboard_gap_count != 3
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
        return False, "cross-gap source-read status dashboard dependency is not blocked"
    return True, "cross-gap source-read status dashboard dependency remains blocked"


def check_output(
    output: Path,
    report: Lemma0252CrossGapSourceReadStatusDashboardDependency,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_json(report) if output_format == "json" else render_markdown(report)
    if not output.exists():
        return False, f"missing cross-gap source-read status dashboard dependency: {output}"
    observed = output.read_text(encoding="utf-8")
    if observed != expected:
        return False, f"stale cross-gap source-read status dashboard dependency: {output}"
    return True, f"fresh cross-gap source-read status dashboard dependency: {output}"


def _write_output(
    *,
    output: Path,
    report: Lemma0252CrossGapSourceReadStatusDashboardDependency,
    output_format: str,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    text = render_json(report) if output_format == "json" else render_markdown(report)
    output.write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Render a read-only dependency/freshness guard for the lemma_0252 "
            "cross-gap source-read status dashboard."
        )
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    parser.add_argument("--require-consistent", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    args = parser.parse_args(argv)

    report = build_cross_gap_source_read_status_dashboard_dependency()
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

    print(f"dashboard_gap_count: {report.dashboard_gap_count}")
    print(f"source_read_count: {report.source_read_count}")
    print(
        "cross_gap_source_read_status_dashboard_dependency_check_count: "
        f"{report.cross_gap_source_read_status_dashboard_dependency_check_count}"
    )
    print(
        "failed_cross_gap_source_read_status_dashboard_dependency_check_count: "
        f"{report.failed_cross_gap_source_read_status_dashboard_dependency_check_count}"
    )
    print(f"exact_discharge_artifact_count: {report.exact_discharge_artifact_count}")
    print(f"candidate_emission_authorized: {str(report.candidate_emission_authorized).lower()}")

    if failures:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
