from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from promotion_gate_blocker_ledger import (
    BLOCKER_KIND_BY_FAMILY,
    DEFAULT_JSON_OUTPUT as DEFAULT_LEDGER_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_LEDGER_MARKDOWN_OUTPUT,
    DEFAULT_REPORT_DIR,
    BlockerLedgerEntry,
    PromotionGateBlockerLedger,
    build_blocker_ledger,
)
from promotion_gate_regression import DEFAULT_CANDIDATE_DIR, DEFAULT_SMOKE_SUMMARY


DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "promotion_gate_action_readiness.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "promotion_gate_action_readiness.json"
ANALYTIC_FAMILIES = ("proof_obligation", "closure")
PROCESS_FAMILIES = ("staging", "manual_packet", "lifecycle", "v4_preflight")
NON_CLAIMS = (
    "promotion_action_readiness_only",
    "read_only_priority_surface",
    "no_process_gate_discharge",
    "no_file_copy",
    "no_candidate_emission",
    "no_candidate_promotion",
    "no_blocker_discharge",
    "no_navier_stokes_solution",
    "no_epsilon_regularity_theorem",
    "no_weak_to_smooth_upgrade",
)


@dataclass(frozen=True)
class ReadinessEntry:
    action_family: str
    blocker_kind: str
    gate_key: str
    status: str
    priority_tier: int
    readiness_state: str
    actionable_now: bool
    waiting_on: tuple[str, ...]
    operator_instruction: str


@dataclass(frozen=True)
class PromotionGateActionReadiness:
    schema_version: int
    candidate_dir: str
    ledger_markdown: str
    ledger_json: str
    real_emission_ready: bool
    source_blocker_count: int
    analytic_blocker_count: int
    process_blocker_count: int
    analytic_first_guard_active: bool
    process_actionable_count: int
    process_blocked_by_analytic_count: int
    analytic_focus_count: int
    promotion_action_authorized: bool
    hard_failure_count: int
    issues: tuple[str, ...]
    entries: tuple[ReadinessEntry, ...]
    non_claims: tuple[str, ...]


def _analytic_blockers(ledger: PromotionGateBlockerLedger) -> tuple[BlockerLedgerEntry, ...]:
    return tuple(entry for entry in ledger.entries if entry.action_family in ANALYTIC_FAMILIES)


def _entry_readiness(
    entry: BlockerLedgerEntry,
    analytic_waiting_on: tuple[str, ...],
) -> ReadinessEntry:
    if entry.action_family in ANALYTIC_FAMILIES:
        return ReadinessEntry(
            action_family=entry.action_family,
            blocker_kind=entry.blocker_kind,
            gate_key=entry.gate_key,
            status=entry.status,
            priority_tier=1,
            readiness_state="analytic_first_research_focus",
            actionable_now=True,
            waiting_on=(),
            operator_instruction=(
                "Only analytic proof-obligation or closure work can move this family; "
                "do not treat this as candidate promotion."
            ),
        )
    if entry.action_family in PROCESS_FAMILIES:
        return ReadinessEntry(
            action_family=entry.action_family,
            blocker_kind=entry.blocker_kind,
            gate_key=entry.gate_key,
            status=entry.status,
            priority_tier=2,
            readiness_state="waiting_on_analytic_blockers",
            actionable_now=False,
            waiting_on=analytic_waiting_on,
            operator_instruction=(
                "Keep this process gate blocked until proof_obligation and closure blockers "
                "are genuinely discharged."
            ),
        )
    return ReadinessEntry(
        action_family=entry.action_family,
        blocker_kind=entry.blocker_kind,
        gate_key=entry.gate_key,
        status=entry.status,
        priority_tier=99,
        readiness_state="unknown_family_requires_classification",
        actionable_now=False,
        waiting_on=analytic_waiting_on,
        operator_instruction="Classify this family before any promotion action.",
    )


def build_action_readiness(
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
    smoke_summary: Path = DEFAULT_SMOKE_SUMMARY,
    ledger_markdown: Path = DEFAULT_LEDGER_MARKDOWN_OUTPUT,
    ledger_json: Path = DEFAULT_LEDGER_JSON_OUTPUT,
) -> PromotionGateActionReadiness:
    ledger = build_blocker_ledger(candidate_dir=candidate_dir, smoke_summary=smoke_summary)
    analytic_entries = _analytic_blockers(ledger)
    analytic_waiting_on = tuple(entry.action_family for entry in analytic_entries)
    entries = tuple(_entry_readiness(entry, analytic_waiting_on) for entry in ledger.entries)

    issues: list[str] = []
    if not analytic_entries:
        issues.append("missing analytic blockers; process gates must not become actionable by default")
    if ledger.source_failure_gate_count:
        issues.append("source promotion gate regression has hard failures")
    if not ledger.closure_dependency_consistent:
        issues.append("source closure dependency is inconsistent")

    process_entries = tuple(entry for entry in entries if entry.action_family in PROCESS_FAMILIES)
    process_actionable_count = sum(1 for entry in process_entries if entry.actionable_now)
    process_blocked_by_analytic_count = sum(
        1
        for entry in process_entries
        if entry.readiness_state == "waiting_on_analytic_blockers" and entry.waiting_on
    )
    if analytic_entries and process_actionable_count:
        issues.append("process blockers became actionable while analytic blockers remain")

    promotion_action_authorized = (
        ledger.real_emission_ready
        and not issues
        and not analytic_entries
        and process_actionable_count == len(process_entries)
    )

    return PromotionGateActionReadiness(
        schema_version=1,
        candidate_dir=ledger.candidate_dir,
        ledger_markdown=str(ledger_markdown),
        ledger_json=str(ledger_json),
        real_emission_ready=ledger.real_emission_ready,
        source_blocker_count=ledger.blocker_count,
        analytic_blocker_count=len(analytic_entries),
        process_blocker_count=len(process_entries),
        analytic_first_guard_active=bool(analytic_entries) and process_actionable_count == 0,
        process_actionable_count=process_actionable_count,
        process_blocked_by_analytic_count=process_blocked_by_analytic_count,
        analytic_focus_count=sum(1 for entry in entries if entry.action_family in ANALYTIC_FAMILIES),
        promotion_action_authorized=promotion_action_authorized,
        hard_failure_count=ledger.source_failure_gate_count,
        issues=tuple(issues),
        entries=entries,
        non_claims=NON_CLAIMS,
    )


def action_readiness_to_dict(readiness: PromotionGateActionReadiness) -> dict[str, object]:
    return {
        "schema_version": readiness.schema_version,
        "candidate_dir": readiness.candidate_dir,
        "ledger_markdown": readiness.ledger_markdown,
        "ledger_json": readiness.ledger_json,
        "real_emission_ready": readiness.real_emission_ready,
        "source_blocker_count": readiness.source_blocker_count,
        "analytic_blocker_count": readiness.analytic_blocker_count,
        "process_blocker_count": readiness.process_blocker_count,
        "analytic_first_guard_active": readiness.analytic_first_guard_active,
        "process_actionable_count": readiness.process_actionable_count,
        "process_blocked_by_analytic_count": readiness.process_blocked_by_analytic_count,
        "analytic_focus_count": readiness.analytic_focus_count,
        "promotion_action_authorized": readiness.promotion_action_authorized,
        "hard_failure_count": readiness.hard_failure_count,
        "issues": list(readiness.issues),
        "entries": [asdict(entry) for entry in readiness.entries],
        "non_claims": list(readiness.non_claims),
        "family_kinds": dict(BLOCKER_KIND_BY_FAMILY),
        "docs": {
            "blocker_ledger_doc": "docs/STEP94_PROMOTION_GATE_BLOCKER_LEDGER.md",
            "gate_regression_doc": "docs/STEP86_PROMOTION_GATE_REGRESSION.md",
            "closure_dependency_doc": "docs/STEP93_PROMOTION_GATE_CLOSURE_DEPENDENCY.md",
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _entry_rows(readiness: PromotionGateActionReadiness) -> list[str]:
    rows = [
        "| family | gate | tier | state | actionable now | waiting on | instruction |",
        "|---|---|---:|---|---|---|---|",
    ]
    for entry in readiness.entries:
        waiting_on = ", ".join(entry.waiting_on) or "none"
        rows.append(
            "| "
            f"`{entry.action_family}` | "
            f"`{entry.gate_key}` | "
            f"{entry.priority_tier} | "
            f"`{entry.readiness_state}` | "
            f"`{str(entry.actionable_now).lower()}` | "
            f"`{waiting_on}` | "
            f"{_format(entry.operator_instruction)} |"
        )
    return rows


def render_markdown(readiness: PromotionGateActionReadiness) -> str:
    return "\n".join(
        (
            "# Promotion Gate Action Readiness",
            "",
            "Generated by `track-a-regularity/evaluator/promotion_gate_action_readiness.py`.",
            "",
            "This read-only dashboard prevents process blockers from being treated as actionable",
            "while analytic proof-obligation or closure blockers remain unresolved.",
            "",
            "## Summary",
            "",
            f"- candidate_dir: `{readiness.candidate_dir}`",
            f"- ledger_markdown: `{readiness.ledger_markdown}`",
            f"- ledger_json: `{readiness.ledger_json}`",
            f"- real_emission_ready: `{str(readiness.real_emission_ready).lower()}`",
            f"- source_blocker_count: `{readiness.source_blocker_count}`",
            f"- analytic_blocker_count: `{readiness.analytic_blocker_count}`",
            f"- process_blocker_count: `{readiness.process_blocker_count}`",
            f"- analytic_first_guard_active: `{str(readiness.analytic_first_guard_active).lower()}`",
            f"- process_actionable_count: `{readiness.process_actionable_count}`",
            f"- process_blocked_by_analytic_count: `{readiness.process_blocked_by_analytic_count}`",
            f"- analytic_focus_count: `{readiness.analytic_focus_count}`",
            f"- promotion_action_authorized: `{str(readiness.promotion_action_authorized).lower()}`",
            f"- hard_failure_count: `{readiness.hard_failure_count}`",
            f"- issues: `{', '.join(readiness.issues) or 'none'}`",
            "",
            "## Readiness Rows",
            "",
            *_entry_rows(readiness),
            "",
            "## Non-Claims",
            "",
            *(f"- `{item}`" for item in readiness.non_claims),
            "",
        )
    )


def render_json(readiness: PromotionGateActionReadiness) -> str:
    return json.dumps(action_readiness_to_dict(readiness), indent=2, sort_keys=True) + "\n"


def render_output(readiness: PromotionGateActionReadiness, output_format: str) -> str:
    if output_format == "markdown":
        return render_markdown(readiness)
    if output_format == "json":
        return render_json(readiness)
    raise ValueError(f"unknown promotion gate action readiness format: {output_format}")


def write_output(output: Path, readiness: PromotionGateActionReadiness, output_format: str) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(readiness, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    readiness: PromotionGateActionReadiness,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(readiness, output_format)
    if not output.exists():
        return False, f"missing promotion gate action readiness report: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale promotion gate action readiness report: {output}"
    return True, f"fresh promotion gate action readiness report: {output}"


def check_analytic_first(readiness: PromotionGateActionReadiness) -> tuple[bool, str]:
    if not readiness.analytic_first_guard_active:
        return False, "analytic-first guard is not active"
    if readiness.analytic_blocker_count != len(ANALYTIC_FAMILIES):
        return False, "analytic-first guard expected proof_obligation and closure blockers"
    return True, "analytic-first guard is active"


def check_no_process_action(readiness: PromotionGateActionReadiness) -> tuple[bool, str]:
    if readiness.process_actionable_count:
        return False, "process blockers are actionable while analytic blockers remain"
    if readiness.process_blocked_by_analytic_count != readiness.process_blocker_count:
        return False, "not all process blockers are waiting on analytic blockers"
    return True, "all process blockers are waiting on analytic blockers"


def check_no_promotion_authorization(readiness: PromotionGateActionReadiness) -> tuple[bool, str]:
    if readiness.promotion_action_authorized:
        return False, "promotion action became authorized"
    if readiness.real_emission_ready:
        return False, "real emission became ready"
    if readiness.hard_failure_count:
        return False, "source readiness has hard failures"
    if readiness.issues:
        return False, f"promotion gate action readiness issues: {', '.join(readiness.issues)}"
    return True, "promotion action remains unauthorized"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown promotion gate action readiness format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a read-only readiness guard for promotion gate actions."
    )
    parser.add_argument("--candidate-dir", type=Path, default=DEFAULT_CANDIDATE_DIR)
    parser.add_argument("--smoke-summary", type=Path, default=DEFAULT_SMOKE_SUMMARY)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-analytic-first", action="store_true")
    parser.add_argument("--require-no-process-action", action="store_true")
    parser.add_argument("--require-no-promotion-authorization", action="store_true")
    args = parser.parse_args(argv)

    try:
        readiness = build_action_readiness(
            candidate_dir=args.candidate_dir,
            smoke_summary=args.smoke_summary,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report readiness setup failures.
        print(f"failed to build promotion gate action readiness report: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, readiness, args.format)
        print(message)
        if not ok:
            print("run without --check-output to regenerate the action readiness report", file=sys.stderr)
            return 1
    else:
        written = write_output(output, readiness, args.format)
        print(f"wrote {written}")

    if args.require_analytic_first:
        ok, message = check_analytic_first(readiness)
        print(message)
        if not ok:
            return 1
    if args.require_no_process_action:
        ok, message = check_no_process_action(readiness)
        print(message)
        if not ok:
            return 1
    if args.require_no_promotion_authorization:
        ok, message = check_no_promotion_authorization(readiness)
        print(message)
        if not ok:
            return 1

    print(f"analytic_first_guard_active: {str(readiness.analytic_first_guard_active).lower()}")
    print(f"process_actionable_count: {readiness.process_actionable_count}")
    print(f"process_blocked_by_analytic_count: {readiness.process_blocked_by_analytic_count}")
    print(f"promotion_action_authorized: {str(readiness.promotion_action_authorized).lower()}")
    print(f"issues: {', '.join(readiness.issues) or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
