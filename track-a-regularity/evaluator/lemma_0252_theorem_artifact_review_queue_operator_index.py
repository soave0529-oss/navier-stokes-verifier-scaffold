from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from lemma_0252_theorem_artifact_review_queue import (
    DEFAULT_JSON_OUTPUT as DEFAULT_QUEUE_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_QUEUE_MARKDOWN,
)
from lemma_0252_theorem_artifact_review_queue_dependency import (
    DEFAULT_JSON_OUTPUT as DEFAULT_QUEUE_DEPENDENCY_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_QUEUE_DEPENDENCY_MARKDOWN,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = (
    DEFAULT_REPORT_DIR / "lemma_0252_theorem_artifact_review_queue_operator_index.md"
)
DEFAULT_JSON_OUTPUT = (
    DEFAULT_REPORT_DIR / "lemma_0252_theorem_artifact_review_queue_operator_index.json"
)

NON_CLAIMS = (
    "read_only_theorem_artifact_review_queue_operator_index",
    "source_index_for_review_only",
    "no_candidate_promotion",
    "no_candidate_emission",
    "no_blocker_discharge",
    "no_process_gate_opened",
    "no_file_copy",
    "no_epsilon_regularity_theorem",
    "no_compactness_or_liouville_theorem",
    "no_bkm_or_serrin_or_high_sobolev_bound",
    "no_weak_to_smooth_upgrade",
    "no_navier_stokes_solution",
)


@dataclass(frozen=True)
class TheoremArtifactReviewQueueOperatorSection:
    step: int
    name: str
    role: str
    markdown_report: str
    json_report: str
    status: str
    primary_count_label: str
    primary_count: int
    blocked_count: int
    actionable_count: int
    consistent: bool
    missing_source_count: int


@dataclass(frozen=True)
class TheoremArtifactReviewQueueOperatorCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class Lemma0252TheoremArtifactReviewQueueOperatorIndex:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    section_count: int
    source_report_count: int
    source_ref_count: int
    queue_item_count: int
    direct_analytic_gap_count: int
    blocked_queue_item_count: int
    actionable_queue_item_count: int
    may_discharge_queue_item_count: int
    direct_theorem_artifact_count: int
    queue_source_edge_count: int
    direct_branch_source_edge_count: int
    cross_cutting_source_edge_count: int
    unique_literature_source_count: int
    literature_source_count: int
    gap_count: int
    source_gap_edge_count: int
    blocked_gap_count: int
    actionable_gap_count: int
    may_discharge_gap_count: int
    direct_discharge_source_count: int
    theorem_artifact_review_queue_dependency_check_count: int
    failed_theorem_artifact_review_queue_dependency_check_count: int
    theorem_artifact_review_queue_dependency_consistent: bool
    analytic_gap_stack_consistent: bool
    operator_stack_consistent: bool
    theorem_artifact_review_queue_operator_index_check_count: int
    passed_theorem_artifact_review_queue_operator_index_check_count: int
    failed_theorem_artifact_review_queue_operator_index_check_count: int
    theorem_artifact_review_queue_operator_index_consistent: bool
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    issues: tuple[str, ...]
    sections: tuple[TheoremArtifactReviewQueueOperatorSection, ...]
    checks: tuple[TheoremArtifactReviewQueueOperatorCheck, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]
    theorem_artifact_review_queue_snapshot: dict[str, object]
    theorem_artifact_review_queue_dependency_snapshot: dict[str, object]


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
) -> TheoremArtifactReviewQueueOperatorCheck:
    return TheoremArtifactReviewQueueOperatorCheck(
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
        "track-a-regularity/reports/lemma_0252_theorem_artifact_review_queue.md",
        "track-a-regularity/reports/lemma_0252_theorem_artifact_review_queue.json",
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_dependency.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_dependency.json"
        ),
    )


def _sections(
    queue: dict[str, object],
    dependency: dict[str, object],
) -> tuple[TheoremArtifactReviewQueueOperatorSection, ...]:
    return (
        TheoremArtifactReviewQueueOperatorSection(
            step=112,
            name="theorem_artifact_review_queue",
            role=(
                "Maps direct analytic gaps to local blocker literature and the missing "
                "theorem/formal artifacts needed for future review."
            ),
            markdown_report=str(DEFAULT_QUEUE_MARKDOWN),
            json_report=str(DEFAULT_QUEUE_JSON),
            status="blocked_theorem_artifact_review_queue",
            primary_count_label="queue_item_count",
            primary_count=int(queue.get("queue_item_count", 0)),
            blocked_count=int(queue.get("blocked_queue_item_count", 0)),
            actionable_count=int(queue.get("actionable_queue_item_count", 0))
            + int(queue.get("may_discharge_queue_item_count", 0))
            + int(queue.get("direct_theorem_artifact_count", 0)),
            consistent=bool(queue.get("analytic_gap_stack_consistent"))
            and bool(queue.get("operator_stack_consistent"))
            and not queue.get("issues"),
            missing_source_count=int(queue.get("missing_source_count", 0)),
        ),
        TheoremArtifactReviewQueueOperatorSection(
            step=113,
            name="theorem_artifact_review_queue_dependency",
            role=(
                "Keeps the theorem-artifact review queue synchronized with the analytic "
                "gap index, literature-gap stack, and local blocker-paper inventory."
            ),
            markdown_report=str(DEFAULT_QUEUE_DEPENDENCY_MARKDOWN),
            json_report=str(DEFAULT_QUEUE_DEPENDENCY_JSON),
            status="theorem_artifact_review_queue_dependency_guard",
            primary_count_label="theorem_artifact_review_queue_dependency_check_count",
            primary_count=int(
                dependency.get("theorem_artifact_review_queue_dependency_check_count", 0)
            ),
            blocked_count=int(dependency.get("blocked_queue_item_count", 0)),
            actionable_count=int(dependency.get("actionable_queue_item_count", 0))
            + int(dependency.get("may_discharge_queue_item_count", 0))
            + int(dependency.get("direct_theorem_artifact_count", 0)),
            consistent=bool(
                dependency.get("theorem_artifact_review_queue_dependency_consistent")
            ),
            missing_source_count=int(dependency.get("missing_source_count", 0)),
        ),
    )


def build_theorem_artifact_review_queue_operator_index(
    *,
    theorem_artifact_review_queue_json: Path = DEFAULT_QUEUE_JSON,
    theorem_artifact_review_queue_dependency_json: Path = DEFAULT_QUEUE_DEPENDENCY_JSON,
) -> Lemma0252TheoremArtifactReviewQueueOperatorIndex:
    queue = _load_json(theorem_artifact_review_queue_json)
    dependency = _load_json(theorem_artifact_review_queue_dependency_json)

    queue_source = (
        "track-a-regularity/reports/lemma_0252_theorem_artifact_review_queue.md",
        "track-a-regularity/reports/lemma_0252_theorem_artifact_review_queue.json",
    )
    dependency_source = (
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_dependency.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_dependency.json"
        ),
    )
    source_refs = tuple(
        dict.fromkeys(
            _direct_sources()
            + tuple(str(item) for item in queue.get("source_refs", ()))
            + tuple(str(item) for item in dependency.get("source_refs", ()))
        )
    )
    missing_sources = _missing_sources(source_refs)
    sections = _sections(queue, dependency)

    checks = (
        _check(
            key="queue.lemma_id.matches_dependency",
            expected=dependency.get("lemma_id"),
            observed=queue.get("lemma_id"),
            source_artifacts=queue_source + dependency_source,
        ),
        _check(
            key="queue.candidate_status.matches_dependency",
            expected=dependency.get("candidate_status"),
            observed=queue.get("candidate_status"),
            source_artifacts=queue_source + dependency_source,
        ),
        _check(
            key="queue.active_candidate.matches_dependency",
            expected=dependency.get("active_candidate"),
            observed=queue.get("active_candidate"),
            source_artifacts=queue_source + dependency_source,
        ),
        _check(
            key="queue.queue_item_count.matches_dependency",
            expected=dependency.get("queue_item_count"),
            observed=queue.get("queue_item_count"),
            source_artifacts=queue_source + dependency_source,
        ),
        _check(
            key="queue.direct_analytic_gap_count.matches_dependency",
            expected=dependency.get("direct_analytic_gap_count"),
            observed=queue.get("direct_analytic_gap_count"),
            source_artifacts=queue_source + dependency_source,
        ),
        _check(
            key="queue.blocked_queue_item_count.matches_dependency",
            expected=dependency.get("blocked_queue_item_count"),
            observed=queue.get("blocked_queue_item_count"),
            source_artifacts=queue_source + dependency_source,
        ),
        _check(
            key="queue.actionable_queue_item_count.remains_zero",
            expected=0,
            observed=queue.get("actionable_queue_item_count"),
            source_artifacts=queue_source,
        ),
        _check(
            key="dependency.actionable_queue_item_count.remains_zero",
            expected=0,
            observed=dependency.get("actionable_queue_item_count"),
            source_artifacts=dependency_source,
        ),
        _check(
            key="queue.may_discharge_queue_item_count.remains_zero",
            expected=0,
            observed=queue.get("may_discharge_queue_item_count"),
            source_artifacts=queue_source,
        ),
        _check(
            key="dependency.may_discharge_queue_item_count.remains_zero",
            expected=0,
            observed=dependency.get("may_discharge_queue_item_count"),
            source_artifacts=dependency_source,
        ),
        _check(
            key="queue.direct_theorem_artifact_count.remains_zero",
            expected=0,
            observed=queue.get("direct_theorem_artifact_count"),
            source_artifacts=queue_source,
        ),
        _check(
            key="dependency.direct_theorem_artifact_count.remains_zero",
            expected=0,
            observed=dependency.get("direct_theorem_artifact_count"),
            source_artifacts=dependency_source,
        ),
        _check(
            key="queue.queue_source_edge_count.matches_dependency",
            expected=dependency.get("queue_source_edge_count"),
            observed=queue.get("queue_source_edge_count"),
            source_artifacts=queue_source + dependency_source,
        ),
        _check(
            key="queue.direct_branch_source_edge_count.matches_dependency",
            expected=dependency.get("direct_branch_source_edge_count"),
            observed=queue.get("direct_branch_source_edge_count"),
            source_artifacts=queue_source + dependency_source,
        ),
        _check(
            key="queue.cross_cutting_source_edge_count.matches_dependency",
            expected=dependency.get("cross_cutting_source_edge_count"),
            observed=queue.get("cross_cutting_source_edge_count"),
            source_artifacts=queue_source + dependency_source,
        ),
        _check(
            key="queue.unique_literature_source_count.matches_dependency",
            expected=dependency.get("unique_literature_source_count"),
            observed=queue.get("unique_literature_source_count"),
            source_artifacts=queue_source + dependency_source,
        ),
        _check(
            key="queue.literature_source_count.matches_dependency",
            expected=dependency.get("literature_source_count"),
            observed=queue.get("literature_source_count"),
            source_artifacts=queue_source + dependency_source,
        ),
        _check(
            key="queue.gap_count.matches_dependency",
            expected=dependency.get("gap_count"),
            observed=queue.get("gap_count"),
            source_artifacts=queue_source + dependency_source,
        ),
        _check(
            key="queue.source_gap_edge_count.matches_dependency",
            expected=dependency.get("source_gap_edge_count"),
            observed=queue.get("source_gap_edge_count"),
            source_artifacts=queue_source + dependency_source,
        ),
        _check(
            key="queue.blocked_gap_count.matches_dependency",
            expected=dependency.get("blocked_gap_count"),
            observed=queue.get("blocked_gap_count"),
            source_artifacts=queue_source + dependency_source,
        ),
        _check(
            key="queue.actionable_gap_count.remains_zero",
            expected=0,
            observed=queue.get("actionable_gap_count"),
            source_artifacts=queue_source,
        ),
        _check(
            key="dependency.actionable_gap_count.remains_zero",
            expected=0,
            observed=dependency.get("actionable_gap_count"),
            source_artifacts=dependency_source,
        ),
        _check(
            key="queue.may_discharge_gap_count.remains_zero",
            expected=0,
            observed=queue.get("may_discharge_gap_count"),
            source_artifacts=queue_source,
        ),
        _check(
            key="dependency.may_discharge_gap_count.remains_zero",
            expected=0,
            observed=dependency.get("may_discharge_gap_count"),
            source_artifacts=dependency_source,
        ),
        _check(
            key="queue.direct_discharge_source_count.remains_zero",
            expected=0,
            observed=queue.get("direct_discharge_source_count"),
            source_artifacts=queue_source,
        ),
        _check(
            key="dependency.direct_discharge_source_count.remains_zero",
            expected=0,
            observed=dependency.get("direct_discharge_source_count"),
            source_artifacts=dependency_source,
        ),
        _check(
            key="dependency.check_count.expected_seventy",
            expected=70,
            observed=dependency.get("theorem_artifact_review_queue_dependency_check_count"),
            source_artifacts=dependency_source,
        ),
        _check(
            key="dependency.failed_checks.remains_zero",
            expected=0,
            observed=dependency.get(
                "failed_theorem_artifact_review_queue_dependency_check_count"
            ),
            source_artifacts=dependency_source,
        ),
        _check(
            key="dependency.consistent.true",
            expected=True,
            observed=dependency.get("theorem_artifact_review_queue_dependency_consistent"),
            source_artifacts=dependency_source,
        ),
        _check(
            key="queue.analytic_gap_stack_consistent.true",
            expected=True,
            observed=queue.get("analytic_gap_stack_consistent"),
            source_artifacts=queue_source,
        ),
        _check(
            key="queue.operator_stack_consistent.true",
            expected=True,
            observed=queue.get("operator_stack_consistent"),
            source_artifacts=queue_source,
        ),
        _check(
            key="dependency.analytic_gap_stack_consistent.true",
            expected=True,
            observed=dependency.get("analytic_gap_stack_consistent"),
            source_artifacts=dependency_source,
        ),
        _check(
            key="dependency.operator_stack_consistent.true",
            expected=True,
            observed=dependency.get("operator_stack_consistent"),
            source_artifacts=dependency_source,
        ),
        _check(
            key="source_reports.issues.all_empty",
            expected=((), ()),
            observed=(tuple(queue.get("issues", ())), tuple(dependency.get("issues", ()))),
            source_artifacts=queue_source + dependency_source,
        ),
        _check(
            key="source_report_count.matches_sections_times_two",
            expected=len(sections) * 2,
            observed=len(_direct_sources()),
            source_artifacts=queue_source + dependency_source,
        ),
        _check(
            key="all.process_gate_open_authorized.false",
            expected=(False, False),
            observed=(
                queue.get("process_gate_open_authorized"),
                dependency.get("process_gate_open_authorized"),
            ),
            source_artifacts=queue_source + dependency_source,
        ),
        _check(
            key="all.blocker_state_changed.false",
            expected=(False, False),
            observed=(queue.get("blocker_state_changed"), dependency.get("blocker_state_changed")),
            source_artifacts=queue_source + dependency_source,
        ),
        _check(
            key="all.candidate_emission_authorized.false",
            expected=(False, False),
            observed=(
                queue.get("candidate_emission_authorized"),
                dependency.get("candidate_emission_authorized"),
            ),
            source_artifacts=queue_source + dependency_source,
        ),
        _check(
            key="candidate_status.remains_needs_review",
            expected="needs_review",
            observed=queue.get("candidate_status"),
            source_artifacts=queue_source,
        ),
        _check(
            key="active_candidate.remains_false",
            expected=False,
            observed=queue.get("active_candidate"),
            source_artifacts=queue_source,
        ),
        _check(
            key="source_refs.missing_count.remains_zero",
            expected=0,
            observed=len(missing_sources),
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.include_theorem_artifact_queue_reports",
            expected=queue_source,
            observed=tuple(source for source in queue_source if source in source_refs),
            source_artifacts=queue_source,
        ),
        _check(
            key="source_refs.include_theorem_artifact_queue_dependency_reports",
            expected=dependency_source,
            observed=tuple(source for source in dependency_source if source in source_refs),
            source_artifacts=dependency_source,
        ),
        _check(
            key="source_refs.include_papers_blockers_index",
            expected=True,
            observed="papers/blockers/index.md" in source_refs,
            source_artifacts=("papers/blockers/index.md",),
        ),
    )
    issues = tuple(check.key for check in checks if not check.passed)

    reports = (queue, dependency)
    process_gate_open_authorized = any(
        bool(report.get("process_gate_open_authorized")) for report in reports
    )
    blocker_state_changed = any(bool(report.get("blocker_state_changed")) for report in reports)
    candidate_emission_authorized = any(
        bool(report.get("candidate_emission_authorized")) for report in reports
    )

    return Lemma0252TheoremArtifactReviewQueueOperatorIndex(
        schema_version=1,
        lemma_id=str(queue.get("lemma_id")),
        candidate_status=str(queue.get("candidate_status")),
        active_candidate=bool(queue.get("active_candidate")),
        section_count=len(sections),
        source_report_count=len(_direct_sources()),
        source_ref_count=len(source_refs),
        queue_item_count=int(queue.get("queue_item_count", 0)),
        direct_analytic_gap_count=int(queue.get("direct_analytic_gap_count", 0)),
        blocked_queue_item_count=int(queue.get("blocked_queue_item_count", 0)),
        actionable_queue_item_count=int(queue.get("actionable_queue_item_count", 0)),
        may_discharge_queue_item_count=int(queue.get("may_discharge_queue_item_count", 0)),
        direct_theorem_artifact_count=int(queue.get("direct_theorem_artifact_count", 0)),
        queue_source_edge_count=int(queue.get("queue_source_edge_count", 0)),
        direct_branch_source_edge_count=int(queue.get("direct_branch_source_edge_count", 0)),
        cross_cutting_source_edge_count=int(queue.get("cross_cutting_source_edge_count", 0)),
        unique_literature_source_count=int(queue.get("unique_literature_source_count", 0)),
        literature_source_count=int(queue.get("literature_source_count", 0)),
        gap_count=int(queue.get("gap_count", 0)),
        source_gap_edge_count=int(queue.get("source_gap_edge_count", 0)),
        blocked_gap_count=int(queue.get("blocked_gap_count", 0)),
        actionable_gap_count=int(queue.get("actionable_gap_count", 0)),
        may_discharge_gap_count=int(queue.get("may_discharge_gap_count", 0)),
        direct_discharge_source_count=int(queue.get("direct_discharge_source_count", 0)),
        theorem_artifact_review_queue_dependency_check_count=int(
            dependency.get("theorem_artifact_review_queue_dependency_check_count", 0)
        ),
        failed_theorem_artifact_review_queue_dependency_check_count=int(
            dependency.get("failed_theorem_artifact_review_queue_dependency_check_count", 0)
        ),
        theorem_artifact_review_queue_dependency_consistent=bool(
            dependency.get("theorem_artifact_review_queue_dependency_consistent")
        ),
        analytic_gap_stack_consistent=bool(queue.get("analytic_gap_stack_consistent"))
        and bool(dependency.get("analytic_gap_stack_consistent")),
        operator_stack_consistent=bool(queue.get("operator_stack_consistent"))
        and bool(dependency.get("operator_stack_consistent")),
        theorem_artifact_review_queue_operator_index_check_count=len(checks),
        passed_theorem_artifact_review_queue_operator_index_check_count=(
            len(checks) - len(issues)
        ),
        failed_theorem_artifact_review_queue_operator_index_check_count=len(issues),
        theorem_artifact_review_queue_operator_index_consistent=not issues
        and not missing_sources,
        process_gate_open_authorized=process_gate_open_authorized,
        blocker_state_changed=blocker_state_changed,
        candidate_emission_authorized=candidate_emission_authorized,
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        issues=issues,
        sections=sections,
        checks=checks,
        source_refs=source_refs,
        non_claims=NON_CLAIMS,
        theorem_artifact_review_queue_snapshot=queue,
        theorem_artifact_review_queue_dependency_snapshot=dependency,
    )


def theorem_artifact_review_queue_operator_index_to_dict(
    report: Lemma0252TheoremArtifactReviewQueueOperatorIndex,
) -> dict[str, object]:
    return {
        "schema_version": report.schema_version,
        "lemma_id": report.lemma_id,
        "candidate_status": report.candidate_status,
        "active_candidate": report.active_candidate,
        "section_count": report.section_count,
        "source_report_count": report.source_report_count,
        "source_ref_count": report.source_ref_count,
        "queue_item_count": report.queue_item_count,
        "direct_analytic_gap_count": report.direct_analytic_gap_count,
        "blocked_queue_item_count": report.blocked_queue_item_count,
        "actionable_queue_item_count": report.actionable_queue_item_count,
        "may_discharge_queue_item_count": report.may_discharge_queue_item_count,
        "direct_theorem_artifact_count": report.direct_theorem_artifact_count,
        "queue_source_edge_count": report.queue_source_edge_count,
        "direct_branch_source_edge_count": report.direct_branch_source_edge_count,
        "cross_cutting_source_edge_count": report.cross_cutting_source_edge_count,
        "unique_literature_source_count": report.unique_literature_source_count,
        "literature_source_count": report.literature_source_count,
        "gap_count": report.gap_count,
        "source_gap_edge_count": report.source_gap_edge_count,
        "blocked_gap_count": report.blocked_gap_count,
        "actionable_gap_count": report.actionable_gap_count,
        "may_discharge_gap_count": report.may_discharge_gap_count,
        "direct_discharge_source_count": report.direct_discharge_source_count,
        "theorem_artifact_review_queue_dependency_check_count": (
            report.theorem_artifact_review_queue_dependency_check_count
        ),
        "failed_theorem_artifact_review_queue_dependency_check_count": (
            report.failed_theorem_artifact_review_queue_dependency_check_count
        ),
        "theorem_artifact_review_queue_dependency_consistent": (
            report.theorem_artifact_review_queue_dependency_consistent
        ),
        "analytic_gap_stack_consistent": report.analytic_gap_stack_consistent,
        "operator_stack_consistent": report.operator_stack_consistent,
        "theorem_artifact_review_queue_operator_index_check_count": (
            report.theorem_artifact_review_queue_operator_index_check_count
        ),
        "passed_theorem_artifact_review_queue_operator_index_check_count": (
            report.passed_theorem_artifact_review_queue_operator_index_check_count
        ),
        "failed_theorem_artifact_review_queue_operator_index_check_count": (
            report.failed_theorem_artifact_review_queue_operator_index_check_count
        ),
        "theorem_artifact_review_queue_operator_index_consistent": (
            report.theorem_artifact_review_queue_operator_index_consistent
        ),
        "process_gate_open_authorized": report.process_gate_open_authorized,
        "blocker_state_changed": report.blocker_state_changed,
        "candidate_emission_authorized": report.candidate_emission_authorized,
        "missing_source_count": report.missing_source_count,
        "missing_sources": list(report.missing_sources),
        "issues": list(report.issues),
        "sections": [asdict(section) for section in report.sections],
        "checks": [asdict(check) for check in report.checks],
        "source_refs": list(report.source_refs),
        "non_claims": list(report.non_claims),
        "theorem_artifact_review_queue_snapshot": (
            report.theorem_artifact_review_queue_snapshot
        ),
        "theorem_artifact_review_queue_dependency_snapshot": (
            report.theorem_artifact_review_queue_dependency_snapshot
        ),
        "docs": {
            "step_doc": (
                "docs/STEP114_LEMMA_0252_THEOREM_ARTIFACT_REVIEW_QUEUE_OPERATOR_INDEX.md"
            ),
            "theorem_artifact_review_queue_doc": (
                "docs/STEP112_LEMMA_0252_THEOREM_ARTIFACT_REVIEW_QUEUE.md"
            ),
            "theorem_artifact_review_queue_dependency_doc": (
                "docs/STEP113_LEMMA_0252_THEOREM_ARTIFACT_REVIEW_QUEUE_DEPENDENCY.md"
            ),
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _section_rows(
    report: Lemma0252TheoremArtifactReviewQueueOperatorIndex,
) -> list[str]:
    rows = [
        "| step | section | status | primary | blocked | actionable | consistent | sources |",
        "|---:|---|---|---:|---:|---:|---|---|",
    ]
    for section in report.sections:
        sources = "<br>".join(
            (f"`{section.markdown_report}`", f"`{section.json_report}`")
        )
        rows.append(
            "| "
            f"{section.step} | "
            f"`{section.name}` | "
            f"`{section.status}` | "
            f"{section.primary_count} `{section.primary_count_label}` | "
            f"{section.blocked_count} | "
            f"{section.actionable_count} | "
            f"`{str(section.consistent).lower()}` | "
            f"{sources} |"
        )
    return rows


def _check_rows(
    report: Lemma0252TheoremArtifactReviewQueueOperatorIndex,
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
    report: Lemma0252TheoremArtifactReviewQueueOperatorIndex,
) -> str:
    return "\n".join(
        (
            "# Lemma 0252 Theorem Artifact Review Queue Operator Index",
            "",
            "Generated by `track-a-regularity/evaluator/"
            "lemma_0252_theorem_artifact_review_queue_operator_index.py`.",
            "",
            "This compact read-only operator/source index consolidates the Step 112",
            "theorem-artifact review queue and the Step 113 queue-dependency guard.",
            "It is an inspection surface only; it does not discharge blockers or",
            "authorize process gates.",
            "",
            "## Summary",
            "",
            f"- lemma_id: `{report.lemma_id}`",
            f"- candidate_status: `{report.candidate_status}`",
            f"- active_candidate: `{str(report.active_candidate).lower()}`",
            f"- section_count: `{report.section_count}`",
            f"- source_report_count: `{report.source_report_count}`",
            f"- source_ref_count: `{report.source_ref_count}`",
            f"- queue_item_count: `{report.queue_item_count}`",
            f"- direct_analytic_gap_count: `{report.direct_analytic_gap_count}`",
            f"- blocked_queue_item_count: `{report.blocked_queue_item_count}`",
            f"- actionable_queue_item_count: `{report.actionable_queue_item_count}`",
            f"- may_discharge_queue_item_count: `{report.may_discharge_queue_item_count}`",
            f"- direct_theorem_artifact_count: `{report.direct_theorem_artifact_count}`",
            f"- queue_source_edge_count: `{report.queue_source_edge_count}`",
            f"- direct_branch_source_edge_count: `{report.direct_branch_source_edge_count}`",
            f"- cross_cutting_source_edge_count: `{report.cross_cutting_source_edge_count}`",
            f"- unique_literature_source_count: `{report.unique_literature_source_count}`",
            f"- literature_source_count: `{report.literature_source_count}`",
            f"- gap_count: `{report.gap_count}`",
            f"- source_gap_edge_count: `{report.source_gap_edge_count}`",
            f"- blocked_gap_count: `{report.blocked_gap_count}`",
            f"- actionable_gap_count: `{report.actionable_gap_count}`",
            f"- may_discharge_gap_count: `{report.may_discharge_gap_count}`",
            f"- direct_discharge_source_count: `{report.direct_discharge_source_count}`",
            (
                "- theorem_artifact_review_queue_dependency_check_count: "
                f"`{report.theorem_artifact_review_queue_dependency_check_count}`"
            ),
            (
                "- failed_theorem_artifact_review_queue_dependency_check_count: "
                f"`{report.failed_theorem_artifact_review_queue_dependency_check_count}`"
            ),
            (
                "- theorem_artifact_review_queue_dependency_consistent: "
                f"`{str(report.theorem_artifact_review_queue_dependency_consistent).lower()}`"
            ),
            f"- analytic_gap_stack_consistent: `{str(report.analytic_gap_stack_consistent).lower()}`",
            f"- operator_stack_consistent: `{str(report.operator_stack_consistent).lower()}`",
            (
                "- theorem_artifact_review_queue_operator_index_check_count: "
                f"`{report.theorem_artifact_review_queue_operator_index_check_count}`"
            ),
            (
                "- passed_theorem_artifact_review_queue_operator_index_check_count: "
                f"`{report.passed_theorem_artifact_review_queue_operator_index_check_count}`"
            ),
            (
                "- failed_theorem_artifact_review_queue_operator_index_check_count: "
                f"`{report.failed_theorem_artifact_review_queue_operator_index_check_count}`"
            ),
            (
                "- theorem_artifact_review_queue_operator_index_consistent: "
                f"`{str(report.theorem_artifact_review_queue_operator_index_consistent).lower()}`"
            ),
            f"- process_gate_open_authorized: `{str(report.process_gate_open_authorized).lower()}`",
            f"- blocker_state_changed: `{str(report.blocker_state_changed).lower()}`",
            f"- candidate_emission_authorized: `{str(report.candidate_emission_authorized).lower()}`",
            f"- missing_source_count: `{report.missing_source_count}`",
            f"- issues: `{', '.join(report.issues) or 'none'}`",
            "",
            "## Sections",
            "",
            *_section_rows(report),
            "",
            "## Operator Checks",
            "",
            *_check_rows(report),
            "",
            "## Non-Claims",
            "",
            *(f"- `{item}`" for item in report.non_claims),
            "",
        )
    )


def render_json(report: Lemma0252TheoremArtifactReviewQueueOperatorIndex) -> str:
    return json.dumps(
        theorem_artifact_review_queue_operator_index_to_dict(report),
        indent=2,
        sort_keys=True,
    ) + "\n"


def render_output(
    report: Lemma0252TheoremArtifactReviewQueueOperatorIndex,
    output_format: str,
) -> str:
    if output_format == "markdown":
        return render_markdown(report)
    if output_format == "json":
        return render_json(report)
    raise ValueError(
        f"unknown theorem artifact review queue operator index format: {output_format}"
    )


def write_output(
    output: Path,
    report: Lemma0252TheoremArtifactReviewQueueOperatorIndex,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(report, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    report: Lemma0252TheoremArtifactReviewQueueOperatorIndex,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(report, output_format)
    if not output.exists():
        return False, f"missing lemma_0252 theorem artifact review queue operator index: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale lemma_0252 theorem artifact review queue operator index: {output}"
    return True, f"fresh lemma_0252 theorem artifact review queue operator index: {output}"


def check_consistent(
    report: Lemma0252TheoremArtifactReviewQueueOperatorIndex,
) -> tuple[bool, str]:
    if not report.theorem_artifact_review_queue_operator_index_consistent:
        return (
            False,
            "lemma_0252 theorem artifact review queue operator index inconsistent: "
            + ", ".join(report.issues),
        )
    return True, "lemma_0252 theorem artifact review queue operator index is consistent"


def check_sources(
    report: Lemma0252TheoremArtifactReviewQueueOperatorIndex,
) -> tuple[bool, str]:
    if report.missing_source_count:
        return (
            False,
            "missing lemma_0252 theorem artifact review queue operator index sources: "
            + ", ".join(report.missing_sources),
        )
    return True, "all lemma_0252 theorem artifact review queue operator index sources exist"


def check_blocked(
    report: Lemma0252TheoremArtifactReviewQueueOperatorIndex,
) -> tuple[bool, str]:
    if report.process_gate_open_authorized:
        return False, "process gate open became authorized"
    if report.blocker_state_changed:
        return False, "theorem artifact review queue operator index changed blocker state"
    if report.candidate_emission_authorized:
        return False, "theorem artifact review queue operator index authorized candidate emission"
    if report.actionable_queue_item_count:
        return False, "theorem artifact review queue operator index found actionable queue items"
    if report.may_discharge_queue_item_count:
        return False, "theorem artifact review queue operator index found discharge-capable items"
    if report.direct_theorem_artifact_count:
        return False, "theorem artifact review queue operator index found direct theorem artifacts"
    if report.actionable_gap_count:
        return False, "theorem artifact review queue operator index found actionable gaps"
    if report.may_discharge_gap_count:
        return False, "theorem artifact review queue operator index found discharge-capable gaps"
    if report.direct_discharge_source_count:
        return False, "theorem artifact review queue operator index found direct discharge sources"
    if report.blocked_queue_item_count != report.queue_item_count:
        return False, "not all theorem artifact review queue items remain blocked"
    if report.blocked_gap_count != report.gap_count:
        return False, "not all upstream analytic-discharge gaps remain blocked"
    return True, "lemma_0252 theorem artifact review queue operator index keeps items blocked"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(
        f"unknown theorem artifact review queue operator index format: {output_format}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Summarize Step 112-113 lemma_0252 theorem-artifact queue artifacts."
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-consistent", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    args = parser.parse_args(argv)

    try:
        report = build_theorem_artifact_review_queue_operator_index()
    except Exception as exc:  # noqa: BLE001 - CLI should report setup failures.
        print(
            f"failed to build lemma_0252 theorem artifact review queue operator index: {exc}",
            file=sys.stderr,
        )
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, report, args.format)
        print(message)
        if not ok:
            print(
                "run without --check-output to regenerate the theorem artifact review queue operator index",
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
        "theorem_artifact_review_queue_operator_index_check_count: "
        f"{report.theorem_artifact_review_queue_operator_index_check_count}"
    )
    print(
        "passed_theorem_artifact_review_queue_operator_index_check_count: "
        f"{report.passed_theorem_artifact_review_queue_operator_index_check_count}"
    )
    print(
        "failed_theorem_artifact_review_queue_operator_index_check_count: "
        f"{report.failed_theorem_artifact_review_queue_operator_index_check_count}"
    )
    print(
        "theorem_artifact_review_queue_operator_index_consistent: "
        f"{str(report.theorem_artifact_review_queue_operator_index_consistent).lower()}"
    )
    print(
        "process_gate_open_authorized: "
        f"{str(report.process_gate_open_authorized).lower()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
