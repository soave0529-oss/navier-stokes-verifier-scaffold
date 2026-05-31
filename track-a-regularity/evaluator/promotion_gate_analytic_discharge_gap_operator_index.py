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
from promotion_gate_regression import DEFAULT_CANDIDATE_DIR, DEFAULT_SMOKE_SUMMARY
from proof_obligation_blockers import DEFAULT_INPUT as DEFAULT_PROOF_GRAPH_JSON


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = (
    DEFAULT_REPORT_DIR / "promotion_gate_analytic_discharge_gap_operator_index.md"
)
DEFAULT_JSON_OUTPUT = (
    DEFAULT_REPORT_DIR / "promotion_gate_analytic_discharge_gap_operator_index.json"
)

NON_CLAIMS = (
    "analytic_discharge_gap_operator_index_only",
    "read_only_gap_source_index",
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
class GapOperatorIndexSection:
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
class GapOperatorIndexCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class AnalyticDischargeGapOperatorIndex:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    section_count: int
    source_report_count: int
    source_ref_count: int
    gap_count: int
    blocked_gap_count: int
    actionable_gap_count: int
    may_discharge_gap_count: int
    missing_artifact_count: int
    gap_dependency_check_count: int
    gap_dependency_failed_check_count: int
    gap_dependency_consistent: bool
    operator_stack_consistent: bool
    operator_index_check_count: int
    passed_operator_index_check_count: int
    failed_operator_index_check_count: int
    operator_index_consistent: bool
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    issues: tuple[str, ...]
    sections: tuple[GapOperatorIndexSection, ...]
    checks: tuple[GapOperatorIndexCheck, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]
    gap_index_snapshot: dict[str, object]
    gap_dependency_snapshot: dict[str, object]


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
) -> GapOperatorIndexCheck:
    return GapOperatorIndexCheck(
        key=key,
        expected=str(expected),
        observed=str(observed),
        passed=expected == observed,
        source_artifacts=source_artifacts,
    )


def _missing_sources(source_refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(source for source in source_refs if not (ROOT / source).exists())


def _sections(
    gap_index: dict[str, object],
    gap_dependency: dict[str, object],
) -> tuple[GapOperatorIndexSection, ...]:
    return (
        GapOperatorIndexSection(
            step=102,
            name="analytic_discharge_gap_index",
            role=(
                "Maps blocked work-order/template types to missing theorem or formal "
                "artifacts."
            ),
            markdown_report=str(DEFAULT_GAP_INDEX_MARKDOWN_OUTPUT),
            json_report=str(DEFAULT_GAP_INDEX_JSON_OUTPUT),
            status="blocked_gap_index",
            primary_count_label="gap_count",
            primary_count=int(gap_index.get("gap_count", 0)),
            blocked_count=int(gap_index.get("blocked_gap_count", 0)),
            actionable_count=int(gap_index.get("actionable_gap_count", 0))
            + int(gap_index.get("may_discharge_gap_count", 0)),
            consistent=bool(gap_index.get("stack_consistent")) and not gap_index.get("issues"),
            missing_source_count=int(gap_index.get("missing_source_count", 0)),
        ),
        GapOperatorIndexSection(
            step=103,
            name="analytic_discharge_gap_dependency",
            role=(
                "Checks the gap index against the operator dashboard, template audit, "
                "template dependency, and work-order matrix."
            ),
            markdown_report=str(DEFAULT_GAP_DEPENDENCY_MARKDOWN_OUTPUT),
            json_report=str(DEFAULT_GAP_DEPENDENCY_JSON_OUTPUT),
            status="gap_dependency_guard",
            primary_count_label="dependency_check_count",
            primary_count=int(gap_dependency.get("dependency_check_count", 0)),
            blocked_count=int(gap_dependency.get("blocked_gap_count", 0)),
            actionable_count=int(gap_dependency.get("actionable_gap_count", 0))
            + int(gap_dependency.get("may_discharge_gap_count", 0)),
            consistent=bool(gap_dependency.get("dependency_consistent")),
            missing_source_count=int(gap_dependency.get("missing_source_count", 0)),
        ),
    )


def build_analytic_discharge_gap_operator_index(
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
    smoke_summary: Path = DEFAULT_SMOKE_SUMMARY,
    proof_graph_json: Path = DEFAULT_PROOF_GRAPH_JSON,
) -> AnalyticDischargeGapOperatorIndex:
    del candidate_dir, smoke_summary, proof_graph_json

    gap_index = _load_json(DEFAULT_GAP_INDEX_JSON_OUTPUT)
    gap_dependency = _load_json(DEFAULT_GAP_DEPENDENCY_JSON_OUTPUT)

    gap_index_source = (
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.md",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.json",
    )
    gap_dependency_source = (
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_dependency.md",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_dependency.json",
    )
    source_refs = tuple(
        dict.fromkeys(
            gap_index_source
            + gap_dependency_source
            + tuple(str(item) for item in gap_index.get("source_refs", ()))
            + tuple(str(item) for item in gap_dependency.get("source_refs", ()))
        )
    )
    missing_sources = _missing_sources(source_refs)
    sections = _sections(gap_index, gap_dependency)

    checks = (
        _check(
            key="gap.lemma_id.matches_dependency",
            expected=gap_dependency.get("lemma_id"),
            observed=gap_index.get("lemma_id"),
            source_artifacts=gap_dependency_source + gap_index_source,
        ),
        _check(
            key="gap.candidate_status.matches_dependency",
            expected=gap_dependency.get("candidate_status"),
            observed=gap_index.get("candidate_status"),
            source_artifacts=gap_dependency_source + gap_index_source,
        ),
        _check(
            key="gap.active_candidate.matches_dependency",
            expected=gap_dependency.get("active_candidate"),
            observed=gap_index.get("active_candidate"),
            source_artifacts=gap_dependency_source + gap_index_source,
        ),
        _check(
            key="gap.gap_count.matches_dependency",
            expected=gap_dependency.get("gap_count"),
            observed=gap_index.get("gap_count"),
            source_artifacts=gap_dependency_source + gap_index_source,
        ),
        _check(
            key="gap.blocked_gap_count.matches_dependency",
            expected=gap_dependency.get("blocked_gap_count"),
            observed=gap_index.get("blocked_gap_count"),
            source_artifacts=gap_dependency_source + gap_index_source,
        ),
        _check(
            key="gap.actionable_gap_count.remains_zero",
            expected=0,
            observed=gap_index.get("actionable_gap_count"),
            source_artifacts=gap_index_source,
        ),
        _check(
            key="gap.may_discharge_gap_count.remains_zero",
            expected=0,
            observed=gap_index.get("may_discharge_gap_count"),
            source_artifacts=gap_index_source,
        ),
        _check(
            key="gap.missing_artifact_count.matches_dependency",
            expected=gap_dependency.get("missing_artifact_count"),
            observed=gap_index.get("missing_artifact_count"),
            source_artifacts=gap_dependency_source + gap_index_source,
        ),
        _check(
            key="gap.process_gate_open_authorized.false",
            expected=False,
            observed=gap_index.get("process_gate_open_authorized"),
            source_artifacts=gap_index_source,
        ),
        _check(
            key="dependency.process_gate_open_authorized.false",
            expected=False,
            observed=gap_dependency.get("process_gate_open_authorized"),
            source_artifacts=gap_dependency_source,
        ),
        _check(
            key="blocker_state_changed.all_false",
            expected=(False, False),
            observed=(
                gap_index.get("blocker_state_changed"),
                gap_dependency.get("blocker_state_changed"),
            ),
            source_artifacts=gap_dependency_source + gap_index_source,
        ),
        _check(
            key="candidate_emission_authorized.all_false",
            expected=(False, False),
            observed=(
                gap_index.get("candidate_emission_authorized"),
                gap_dependency.get("candidate_emission_authorized"),
            ),
            source_artifacts=gap_dependency_source + gap_index_source,
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
            key="gap_dependency.operator_stack_consistent.true",
            expected=True,
            observed=gap_dependency.get("operator_stack_consistent"),
            source_artifacts=gap_dependency_source,
        ),
        _check(
            key="gap_index.stack_consistent.true",
            expected=True,
            observed=gap_index.get("stack_consistent"),
            source_artifacts=gap_index_source,
        ),
        _check(
            key="source_reports.issues.all_empty",
            expected=((), ()),
            observed=(
                tuple(gap_index.get("issues", ())),
                tuple(gap_dependency.get("issues", ())),
            ),
            source_artifacts=gap_dependency_source + gap_index_source,
        ),
        _check(
            key="source_report_count.matches_sections_times_two",
            expected=len(sections) * 2,
            observed=4,
            source_artifacts=gap_dependency_source + gap_index_source,
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
    operator_index_consistent = failed_count == 0 and not missing_sources

    return AnalyticDischargeGapOperatorIndex(
        schema_version=1,
        lemma_id=str(gap_index.get("lemma_id")),
        candidate_status=str(gap_index.get("candidate_status")),
        active_candidate=bool(gap_index.get("active_candidate")),
        section_count=len(sections),
        source_report_count=4,
        source_ref_count=len(source_refs),
        gap_count=int(gap_index.get("gap_count", 0)),
        blocked_gap_count=int(gap_index.get("blocked_gap_count", 0)),
        actionable_gap_count=int(gap_index.get("actionable_gap_count", 0)),
        may_discharge_gap_count=int(gap_index.get("may_discharge_gap_count", 0)),
        missing_artifact_count=int(gap_index.get("missing_artifact_count", 0)),
        gap_dependency_check_count=int(gap_dependency.get("dependency_check_count", 0)),
        gap_dependency_failed_check_count=int(
            gap_dependency.get("failed_dependency_check_count", 0)
        ),
        gap_dependency_consistent=bool(gap_dependency.get("dependency_consistent")),
        operator_stack_consistent=bool(gap_dependency.get("operator_stack_consistent")),
        operator_index_check_count=len(checks),
        passed_operator_index_check_count=len(checks) - failed_count,
        failed_operator_index_check_count=failed_count,
        operator_index_consistent=operator_index_consistent,
        process_gate_open_authorized=bool(gap_index.get("process_gate_open_authorized"))
        or bool(gap_dependency.get("process_gate_open_authorized")),
        blocker_state_changed=bool(gap_index.get("blocker_state_changed"))
        or bool(gap_dependency.get("blocker_state_changed")),
        candidate_emission_authorized=bool(gap_index.get("candidate_emission_authorized"))
        or bool(gap_dependency.get("candidate_emission_authorized")),
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        issues=issues,
        sections=sections,
        checks=checks,
        source_refs=source_refs,
        non_claims=NON_CLAIMS,
        gap_index_snapshot=gap_index,
        gap_dependency_snapshot=gap_dependency,
    )


def gap_operator_index_to_dict(
    report: AnalyticDischargeGapOperatorIndex,
) -> dict[str, object]:
    return {
        "schema_version": report.schema_version,
        "lemma_id": report.lemma_id,
        "candidate_status": report.candidate_status,
        "active_candidate": report.active_candidate,
        "section_count": report.section_count,
        "source_report_count": report.source_report_count,
        "source_ref_count": report.source_ref_count,
        "gap_count": report.gap_count,
        "blocked_gap_count": report.blocked_gap_count,
        "actionable_gap_count": report.actionable_gap_count,
        "may_discharge_gap_count": report.may_discharge_gap_count,
        "missing_artifact_count": report.missing_artifact_count,
        "gap_dependency_check_count": report.gap_dependency_check_count,
        "gap_dependency_failed_check_count": report.gap_dependency_failed_check_count,
        "gap_dependency_consistent": report.gap_dependency_consistent,
        "operator_stack_consistent": report.operator_stack_consistent,
        "operator_index_check_count": report.operator_index_check_count,
        "passed_operator_index_check_count": report.passed_operator_index_check_count,
        "failed_operator_index_check_count": report.failed_operator_index_check_count,
        "operator_index_consistent": report.operator_index_consistent,
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
        "gap_index_snapshot": report.gap_index_snapshot,
        "gap_dependency_snapshot": report.gap_dependency_snapshot,
        "docs": {
            "gap_index_doc": "docs/STEP102_PROMOTION_GATE_ANALYTIC_DISCHARGE_GAP_INDEX.md",
            "gap_dependency_doc": (
                "docs/STEP103_PROMOTION_GATE_ANALYTIC_DISCHARGE_GAP_DEPENDENCY.md"
            ),
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _section_rows(report: AnalyticDischargeGapOperatorIndex) -> list[str]:
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


def _check_rows(report: AnalyticDischargeGapOperatorIndex) -> list[str]:
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


def render_markdown(report: AnalyticDischargeGapOperatorIndex) -> str:
    return "\n".join(
        (
            "# Promotion Gate Analytic Discharge Gap Operator Index",
            "",
            "Generated by `track-a-regularity/evaluator/promotion_gate_analytic_discharge_gap_operator_index.py`.",
            "",
            "This read-only index consolidates the Step 102 gap index and the Step 103",
            "gap-dependency guard for future analytic-discharge review. It does not discharge",
            "any blocker and does not authorize process gates.",
            "",
            "## Summary",
            "",
            f"- lemma_id: `{report.lemma_id}`",
            f"- candidate_status: `{report.candidate_status}`",
            f"- active_candidate: `{str(report.active_candidate).lower()}`",
            f"- section_count: `{report.section_count}`",
            f"- source_report_count: `{report.source_report_count}`",
            f"- source_ref_count: `{report.source_ref_count}`",
            f"- gap_count: `{report.gap_count}`",
            f"- blocked_gap_count: `{report.blocked_gap_count}`",
            f"- actionable_gap_count: `{report.actionable_gap_count}`",
            f"- may_discharge_gap_count: `{report.may_discharge_gap_count}`",
            f"- missing_artifact_count: `{report.missing_artifact_count}`",
            f"- gap_dependency_check_count: `{report.gap_dependency_check_count}`",
            f"- gap_dependency_failed_check_count: `{report.gap_dependency_failed_check_count}`",
            f"- gap_dependency_consistent: `{str(report.gap_dependency_consistent).lower()}`",
            f"- operator_stack_consistent: `{str(report.operator_stack_consistent).lower()}`",
            f"- operator_index_check_count: `{report.operator_index_check_count}`",
            f"- passed_operator_index_check_count: `{report.passed_operator_index_check_count}`",
            f"- failed_operator_index_check_count: `{report.failed_operator_index_check_count}`",
            f"- operator_index_consistent: `{str(report.operator_index_consistent).lower()}`",
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


def render_json(report: AnalyticDischargeGapOperatorIndex) -> str:
    return json.dumps(
        gap_operator_index_to_dict(report),
        indent=2,
        sort_keys=True,
    ) + "\n"


def render_output(
    report: AnalyticDischargeGapOperatorIndex,
    output_format: str,
) -> str:
    if output_format == "markdown":
        return render_markdown(report)
    if output_format == "json":
        return render_json(report)
    raise ValueError(f"unknown analytic discharge gap operator index format: {output_format}")


def write_output(
    output: Path,
    report: AnalyticDischargeGapOperatorIndex,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(report, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    report: AnalyticDischargeGapOperatorIndex,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(report, output_format)
    if not output.exists():
        return False, f"missing promotion gate analytic discharge gap operator index: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale promotion gate analytic discharge gap operator index: {output}"
    return True, f"fresh promotion gate analytic discharge gap operator index: {output}"


def check_consistent(report: AnalyticDischargeGapOperatorIndex) -> tuple[bool, str]:
    if not report.operator_index_consistent:
        return False, "analytic discharge gap operator index inconsistent: " + ", ".join(
            report.issues
        )
    return True, "analytic discharge gap operator index is consistent"


def check_sources(report: AnalyticDischargeGapOperatorIndex) -> tuple[bool, str]:
    if report.missing_source_count:
        return False, "missing analytic discharge gap operator index sources: " + ", ".join(
            report.missing_sources
        )
    return True, "all analytic discharge gap operator index sources exist"


def check_blocked(report: AnalyticDischargeGapOperatorIndex) -> tuple[bool, str]:
    if report.process_gate_open_authorized:
        return False, "process gate open became authorized"
    if report.blocker_state_changed:
        return False, "gap operator index changed blocker state"
    if report.candidate_emission_authorized:
        return False, "gap operator index authorized candidate emission"
    if report.actionable_gap_count:
        return False, "gap operator index found actionable gaps"
    if report.may_discharge_gap_count:
        return False, "gap operator index found blocker-discharge-capable gaps"
    if report.blocked_gap_count != report.gap_count:
        return False, "not all gaps remain blocked"
    return True, "analytic discharge gap operator index keeps gaps blocked"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown analytic discharge gap operator index format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Summarize Step 102-103 analytic discharge gap artifacts."
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
        report = build_analytic_discharge_gap_operator_index(
            candidate_dir=args.candidate_dir,
            smoke_summary=args.smoke_summary,
            proof_graph_json=args.proof_graph_json,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report setup failures.
        print(f"failed to build analytic discharge gap operator index: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, report, args.format)
        print(message)
        if not ok:
            print(
                "run without --check-output to regenerate the analytic discharge gap operator index",
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

    print(f"operator_index_check_count: {report.operator_index_check_count}")
    print(f"passed_operator_index_check_count: {report.passed_operator_index_check_count}")
    print(f"failed_operator_index_check_count: {report.failed_operator_index_check_count}")
    print(f"operator_index_consistent: {str(report.operator_index_consistent).lower()}")
    print(f"process_gate_open_authorized: {str(report.process_gate_open_authorized).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
