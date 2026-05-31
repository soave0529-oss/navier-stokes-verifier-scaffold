from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from promotion_gate_analytic_discharge_templates import (
    DEFAULT_JSON_OUTPUT as DEFAULT_TEMPLATE_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_TEMPLATE_MARKDOWN_OUTPUT,
    FORBIDDEN_MUTATIONS,
    REQUIRED_EVIDENCE_KEYS,
    audit_to_dict,
    build_analytic_discharge_template_audit,
)
from promotion_gate_analytic_prerequisite_dependency import (
    DEFAULT_JSON_OUTPUT as DEFAULT_DEPENDENCY_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_DEPENDENCY_MARKDOWN_OUTPUT,
    build_analytic_prerequisite_dependency_report,
    dependency_report_to_dict,
)
from promotion_gate_analytic_prerequisites import (
    DEFAULT_JSON_OUTPUT as DEFAULT_PACKET_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_PACKET_MARKDOWN_OUTPUT,
    build_analytic_prerequisite_packet,
    packet_to_dict,
)
from promotion_gate_analytic_work_order_matrix import (
    DEFAULT_JSON_OUTPUT as DEFAULT_MATRIX_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_MATRIX_MARKDOWN_OUTPUT,
    build_analytic_work_order_matrix,
    matrix_to_dict,
)
from promotion_gate_regression import DEFAULT_CANDIDATE_DIR, DEFAULT_SMOKE_SUMMARY
from proof_obligation_blockers import DEFAULT_INPUT as DEFAULT_PROOF_GRAPH_JSON


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = (
    DEFAULT_REPORT_DIR / "promotion_gate_analytic_discharge_template_dependency.md"
)
DEFAULT_JSON_OUTPUT = (
    DEFAULT_REPORT_DIR / "promotion_gate_analytic_discharge_template_dependency.json"
)
NON_CLAIMS = (
    "analytic_discharge_template_dependency_guard_only",
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
class TemplateDependencyCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class AnalyticDischargeTemplateDependencyReport:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    template_markdown: str
    template_json: str
    matrix_markdown: str
    matrix_json: str
    packet_markdown: str
    packet_json: str
    dependency_markdown: str
    dependency_json: str
    dependency_check_count: int
    passed_dependency_check_count: int
    failed_dependency_check_count: int
    dependency_consistent: bool
    template_count: int
    matrix_work_order_count: int
    packet_prerequisite_count: int
    blocked_template_count: int
    actionable_template_count: int
    may_discharge_template_count: int
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    issues: tuple[str, ...]
    checks: tuple[TemplateDependencyCheck, ...]
    non_claims: tuple[str, ...]


def _check(
    *,
    key: str,
    expected: object,
    observed: object,
    source_artifacts: tuple[str, ...],
) -> TemplateDependencyCheck:
    return TemplateDependencyCheck(
        key=key,
        expected=str(expected),
        observed=str(observed),
        passed=expected == observed,
        source_artifacts=source_artifacts,
    )


def _missing_sources(source_refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(source for source in source_refs if not (ROOT / source).exists())


def _template_ids(templates: tuple[object, ...], attr: str) -> tuple[object, ...]:
    return tuple(getattr(template, attr) for template in templates)


def _matrix_ids(work_orders: tuple[object, ...], attr: str) -> tuple[object, ...]:
    return tuple(getattr(order, attr) for order in work_orders)


def _all_templates_have(
    templates: tuple[object, ...],
    attr: str,
    expected: tuple[str, ...],
) -> tuple[tuple[str, tuple[str, ...]], ...]:
    return tuple(
        (
            str(getattr(template, "template_id")),
            tuple(getattr(template, attr)),
        )
        for template in templates
        if tuple(getattr(template, attr)) != expected
    )


def build_analytic_discharge_template_dependency_report(
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
    smoke_summary: Path = DEFAULT_SMOKE_SUMMARY,
    proof_graph_json: Path = DEFAULT_PROOF_GRAPH_JSON,
) -> AnalyticDischargeTemplateDependencyReport:
    template_audit = build_analytic_discharge_template_audit(
        candidate_dir=candidate_dir,
        smoke_summary=smoke_summary,
        proof_graph_json=proof_graph_json,
    )
    matrix = build_analytic_work_order_matrix(
        candidate_dir=candidate_dir,
        smoke_summary=smoke_summary,
        proof_graph_json=proof_graph_json,
    )
    packet = build_analytic_prerequisite_packet(
        candidate_dir=candidate_dir,
        smoke_summary=smoke_summary,
        proof_graph_json=proof_graph_json,
    )
    dependency = build_analytic_prerequisite_dependency_report(
        candidate_dir=candidate_dir,
        smoke_summary=smoke_summary,
        proof_graph_json=proof_graph_json,
    )

    template_source = (
        "track-a-regularity/reports/promotion_gate_analytic_discharge_templates.md",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_templates.json",
    )
    matrix_source = (
        "track-a-regularity/reports/promotion_gate_analytic_work_order_matrix.md",
        "track-a-regularity/reports/promotion_gate_analytic_work_order_matrix.json",
    )
    packet_source = (
        "track-a-regularity/reports/promotion_gate_analytic_prerequisites.md",
        "track-a-regularity/reports/promotion_gate_analytic_prerequisites.json",
    )
    dependency_source = (
        "track-a-regularity/reports/promotion_gate_analytic_prerequisite_dependency.md",
        "track-a-regularity/reports/promotion_gate_analytic_prerequisite_dependency.json",
    )
    source_refs = tuple(
        dict.fromkeys(
            template_source
            + matrix_source
            + packet_source
            + dependency_source
            + tuple(template_audit.source_refs)
            + tuple(matrix.source_refs)
        )
    )
    missing_sources = _missing_sources(source_refs)

    matrix_work_order_ids = _matrix_ids(matrix.work_orders, "work_order_id")
    template_work_order_ids = _template_ids(template_audit.templates, "work_order_id")
    checks = (
        _check(
            key="template.lemma_id.matches_matrix",
            expected=matrix.lemma_id,
            observed=template_audit.lemma_id,
            source_artifacts=matrix_source,
        ),
        _check(
            key="template.candidate_status.matches_matrix",
            expected=matrix.candidate_status,
            observed=template_audit.candidate_status,
            source_artifacts=matrix_source,
        ),
        _check(
            key="template.active_candidate.matches_matrix",
            expected=matrix.active_candidate,
            observed=template_audit.active_candidate,
            source_artifacts=matrix_source,
        ),
        _check(
            key="template.template_count.matches_matrix_work_order_count",
            expected=matrix.work_order_count,
            observed=template_audit.template_count,
            source_artifacts=matrix_source,
        ),
        _check(
            key="template.template_count.matches_packet_prerequisite_count",
            expected=packet.prerequisite_count,
            observed=template_audit.template_count,
            source_artifacts=packet_source,
        ),
        _check(
            key="template.blocked_template_count.matches_matrix_blocked_work_orders",
            expected=matrix.blocked_work_order_count,
            observed=template_audit.blocked_template_count,
            source_artifacts=matrix_source,
        ),
        _check(
            key="template.actionable_template_count.matches_matrix_actionable_count",
            expected=matrix.actionable_work_order_count,
            observed=template_audit.actionable_template_count,
            source_artifacts=matrix_source,
        ),
        _check(
            key="template.source_branch_count.matches_matrix",
            expected=matrix.source_branch_count,
            observed=template_audit.source_branch_count,
            source_artifacts=matrix_source,
        ),
        _check(
            key="template.artifact_type_count.matches_matrix",
            expected=matrix.artifact_type_count,
            observed=template_audit.artifact_type_count,
            source_artifacts=matrix_source,
        ),
        _check(
            key="template.dependency_consistent.matches_matrix",
            expected=matrix.dependency_consistent,
            observed=template_audit.dependency_consistent,
            source_artifacts=matrix_source,
        ),
        _check(
            key="matrix.dependency_consistent.matches_dependency_report",
            expected=dependency.dependency_consistent,
            observed=matrix.dependency_consistent,
            source_artifacts=dependency_source,
        ),
        _check(
            key="matrix.work_order_count.matches_packet_prerequisite_count",
            expected=packet.prerequisite_count,
            observed=matrix.work_order_count,
            source_artifacts=packet_source,
        ),
        _check(
            key="template.work_order_ids.match_matrix_work_order_ids",
            expected=matrix_work_order_ids,
            observed=template_work_order_ids,
            source_artifacts=matrix_source,
        ),
        _check(
            key="template.prerequisite_keys.match_matrix",
            expected=_matrix_ids(matrix.work_orders, "prerequisite_key"),
            observed=_template_ids(template_audit.templates, "prerequisite_key"),
            source_artifacts=matrix_source,
        ),
        _check(
            key="template.required_artifact_types.match_matrix",
            expected=_matrix_ids(matrix.work_orders, "required_artifact_type"),
            observed=_template_ids(template_audit.templates, "required_artifact_type"),
            source_artifacts=matrix_source,
        ),
        _check(
            key="template.source_branches.match_matrix",
            expected=_matrix_ids(matrix.work_orders, "source_branch"),
            observed=_template_ids(template_audit.templates, "source_branch"),
            source_artifacts=matrix_source,
        ),
        _check(
            key="template.dependency_guard_keys.match_matrix",
            expected=_matrix_ids(matrix.work_orders, "dependency_guard_keys"),
            observed=_template_ids(template_audit.templates, "dependency_guard_keys"),
            source_artifacts=matrix_source,
        ),
        _check(
            key="template.source_artifacts.match_matrix",
            expected=_matrix_ids(matrix.work_orders, "source_artifact"),
            observed=_template_ids(template_audit.templates, "source_artifact"),
            source_artifacts=matrix_source,
        ),
        _check(
            key="template.required_evidence_keys.all_expected",
            expected=(),
            observed=_all_templates_have(
                template_audit.templates,
                "required_evidence_keys",
                REQUIRED_EVIDENCE_KEYS,
            ),
            source_artifacts=template_source,
        ),
        _check(
            key="template.forbidden_mutations.all_expected",
            expected=(),
            observed=_all_templates_have(
                template_audit.templates,
                "forbidden_mutations",
                FORBIDDEN_MUTATIONS,
            ),
            source_artifacts=template_source,
        ),
        _check(
            key="template.process_gate_open_authorized.matches_packet",
            expected=packet.process_gate_open_authorized,
            observed=template_audit.process_gate_open_authorized,
            source_artifacts=packet_source,
        ),
        _check(
            key="template.process_gate_open_authorized.matches_dependency_report",
            expected=dependency.process_gate_open_authorized,
            observed=template_audit.process_gate_open_authorized,
            source_artifacts=dependency_source,
        ),
        _check(
            key="template.process_gate_open_authorized.matches_matrix",
            expected=matrix.process_gate_open_authorized,
            observed=template_audit.process_gate_open_authorized,
            source_artifacts=matrix_source,
        ),
        _check(
            key="template.may_discharge_template_count.remains_zero",
            expected=0,
            observed=template_audit.may_discharge_template_count,
            source_artifacts=template_source,
        ),
        _check(
            key="template.blocker_state_changed.remains_false",
            expected=False,
            observed=template_audit.blocker_state_changed,
            source_artifacts=template_source,
        ),
        _check(
            key="template.candidate_emission_authorized.remains_false",
            expected=False,
            observed=template_audit.candidate_emission_authorized,
            source_artifacts=template_source,
        ),
    )

    issues = tuple(check.key for check in checks if not check.passed)
    failed_count = len(issues)
    dependency_consistent = failed_count == 0 and not missing_sources

    return AnalyticDischargeTemplateDependencyReport(
        schema_version=1,
        lemma_id=template_audit.lemma_id,
        candidate_status=template_audit.candidate_status,
        active_candidate=template_audit.active_candidate,
        template_markdown=str(DEFAULT_TEMPLATE_MARKDOWN_OUTPUT),
        template_json=str(DEFAULT_TEMPLATE_JSON_OUTPUT),
        matrix_markdown=str(DEFAULT_MATRIX_MARKDOWN_OUTPUT),
        matrix_json=str(DEFAULT_MATRIX_JSON_OUTPUT),
        packet_markdown=str(DEFAULT_PACKET_MARKDOWN_OUTPUT),
        packet_json=str(DEFAULT_PACKET_JSON_OUTPUT),
        dependency_markdown=str(DEFAULT_DEPENDENCY_MARKDOWN_OUTPUT),
        dependency_json=str(DEFAULT_DEPENDENCY_JSON_OUTPUT),
        dependency_check_count=len(checks),
        passed_dependency_check_count=len(checks) - failed_count,
        failed_dependency_check_count=failed_count,
        dependency_consistent=dependency_consistent,
        template_count=template_audit.template_count,
        matrix_work_order_count=matrix.work_order_count,
        packet_prerequisite_count=packet.prerequisite_count,
        blocked_template_count=template_audit.blocked_template_count,
        actionable_template_count=template_audit.actionable_template_count,
        may_discharge_template_count=template_audit.may_discharge_template_count,
        process_gate_open_authorized=template_audit.process_gate_open_authorized,
        blocker_state_changed=template_audit.blocker_state_changed,
        candidate_emission_authorized=template_audit.candidate_emission_authorized,
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        issues=issues,
        checks=checks,
        non_claims=NON_CLAIMS,
    )


def template_dependency_report_to_dict(
    report: AnalyticDischargeTemplateDependencyReport,
) -> dict[str, object]:
    return {
        "schema_version": report.schema_version,
        "lemma_id": report.lemma_id,
        "candidate_status": report.candidate_status,
        "active_candidate": report.active_candidate,
        "template_markdown": report.template_markdown,
        "template_json": report.template_json,
        "matrix_markdown": report.matrix_markdown,
        "matrix_json": report.matrix_json,
        "packet_markdown": report.packet_markdown,
        "packet_json": report.packet_json,
        "dependency_markdown": report.dependency_markdown,
        "dependency_json": report.dependency_json,
        "dependency_check_count": report.dependency_check_count,
        "passed_dependency_check_count": report.passed_dependency_check_count,
        "failed_dependency_check_count": report.failed_dependency_check_count,
        "dependency_consistent": report.dependency_consistent,
        "template_count": report.template_count,
        "matrix_work_order_count": report.matrix_work_order_count,
        "packet_prerequisite_count": report.packet_prerequisite_count,
        "blocked_template_count": report.blocked_template_count,
        "actionable_template_count": report.actionable_template_count,
        "may_discharge_template_count": report.may_discharge_template_count,
        "process_gate_open_authorized": report.process_gate_open_authorized,
        "blocker_state_changed": report.blocker_state_changed,
        "candidate_emission_authorized": report.candidate_emission_authorized,
        "missing_source_count": report.missing_source_count,
        "missing_sources": list(report.missing_sources),
        "issues": list(report.issues),
        "checks": [asdict(check) for check in report.checks],
        "non_claims": list(report.non_claims),
        "template_snapshot": audit_to_dict(build_analytic_discharge_template_audit()),
        "matrix_snapshot": matrix_to_dict(build_analytic_work_order_matrix()),
        "packet_snapshot": packet_to_dict(build_analytic_prerequisite_packet()),
        "dependency_snapshot": dependency_report_to_dict(
            build_analytic_prerequisite_dependency_report()
        ),
        "docs": {
            "analytic_discharge_templates_doc": (
                "docs/STEP99_PROMOTION_GATE_ANALYTIC_DISCHARGE_TEMPLATES.md"
            ),
            "analytic_work_order_matrix_doc": (
                "docs/STEP98_PROMOTION_GATE_ANALYTIC_WORK_ORDER_MATRIX.md"
            ),
            "analytic_prerequisites_doc": (
                "docs/STEP96_PROMOTION_GATE_ANALYTIC_PREREQUISITES.md"
            ),
            "analytic_dependency_doc": (
                "docs/STEP97_PROMOTION_GATE_ANALYTIC_PREREQUISITE_DEPENDENCY.md"
            ),
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _check_rows(report: AnalyticDischargeTemplateDependencyReport) -> list[str]:
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


def render_markdown(report: AnalyticDischargeTemplateDependencyReport) -> str:
    return "\n".join(
        (
            "# Promotion Gate Analytic Discharge Template Dependency",
            "",
            "Generated by `track-a-regularity/evaluator/promotion_gate_analytic_discharge_template_dependency.py`.",
            "",
            "This read-only report checks that the Step 99 analytic discharge template audit",
            "matches the Step 98 work-order matrix, Step 96 prerequisite packet, and Step 97",
            "dependency report it depends on.",
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
            f"- template_count: `{report.template_count}`",
            f"- matrix_work_order_count: `{report.matrix_work_order_count}`",
            f"- packet_prerequisite_count: `{report.packet_prerequisite_count}`",
            f"- blocked_template_count: `{report.blocked_template_count}`",
            f"- actionable_template_count: `{report.actionable_template_count}`",
            f"- may_discharge_template_count: `{report.may_discharge_template_count}`",
            f"- process_gate_open_authorized: `{str(report.process_gate_open_authorized).lower()}`",
            f"- blocker_state_changed: `{str(report.blocker_state_changed).lower()}`",
            f"- candidate_emission_authorized: `{str(report.candidate_emission_authorized).lower()}`",
            f"- missing_source_count: `{report.missing_source_count}`",
            f"- issues: `{', '.join(report.issues) or 'none'}`",
            "",
            "## Source Reports",
            "",
            f"- template_markdown: `{report.template_markdown}`",
            f"- template_json: `{report.template_json}`",
            f"- matrix_markdown: `{report.matrix_markdown}`",
            f"- matrix_json: `{report.matrix_json}`",
            f"- packet_markdown: `{report.packet_markdown}`",
            f"- packet_json: `{report.packet_json}`",
            f"- dependency_markdown: `{report.dependency_markdown}`",
            f"- dependency_json: `{report.dependency_json}`",
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


def render_json(report: AnalyticDischargeTemplateDependencyReport) -> str:
    return json.dumps(
        template_dependency_report_to_dict(report),
        indent=2,
        sort_keys=True,
    ) + "\n"


def render_output(
    report: AnalyticDischargeTemplateDependencyReport,
    output_format: str,
) -> str:
    if output_format == "markdown":
        return render_markdown(report)
    if output_format == "json":
        return render_json(report)
    raise ValueError(f"unknown analytic discharge template dependency format: {output_format}")


def write_output(
    output: Path,
    report: AnalyticDischargeTemplateDependencyReport,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(report, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    report: AnalyticDischargeTemplateDependencyReport,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(report, output_format)
    if not output.exists():
        return False, f"missing promotion gate analytic discharge template dependency: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale promotion gate analytic discharge template dependency: {output}"
    return True, f"fresh promotion gate analytic discharge template dependency: {output}"


def check_consistent(
    report: AnalyticDischargeTemplateDependencyReport,
) -> tuple[bool, str]:
    if not report.dependency_consistent:
        return False, "analytic discharge template dependency inconsistent: " + ", ".join(
            report.issues
        )
    return True, "analytic discharge template dependency is consistent"


def check_sources(report: AnalyticDischargeTemplateDependencyReport) -> tuple[bool, str]:
    if report.missing_source_count:
        return False, "missing analytic discharge template dependency sources: " + ", ".join(
            report.missing_sources
        )
    return True, "all analytic discharge template dependency sources exist"


def check_blocked(report: AnalyticDischargeTemplateDependencyReport) -> tuple[bool, str]:
    if report.process_gate_open_authorized:
        return False, "process gate open became authorized"
    if report.blocker_state_changed:
        return False, "template dependency changed blocker state"
    if report.candidate_emission_authorized:
        return False, "template dependency authorized candidate emission"
    if report.actionable_template_count:
        return False, "template dependency found actionable templates"
    if report.may_discharge_template_count:
        return False, "template dependency found blocker-discharge-capable templates"
    if report.blocked_template_count != report.template_count:
        return False, "not all templates remain blocked"
    return True, "analytic discharge template dependency keeps templates blocked"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown analytic discharge template dependency format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check Step 99 analytic discharge template dependencies against source reports."
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
        report = build_analytic_discharge_template_dependency_report(
            candidate_dir=args.candidate_dir,
            smoke_summary=args.smoke_summary,
            proof_graph_json=args.proof_graph_json,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report setup failures.
        print(f"failed to build analytic discharge template dependency: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, report, args.format)
        print(message)
        if not ok:
            print(
                "run without --check-output to regenerate the analytic discharge template dependency",
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
