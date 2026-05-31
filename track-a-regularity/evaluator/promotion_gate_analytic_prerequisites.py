from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from lemma_0252_blocker_closure_dashboard import (
    DEFAULT_JSON_OUTPUT as DEFAULT_CLOSURE_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_CLOSURE_MARKDOWN_OUTPUT,
    Lemma0252BlockerClosureDashboard,
    build_blocker_closure_dashboard,
)
from promotion_gate_action_readiness import (
    DEFAULT_JSON_OUTPUT as DEFAULT_READINESS_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_READINESS_MARKDOWN_OUTPUT,
    PromotionGateActionReadiness,
    build_action_readiness,
)
from promotion_gate_regression import DEFAULT_CANDIDATE_DIR, DEFAULT_SMOKE_SUMMARY
from proof_obligation_blockers import DEFAULT_INPUT as DEFAULT_PROOF_GRAPH_JSON


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "promotion_gate_analytic_prerequisites.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "promotion_gate_analytic_prerequisites.json"
EXPECTED_FAMILIES = ("proof_obligation", "closure")
PROCESS_FAMILIES = ("staging", "manual_packet", "lifecycle", "v4_preflight")
PROOF_BLOCKER_REQUIRED_STATES = {
    "finite_bound_to_smallness": (
        "Provide a verified theorem or formal sidecar turning the finite critical local enstrophy "
        "bound into the epsilon-small velocity/pressure/local-energy package needed by known "
        "regularity criteria."
    ),
    "compactness_liouville": (
        "Provide a verified ancient-limit compactness theorem plus a matching Liouville or "
        "backward-uniqueness result in the exact suitable-weak setting."
    ),
    "smooth_continuation_bridge": (
        "Provide continuation-criterion input, such as BKM/Serrin/high-Sobolev/terminal-cover "
        "data, that follows from the local metadata rather than from an extra assumption."
    ),
}
SOURCE_REFS = (
    "track-a-regularity/reports/promotion_gate_action_readiness.md",
    "track-a-regularity/reports/promotion_gate_action_readiness.json",
    "track-a-regularity/reports/lemma_0252_proof_obligation_graph.md",
    "track-a-regularity/reports/lemma_0252_proof_obligation_graph.json",
    "track-a-regularity/reports/lemma_0252_blocker_closure_dashboard.md",
    "track-a-regularity/reports/lemma_0252_blocker_closure_dashboard.json",
    "track-a-regularity/reports/lemma_0252_compactness_liouville_checklist.md",
    "track-a-regularity/reports/lemma_0252_finite_bound_smallness_checklist.md",
    "track-a-regularity/reports/lemma_0252_smooth_continuation_checklist.md",
    "docs/STEP91_BLOCKER_CLOSURE_DASHBOARD.md",
    "docs/STEP94_PROMOTION_GATE_BLOCKER_LEDGER.md",
    "docs/STEP95_PROMOTION_GATE_ACTION_READINESS.md",
)
NON_CLAIMS = (
    "analytic_prerequisite_packet_only",
    "read_only_discharge_requirements",
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
class AnalyticPrerequisite:
    family: str
    prerequisite_key: str
    current_state: str
    required_state: str
    satisfied: bool
    source_artifact: str
    discharge_artifact_required: str
    blocks_process_gate_open: bool


@dataclass(frozen=True)
class FamilyPrerequisiteSummary:
    family: str
    prerequisite_count: int
    satisfied_count: int
    unsatisfied_count: int
    blocks_process_gate_open: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class AnalyticPrerequisitePacket:
    schema_version: int
    candidate_dir: str
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    process_families_waiting: tuple[str, ...]
    analytic_families: tuple[str, ...]
    source_blocker_count: int
    analytic_blocker_count: int
    process_actionable_count: int
    process_blocked_by_analytic_count: int
    closure_verdict: str
    promotion_blocker_count: int
    closure_unresolved_branch_count: int
    closure_discharged_blocker_count: int
    prerequisite_count: int
    satisfied_prerequisite_count: int
    unsatisfied_prerequisite_count: int
    process_gate_open_authorized: bool
    process_gate_open_blocked_by: tuple[str, ...]
    missing_source_count: int
    missing_sources: tuple[str, ...]
    prerequisites: tuple[AnalyticPrerequisite, ...]
    family_summaries: tuple[FamilyPrerequisiteSummary, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _promotion_blockers(path: Path) -> tuple[dict[str, Any], ...]:
    data = _load_json(path)
    blockers = data.get("promotion_blockers", [])
    if not isinstance(blockers, list):
        raise ValueError(f"promotion_blockers must be a list in {path}")
    return tuple(blocker for blocker in blockers if isinstance(blocker, dict))


def _proof_graph_state(path: Path) -> tuple[str, bool]:
    data = _load_json(path)
    candidate_status = data.get("candidate_status")
    active_candidate = data.get("active_candidate")
    if not isinstance(candidate_status, str):
        raise ValueError(f"candidate_status must be a string in {path}")
    if not isinstance(active_candidate, bool):
        raise ValueError(f"active_candidate must be a boolean in {path}")
    return candidate_status, active_candidate


def _proof_prerequisites(proof_graph_json: Path) -> tuple[AnalyticPrerequisite, ...]:
    blockers = _promotion_blockers(proof_graph_json)
    items = [
        AnalyticPrerequisite(
            family="proof_obligation",
            prerequisite_key="proof_obligation.zero_promotion_blockers",
            current_state=f"promotion_blocker_count={len(blockers)}",
            required_state="promotion_blocker_count=0 with reviewed discharge artifacts",
            satisfied=len(blockers) == 0,
            source_artifact="track-a-regularity/reports/lemma_0252_proof_obligation_graph.json",
            discharge_artifact_required=(
                "Update the proof-obligation graph only after every promotion blocker has a "
                "reviewed theorem/mechanism sidecar."
            ),
            blocks_process_gate_open=bool(blockers),
        )
    ]
    for blocker in blockers:
        key = str(blocker.get("key", "unknown"))
        status = str(blocker.get("status", "unknown"))
        items.append(
            AnalyticPrerequisite(
                family="proof_obligation",
                prerequisite_key=f"proof_obligation.{key}.discharge_artifact",
                current_state=f"status={status}; listed_in_promotion_blockers=true",
                required_state=PROOF_BLOCKER_REQUIRED_STATES.get(
                    key,
                    "Provide a reviewed discharge artifact before removing this blocker.",
                ),
                satisfied=False,
                source_artifact="track-a-regularity/reports/lemma_0252_proof_obligation_graph.json",
                discharge_artifact_required=(
                    f"Create a reviewed discharge memo and matching machine-readable proof "
                    f"obligation update for `{key}`."
                ),
                blocks_process_gate_open=True,
            )
        )
    return tuple(items)


def _closure_prerequisites(
    dashboard: Lemma0252BlockerClosureDashboard,
) -> tuple[AnalyticPrerequisite, ...]:
    required_discharged = dashboard.substantive_blocker_count
    return (
        AnalyticPrerequisite(
            family="closure",
            prerequisite_key="closure.verdict_not_blocked",
            current_state=f"closure_verdict={dashboard.closure_verdict}",
            required_state="closure_verdict=closed_with_discharge or equivalent reviewed non-blocked state",
            satisfied=dashboard.closure_verdict != "blocked_no_discharge",
            source_artifact="track-a-regularity/reports/lemma_0252_blocker_closure_dashboard.json",
            discharge_artifact_required=(
                "Refresh the closure dashboard only after all substantive branches have reviewed "
                "discharge evidence."
            ),
            blocks_process_gate_open=dashboard.closure_verdict == "blocked_no_discharge",
        ),
        AnalyticPrerequisite(
            family="closure",
            prerequisite_key="closure.no_unresolved_branches",
            current_state=f"unresolved_branch_count={dashboard.unresolved_branch_count}",
            required_state="unresolved_branch_count=0",
            satisfied=dashboard.unresolved_branch_count == 0,
            source_artifact="track-a-regularity/reports/lemma_0252_blocker_closure_dashboard.json",
            discharge_artifact_required=(
                "Resolve finite-bound-to-smallness, compactness/Liouville, and smooth-continuation "
                "branches with reviewed theorem artifacts."
            ),
            blocks_process_gate_open=dashboard.unresolved_branch_count > 0,
        ),
        AnalyticPrerequisite(
            family="closure",
            prerequisite_key="closure.all_substantive_blockers_discharged",
            current_state=(
                f"discharged_blocker_count={dashboard.discharged_blocker_count}; "
                f"required={required_discharged}"
            ),
            required_state=f"discharged_blocker_count={required_discharged}",
            satisfied=dashboard.discharged_blocker_count == required_discharged,
            source_artifact="track-a-regularity/reports/lemma_0252_blocker_closure_dashboard.json",
            discharge_artifact_required=(
                "Each substantive branch must identify an applicable theorem or a new proved "
                "result in the exact solution class."
            ),
            blocks_process_gate_open=dashboard.discharged_blocker_count != required_discharged,
        ),
        AnalyticPrerequisite(
            family="closure",
            prerequisite_key="closure.candidate_emission_authorized",
            current_state=f"candidate_emission_authorized={str(dashboard.candidate_emission_authorized).lower()}",
            required_state="candidate_emission_authorized=true",
            satisfied=dashboard.candidate_emission_authorized,
            source_artifact="track-a-regularity/reports/lemma_0252_blocker_closure_dashboard.json",
            discharge_artifact_required=(
                "Candidate emission authorization must come from closure evidence, not from "
                "checklist presence."
            ),
            blocks_process_gate_open=not dashboard.candidate_emission_authorized,
        ),
    )


def _family_summaries(
    prerequisites: tuple[AnalyticPrerequisite, ...]
) -> tuple[FamilyPrerequisiteSummary, ...]:
    summaries: list[FamilyPrerequisiteSummary] = []
    for family in EXPECTED_FAMILIES:
        family_items = tuple(item for item in prerequisites if item.family == family)
        summaries.append(
            FamilyPrerequisiteSummary(
                family=family,
                prerequisite_count=len(family_items),
                satisfied_count=sum(1 for item in family_items if item.satisfied),
                unsatisfied_count=sum(1 for item in family_items if not item.satisfied),
                blocks_process_gate_open=any(item.blocks_process_gate_open for item in family_items),
                source_artifacts=tuple(sorted({item.source_artifact for item in family_items})),
            )
        )
    return tuple(summaries)


def _missing_sources() -> tuple[str, ...]:
    return tuple(source for source in SOURCE_REFS if not (ROOT / source).exists())


def build_analytic_prerequisite_packet(
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
    smoke_summary: Path = DEFAULT_SMOKE_SUMMARY,
    proof_graph_json: Path = DEFAULT_PROOF_GRAPH_JSON,
) -> AnalyticPrerequisitePacket:
    readiness = build_action_readiness(candidate_dir=candidate_dir, smoke_summary=smoke_summary)
    closure_dashboard = build_blocker_closure_dashboard(proof_obligation_json=proof_graph_json)
    candidate_status, active_candidate = _proof_graph_state(proof_graph_json)
    proof_items = _proof_prerequisites(proof_graph_json)
    closure_items = _closure_prerequisites(closure_dashboard)
    prerequisites = proof_items + closure_items
    family_summaries = _family_summaries(prerequisites)
    missing_sources = _missing_sources()
    unsatisfied_count = sum(1 for item in prerequisites if not item.satisfied)
    blocked_by = tuple(summary.family for summary in family_summaries if summary.blocks_process_gate_open)
    process_gate_open_authorized = (
        readiness.process_actionable_count > 0
        and readiness.promotion_action_authorized
        and unsatisfied_count == 0
        and not blocked_by
        and not missing_sources
    )

    return AnalyticPrerequisitePacket(
        schema_version=1,
        candidate_dir=readiness.candidate_dir,
        lemma_id=closure_dashboard.lemma_id,
        candidate_status=candidate_status,
        active_candidate=active_candidate,
        process_families_waiting=PROCESS_FAMILIES,
        analytic_families=EXPECTED_FAMILIES,
        source_blocker_count=readiness.source_blocker_count,
        analytic_blocker_count=readiness.analytic_blocker_count,
        process_actionable_count=readiness.process_actionable_count,
        process_blocked_by_analytic_count=readiness.process_blocked_by_analytic_count,
        closure_verdict=closure_dashboard.closure_verdict,
        promotion_blocker_count=len(_promotion_blockers(proof_graph_json)),
        closure_unresolved_branch_count=closure_dashboard.unresolved_branch_count,
        closure_discharged_blocker_count=closure_dashboard.discharged_blocker_count,
        prerequisite_count=len(prerequisites),
        satisfied_prerequisite_count=len(prerequisites) - unsatisfied_count,
        unsatisfied_prerequisite_count=unsatisfied_count,
        process_gate_open_authorized=process_gate_open_authorized,
        process_gate_open_blocked_by=blocked_by,
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        prerequisites=prerequisites,
        family_summaries=family_summaries,
        source_refs=SOURCE_REFS,
        non_claims=NON_CLAIMS,
    )


def packet_to_dict(packet: AnalyticPrerequisitePacket) -> dict[str, object]:
    return {
        "schema_version": packet.schema_version,
        "candidate_dir": packet.candidate_dir,
        "lemma_id": packet.lemma_id,
        "candidate_status": packet.candidate_status,
        "active_candidate": packet.active_candidate,
        "process_families_waiting": list(packet.process_families_waiting),
        "analytic_families": list(packet.analytic_families),
        "source_blocker_count": packet.source_blocker_count,
        "analytic_blocker_count": packet.analytic_blocker_count,
        "process_actionable_count": packet.process_actionable_count,
        "process_blocked_by_analytic_count": packet.process_blocked_by_analytic_count,
        "closure_verdict": packet.closure_verdict,
        "promotion_blocker_count": packet.promotion_blocker_count,
        "closure_unresolved_branch_count": packet.closure_unresolved_branch_count,
        "closure_discharged_blocker_count": packet.closure_discharged_blocker_count,
        "prerequisite_count": packet.prerequisite_count,
        "satisfied_prerequisite_count": packet.satisfied_prerequisite_count,
        "unsatisfied_prerequisite_count": packet.unsatisfied_prerequisite_count,
        "process_gate_open_authorized": packet.process_gate_open_authorized,
        "process_gate_open_blocked_by": list(packet.process_gate_open_blocked_by),
        "missing_source_count": packet.missing_source_count,
        "missing_sources": list(packet.missing_sources),
        "prerequisites": [asdict(item) for item in packet.prerequisites],
        "family_summaries": [asdict(summary) for summary in packet.family_summaries],
        "source_refs": list(packet.source_refs),
        "non_claims": list(packet.non_claims),
        "docs": {
            "action_readiness_doc": "docs/STEP95_PROMOTION_GATE_ACTION_READINESS.md",
            "blocker_ledger_doc": "docs/STEP94_PROMOTION_GATE_BLOCKER_LEDGER.md",
            "closure_dashboard_doc": "docs/STEP91_BLOCKER_CLOSURE_DASHBOARD.md",
        },
        "canonical_reports": {
            "action_readiness_markdown": str(DEFAULT_READINESS_MARKDOWN_OUTPUT),
            "action_readiness_json": str(DEFAULT_READINESS_JSON_OUTPUT),
            "closure_dashboard_markdown": str(DEFAULT_CLOSURE_MARKDOWN_OUTPUT),
            "closure_dashboard_json": str(DEFAULT_CLOSURE_JSON_OUTPUT),
            "proof_obligation_graph_json": str(DEFAULT_PROOF_GRAPH_JSON),
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _family_rows(packet: AnalyticPrerequisitePacket) -> list[str]:
    rows = [
        "| family | prerequisites | satisfied | unsatisfied | blocks process gates | source artifacts |",
        "|---|---:|---:|---:|---|---|",
    ]
    for summary in packet.family_summaries:
        rows.append(
            "| "
            f"`{summary.family}` | "
            f"{summary.prerequisite_count} | "
            f"{summary.satisfied_count} | "
            f"{summary.unsatisfied_count} | "
            f"`{str(summary.blocks_process_gate_open).lower()}` | "
            f"{'<br>'.join(f'`{artifact}`' for artifact in summary.source_artifacts)} |"
        )
    return rows


def _prerequisite_rows(packet: AnalyticPrerequisitePacket) -> list[str]:
    rows = [
        "| family | prerequisite | current state | required state | satisfied | discharge artifact required |",
        "|---|---|---|---|---|---|",
    ]
    for item in packet.prerequisites:
        rows.append(
            "| "
            f"`{item.family}` | "
            f"`{item.prerequisite_key}` | "
            f"`{_format(item.current_state)}` | "
            f"{_format(item.required_state)} | "
            f"`{str(item.satisfied).lower()}` | "
            f"{_format(item.discharge_artifact_required)} |"
        )
    return rows


def render_markdown(packet: AnalyticPrerequisitePacket) -> str:
    return "\n".join(
        (
            "# Promotion Gate Analytic Prerequisites",
            "",
            "Generated by `track-a-regularity/evaluator/promotion_gate_analytic_prerequisites.py`.",
            "",
            "This read-only packet lists the analytic discharge prerequisites that must be met",
            "before any process gate can open. It does not discharge blockers or promote a candidate.",
            "",
            "## Summary",
            "",
            f"- lemma_id: `{packet.lemma_id}`",
            f"- candidate_status: `{packet.candidate_status}`",
            f"- active_candidate: `{str(packet.active_candidate).lower()}`",
            f"- source_blocker_count: `{packet.source_blocker_count}`",
            f"- analytic_blocker_count: `{packet.analytic_blocker_count}`",
            f"- process_actionable_count: `{packet.process_actionable_count}`",
            f"- process_blocked_by_analytic_count: `{packet.process_blocked_by_analytic_count}`",
            f"- closure_verdict: `{packet.closure_verdict}`",
            f"- promotion_blocker_count: `{packet.promotion_blocker_count}`",
            f"- closure_unresolved_branch_count: `{packet.closure_unresolved_branch_count}`",
            f"- closure_discharged_blocker_count: `{packet.closure_discharged_blocker_count}`",
            f"- prerequisite_count: `{packet.prerequisite_count}`",
            f"- satisfied_prerequisite_count: `{packet.satisfied_prerequisite_count}`",
            f"- unsatisfied_prerequisite_count: `{packet.unsatisfied_prerequisite_count}`",
            f"- process_gate_open_authorized: `{str(packet.process_gate_open_authorized).lower()}`",
            f"- process_gate_open_blocked_by: `{', '.join(packet.process_gate_open_blocked_by) or 'none'}`",
            f"- missing_source_count: `{packet.missing_source_count}`",
            "",
            "## Family Summary",
            "",
            *_family_rows(packet),
            "",
            "## Prerequisites",
            "",
            *_prerequisite_rows(packet),
            "",
            "## Non-Claims",
            "",
            *(f"- `{item}`" for item in packet.non_claims),
            "",
        )
    )


def render_json(packet: AnalyticPrerequisitePacket) -> str:
    return json.dumps(packet_to_dict(packet), indent=2, sort_keys=True) + "\n"


def render_output(packet: AnalyticPrerequisitePacket, output_format: str) -> str:
    if output_format == "markdown":
        return render_markdown(packet)
    if output_format == "json":
        return render_json(packet)
    raise ValueError(f"unknown analytic prerequisite packet format: {output_format}")


def write_output(output: Path, packet: AnalyticPrerequisitePacket, output_format: str) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(packet, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    packet: AnalyticPrerequisitePacket,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(packet, output_format)
    if not output.exists():
        return False, f"missing promotion gate analytic prerequisite packet: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale promotion gate analytic prerequisite packet: {output}"
    return True, f"fresh promotion gate analytic prerequisite packet: {output}"


def check_blocked(packet: AnalyticPrerequisitePacket) -> tuple[bool, str]:
    if packet.process_gate_open_authorized:
        return False, "process gate open became authorized"
    if packet.satisfied_prerequisite_count:
        return False, "analytic prerequisites unexpectedly appear satisfied"
    if packet.unsatisfied_prerequisite_count != packet.prerequisite_count:
        return False, "not all analytic prerequisites are explicitly unsatisfied"
    if tuple(packet.process_gate_open_blocked_by) != EXPECTED_FAMILIES:
        return False, "process gate open is not blocked by both expected analytic families"
    return True, "analytic prerequisite packet remains blocked"


def check_expected_families(packet: AnalyticPrerequisitePacket) -> tuple[bool, str]:
    families = tuple(summary.family for summary in packet.family_summaries)
    if families != EXPECTED_FAMILIES:
        return False, f"expected analytic families {EXPECTED_FAMILIES}, found {families}"
    if packet.analytic_blocker_count != len(EXPECTED_FAMILIES):
        return False, "readiness source does not expose the two analytic blockers"
    return True, "analytic prerequisite packet covers expected families"


def check_sources(packet: AnalyticPrerequisitePacket) -> tuple[bool, str]:
    if packet.missing_source_count:
        return False, "missing analytic prerequisite sources: " + ", ".join(packet.missing_sources)
    return True, "all analytic prerequisite sources exist"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown analytic prerequisite packet format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a read-only packet of analytic blocker discharge prerequisites."
    )
    parser.add_argument("--candidate-dir", type=Path, default=DEFAULT_CANDIDATE_DIR)
    parser.add_argument("--smoke-summary", type=Path, default=DEFAULT_SMOKE_SUMMARY)
    parser.add_argument("--proof-graph-json", type=Path, default=DEFAULT_PROOF_GRAPH_JSON)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    parser.add_argument("--require-expected-families", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    args = parser.parse_args(argv)

    try:
        packet = build_analytic_prerequisite_packet(
            candidate_dir=args.candidate_dir,
            smoke_summary=args.smoke_summary,
            proof_graph_json=args.proof_graph_json,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report setup failures.
        print(f"failed to build analytic prerequisite packet: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, packet, args.format)
        print(message)
        if not ok:
            print("run without --check-output to regenerate the analytic prerequisite packet", file=sys.stderr)
            return 1
    else:
        written = write_output(output, packet, args.format)
        print(f"wrote {written}")

    if args.require_blocked:
        ok, message = check_blocked(packet)
        print(message)
        if not ok:
            return 1
    if args.require_expected_families:
        ok, message = check_expected_families(packet)
        print(message)
        if not ok:
            return 1
    if args.require_sources_exist:
        ok, message = check_sources(packet)
        print(message)
        if not ok:
            return 1

    print(f"prerequisite_count: {packet.prerequisite_count}")
    print(f"satisfied_prerequisite_count: {packet.satisfied_prerequisite_count}")
    print(f"unsatisfied_prerequisite_count: {packet.unsatisfied_prerequisite_count}")
    print(f"process_gate_open_authorized: {str(packet.process_gate_open_authorized).lower()}")
    print(f"process_gate_open_blocked_by: {', '.join(packet.process_gate_open_blocked_by) or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
