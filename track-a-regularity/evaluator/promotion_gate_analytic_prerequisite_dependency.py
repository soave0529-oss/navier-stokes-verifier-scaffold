from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from lemma_0252_blocker_closure_dashboard import build_blocker_closure_dashboard
from promotion_gate_action_readiness import build_action_readiness
from promotion_gate_analytic_prerequisites import (
    DEFAULT_JSON_OUTPUT as DEFAULT_PACKET_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_PACKET_MARKDOWN_OUTPUT,
    EXPECTED_FAMILIES,
    build_analytic_prerequisite_packet,
    packet_to_dict,
)
from promotion_gate_regression import DEFAULT_CANDIDATE_DIR, DEFAULT_SMOKE_SUMMARY
from proof_obligation_blockers import DEFAULT_INPUT as DEFAULT_PROOF_GRAPH_JSON


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "promotion_gate_analytic_prerequisite_dependency.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "promotion_gate_analytic_prerequisite_dependency.json"
EXPECTED_CLOSURE_KEYS = (
    "closure.verdict_not_blocked",
    "closure.no_unresolved_branches",
    "closure.all_substantive_blockers_discharged",
    "closure.candidate_emission_authorized",
)
NON_CLAIMS = (
    "analytic_prerequisite_dependency_guard_only",
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
class DependencyCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class AnalyticPrerequisiteDependencyReport:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    packet_markdown: str
    packet_json: str
    action_readiness_source: str
    proof_graph_source: str
    closure_dashboard_source: str
    dependency_check_count: int
    passed_dependency_check_count: int
    failed_dependency_check_count: int
    dependency_consistent: bool
    process_gate_open_authorized: bool
    process_gate_open_blocked_by: tuple[str, ...]
    missing_source_count: int
    missing_sources: tuple[str, ...]
    issues: tuple[str, ...]
    checks: tuple[DependencyCheck, ...]
    non_claims: tuple[str, ...]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _proof_blocker_keys(path: Path) -> tuple[str, ...]:
    data = _load_json(path)
    blockers = data.get("promotion_blockers", [])
    if not isinstance(blockers, list):
        raise ValueError(f"promotion_blockers must be a list in {path}")
    keys: list[str] = []
    for blocker in blockers:
        if isinstance(blocker, dict):
            keys.append(str(blocker.get("key", "unknown")))
    return tuple(keys)


def _proof_state(path: Path) -> tuple[str, bool]:
    data = _load_json(path)
    candidate_status = data.get("candidate_status")
    active_candidate = data.get("active_candidate")
    if not isinstance(candidate_status, str):
        raise ValueError(f"candidate_status must be a string in {path}")
    if not isinstance(active_candidate, bool):
        raise ValueError(f"active_candidate must be a bool in {path}")
    return candidate_status, active_candidate


def _check(
    *,
    key: str,
    expected: object,
    observed: object,
    source_artifacts: tuple[str, ...],
) -> DependencyCheck:
    return DependencyCheck(
        key=key,
        expected=str(expected),
        observed=str(observed),
        passed=expected == observed,
        source_artifacts=source_artifacts,
    )


def _missing_sources(source_refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(source for source in source_refs if not (ROOT / source).exists())


def build_analytic_prerequisite_dependency_report(
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
    smoke_summary: Path = DEFAULT_SMOKE_SUMMARY,
    proof_graph_json: Path = DEFAULT_PROOF_GRAPH_JSON,
    packet_markdown: Path = DEFAULT_PACKET_MARKDOWN_OUTPUT,
    packet_json: Path = DEFAULT_PACKET_JSON_OUTPUT,
) -> AnalyticPrerequisiteDependencyReport:
    packet = build_analytic_prerequisite_packet(
        candidate_dir=candidate_dir,
        smoke_summary=smoke_summary,
        proof_graph_json=proof_graph_json,
    )
    readiness = build_action_readiness(candidate_dir=candidate_dir, smoke_summary=smoke_summary)
    closure = build_blocker_closure_dashboard(proof_obligation_json=proof_graph_json)
    proof_candidate_status, proof_active_candidate = _proof_state(proof_graph_json)
    proof_blocker_keys = _proof_blocker_keys(proof_graph_json)
    packet_prerequisite_keys = tuple(item.prerequisite_key for item in packet.prerequisites)
    packet_family_sources = {
        summary.family: tuple(summary.source_artifacts) for summary in packet.family_summaries
    }

    readiness_source = (
        "track-a-regularity/reports/promotion_gate_action_readiness.md",
        "track-a-regularity/reports/promotion_gate_action_readiness.json",
    )
    proof_source = (
        "track-a-regularity/reports/lemma_0252_proof_obligation_graph.json",
    )
    closure_source = (
        "track-a-regularity/reports/lemma_0252_blocker_closure_dashboard.json",
    )
    packet_source = (
        "track-a-regularity/reports/promotion_gate_analytic_prerequisites.md",
        "track-a-regularity/reports/promotion_gate_analytic_prerequisites.json",
    )
    source_refs = readiness_source + proof_source + closure_source + packet_source

    expected_proof_keys = (
        "proof_obligation.zero_promotion_blockers",
        *(f"proof_obligation.{key}.discharge_artifact" for key in proof_blocker_keys),
    )
    checks = (
        _check(
            key="packet.candidate_status.matches_proof_graph",
            expected=proof_candidate_status,
            observed=packet.candidate_status,
            source_artifacts=proof_source,
        ),
        _check(
            key="packet.active_candidate.matches_proof_graph",
            expected=proof_active_candidate,
            observed=packet.active_candidate,
            source_artifacts=proof_source,
        ),
        _check(
            key="packet.source_blocker_count.matches_action_readiness",
            expected=readiness.source_blocker_count,
            observed=packet.source_blocker_count,
            source_artifacts=readiness_source,
        ),
        _check(
            key="packet.analytic_blocker_count.matches_action_readiness",
            expected=readiness.analytic_blocker_count,
            observed=packet.analytic_blocker_count,
            source_artifacts=readiness_source,
        ),
        _check(
            key="packet.process_actionable_count.matches_action_readiness",
            expected=readiness.process_actionable_count,
            observed=packet.process_actionable_count,
            source_artifacts=readiness_source,
        ),
        _check(
            key="packet.process_blocked_by_analytic_count.matches_action_readiness",
            expected=readiness.process_blocked_by_analytic_count,
            observed=packet.process_blocked_by_analytic_count,
            source_artifacts=readiness_source,
        ),
        _check(
            key="packet.promotion_blocker_count.matches_proof_graph",
            expected=len(proof_blocker_keys),
            observed=packet.promotion_blocker_count,
            source_artifacts=proof_source,
        ),
        _check(
            key="packet.proof_prerequisite_keys.match_proof_blockers",
            expected=expected_proof_keys,
            observed=tuple(
                key for key in packet_prerequisite_keys if key.startswith("proof_obligation.")
            ),
            source_artifacts=proof_source,
        ),
        _check(
            key="packet.closure_verdict.matches_closure_dashboard",
            expected=closure.closure_verdict,
            observed=packet.closure_verdict,
            source_artifacts=closure_source,
        ),
        _check(
            key="packet.closure_unresolved_branch_count.matches_closure_dashboard",
            expected=closure.unresolved_branch_count,
            observed=packet.closure_unresolved_branch_count,
            source_artifacts=closure_source,
        ),
        _check(
            key="packet.closure_discharged_blocker_count.matches_closure_dashboard",
            expected=closure.discharged_blocker_count,
            observed=packet.closure_discharged_blocker_count,
            source_artifacts=closure_source,
        ),
        _check(
            key="packet.closure_prerequisite_keys.match_expected_closure_keys",
            expected=EXPECTED_CLOSURE_KEYS,
            observed=tuple(key for key in packet_prerequisite_keys if key.startswith("closure.")),
            source_artifacts=closure_source,
        ),
        _check(
            key="packet.family_summaries.match_expected_families",
            expected=EXPECTED_FAMILIES,
            observed=tuple(summary.family for summary in packet.family_summaries),
            source_artifacts=packet_source,
        ),
        _check(
            key="packet.proof_family_source.matches_proof_graph",
            expected=("track-a-regularity/reports/lemma_0252_proof_obligation_graph.json",),
            observed=packet_family_sources.get("proof_obligation", ()),
            source_artifacts=proof_source,
        ),
        _check(
            key="packet.closure_family_source.matches_closure_dashboard",
            expected=("track-a-regularity/reports/lemma_0252_blocker_closure_dashboard.json",),
            observed=packet_family_sources.get("closure", ()),
            source_artifacts=closure_source,
        ),
        _check(
            key="packet.process_gate_open_authorized.remains_false",
            expected=False,
            observed=packet.process_gate_open_authorized,
            source_artifacts=packet_source,
        ),
        _check(
            key="packet.process_gate_open_blocked_by.matches_expected_families",
            expected=EXPECTED_FAMILIES,
            observed=packet.process_gate_open_blocked_by,
            source_artifacts=packet_source,
        ),
    )

    missing_sources = _missing_sources(source_refs)
    issues = tuple(check.key for check in checks if not check.passed)
    failed_count = len(issues)
    dependency_consistent = failed_count == 0 and not missing_sources

    return AnalyticPrerequisiteDependencyReport(
        schema_version=1,
        lemma_id=packet.lemma_id,
        candidate_status=packet.candidate_status,
        active_candidate=packet.active_candidate,
        packet_markdown=str(packet_markdown),
        packet_json=str(packet_json),
        action_readiness_source="track-a-regularity/reports/promotion_gate_action_readiness.json",
        proof_graph_source="track-a-regularity/reports/lemma_0252_proof_obligation_graph.json",
        closure_dashboard_source="track-a-regularity/reports/lemma_0252_blocker_closure_dashboard.json",
        dependency_check_count=len(checks),
        passed_dependency_check_count=len(checks) - failed_count,
        failed_dependency_check_count=failed_count,
        dependency_consistent=dependency_consistent,
        process_gate_open_authorized=packet.process_gate_open_authorized,
        process_gate_open_blocked_by=packet.process_gate_open_blocked_by,
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        issues=issues,
        checks=checks,
        non_claims=NON_CLAIMS,
    )


def dependency_report_to_dict(report: AnalyticPrerequisiteDependencyReport) -> dict[str, object]:
    return {
        "schema_version": report.schema_version,
        "lemma_id": report.lemma_id,
        "candidate_status": report.candidate_status,
        "active_candidate": report.active_candidate,
        "packet_markdown": report.packet_markdown,
        "packet_json": report.packet_json,
        "action_readiness_source": report.action_readiness_source,
        "proof_graph_source": report.proof_graph_source,
        "closure_dashboard_source": report.closure_dashboard_source,
        "dependency_check_count": report.dependency_check_count,
        "passed_dependency_check_count": report.passed_dependency_check_count,
        "failed_dependency_check_count": report.failed_dependency_check_count,
        "dependency_consistent": report.dependency_consistent,
        "process_gate_open_authorized": report.process_gate_open_authorized,
        "process_gate_open_blocked_by": list(report.process_gate_open_blocked_by),
        "missing_source_count": report.missing_source_count,
        "missing_sources": list(report.missing_sources),
        "issues": list(report.issues),
        "checks": [asdict(check) for check in report.checks],
        "non_claims": list(report.non_claims),
        "packet_snapshot": packet_to_dict(build_analytic_prerequisite_packet()),
        "docs": {
            "analytic_prerequisites_doc": "docs/STEP96_PROMOTION_GATE_ANALYTIC_PREREQUISITES.md",
            "action_readiness_doc": "docs/STEP95_PROMOTION_GATE_ACTION_READINESS.md",
            "closure_dashboard_doc": "docs/STEP91_BLOCKER_CLOSURE_DASHBOARD.md",
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _check_rows(report: AnalyticPrerequisiteDependencyReport) -> list[str]:
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


def render_markdown(report: AnalyticPrerequisiteDependencyReport) -> str:
    return "\n".join(
        (
            "# Promotion Gate Analytic Prerequisite Dependency",
            "",
            "Generated by `track-a-regularity/evaluator/promotion_gate_analytic_prerequisite_dependency.py`.",
            "",
            "This read-only report checks that the Step 96 analytic-prerequisite packet",
            "matches the Step 95 action-readiness surface, the proof-obligation graph, and",
            "the Step 91 closure dashboard it cites.",
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
            f"- process_gate_open_authorized: `{str(report.process_gate_open_authorized).lower()}`",
            f"- process_gate_open_blocked_by: `{', '.join(report.process_gate_open_blocked_by) or 'none'}`",
            f"- missing_source_count: `{report.missing_source_count}`",
            f"- issues: `{', '.join(report.issues) or 'none'}`",
            "",
            "## Source Reports",
            "",
            f"- packet_markdown: `{report.packet_markdown}`",
            f"- packet_json: `{report.packet_json}`",
            f"- action_readiness_source: `{report.action_readiness_source}`",
            f"- proof_graph_source: `{report.proof_graph_source}`",
            f"- closure_dashboard_source: `{report.closure_dashboard_source}`",
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


def render_json(report: AnalyticPrerequisiteDependencyReport) -> str:
    return json.dumps(dependency_report_to_dict(report), indent=2, sort_keys=True) + "\n"


def render_output(report: AnalyticPrerequisiteDependencyReport, output_format: str) -> str:
    if output_format == "markdown":
        return render_markdown(report)
    if output_format == "json":
        return render_json(report)
    raise ValueError(f"unknown analytic prerequisite dependency format: {output_format}")


def write_output(
    output: Path,
    report: AnalyticPrerequisiteDependencyReport,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(report, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    report: AnalyticPrerequisiteDependencyReport,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(report, output_format)
    if not output.exists():
        return False, f"missing promotion gate analytic prerequisite dependency report: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale promotion gate analytic prerequisite dependency report: {output}"
    return True, f"fresh promotion gate analytic prerequisite dependency report: {output}"


def check_consistent(report: AnalyticPrerequisiteDependencyReport) -> tuple[bool, str]:
    if not report.dependency_consistent:
        return False, "analytic prerequisite dependency inconsistent: " + ", ".join(report.issues)
    return True, "analytic prerequisite dependency is consistent"


def check_sources(report: AnalyticPrerequisiteDependencyReport) -> tuple[bool, str]:
    if report.missing_source_count:
        return False, "missing analytic prerequisite dependency sources: " + ", ".join(
            report.missing_sources
        )
    return True, "all analytic prerequisite dependency sources exist"


def check_blocked(report: AnalyticPrerequisiteDependencyReport) -> tuple[bool, str]:
    if report.process_gate_open_authorized:
        return False, "process gate open became authorized"
    if tuple(report.process_gate_open_blocked_by) != EXPECTED_FAMILIES:
        return False, "process gate open is not blocked by both expected analytic families"
    return True, "analytic prerequisite dependency keeps process gates blocked"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown analytic prerequisite dependency format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check Step 96 analytic-prerequisite dependencies against their sources."
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
        report = build_analytic_prerequisite_dependency_report(
            candidate_dir=args.candidate_dir,
            smoke_summary=args.smoke_summary,
            proof_graph_json=args.proof_graph_json,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report setup failures.
        print(f"failed to build analytic prerequisite dependency report: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, report, args.format)
        print(message)
        if not ok:
            print(
                "run without --check-output to regenerate the analytic prerequisite dependency report",
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
