from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

from lemma_0252_blocker_known_theorem_mapping import build_known_theorem_mapping
from lemma_0252_compactness_liouville_checklist import (
    build_compactness_liouville_checklist,
)
from lemma_0252_finite_bound_smallness_checklist import (
    build_finite_bound_smallness_checklist,
)
from lemma_0252_smooth_continuation_checklist import (
    build_smooth_continuation_checklist,
)
from proof_obligation_blockers import DEFAULT_INPUT


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "lemma_0252_blocker_closure_dashboard.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "lemma_0252_blocker_closure_dashboard.json"

EXPECTED_BRANCHES = (
    "finite_bound_to_smallness",
    "compactness_liouville",
    "smooth_continuation_bridge",
)
LOCAL_SOURCE_REFS = (
    "track-a-regularity/reports/lemma_0252_blocker_known_theorem_mapping.md",
    "track-a-regularity/reports/lemma_0252_blocker_known_theorem_mapping.json",
    "track-a-regularity/reports/lemma_0252_compactness_liouville_checklist.md",
    "track-a-regularity/reports/lemma_0252_compactness_liouville_checklist.json",
    "track-a-regularity/reports/lemma_0252_finite_bound_smallness_checklist.md",
    "track-a-regularity/reports/lemma_0252_finite_bound_smallness_checklist.json",
    "track-a-regularity/reports/lemma_0252_smooth_continuation_checklist.md",
    "track-a-regularity/reports/lemma_0252_smooth_continuation_checklist.json",
    "track-a-regularity/reports/lemma_0252_proof_obligation_graph.json",
    "docs/LEMMA_0252_PROOF_OBLIGATIONS.md",
    "docs/LEMMA_0252_LOCAL_ENERGY_FORMAL_MAP.md",
    "docs/STEP87_LEMMA_0252_KNOWN_THEOREM_MAPPING.md",
    "docs/STEP88_COMPACTNESS_LIOUVILLE_CHECKLIST.md",
    "docs/STEP89_FINITE_BOUND_SMALLNESS_CHECKLIST.md",
    "docs/STEP90_SMOOTH_CONTINUATION_CHECKLIST.md",
    "track-c-formal/lean/NavierStokesProgram/ProofObligationGraph.lean",
    "track-c-formal/lean/NavierStokesProgram/SolutionClasses.lean",
)
NON_CLAIMS = (
    "read_only_blocker_closure_dashboard",
    "checklist_presence_is_not_discharge",
    "no_candidate_promotion",
    "no_blocker_discharge",
    "no_epsilon_regularity_theorem",
    "no_compactness_or_liouville_theorem",
    "no_bkm_or_serrin_or_high_sobolev_bound",
    "no_weak_to_smooth_upgrade",
    "no_navier_stokes_solution",
)


@dataclass(frozen=True)
class BranchClosure:
    blocker_id: str
    checklist_report: str
    checklist_json: str
    branch_verdict: str
    mapping_row_count: int
    checklist_item_count: int
    theorem_branch_count: int
    dischargeable_now_count: int
    direct_theorem_branch_count: int
    closure_status: str
    candidate_emission_authorized: bool
    required_next_action: str


@dataclass(frozen=True)
class Lemma0252BlockerClosureDashboard:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    closure_verdict: str
    substantive_blocker_count: int
    checklist_branch_count: int
    discharged_blocker_count: int
    direct_known_route_count: int
    direct_theorem_branch_count: int
    unresolved_branch_count: int
    candidate_emission_authorized: bool
    checklist_presence_authorizes_candidate: bool
    all_expected_branches_present: bool
    branch_closures: tuple[BranchClosure, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]


def _mapping_row_count_by_blocker(blocker_id: str) -> int:
    mapping = build_known_theorem_mapping()
    return mapping.rows_per_blocker.get(blocker_id, 0)


def _direct_branch_count(theorem_branches: object) -> int:
    return sum(
        1
        for branch in theorem_branches  # type: ignore[union-attr]
        if getattr(branch, "applies_to_lemma_0252")
    )


def _branch_closure(
    *,
    blocker_id: str,
    checklist_report: str,
    checklist_json: str,
    branch_verdict: str,
    mapping_row_count: int,
    checklist_item_count: int,
    theorem_branch_count: int,
    dischargeable_now_count: int,
    direct_theorem_branch_count: int,
    required_next_action: str,
) -> BranchClosure:
    if dischargeable_now_count or direct_theorem_branch_count:
        closure_status = "unexpected_discharge"
        candidate_emission_authorized = True
    else:
        closure_status = "present_unresolved"
        candidate_emission_authorized = False
    return BranchClosure(
        blocker_id=blocker_id,
        checklist_report=checklist_report,
        checklist_json=checklist_json,
        branch_verdict=branch_verdict,
        mapping_row_count=mapping_row_count,
        checklist_item_count=checklist_item_count,
        theorem_branch_count=theorem_branch_count,
        dischargeable_now_count=dischargeable_now_count,
        direct_theorem_branch_count=direct_theorem_branch_count,
        closure_status=closure_status,
        candidate_emission_authorized=candidate_emission_authorized,
        required_next_action=required_next_action,
    )


def _missing_source_refs() -> tuple[str, ...]:
    return tuple(source for source in LOCAL_SOURCE_REFS if not (ROOT / source).exists())


def build_blocker_closure_dashboard(
    *,
    proof_obligation_json: Path = DEFAULT_INPUT,
) -> Lemma0252BlockerClosureDashboard:
    mapping = build_known_theorem_mapping(proof_obligation_json=proof_obligation_json)
    compactness = build_compactness_liouville_checklist(
        proof_obligation_json=proof_obligation_json,
    )
    finite = build_finite_bound_smallness_checklist(
        proof_obligation_json=proof_obligation_json,
    )
    smooth = build_smooth_continuation_checklist(
        proof_obligation_json=proof_obligation_json,
    )

    branch_closures = (
        _branch_closure(
            blocker_id=finite.source_blocker_id,
            checklist_report="track-a-regularity/reports/lemma_0252_finite_bound_smallness_checklist.md",
            checklist_json="track-a-regularity/reports/lemma_0252_finite_bound_smallness_checklist.json",
            branch_verdict=finite.branch_verdict,
            mapping_row_count=_mapping_row_count_by_blocker(finite.source_blocker_id),
            checklist_item_count=finite.checklist_item_count,
            theorem_branch_count=finite.theorem_branch_count,
            dischargeable_now_count=finite.dischargeable_now_count,
            direct_theorem_branch_count=_direct_branch_count(finite.theorem_branches),
            required_next_action=(
                "Prove a finite-bound-to-smallness mechanism or keep the branch blocked."
            ),
        ),
        _branch_closure(
            blocker_id=compactness.source_blocker_id,
            checklist_report="track-a-regularity/reports/lemma_0252_compactness_liouville_checklist.md",
            checklist_json="track-a-regularity/reports/lemma_0252_compactness_liouville_checklist.json",
            branch_verdict=compactness.branch_verdict,
            mapping_row_count=_mapping_row_count_by_blocker(compactness.source_blocker_id),
            checklist_item_count=compactness.checklist_item_count,
            theorem_branch_count=compactness.theorem_branch_count,
            dischargeable_now_count=compactness.dischargeable_now_count,
            direct_theorem_branch_count=_direct_branch_count(compactness.theorem_branches),
            required_next_action=(
                "Provide an ancient-limit compactness/Liouville theorem or keep the branch blocked."
            ),
        ),
        _branch_closure(
            blocker_id=smooth.source_blocker_id,
            checklist_report="track-a-regularity/reports/lemma_0252_smooth_continuation_checklist.md",
            checklist_json="track-a-regularity/reports/lemma_0252_smooth_continuation_checklist.json",
            branch_verdict=smooth.branch_verdict,
            mapping_row_count=_mapping_row_count_by_blocker(smooth.source_blocker_id),
            checklist_item_count=smooth.checklist_item_count,
            theorem_branch_count=smooth.theorem_branch_count,
            dischargeable_now_count=smooth.dischargeable_now_count,
            direct_theorem_branch_count=_direct_branch_count(smooth.theorem_branches),
            required_next_action=(
                "Supply BKM/Serrin/high-Sobolev/terminal-cover continuation input or keep the branch blocked."
            ),
        ),
    )

    present = tuple(branch.blocker_id for branch in branch_closures)
    all_expected_branches_present = present == EXPECTED_BRANCHES
    discharged_blocker_count = sum(
        1 for branch in branch_closures if branch.dischargeable_now_count
    )
    direct_theorem_branch_count = sum(
        branch.direct_theorem_branch_count for branch in branch_closures
    )
    candidate_emission_authorized = any(
        branch.candidate_emission_authorized for branch in branch_closures
    )
    if (
        all_expected_branches_present
        and not discharged_blocker_count
        and not mapping.resolvable_known_count
        and not direct_theorem_branch_count
        and not candidate_emission_authorized
        and mapping.candidate_status == "needs_review"
        and not mapping.active_candidate
    ):
        closure_verdict = "blocked_no_discharge"
    else:
        closure_verdict = "inconsistent_review_required"

    return Lemma0252BlockerClosureDashboard(
        schema_version=1,
        lemma_id=mapping.lemma_id,
        candidate_status=mapping.candidate_status,
        active_candidate=mapping.active_candidate,
        closure_verdict=closure_verdict,
        substantive_blocker_count=len(EXPECTED_BRANCHES),
        checklist_branch_count=len(branch_closures),
        discharged_blocker_count=discharged_blocker_count,
        direct_known_route_count=mapping.resolvable_known_count,
        direct_theorem_branch_count=direct_theorem_branch_count,
        unresolved_branch_count=sum(
            1 for branch in branch_closures if branch.closure_status == "present_unresolved"
        ),
        candidate_emission_authorized=candidate_emission_authorized,
        checklist_presence_authorizes_candidate=False,
        all_expected_branches_present=all_expected_branches_present,
        branch_closures=branch_closures,
        source_refs=LOCAL_SOURCE_REFS,
        non_claims=NON_CLAIMS,
    )


def dashboard_to_dict(
    dashboard: Lemma0252BlockerClosureDashboard,
) -> dict[str, object]:
    return {
        "schema_version": dashboard.schema_version,
        "lemma_id": dashboard.lemma_id,
        "candidate_status": dashboard.candidate_status,
        "active_candidate": dashboard.active_candidate,
        "closure_verdict": dashboard.closure_verdict,
        "substantive_blocker_count": dashboard.substantive_blocker_count,
        "checklist_branch_count": dashboard.checklist_branch_count,
        "discharged_blocker_count": dashboard.discharged_blocker_count,
        "direct_known_route_count": dashboard.direct_known_route_count,
        "direct_theorem_branch_count": dashboard.direct_theorem_branch_count,
        "unresolved_branch_count": dashboard.unresolved_branch_count,
        "candidate_emission_authorized": dashboard.candidate_emission_authorized,
        "checklist_presence_authorizes_candidate": dashboard.checklist_presence_authorizes_candidate,
        "all_expected_branches_present": dashboard.all_expected_branches_present,
        "branch_closures": [
            {
                "blocker_id": branch.blocker_id,
                "checklist_report": branch.checklist_report,
                "checklist_json": branch.checklist_json,
                "branch_verdict": branch.branch_verdict,
                "mapping_row_count": branch.mapping_row_count,
                "checklist_item_count": branch.checklist_item_count,
                "theorem_branch_count": branch.theorem_branch_count,
                "dischargeable_now_count": branch.dischargeable_now_count,
                "direct_theorem_branch_count": branch.direct_theorem_branch_count,
                "closure_status": branch.closure_status,
                "candidate_emission_authorized": branch.candidate_emission_authorized,
                "required_next_action": branch.required_next_action,
            }
            for branch in dashboard.branch_closures
        ],
        "source_refs": list(dashboard.source_refs),
        "non_claims": list(dashboard.non_claims),
    }


def _table_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "/")


def render_markdown(dashboard: Lemma0252BlockerClosureDashboard) -> str:
    branch_rows = [
        "| blocker_id | branch_verdict | checklist_items | theorem_branches | discharged | direct_branches | closure_status | candidate_emission_authorized | required_next_action |",
        "|---|---|---:|---:|---:|---:|---|---:|---|",
    ]
    for branch in dashboard.branch_closures:
        branch_rows.append(
            "| "
            f"`{_table_cell(branch.blocker_id)}` | "
            f"`{_table_cell(branch.branch_verdict)}` | "
            f"{branch.checklist_item_count} | "
            f"{branch.theorem_branch_count} | "
            f"{branch.dischargeable_now_count} | "
            f"{branch.direct_theorem_branch_count} | "
            f"`{_table_cell(branch.closure_status)}` | "
            f"`{str(branch.candidate_emission_authorized).lower()}` | "
            f"{_table_cell(branch.required_next_action)} |"
        )

    return "\n".join(
        (
            "# Lemma 0252 Blocker-Closure Dashboard",
            "",
            "Generated by `track-a-regularity/evaluator/lemma_0252_blocker_closure_dashboard.py`.",
            "",
            "This read-only dashboard joins the Step 87 known-theorem mapping with the Step",
            "88-90 branch checklists. It makes explicit that branch checklist presence is",
            "not proof-obligation discharge and does not authorize active candidate emission.",
            "",
            "## Summary",
            "",
            f"- lemma_id: `{dashboard.lemma_id}`",
            f"- candidate_status: `{dashboard.candidate_status}`",
            f"- active_candidate: `{str(dashboard.active_candidate).lower()}`",
            f"- closure_verdict: `{dashboard.closure_verdict}`",
            f"- substantive_blocker_count: `{dashboard.substantive_blocker_count}`",
            f"- checklist_branch_count: `{dashboard.checklist_branch_count}`",
            f"- discharged_blocker_count: `{dashboard.discharged_blocker_count}`",
            f"- direct_known_route_count: `{dashboard.direct_known_route_count}`",
            f"- direct_theorem_branch_count: `{dashboard.direct_theorem_branch_count}`",
            f"- unresolved_branch_count: `{dashboard.unresolved_branch_count}`",
            f"- candidate_emission_authorized: `{str(dashboard.candidate_emission_authorized).lower()}`",
            f"- checklist_presence_authorizes_candidate: `{str(dashboard.checklist_presence_authorizes_candidate).lower()}`",
            f"- all_expected_branches_present: `{str(dashboard.all_expected_branches_present).lower()}`",
            "",
            "## Branch Closure Rows",
            "",
            *branch_rows,
            "",
            "## Guardrail",
            "",
            "- The three substantive blockers now have branch checklists.",
            "- All three branch checklists remain unresolved.",
            "- The dashboard has zero discharged blockers and zero direct known theorem routes.",
            "- Therefore `lemma_0252` cannot be emitted as an active candidate from checklist presence alone.",
            "",
            "## Local Source Refs",
            "",
            *(f"- `{source}`" for source in dashboard.source_refs),
            "",
            "## Non-Claims",
            "",
            *(f"- `{claim}`" for claim in dashboard.non_claims),
            "",
        )
    )


def render_json(dashboard: Lemma0252BlockerClosureDashboard) -> str:
    return json.dumps(dashboard_to_dict(dashboard), indent=2, sort_keys=True) + "\n"


def render_output(
    dashboard: Lemma0252BlockerClosureDashboard,
    output_format: str,
) -> str:
    if output_format == "markdown":
        return render_markdown(dashboard)
    if output_format == "json":
        return render_json(dashboard)
    raise ValueError(f"unknown blocker-closure dashboard format: {output_format}")


def write_output(
    output: Path,
    dashboard: Lemma0252BlockerClosureDashboard,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(dashboard, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    dashboard: Lemma0252BlockerClosureDashboard,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(dashboard, output_format)
    if not output.exists():
        return False, f"missing lemma_0252 blocker-closure dashboard: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale lemma_0252 blocker-closure dashboard: {output}"
    return True, f"fresh lemma_0252 blocker-closure dashboard: {output}"


def check_all_branches_present(
    dashboard: Lemma0252BlockerClosureDashboard,
) -> tuple[bool, str]:
    actual = tuple(branch.blocker_id for branch in dashboard.branch_closures)
    if actual != EXPECTED_BRANCHES:
        return False, f"unexpected closure branches: {actual!r}"
    if not dashboard.all_expected_branches_present:
        return False, "dashboard does not mark all expected branches present"
    return True, "all expected lemma_0252 blocker branches are present"


def check_no_discharged_blockers(
    dashboard: Lemma0252BlockerClosureDashboard,
) -> tuple[bool, str]:
    if dashboard.discharged_blocker_count:
        return False, f"discharged blockers present: {dashboard.discharged_blocker_count}"
    if dashboard.direct_known_route_count:
        return False, f"direct known routes present: {dashboard.direct_known_route_count}"
    if dashboard.direct_theorem_branch_count:
        return False, f"direct theorem branches present: {dashboard.direct_theorem_branch_count}"
    unexpected = [
        branch.blocker_id
        for branch in dashboard.branch_closures
        if branch.closure_status != "present_unresolved"
    ]
    if unexpected:
        return False, "unexpected branch closure status for: " + ", ".join(unexpected)
    return True, "all lemma_0252 blocker branches remain present but unresolved"


def check_no_candidate_authorization(
    dashboard: Lemma0252BlockerClosureDashboard,
) -> tuple[bool, str]:
    if dashboard.candidate_emission_authorized:
        return False, "dashboard authorizes active candidate emission"
    if dashboard.checklist_presence_authorizes_candidate:
        return False, "checklist presence is incorrectly marked as candidate authorization"
    if dashboard.candidate_status != "needs_review" or dashboard.active_candidate:
        return False, "lemma_0252 candidate state changed unexpectedly"
    if dashboard.closure_verdict != "blocked_no_discharge":
        return False, f"unexpected closure_verdict: {dashboard.closure_verdict}"
    return True, "checklist presence does not authorize active candidate emission"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown blocker-closure dashboard format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render the lemma_0252 blocker-closure dashboard."
    )
    parser.add_argument("--proof-obligation-json", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--check-output",
        action="store_true",
        help="Check that --output already matches the rendered dashboard.",
    )
    parser.add_argument(
        "--require-all-branches",
        action="store_true",
        help="Fail unless all three substantive blocker branches are present.",
    )
    parser.add_argument(
        "--require-no-discharged",
        action="store_true",
        help="Fail if any branch is marked discharged or directly applicable.",
    )
    parser.add_argument(
        "--require-no-candidate-authorization",
        action="store_true",
        help="Fail if checklist presence authorizes candidate emission.",
    )
    parser.add_argument(
        "--require-sources-exist",
        action="store_true",
        help="Fail if local source references are missing.",
    )
    args = parser.parse_args(argv)

    try:
        dashboard = build_blocker_closure_dashboard(
            proof_obligation_json=args.proof_obligation_json,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report readable setup failures.
        print(f"failed to build lemma_0252 blocker-closure dashboard: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, dashboard, args.format)
        print(message)
        if not ok:
            print("run without --check-output to regenerate the blocker-closure dashboard", file=sys.stderr)
            return 1
    else:
        written = write_output(output, dashboard, args.format)
        print(f"wrote {written}")

    if args.require_all_branches:
        ok, message = check_all_branches_present(dashboard)
        print(message)
        if not ok:
            return 1

    if args.require_no_discharged:
        ok, message = check_no_discharged_blockers(dashboard)
        print(message)
        if not ok:
            return 1

    if args.require_no_candidate_authorization:
        ok, message = check_no_candidate_authorization(dashboard)
        print(message)
        if not ok:
            return 1

    if args.require_sources_exist:
        missing_sources = _missing_source_refs()
        if missing_sources:
            print("missing source refs: " + ", ".join(missing_sources), file=sys.stderr)
            return 1
        print("all blocker-closure dashboard source refs exist")

    print(f"lemma_id: {dashboard.lemma_id}")
    print(f"candidate_status: {dashboard.candidate_status}")
    print(f"active_candidate: {str(dashboard.active_candidate).lower()}")
    print(f"closure_verdict: {dashboard.closure_verdict}")
    print(f"checklist_branch_count: {dashboard.checklist_branch_count}")
    print(f"discharged_blocker_count: {dashboard.discharged_blocker_count}")
    print(f"candidate_emission_authorized: {str(dashboard.candidate_emission_authorized).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
