from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from promotion_gate_regression import (
    DEFAULT_CANDIDATE_DIR,
    DEFAULT_REPORT_DIR,
    DEFAULT_SMOKE_SUMMARY,
    GateCheck,
    PromotionGateRegression,
    build_gate_regression,
)


DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "promotion_gate_blocker_ledger.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "promotion_gate_blocker_ledger.json"
EXPECTED_BLOCKING_FAMILIES = (
    "staging",
    "manual_packet",
    "lifecycle",
    "proof_obligation",
    "closure",
    "v4_preflight",
)
ACTION_FAMILY_BY_GATE = {
    "staged_candidate_ready": "staging",
    "manual_promotion_packet_ready": "manual_packet",
    "promotion_lifecycle_ready_or_authorized": "lifecycle",
    "proof_obligation_zero_blocker_real_candidate": "proof_obligation",
    "lemma_0252_blocker_closure_not_blocked": "closure",
    "v4_preflight_current_pool": "v4_preflight",
}
BLOCKER_KIND_BY_FAMILY = {
    "staging": "process_blocker",
    "manual_packet": "process_blocker",
    "lifecycle": "process_blocker",
    "proof_obligation": "analytic_blocker",
    "closure": "analytic_closure_blocker",
    "v4_preflight": "process_blocker",
}
NEXT_ACTION_BY_FAMILY = {
    "staging": "Do not stage a real YAML until a genuine zero-blocker proof route exists.",
    "manual_packet": "Keep the packet blocked until a real staged YAML is ready for manual copy.",
    "lifecycle": "Keep lifecycle blocked until staging and manual packet are both ready.",
    "proof_obligation": "Discharge real proof-obligation blockers before treating any candidate as active.",
    "closure": "Resolve closure_verdict=blocked_no_discharge through genuine blocker discharge.",
    "v4_preflight": "Only run active-pool v4 preflight on real candidate-status YAML after upstream gates pass.",
}
NON_CLAIMS = (
    "promotion_blocker_ledger_only",
    "read_only_operator_surface",
    "no_file_copy",
    "no_candidate_emission",
    "no_candidate_promotion",
    "no_blocker_discharge",
    "no_navier_stokes_solution",
    "no_epsilon_regularity_theorem",
    "no_weak_to_smooth_upgrade",
)


@dataclass(frozen=True)
class BlockerLedgerEntry:
    gate_key: str
    action_family: str
    blocker_kind: str
    artifact: str
    status: str
    blocks_real_emission: bool
    current_state: str
    required_for_real_emission: str
    operator_next_action: str


@dataclass(frozen=True)
class FamilySummary:
    action_family: str
    blocker_kind: str
    blocker_count: int
    gate_keys: tuple[str, ...]


@dataclass(frozen=True)
class PromotionGateBlockerLedger:
    schema_version: int
    candidate_dir: str
    source_gate_count: int
    source_blocking_gate_count: int
    source_failure_gate_count: int
    real_emission_ready: bool
    closure_dependency_consistent: bool
    blocker_count: int
    known_family_blocker_count: int
    unknown_family_blocker_count: int
    expected_family_count: int
    missing_expected_families: tuple[str, ...]
    unexpected_families: tuple[str, ...]
    process_blocker_count: int
    analytic_blocker_count: int
    analytic_closure_blocker_count: int
    entries: tuple[BlockerLedgerEntry, ...]
    family_summaries: tuple[FamilySummary, ...]
    non_claims: tuple[str, ...]


def _blocking_gates(regression: PromotionGateRegression) -> tuple[GateCheck, ...]:
    return tuple(gate for gate in regression.gates if gate.status == "blocked")


def _entry_from_gate(gate: GateCheck) -> BlockerLedgerEntry:
    action_family = ACTION_FAMILY_BY_GATE.get(gate.gate_key, "unknown")
    blocker_kind = BLOCKER_KIND_BY_FAMILY.get(action_family, "unknown_blocker")
    return BlockerLedgerEntry(
        gate_key=gate.gate_key,
        action_family=action_family,
        blocker_kind=blocker_kind,
        artifact=gate.artifact,
        status=gate.status,
        blocks_real_emission=gate.blocks_real_emission,
        current_state=gate.current_state,
        required_for_real_emission=gate.required_for_real_emission,
        operator_next_action=NEXT_ACTION_BY_FAMILY.get(
            action_family,
            "Classify this gate before attempting a promotion action.",
        ),
    )


def build_blocker_ledger(
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
    smoke_summary: Path = DEFAULT_SMOKE_SUMMARY,
) -> PromotionGateBlockerLedger:
    regression = build_gate_regression(
        candidate_dir=candidate_dir,
        smoke_summary=smoke_summary,
    )
    entries = tuple(_entry_from_gate(gate) for gate in _blocking_gates(regression))
    observed_families = tuple(entry.action_family for entry in entries)
    missing_expected = tuple(
        family for family in EXPECTED_BLOCKING_FAMILIES if family not in observed_families
    )
    unexpected = tuple(
        family
        for family in sorted(set(observed_families))
        if family not in EXPECTED_BLOCKING_FAMILIES
    )
    family_summaries = tuple(
        FamilySummary(
            action_family=family,
            blocker_kind=BLOCKER_KIND_BY_FAMILY.get(family, "unknown_blocker"),
            blocker_count=sum(1 for entry in entries if entry.action_family == family),
            gate_keys=tuple(entry.gate_key for entry in entries if entry.action_family == family),
        )
        for family in EXPECTED_BLOCKING_FAMILIES
        if family in observed_families
    )

    return PromotionGateBlockerLedger(
        schema_version=1,
        candidate_dir=regression.candidate_dir,
        source_gate_count=regression.gate_count,
        source_blocking_gate_count=regression.blocking_gate_count,
        source_failure_gate_count=regression.failure_gate_count,
        real_emission_ready=regression.real_emission_ready,
        closure_dependency_consistent=regression.closure_dependency.consistent,
        blocker_count=len(entries),
        known_family_blocker_count=sum(1 for entry in entries if entry.action_family != "unknown"),
        unknown_family_blocker_count=sum(1 for entry in entries if entry.action_family == "unknown"),
        expected_family_count=len(EXPECTED_BLOCKING_FAMILIES),
        missing_expected_families=missing_expected,
        unexpected_families=unexpected,
        process_blocker_count=sum(1 for entry in entries if entry.blocker_kind == "process_blocker"),
        analytic_blocker_count=sum(1 for entry in entries if entry.blocker_kind == "analytic_blocker"),
        analytic_closure_blocker_count=sum(
            1 for entry in entries if entry.blocker_kind == "analytic_closure_blocker"
        ),
        entries=entries,
        family_summaries=family_summaries,
        non_claims=NON_CLAIMS,
    )


def blocker_ledger_to_dict(ledger: PromotionGateBlockerLedger) -> dict[str, object]:
    return {
        "schema_version": ledger.schema_version,
        "candidate_dir": ledger.candidate_dir,
        "source_gate_count": ledger.source_gate_count,
        "source_blocking_gate_count": ledger.source_blocking_gate_count,
        "source_failure_gate_count": ledger.source_failure_gate_count,
        "real_emission_ready": ledger.real_emission_ready,
        "closure_dependency_consistent": ledger.closure_dependency_consistent,
        "blocker_count": ledger.blocker_count,
        "known_family_blocker_count": ledger.known_family_blocker_count,
        "unknown_family_blocker_count": ledger.unknown_family_blocker_count,
        "expected_family_count": ledger.expected_family_count,
        "missing_expected_families": list(ledger.missing_expected_families),
        "unexpected_families": list(ledger.unexpected_families),
        "process_blocker_count": ledger.process_blocker_count,
        "analytic_blocker_count": ledger.analytic_blocker_count,
        "analytic_closure_blocker_count": ledger.analytic_closure_blocker_count,
        "entries": [asdict(entry) for entry in ledger.entries],
        "family_summaries": [asdict(summary) for summary in ledger.family_summaries],
        "non_claims": list(ledger.non_claims),
        "docs": {
            "gate_regression_doc": "docs/STEP86_PROMOTION_GATE_REGRESSION.md",
            "closure_integration_doc": "docs/STEP92_PROMOTION_GATE_CLOSURE_INTEGRATION.md",
            "closure_dependency_doc": "docs/STEP93_PROMOTION_GATE_CLOSURE_DEPENDENCY.md",
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _entry_rows(ledger: PromotionGateBlockerLedger) -> list[str]:
    rows = [
        "| gate | family | kind | status | artifact | current state | next action |",
        "|---|---|---|---|---|---|---|",
    ]
    for entry in ledger.entries:
        rows.append(
            "| "
            f"`{entry.gate_key}` | "
            f"`{entry.action_family}` | "
            f"`{entry.blocker_kind}` | "
            f"`{entry.status}` | "
            f"`{entry.artifact}` | "
            f"`{_format(entry.current_state)}` | "
            f"{_format(entry.operator_next_action)} |"
        )
    return rows


def _family_rows(ledger: PromotionGateBlockerLedger) -> list[str]:
    rows = [
        "| family | kind | blocker count | gate keys |",
        "|---|---|---:|---|",
    ]
    for summary in ledger.family_summaries:
        rows.append(
            "| "
            f"`{summary.action_family}` | "
            f"`{summary.blocker_kind}` | "
            f"{summary.blocker_count} | "
            f"{'<br>'.join(f'`{key}`' for key in summary.gate_keys)} |"
        )
    return rows


def render_markdown(ledger: PromotionGateBlockerLedger) -> str:
    return "\n".join(
        (
            "# Promotion Gate Blocker Ledger",
            "",
            "Generated by `track-a-regularity/evaluator/promotion_gate_blocker_ledger.py`.",
            "",
            "This read-only ledger classifies the current promotion-blocking gates by operator",
            "action family. It does not emit, copy, or promote candidate YAML.",
            "",
            "## Summary",
            "",
            f"- candidate_dir: `{ledger.candidate_dir}`",
            f"- real_emission_ready: `{str(ledger.real_emission_ready).lower()}`",
            f"- closure_dependency_consistent: `{str(ledger.closure_dependency_consistent).lower()}`",
            f"- source_gate_count: `{ledger.source_gate_count}`",
            f"- source_blocking_gate_count: `{ledger.source_blocking_gate_count}`",
            f"- source_failure_gate_count: `{ledger.source_failure_gate_count}`",
            f"- blocker_count: `{ledger.blocker_count}`",
            f"- known_family_blocker_count: `{ledger.known_family_blocker_count}`",
            f"- unknown_family_blocker_count: `{ledger.unknown_family_blocker_count}`",
            f"- process_blocker_count: `{ledger.process_blocker_count}`",
            f"- analytic_blocker_count: `{ledger.analytic_blocker_count}`",
            f"- analytic_closure_blocker_count: `{ledger.analytic_closure_blocker_count}`",
            f"- missing_expected_families: `{', '.join(ledger.missing_expected_families) or 'none'}`",
            f"- unexpected_families: `{', '.join(ledger.unexpected_families) or 'none'}`",
            "",
            "## Family Summary",
            "",
            *_family_rows(ledger),
            "",
            "## Blocking Gates",
            "",
            *_entry_rows(ledger),
            "",
            "## Non-Claims",
            "",
            *(f"- `{item}`" for item in ledger.non_claims),
            "",
        )
    )


def render_json(ledger: PromotionGateBlockerLedger) -> str:
    return json.dumps(blocker_ledger_to_dict(ledger), indent=2, sort_keys=True) + "\n"


def render_output(ledger: PromotionGateBlockerLedger, output_format: str) -> str:
    if output_format == "markdown":
        return render_markdown(ledger)
    if output_format == "json":
        return render_json(ledger)
    raise ValueError(f"unknown promotion blocker ledger format: {output_format}")


def write_output(output: Path, ledger: PromotionGateBlockerLedger, output_format: str) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(ledger, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    ledger: PromotionGateBlockerLedger,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(ledger, output_format)
    if not output.exists():
        return False, f"missing promotion gate blocker ledger: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale promotion gate blocker ledger: {output}"
    return True, f"fresh promotion gate blocker ledger: {output}"


def check_expected_blockers(ledger: PromotionGateBlockerLedger) -> tuple[bool, str]:
    if ledger.blocker_count != ledger.expected_family_count:
        return False, (
            "promotion gate blocker ledger expected "
            f"{ledger.expected_family_count} blockers, found {ledger.blocker_count}"
        )
    if ledger.missing_expected_families:
        return False, (
            "promotion gate blocker ledger missing expected families: "
            f"{', '.join(ledger.missing_expected_families)}"
        )
    if ledger.unexpected_families or ledger.unknown_family_blocker_count:
        return False, "promotion gate blocker ledger has unknown or unexpected blocker families"
    return True, "promotion gate blocker ledger covers all expected blocker families"


def check_no_hard_failures(ledger: PromotionGateBlockerLedger) -> tuple[bool, str]:
    if ledger.source_failure_gate_count:
        return False, "promotion gate blocker ledger source regression has hard failures"
    if not ledger.closure_dependency_consistent:
        return False, "promotion gate blocker ledger source closure dependency is inconsistent"
    return True, "promotion gate blocker ledger has no source hard failures"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown promotion blocker ledger format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a read-only ledger of current promotion-blocking gate families."
    )
    parser.add_argument("--candidate-dir", type=Path, default=DEFAULT_CANDIDATE_DIR)
    parser.add_argument("--smoke-summary", type=Path, default=DEFAULT_SMOKE_SUMMARY)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-expected-blockers", action="store_true")
    parser.add_argument("--require-no-hard-failures", action="store_true")
    args = parser.parse_args(argv)

    try:
        ledger = build_blocker_ledger(
            candidate_dir=args.candidate_dir,
            smoke_summary=args.smoke_summary,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report ledger setup failures.
        print(f"failed to build promotion gate blocker ledger: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, ledger, args.format)
        print(message)
        if not ok:
            print("run without --check-output to regenerate the promotion gate blocker ledger", file=sys.stderr)
            return 1
    else:
        written = write_output(output, ledger, args.format)
        print(f"wrote {written}")

    if args.require_expected_blockers:
        ok, message = check_expected_blockers(ledger)
        print(message)
        if not ok:
            return 1
    if args.require_no_hard_failures:
        ok, message = check_no_hard_failures(ledger)
        print(message)
        if not ok:
            return 1

    print(f"blocker_count: {ledger.blocker_count}")
    print(f"known_family_blocker_count: {ledger.known_family_blocker_count}")
    print(f"unknown_family_blocker_count: {ledger.unknown_family_blocker_count}")
    print(f"process_blocker_count: {ledger.process_blocker_count}")
    print(f"analytic_blocker_count: {ledger.analytic_blocker_count}")
    print(f"analytic_closure_blocker_count: {ledger.analytic_closure_blocker_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
