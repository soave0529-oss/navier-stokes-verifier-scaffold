from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from promotion_gate_analytic_discharge_operator_dashboard import (
    DEFAULT_JSON_OUTPUT as DEFAULT_OPERATOR_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_OPERATOR_MARKDOWN_OUTPUT,
    build_analytic_discharge_operator_dashboard,
)
from promotion_gate_analytic_discharge_templates import (
    FORBIDDEN_MUTATIONS,
    REQUIRED_EVIDENCE_KEYS,
    AnalyticDischargeTemplate,
    build_analytic_discharge_template_audit,
)
from promotion_gate_analytic_work_order_matrix import (
    DEFAULT_JSON_OUTPUT as DEFAULT_MATRIX_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_MATRIX_MARKDOWN_OUTPUT,
)
from promotion_gate_regression import DEFAULT_CANDIDATE_DIR, DEFAULT_SMOKE_SUMMARY
from proof_obligation_blockers import DEFAULT_INPUT as DEFAULT_PROOF_GRAPH_JSON


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "promotion_gate_analytic_discharge_gap_index.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "promotion_gate_analytic_discharge_gap_index.json"

MISSING_ARTIFACT_BY_TYPE = {
    "zero_blocker_proof_graph_update": (
        "A reviewed proof-obligation graph update in which every promotion blocker has a linked "
        "discharge sidecar and `promotion_blocker_count=0`."
    ),
    "finite_bound_to_smallness_discharge_bundle": (
        "A theorem or formal sidecar proving that the finite critical parabolic Morrey/local "
        "enstrophy bound in `lemma_0252` implies the CKN-style epsilon-small velocity, pressure, "
        "or local-energy package in the exact periodic suitable-weak setting."
    ),
    "compactness_liouville_discharge_bundle": (
        "A compactness theorem producing the required ancient suitable limit plus a matching "
        "Liouville or backward-uniqueness result in the exact solution class and scaling regime."
    ),
    "smooth_continuation_discharge_bundle": (
        "A bridge theorem turning the local regularity metadata into BKM, Prodi-Serrin, "
        "high-Sobolev, or terminal-cover continuation input without adding a new assumption."
    ),
    "closure_dashboard_refresh": (
        "A refreshed closure dashboard backed by reviewed branch discharge artifacts, not by "
        "checklist presence alone."
    ),
    "branch_resolution_artifact_set": (
        "Resolution artifacts for finite-bound-to-smallness, compactness/Liouville, and "
        "smooth-continuation branches, each with source references and applicability checks."
    ),
    "substantive_blocker_discharge_bundle": (
        "A bundle of reviewed discharge artifacts for all three substantive blockers: "
        "finite_bound_to_smallness, compactness_liouville, and smooth_continuation_bridge."
    ),
    "candidate_emission_authorization_record": (
        "An explicit candidate-emission authorization record for the non-promotional-to-promotional "
        "transition that cites zero blockers, fresh v4 metadata, fresh source indexes, and a "
        "passing full smoke run."
    ),
}

MINIMUM_ACCEPTANCE_BY_TYPE = {
    "zero_blocker_proof_graph_update": (
        "proof-obligation JSON/Markdown refreshed",
        "blocker summary reports zero promotion blockers",
        "active-candidate blocker conflict remains false before promotion",
    ),
    "finite_bound_to_smallness_discharge_bundle": (
        "solution class and scaling match `lemma_0252`",
        "finite bound to epsilon-smallness mechanism is explicit",
        "CKN/Lin-style smallness-only limitation is addressed",
    ),
    "compactness_liouville_discharge_bundle": (
        "compactness limit construction is stated in the current suitable-weak setting",
        "Liouville/backward-uniqueness theorem applies to that limit",
        "axisymmetric or exterior-setting assumptions are not silently imported",
    ),
    "smooth_continuation_discharge_bundle": (
        "continuation criterion input follows from the local metadata",
        "BKM/Serrin/high-Sobolev hypothesis is not added externally",
        "terminal-time cover or local-to-global step is explicit",
    ),
    "closure_dashboard_refresh": (
        "closure verdict is changed only after all branches are discharged",
        "closure dashboard dependency checks remain fresh",
        "candidate emission remains separately gated",
    ),
    "branch_resolution_artifact_set": (
        "all three branch checklists point to discharge artifacts",
        "no branch remains `deferred_needs_new_result`",
        "source references exist and are fresh",
    ),
    "substantive_blocker_discharge_bundle": (
        "three substantive blockers are discharged by reviewed artifacts",
        "proof-obligation graph and closure dashboard agree",
        "full reproducibility smoke passes after the metadata change",
    ),
    "candidate_emission_authorization_record": (
        "v4 preflight metadata is complete and fresh",
        "manual promotion packet is ready",
        "active-pool ingress audit authorizes exactly the target candidate",
    ),
}

NON_CLAIMS = (
    "analytic_discharge_gap_index_only",
    "read_only_missing_artifact_index",
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
class DischargeGap:
    gap_id: str
    template_id: str
    work_order_id: str
    family: str
    source_branch: str
    prerequisite_key: str
    required_artifact_type: str
    missing_artifact: str
    required_review_evidence: tuple[str, ...]
    minimum_acceptance_checks: tuple[str, ...]
    current_state: str
    gap_status: str
    actionable_now: bool
    may_discharge_blocker: bool
    source_artifact: str
    dependency_guard_keys: tuple[str, ...]
    forbidden_mutations: tuple[str, ...]


@dataclass(frozen=True)
class GapFamilySummary:
    family: str
    gap_count: int
    blocked_gap_count: int
    actionable_gap_count: int
    may_discharge_gap_count: int
    required_artifact_types: tuple[str, ...]


@dataclass(frozen=True)
class GapSourceBranchSummary:
    source_branch: str
    gap_count: int
    required_artifact_types: tuple[str, ...]
    families: tuple[str, ...]


@dataclass(frozen=True)
class AnalyticDischargeGapIndex:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    operator_dashboard_markdown: str
    operator_dashboard_json: str
    matrix_markdown: str
    matrix_json: str
    gap_count: int
    blocked_gap_count: int
    actionable_gap_count: int
    may_discharge_gap_count: int
    missing_artifact_count: int
    required_review_evidence_key_count: int
    minimum_acceptance_check_count: int
    source_branch_count: int
    artifact_type_count: int
    stack_consistent: bool
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    issues: tuple[str, ...]
    gaps: tuple[DischargeGap, ...]
    family_summaries: tuple[GapFamilySummary, ...]
    source_branch_summaries: tuple[GapSourceBranchSummary, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]


def _missing_sources(source_refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(source for source in source_refs if not (ROOT / source).exists())


def _gap_from_template(index: int, template: AnalyticDischargeTemplate) -> DischargeGap:
    artifact_type = template.required_artifact_type
    return DischargeGap(
        gap_id=f"gap_{index:03d}",
        template_id=template.template_id,
        work_order_id=template.work_order_id,
        family=template.family,
        source_branch=template.source_branch,
        prerequisite_key=template.prerequisite_key,
        required_artifact_type=artifact_type,
        missing_artifact=MISSING_ARTIFACT_BY_TYPE[artifact_type],
        required_review_evidence=REQUIRED_EVIDENCE_KEYS,
        minimum_acceptance_checks=MINIMUM_ACCEPTANCE_BY_TYPE[artifact_type],
        current_state=template.blocker_state_after_template,
        gap_status="blocked_missing_artifact",
        actionable_now=False,
        may_discharge_blocker=False,
        source_artifact=template.source_artifact,
        dependency_guard_keys=template.dependency_guard_keys,
        forbidden_mutations=FORBIDDEN_MUTATIONS,
    )


def _family_summaries(gaps: tuple[DischargeGap, ...]) -> tuple[GapFamilySummary, ...]:
    summaries: list[GapFamilySummary] = []
    for family in sorted({gap.family for gap in gaps}):
        family_gaps = tuple(gap for gap in gaps if gap.family == family)
        summaries.append(
            GapFamilySummary(
                family=family,
                gap_count=len(family_gaps),
                blocked_gap_count=sum(
                    1 for gap in family_gaps if gap.gap_status == "blocked_missing_artifact"
                ),
                actionable_gap_count=sum(1 for gap in family_gaps if gap.actionable_now),
                may_discharge_gap_count=sum(1 for gap in family_gaps if gap.may_discharge_blocker),
                required_artifact_types=tuple(
                    sorted({gap.required_artifact_type for gap in family_gaps})
                ),
            )
        )
    return tuple(summaries)


def _source_branch_summaries(
    gaps: tuple[DischargeGap, ...]
) -> tuple[GapSourceBranchSummary, ...]:
    summaries: list[GapSourceBranchSummary] = []
    for branch in sorted({gap.source_branch for gap in gaps}):
        branch_gaps = tuple(gap for gap in gaps if gap.source_branch == branch)
        summaries.append(
            GapSourceBranchSummary(
                source_branch=branch,
                gap_count=len(branch_gaps),
                required_artifact_types=tuple(
                    sorted({gap.required_artifact_type for gap in branch_gaps})
                ),
                families=tuple(sorted({gap.family for gap in branch_gaps})),
            )
        )
    return tuple(summaries)


def build_analytic_discharge_gap_index(
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
    smoke_summary: Path = DEFAULT_SMOKE_SUMMARY,
    proof_graph_json: Path = DEFAULT_PROOF_GRAPH_JSON,
) -> AnalyticDischargeGapIndex:
    template_audit = build_analytic_discharge_template_audit(
        candidate_dir=candidate_dir,
        smoke_summary=smoke_summary,
        proof_graph_json=proof_graph_json,
    )
    dashboard = build_analytic_discharge_operator_dashboard(
        candidate_dir=candidate_dir,
        smoke_summary=smoke_summary,
        proof_graph_json=proof_graph_json,
    )
    gaps = tuple(
        _gap_from_template(index, template)
        for index, template in enumerate(template_audit.templates, start=1)
    )
    source_refs = tuple(
        dict.fromkeys(
            (
                "track-a-regularity/reports/promotion_gate_analytic_discharge_operator_dashboard.md",
                "track-a-regularity/reports/promotion_gate_analytic_discharge_operator_dashboard.json",
                "track-a-regularity/reports/promotion_gate_analytic_discharge_templates.md",
                "track-a-regularity/reports/promotion_gate_analytic_discharge_templates.json",
                "track-a-regularity/reports/promotion_gate_analytic_work_order_matrix.md",
                "track-a-regularity/reports/promotion_gate_analytic_work_order_matrix.json",
                *(gap.source_artifact for gap in gaps),
            )
        )
    )
    missing_sources = _missing_sources(source_refs)
    blocked_gap_count = sum(1 for gap in gaps if gap.gap_status == "blocked_missing_artifact")
    actionable_gap_count = sum(1 for gap in gaps if gap.actionable_now)
    may_discharge_gap_count = sum(1 for gap in gaps if gap.may_discharge_blocker)
    issues: list[str] = []
    if len(gaps) != template_audit.template_count:
        issues.append("gap_count_mismatch")
    if blocked_gap_count != len(gaps):
        issues.append("unblocked_gap_detected")
    if actionable_gap_count:
        issues.append("actionable_gap_detected")
    if may_discharge_gap_count:
        issues.append("gap_allows_blocker_discharge")
    if not dashboard.stack_consistent:
        issues.append("operator_dashboard_stack_inconsistent")
    if dashboard.process_gate_open_authorized or template_audit.process_gate_open_authorized:
        issues.append("process_gate_open_authorized")
    if missing_sources:
        issues.append("missing_sources")

    return AnalyticDischargeGapIndex(
        schema_version=1,
        lemma_id=template_audit.lemma_id,
        candidate_status=template_audit.candidate_status,
        active_candidate=template_audit.active_candidate,
        operator_dashboard_markdown=str(DEFAULT_OPERATOR_MARKDOWN_OUTPUT),
        operator_dashboard_json=str(DEFAULT_OPERATOR_JSON_OUTPUT),
        matrix_markdown=str(DEFAULT_MATRIX_MARKDOWN_OUTPUT),
        matrix_json=str(DEFAULT_MATRIX_JSON_OUTPUT),
        gap_count=len(gaps),
        blocked_gap_count=blocked_gap_count,
        actionable_gap_count=actionable_gap_count,
        may_discharge_gap_count=may_discharge_gap_count,
        missing_artifact_count=len(gaps),
        required_review_evidence_key_count=len(REQUIRED_EVIDENCE_KEYS),
        minimum_acceptance_check_count=sum(len(gap.minimum_acceptance_checks) for gap in gaps),
        source_branch_count=len({gap.source_branch for gap in gaps}),
        artifact_type_count=len({gap.required_artifact_type for gap in gaps}),
        stack_consistent=dashboard.stack_consistent,
        process_gate_open_authorized=False,
        blocker_state_changed=False,
        candidate_emission_authorized=False,
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        issues=tuple(issues),
        gaps=gaps,
        family_summaries=_family_summaries(gaps),
        source_branch_summaries=_source_branch_summaries(gaps),
        source_refs=source_refs,
        non_claims=NON_CLAIMS,
    )


def gap_index_to_dict(index: AnalyticDischargeGapIndex) -> dict[str, object]:
    return {
        "schema_version": index.schema_version,
        "lemma_id": index.lemma_id,
        "candidate_status": index.candidate_status,
        "active_candidate": index.active_candidate,
        "operator_dashboard_markdown": index.operator_dashboard_markdown,
        "operator_dashboard_json": index.operator_dashboard_json,
        "matrix_markdown": index.matrix_markdown,
        "matrix_json": index.matrix_json,
        "gap_count": index.gap_count,
        "blocked_gap_count": index.blocked_gap_count,
        "actionable_gap_count": index.actionable_gap_count,
        "may_discharge_gap_count": index.may_discharge_gap_count,
        "missing_artifact_count": index.missing_artifact_count,
        "required_review_evidence_key_count": index.required_review_evidence_key_count,
        "minimum_acceptance_check_count": index.minimum_acceptance_check_count,
        "source_branch_count": index.source_branch_count,
        "artifact_type_count": index.artifact_type_count,
        "stack_consistent": index.stack_consistent,
        "process_gate_open_authorized": index.process_gate_open_authorized,
        "blocker_state_changed": index.blocker_state_changed,
        "candidate_emission_authorized": index.candidate_emission_authorized,
        "missing_source_count": index.missing_source_count,
        "missing_sources": list(index.missing_sources),
        "issues": list(index.issues),
        "gaps": [asdict(gap) for gap in index.gaps],
        "family_summaries": [asdict(summary) for summary in index.family_summaries],
        "source_branch_summaries": [
            asdict(summary) for summary in index.source_branch_summaries
        ],
        "source_refs": list(index.source_refs),
        "non_claims": list(index.non_claims),
        "docs": {
            "operator_dashboard_doc": (
                "docs/STEP101_PROMOTION_GATE_ANALYTIC_DISCHARGE_OPERATOR_DASHBOARD.md"
            ),
            "analytic_discharge_templates_doc": (
                "docs/STEP99_PROMOTION_GATE_ANALYTIC_DISCHARGE_TEMPLATES.md"
            ),
            "analytic_work_order_matrix_doc": (
                "docs/STEP98_PROMOTION_GATE_ANALYTIC_WORK_ORDER_MATRIX.md"
            ),
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _family_rows(index: AnalyticDischargeGapIndex) -> list[str]:
    rows = [
        "| family | gaps | blocked | actionable | may discharge | artifact types |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for summary in index.family_summaries:
        rows.append(
            "| "
            f"`{summary.family}` | "
            f"{summary.gap_count} | "
            f"{summary.blocked_gap_count} | "
            f"{summary.actionable_gap_count} | "
            f"{summary.may_discharge_gap_count} | "
            f"{'<br>'.join(f'`{item}`' for item in summary.required_artifact_types)} |"
        )
    return rows


def _gap_rows(index: AnalyticDischargeGapIndex) -> list[str]:
    rows = [
        "| gap | work order | branch | artifact type | missing artifact | status | actionable | may discharge |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for gap in index.gaps:
        rows.append(
            "| "
            f"`{gap.gap_id}` | "
            f"`{gap.work_order_id}` | "
            f"`{gap.source_branch}` | "
            f"`{gap.required_artifact_type}` | "
            f"{_format(gap.missing_artifact)} | "
            f"`{gap.gap_status}` | "
            f"`{str(gap.actionable_now).lower()}` | "
            f"`{str(gap.may_discharge_blocker).lower()}` |"
        )
    return rows


def _acceptance_rows(index: AnalyticDischargeGapIndex) -> list[str]:
    rows = [
        "| gap | required review evidence | minimum acceptance checks |",
        "|---|---|---|",
    ]
    for gap in index.gaps:
        rows.append(
            "| "
            f"`{gap.gap_id}` | "
            f"{'<br>'.join(f'`{item}`' for item in gap.required_review_evidence)} | "
            f"{'<br>'.join(_format(item) for item in gap.minimum_acceptance_checks)} |"
        )
    return rows


def render_markdown(index: AnalyticDischargeGapIndex) -> str:
    return "\n".join(
        (
            "# Promotion Gate Analytic Discharge Gap Index",
            "",
            "Generated by `track-a-regularity/evaluator/promotion_gate_analytic_discharge_gap_index.py`.",
            "",
            "This read-only index maps the eight blocked Step 98/99 analytic-discharge work-order",
            "types to the concrete missing theorem or formal artifacts required before any future",
            "review can consider a blocker discharge.",
            "",
            "## Summary",
            "",
            f"- lemma_id: `{index.lemma_id}`",
            f"- candidate_status: `{index.candidate_status}`",
            f"- active_candidate: `{str(index.active_candidate).lower()}`",
            f"- gap_count: `{index.gap_count}`",
            f"- blocked_gap_count: `{index.blocked_gap_count}`",
            f"- actionable_gap_count: `{index.actionable_gap_count}`",
            f"- may_discharge_gap_count: `{index.may_discharge_gap_count}`",
            f"- missing_artifact_count: `{index.missing_artifact_count}`",
            f"- required_review_evidence_key_count: `{index.required_review_evidence_key_count}`",
            f"- minimum_acceptance_check_count: `{index.minimum_acceptance_check_count}`",
            f"- source_branch_count: `{index.source_branch_count}`",
            f"- artifact_type_count: `{index.artifact_type_count}`",
            f"- stack_consistent: `{str(index.stack_consistent).lower()}`",
            f"- process_gate_open_authorized: `{str(index.process_gate_open_authorized).lower()}`",
            f"- blocker_state_changed: `{str(index.blocker_state_changed).lower()}`",
            f"- candidate_emission_authorized: `{str(index.candidate_emission_authorized).lower()}`",
            f"- missing_source_count: `{index.missing_source_count}`",
            f"- issues: `{', '.join(index.issues) or 'none'}`",
            "",
            "## Family Summary",
            "",
            *_family_rows(index),
            "",
            "## Gap Index",
            "",
            *_gap_rows(index),
            "",
            "## Review Evidence And Acceptance Checks",
            "",
            *_acceptance_rows(index),
            "",
            "## Non-Claims",
            "",
            *(f"- `{item}`" for item in index.non_claims),
            "",
        )
    )


def render_json(index: AnalyticDischargeGapIndex) -> str:
    return json.dumps(gap_index_to_dict(index), indent=2, sort_keys=True) + "\n"


def render_output(index: AnalyticDischargeGapIndex, output_format: str) -> str:
    if output_format == "markdown":
        return render_markdown(index)
    if output_format == "json":
        return render_json(index)
    raise ValueError(f"unknown analytic discharge gap index format: {output_format}")


def write_output(
    output: Path,
    index: AnalyticDischargeGapIndex,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(index, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    index: AnalyticDischargeGapIndex,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(index, output_format)
    if not output.exists():
        return False, f"missing promotion gate analytic discharge gap index: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale promotion gate analytic discharge gap index: {output}"
    return True, f"fresh promotion gate analytic discharge gap index: {output}"


def check_blocked(index: AnalyticDischargeGapIndex) -> tuple[bool, str]:
    if index.process_gate_open_authorized:
        return False, "process gate open became authorized"
    if index.blocker_state_changed:
        return False, "gap index changed blocker state"
    if index.candidate_emission_authorized:
        return False, "gap index authorized candidate emission"
    if index.actionable_gap_count:
        return False, "gap index marked a gap actionable"
    if index.may_discharge_gap_count:
        return False, "gap index marked a gap as blocker-discharge capable"
    if index.blocked_gap_count != index.gap_count:
        return False, "not every gap remains blocked"
    return True, "analytic discharge gap index keeps all gaps blocked"


def check_stack_consistent(index: AnalyticDischargeGapIndex) -> tuple[bool, str]:
    if not index.stack_consistent:
        return False, "analytic discharge gap index stack inconsistent"
    if index.issues:
        return False, "analytic discharge gap index has issues: " + ", ".join(index.issues)
    return True, "analytic discharge gap index stack is consistent"


def check_sources(index: AnalyticDischargeGapIndex) -> tuple[bool, str]:
    if index.missing_source_count:
        return False, "missing analytic discharge gap index sources: " + ", ".join(
            index.missing_sources
        )
    return True, "all analytic discharge gap index sources exist"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown analytic discharge gap index format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a read-only gap index for blocked analytic discharge work orders."
    )
    parser.add_argument("--candidate-dir", type=Path, default=DEFAULT_CANDIDATE_DIR)
    parser.add_argument("--smoke-summary", type=Path, default=DEFAULT_SMOKE_SUMMARY)
    parser.add_argument("--proof-graph-json", type=Path, default=DEFAULT_PROOF_GRAPH_JSON)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    parser.add_argument("--require-stack-consistent", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    args = parser.parse_args(argv)

    try:
        index = build_analytic_discharge_gap_index(
            candidate_dir=args.candidate_dir,
            smoke_summary=args.smoke_summary,
            proof_graph_json=args.proof_graph_json,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report setup failures.
        print(f"failed to build analytic discharge gap index: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, index, args.format)
        print(message)
        if not ok:
            print(
                "run without --check-output to regenerate the analytic discharge gap index",
                file=sys.stderr,
            )
            return 1
    else:
        written = write_output(output, index, args.format)
        print(f"wrote {written}")

    if args.require_blocked:
        ok, message = check_blocked(index)
        print(message)
        if not ok:
            return 1
    if args.require_stack_consistent:
        ok, message = check_stack_consistent(index)
        print(message)
        if not ok:
            return 1
    if args.require_sources_exist:
        ok, message = check_sources(index)
        print(message)
        if not ok:
            return 1

    print(f"gap_count: {index.gap_count}")
    print(f"blocked_gap_count: {index.blocked_gap_count}")
    print(f"actionable_gap_count: {index.actionable_gap_count}")
    print(f"may_discharge_gap_count: {index.may_discharge_gap_count}")
    print(f"stack_consistent: {str(index.stack_consistent).lower()}")
    print(f"process_gate_open_authorized: {str(index.process_gate_open_authorized).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
