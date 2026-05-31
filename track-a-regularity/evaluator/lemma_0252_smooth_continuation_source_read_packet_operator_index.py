from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from lemma_0252_smooth_continuation_source_read_packet import (
    DEFAULT_JSON_OUTPUT as DEFAULT_PACKET_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_PACKET_MARKDOWN,
)
from lemma_0252_smooth_continuation_source_read_packet_dependency import (
    DEFAULT_JSON_OUTPUT as DEFAULT_DEPENDENCY_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_DEPENDENCY_MARKDOWN,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_smooth_continuation_source_read_packet_operator_index.md"
)
DEFAULT_JSON_OUTPUT = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_smooth_continuation_source_read_packet_operator_index.json"
)

GAP_ID = "gap_004"
SOURCE_BRANCH = "smooth_continuation_bridge"
PACKET_STATUS = "blocked_source_read_only"
PACKET_BRANCH_VERDICT = "blocked_needs_new_result"

NON_CLAIMS = (
    "read_only_smooth_continuation_source_read_packet_operator_index",
    "source_index_for_review_only",
    "non_promotional_gap_004_operator_surface",
    "no_candidate_promotion",
    "no_candidate_emission",
    "no_blocker_discharge",
    "no_process_gate_opened",
    "no_file_copy",
    "no_bkm_theorem",
    "no_serrin_theorem",
    "no_high_sobolev_continuation_bridge",
    "no_weak_to_smooth_upgrade",
    "no_navier_stokes_solution",
)


@dataclass(frozen=True)
class SmoothContinuationSourceReadOperatorSection:
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
class SmoothContinuationSourceReadOperatorCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class Lemma0252SmoothContinuationSourceReadOperatorIndex:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    gap_id: str
    source_branch: str
    section_count: int
    source_report_count: int
    source_ref_count: int
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
    smooth_continuation_source_read_packet_dependency_check_count: int
    failed_smooth_continuation_source_read_packet_dependency_check_count: int
    smooth_continuation_source_read_packet_dependency_consistent: bool
    smooth_continuation_source_read_packet_operator_index_check_count: int
    passed_smooth_continuation_source_read_packet_operator_index_check_count: int
    failed_smooth_continuation_source_read_packet_operator_index_check_count: int
    smooth_continuation_source_read_packet_operator_index_consistent: bool
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    issues: tuple[str, ...]
    sections: tuple[SmoothContinuationSourceReadOperatorSection, ...]
    checks: tuple[SmoothContinuationSourceReadOperatorCheck, ...]
    source_refs: tuple[str, ...]
    source_read_ids: tuple[str, ...]
    source_paths: tuple[str, ...]
    non_claims: tuple[str, ...]
    packet_snapshot: dict[str, object]
    dependency_snapshot: dict[str, object]


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
) -> SmoothContinuationSourceReadOperatorCheck:
    return SmoothContinuationSourceReadOperatorCheck(
        key=key,
        expected=str(expected),
        observed=str(observed),
        passed=expected == observed,
        source_artifacts=source_artifacts,
    )


def _missing_sources(source_refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(source for source in source_refs if not (ROOT / source).exists())


def _direct_source_reports() -> tuple[str, ...]:
    return (
        "track-a-regularity/reports/lemma_0252_smooth_continuation_source_read_packet.md",
        "track-a-regularity/reports/lemma_0252_smooth_continuation_source_read_packet.json",
        (
            "track-a-regularity/reports/"
            "lemma_0252_smooth_continuation_source_read_packet_dependency.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_smooth_continuation_source_read_packet_dependency.json"
        ),
    )


def _source_ids_from_packet(packet: dict[str, object]) -> tuple[str, ...]:
    return tuple(
        str(item.get("source_id"))
        for item in packet.get("source_reads", ())
        if isinstance(item, dict)
    )


def _source_paths_from_packet(packet: dict[str, object]) -> tuple[str, ...]:
    return tuple(
        str(item.get("relative_path"))
        for item in packet.get("source_reads", ())
        if isinstance(item, dict)
    )


def _sections(
    packet: dict[str, object],
    dependency: dict[str, object],
) -> tuple[SmoothContinuationSourceReadOperatorSection, ...]:
    return (
        SmoothContinuationSourceReadOperatorSection(
            step=120,
            name="smooth_continuation_source_read_packet",
            role=(
                "Extracts hypothesis, conclusion, and mismatch fields from the local "
                "smooth-continuation sources attached to gap_004."
            ),
            markdown_report=str(DEFAULT_PACKET_MARKDOWN),
            json_report=str(DEFAULT_PACKET_JSON),
            status=str(packet.get("packet_status")),
            primary_count_label="source_read_count",
            primary_count=int(packet.get("source_read_count", 0)),
            blocked_count=int(packet.get("blocked_source_read_count", 0)),
            actionable_count=int(packet.get("actionable_source_read_count", 0))
            + int(packet.get("may_discharge_source_read_count", 0))
            + int(packet.get("exact_discharge_artifact_count", 0)),
            consistent=bool(packet.get("packet_consistent")),
            missing_source_count=int(packet.get("missing_source_count", 0)),
        ),
        SmoothContinuationSourceReadOperatorSection(
            step=121,
            name="smooth_continuation_source_read_packet_dependency",
            role=(
                "Keeps the smooth-continuation source-read packet synchronized with "
                "the Step 90 checklist, Step 112-115 theorem-artifact queue stack, "
                "and local blocker-paper inventory."
            ),
            markdown_report=str(DEFAULT_DEPENDENCY_MARKDOWN),
            json_report=str(DEFAULT_DEPENDENCY_JSON),
            status="smooth_continuation_source_read_packet_dependency_guard",
            primary_count_label=(
                "smooth_continuation_source_read_packet_dependency_check_count"
            ),
            primary_count=int(
                dependency.get(
                    "smooth_continuation_source_read_packet_dependency_check_count",
                    0,
                )
            ),
            blocked_count=int(dependency.get("source_read_count", 0)),
            actionable_count=int(dependency.get("actionable_source_read_count", 0))
            + int(dependency.get("may_discharge_source_read_count", 0))
            + int(dependency.get("exact_discharge_artifact_count", 0)),
            consistent=bool(
                dependency.get(
                    "smooth_continuation_source_read_packet_dependency_consistent"
                )
            ),
            missing_source_count=int(dependency.get("missing_source_count", 0)),
        ),
    )


def build_smooth_continuation_source_read_packet_operator_index(
    *,
    packet_json: Path = DEFAULT_PACKET_JSON,
    dependency_json: Path = DEFAULT_DEPENDENCY_JSON,
) -> Lemma0252SmoothContinuationSourceReadOperatorIndex:
    packet = _load_json(packet_json)
    dependency = _load_json(dependency_json)

    packet_source = (
        "track-a-regularity/reports/lemma_0252_smooth_continuation_source_read_packet.md",
        "track-a-regularity/reports/lemma_0252_smooth_continuation_source_read_packet.json",
    )
    dependency_source = (
        (
            "track-a-regularity/reports/"
            "lemma_0252_smooth_continuation_source_read_packet_dependency.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_smooth_continuation_source_read_packet_dependency.json"
        ),
    )
    source_ids = _source_ids_from_packet(packet)
    source_paths = _source_paths_from_packet(packet)
    source_refs = tuple(
        dict.fromkeys(
            _direct_source_reports()
            + source_paths
            + tuple(str(item) for item in packet.get("source_refs", ()))
            + tuple(str(item) for item in dependency.get("source_refs", ()))
        )
    )
    missing_sources = _missing_sources(source_refs)
    sections = _sections(packet, dependency)

    checks = (
        _check(
            key="packet.lemma_id.matches_dependency",
            expected=dependency.get("lemma_id"),
            observed=packet.get("lemma_id"),
            source_artifacts=packet_source + dependency_source,
        ),
        _check(
            key="packet.candidate_status.matches_dependency",
            expected=dependency.get("candidate_status"),
            observed=packet.get("candidate_status"),
            source_artifacts=packet_source + dependency_source,
        ),
        _check(
            key="packet.active_candidate.matches_dependency",
            expected=dependency.get("active_candidate"),
            observed=packet.get("active_candidate"),
            source_artifacts=packet_source + dependency_source,
        ),
        _check(
            key="packet.gap_id.matches_dependency",
            expected=dependency.get("gap_id"),
            observed=packet.get("gap_id"),
            source_artifacts=packet_source + dependency_source,
        ),
        _check(
            key="packet.source_branch.matches_dependency",
            expected=dependency.get("source_branch"),
            observed=packet.get("source_branch"),
            source_artifacts=packet_source + dependency_source,
        ),
        _check(
            key="packet.gap_id.expected_gap_004",
            expected=GAP_ID,
            observed=packet.get("gap_id"),
            source_artifacts=packet_source,
        ),
        _check(
            key="packet.source_branch.expected_smooth_continuation_bridge",
            expected=SOURCE_BRANCH,
            observed=packet.get("source_branch"),
            source_artifacts=packet_source,
        ),
        _check(
            key="packet.packet_status.remains_blocked",
            expected=PACKET_STATUS,
            observed=packet.get("packet_status"),
            source_artifacts=packet_source,
        ),
        _check(
            key="packet.branch_verdict.remains_blocked_needs_new_result",
            expected=PACKET_BRANCH_VERDICT,
            observed=packet.get("branch_verdict"),
            source_artifacts=packet_source,
        ),
        _check(
            key="packet.source_read_count.matches_dependency",
            expected=dependency.get("source_read_count"),
            observed=packet.get("source_read_count"),
            source_artifacts=packet_source + dependency_source,
        ),
        _check(
            key="packet.direct_branch_source_read_count.matches_dependency",
            expected=dependency.get("direct_branch_source_read_count"),
            observed=packet.get("direct_branch_source_read_count"),
            source_artifacts=packet_source + dependency_source,
        ),
        _check(
            key="packet.cross_cutting_source_read_count.matches_dependency",
            expected=dependency.get("cross_cutting_source_read_count"),
            observed=packet.get("cross_cutting_source_read_count"),
            source_artifacts=packet_source + dependency_source,
        ),
        _check(
            key="packet.source_ids.match_dependency",
            expected=tuple(dependency.get("source_read_ids", ())),
            observed=source_ids,
            source_artifacts=packet_source + dependency_source,
        ),
        _check(
            key="packet.packet_check_count.expected_thirty_four",
            expected=34,
            observed=packet.get("packet_check_count"),
            source_artifacts=packet_source,
        ),
        _check(
            key="packet.failed_packet_check_count.remains_zero",
            expected=0,
            observed=packet.get("failed_packet_check_count"),
            source_artifacts=packet_source,
        ),
        _check(
            key="packet.packet_consistent.true",
            expected=True,
            observed=packet.get("packet_consistent"),
            source_artifacts=packet_source,
        ),
        _check(
            key="dependency.check_count.expected_fifty",
            expected=50,
            observed=dependency.get(
                "smooth_continuation_source_read_packet_dependency_check_count"
            ),
            source_artifacts=dependency_source,
        ),
        _check(
            key="dependency.failed_checks.remains_zero",
            expected=0,
            observed=dependency.get(
                "failed_smooth_continuation_source_read_packet_dependency_check_count"
            ),
            source_artifacts=dependency_source,
        ),
        _check(
            key="dependency.consistent.true",
            expected=True,
            observed=dependency.get(
                "smooth_continuation_source_read_packet_dependency_consistent"
            ),
            source_artifacts=dependency_source,
        ),
        _check(
            key="packet.exact_discharge_artifact_count.remains_zero",
            expected=0,
            observed=packet.get("exact_discharge_artifact_count"),
            source_artifacts=packet_source,
        ),
        _check(
            key="dependency.exact_discharge_artifact_count.remains_zero",
            expected=0,
            observed=dependency.get("exact_discharge_artifact_count"),
            source_artifacts=dependency_source,
        ),
        _check(
            key="packet.actionable_source_read_count.remains_zero",
            expected=0,
            observed=packet.get("actionable_source_read_count"),
            source_artifacts=packet_source,
        ),
        _check(
            key="dependency.actionable_source_read_count.remains_zero",
            expected=0,
            observed=dependency.get("actionable_source_read_count"),
            source_artifacts=dependency_source,
        ),
        _check(
            key="packet.may_discharge_source_read_count.remains_zero",
            expected=0,
            observed=packet.get("may_discharge_source_read_count"),
            source_artifacts=packet_source,
        ),
        _check(
            key="dependency.may_discharge_source_read_count.remains_zero",
            expected=0,
            observed=dependency.get("may_discharge_source_read_count"),
            source_artifacts=dependency_source,
        ),
        _check(
            key="source_report_count.matches_sections_times_two",
            expected=len(sections) * 2,
            observed=len(_direct_source_reports()),
            source_artifacts=packet_source + dependency_source,
        ),
        _check(
            key="all.process_gate_open_authorized.false",
            expected=(False, False),
            observed=(
                packet.get("process_gate_open_authorized"),
                dependency.get("process_gate_open_authorized"),
            ),
            source_artifacts=packet_source + dependency_source,
        ),
        _check(
            key="all.blocker_state_changed.false",
            expected=(False, False),
            observed=(
                packet.get("blocker_state_changed"),
                dependency.get("blocker_state_changed"),
            ),
            source_artifacts=packet_source + dependency_source,
        ),
        _check(
            key="all.candidate_emission_authorized.false",
            expected=(False, False),
            observed=(
                packet.get("candidate_emission_authorized"),
                dependency.get("candidate_emission_authorized"),
            ),
            source_artifacts=packet_source + dependency_source,
        ),
        _check(
            key="candidate_status.remains_needs_review",
            expected="needs_review",
            observed=packet.get("candidate_status"),
            source_artifacts=packet_source,
        ),
        _check(
            key="active_candidate.remains_false",
            expected=False,
            observed=packet.get("active_candidate"),
            source_artifacts=packet_source,
        ),
        _check(
            key="source_refs.missing_count.remains_zero",
            expected=0,
            observed=len(missing_sources),
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.include_packet_reports",
            expected=packet_source,
            observed=tuple(source for source in packet_source if source in source_refs),
            source_artifacts=packet_source,
        ),
        _check(
            key="source_refs.include_dependency_reports",
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
        _check(
            key="source_refs.include_besov_negative_math0703883",
            expected=True,
            observed=(
                "papers/blockers/smooth_continuation_bridge/"
                "math0703883_besov_negative_blowup.pdf"
            )
            in source_refs,
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.include_robinson_review_1410_4495",
            expected=True,
            observed=(
                "papers/blockers/smooth_continuation_bridge/"
                "1410.4495_robinson_review_NSE.pdf"
            )
            in source_refs,
            source_artifacts=source_refs,
        ),
    )
    issues = tuple(check.key for check in checks if not check.passed)
    process_gate_open_authorized = any(
        bool(report.get("process_gate_open_authorized"))
        for report in (packet, dependency)
    )
    blocker_state_changed = any(
        bool(report.get("blocker_state_changed")) for report in (packet, dependency)
    )
    candidate_emission_authorized = any(
        bool(report.get("candidate_emission_authorized"))
        for report in (packet, dependency)
    )

    return Lemma0252SmoothContinuationSourceReadOperatorIndex(
        schema_version=1,
        lemma_id=str(packet.get("lemma_id")),
        candidate_status=str(packet.get("candidate_status")),
        active_candidate=bool(packet.get("active_candidate")),
        gap_id=GAP_ID,
        source_branch=SOURCE_BRANCH,
        section_count=len(sections),
        source_report_count=len(_direct_source_reports()),
        source_ref_count=len(source_refs),
        source_read_count=int(packet.get("source_read_count", 0)),
        direct_branch_source_read_count=int(
            packet.get("direct_branch_source_read_count", 0)
        ),
        cross_cutting_source_read_count=int(
            packet.get("cross_cutting_source_read_count", 0)
        ),
        blocked_source_read_count=int(packet.get("blocked_source_read_count", 0)),
        actionable_source_read_count=int(packet.get("actionable_source_read_count", 0)),
        may_discharge_source_read_count=int(packet.get("may_discharge_source_read_count", 0)),
        exact_discharge_artifact_count=int(packet.get("exact_discharge_artifact_count", 0)),
        packet_check_count=int(packet.get("packet_check_count", 0)),
        failed_packet_check_count=int(packet.get("failed_packet_check_count", 0)),
        packet_consistent=bool(packet.get("packet_consistent")),
        smooth_continuation_source_read_packet_dependency_check_count=int(
            dependency.get(
                "smooth_continuation_source_read_packet_dependency_check_count", 0
            )
        ),
        failed_smooth_continuation_source_read_packet_dependency_check_count=int(
            dependency.get(
                "failed_smooth_continuation_source_read_packet_dependency_check_count",
                0,
            )
        ),
        smooth_continuation_source_read_packet_dependency_consistent=bool(
            dependency.get(
                "smooth_continuation_source_read_packet_dependency_consistent"
            )
        ),
        smooth_continuation_source_read_packet_operator_index_check_count=len(checks),
        passed_smooth_continuation_source_read_packet_operator_index_check_count=sum(
            1 for check in checks if check.passed
        ),
        failed_smooth_continuation_source_read_packet_operator_index_check_count=len(
            issues
        ),
        smooth_continuation_source_read_packet_operator_index_consistent=len(
            issues
        )
        == 0,
        process_gate_open_authorized=process_gate_open_authorized,
        blocker_state_changed=blocker_state_changed,
        candidate_emission_authorized=candidate_emission_authorized,
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        issues=issues,
        sections=sections,
        checks=checks,
        source_refs=source_refs,
        source_read_ids=source_ids,
        source_paths=source_paths,
        non_claims=NON_CLAIMS,
        packet_snapshot=packet,
        dependency_snapshot=dependency,
    )


def render_markdown(
    report: Lemma0252SmoothContinuationSourceReadOperatorIndex,
) -> str:
    lines = [
        "# Lemma 0252 Smooth-Continuation Source Read Packet Operator Index",
        "",
        "## Summary",
        "",
        f"- lemma_id: `{report.lemma_id}`",
        f"- candidate_status: `{report.candidate_status}`",
        f"- active_candidate: `{str(report.active_candidate).lower()}`",
        f"- gap_id: `{report.gap_id}`",
        f"- source_branch: `{report.source_branch}`",
        f"- section_count: `{report.section_count}`",
        f"- source_report_count: `{report.source_report_count}`",
        f"- source_ref_count: `{report.source_ref_count}`",
        f"- source_read_count: `{report.source_read_count}`",
        f"- blocked_source_read_count: `{report.blocked_source_read_count}`",
        f"- actionable_source_read_count: `{report.actionable_source_read_count}`",
        f"- may_discharge_source_read_count: `{report.may_discharge_source_read_count}`",
        f"- exact_discharge_artifact_count: `{report.exact_discharge_artifact_count}`",
        f"- packet_check_count: `{report.packet_check_count}`",
        f"- failed_packet_check_count: `{report.failed_packet_check_count}`",
        f"- packet_consistent: `{str(report.packet_consistent).lower()}`",
        (
            "- smooth_continuation_source_read_packet_dependency_check_count: "
            f"`{report.smooth_continuation_source_read_packet_dependency_check_count}`"
        ),
        (
            "- failed_smooth_continuation_source_read_packet_dependency_check_count: "
            f"`{report.failed_smooth_continuation_source_read_packet_dependency_check_count}`"
        ),
        (
            "- smooth_continuation_source_read_packet_dependency_consistent: "
            f"`{str(report.smooth_continuation_source_read_packet_dependency_consistent).lower()}`"
        ),
        (
            "- smooth_continuation_source_read_packet_operator_index_check_count: "
            f"`{report.smooth_continuation_source_read_packet_operator_index_check_count}`"
        ),
        (
            "- failed_smooth_continuation_source_read_packet_operator_index_check_count: "
            f"`{report.failed_smooth_continuation_source_read_packet_operator_index_check_count}`"
        ),
        (
            "- smooth_continuation_source_read_packet_operator_index_consistent: "
            f"`{str(report.smooth_continuation_source_read_packet_operator_index_consistent).lower()}`"
        ),
        f"- process_gate_open_authorized: `{str(report.process_gate_open_authorized).lower()}`",
        f"- blocker_state_changed: `{str(report.blocker_state_changed).lower()}`",
        f"- candidate_emission_authorized: `{str(report.candidate_emission_authorized).lower()}`",
        f"- missing_source_count: `{report.missing_source_count}`",
        "",
        "## Sections",
        "",
        (
            "| step | name | status | primary_count_label | primary_count | "
            "blocked_count | actionable_count | consistent | missing_source_count |"
        ),
        "|---:|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for section in report.sections:
        lines.append(
            f"| {section.step} | `{section.name}` | `{section.status}` | "
            f"`{section.primary_count_label}` | {section.primary_count} | "
            f"{section.blocked_count} | {section.actionable_count} | "
            f"{str(section.consistent).lower()} | {section.missing_source_count} |"
        )

    lines.extend(["", "## Source Reads", ""])
    lines.extend(f"- `{source_id}`" for source_id in report.source_read_ids)
    lines.extend(["", "## Checks", ""])
    lines.extend(
        [
            "| key | expected | observed | passed |",
            "|---|---|---|---:|",
        ]
    )
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


def render_json(report: Lemma0252SmoothContinuationSourceReadOperatorIndex) -> str:
    return json.dumps(asdict(report), indent=2, sort_keys=True) + "\n"


def check_sources(
    report: Lemma0252SmoothContinuationSourceReadOperatorIndex,
) -> tuple[bool, str]:
    if report.missing_source_count:
        return False, "missing source refs: " + ", ".join(report.missing_sources)
    return True, "all smooth-continuation source-read operator index sources exist"


def check_consistent(
    report: Lemma0252SmoothContinuationSourceReadOperatorIndex,
) -> tuple[bool, str]:
    if not report.smooth_continuation_source_read_packet_operator_index_consistent:
        return (
            False,
            "inconsistent smooth-continuation source-read operator index: "
            + ", ".join(report.issues),
        )
    return True, "smooth-continuation source-read operator index is consistent"


def check_blocked(
    report: Lemma0252SmoothContinuationSourceReadOperatorIndex,
) -> tuple[bool, str]:
    if (
        report.gap_id != GAP_ID
        or report.source_branch != SOURCE_BRANCH
        or report.blocked_source_read_count != report.source_read_count
        or report.actionable_source_read_count != 0
        or report.may_discharge_source_read_count != 0
        or report.exact_discharge_artifact_count != 0
        or report.process_gate_open_authorized
        or report.blocker_state_changed
        or report.candidate_emission_authorized
    ):
        return False, "smooth-continuation source-read operator index is not blocked"
    return True, "smooth-continuation source-read operator index remains blocked"


def check_output(
    output: Path,
    report: Lemma0252SmoothContinuationSourceReadOperatorIndex,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_json(report) if output_format == "json" else render_markdown(report)
    if not output.exists():
        return False, f"missing smooth-continuation source-read operator index: {output}"
    observed = output.read_text(encoding="utf-8")
    if observed != expected:
        return False, f"stale smooth-continuation source-read operator index: {output}"
    return True, f"fresh smooth-continuation source-read operator index: {output}"


def _write_output(
    *,
    output: Path,
    report: Lemma0252SmoothContinuationSourceReadOperatorIndex,
    output_format: str,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    text = render_json(report) if output_format == "json" else render_markdown(report)
    output.write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Render a compact read-only operator/source index for the lemma_0252 "
            "smooth-continuation source-read packet stack."
        )
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    parser.add_argument("--require-consistent", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    args = parser.parse_args(argv)

    report = build_smooth_continuation_source_read_packet_operator_index()
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

    print(f"source_read_count: {report.source_read_count}")
    print(
        "smooth_continuation_source_read_packet_operator_index_check_count: "
        f"{report.smooth_continuation_source_read_packet_operator_index_check_count}"
    )
    print(
        "failed_smooth_continuation_source_read_packet_operator_index_check_count: "
        f"{report.failed_smooth_continuation_source_read_packet_operator_index_check_count}"
    )
    print(f"exact_discharge_artifact_count: {report.exact_discharge_artifact_count}")
    print(f"candidate_emission_authorized: {str(report.candidate_emission_authorized).lower()}")

    if failures:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
