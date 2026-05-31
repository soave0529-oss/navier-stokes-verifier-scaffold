from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

from lemma_0252_blocker_known_theorem_mapping import build_known_theorem_mapping
from proof_obligation_blockers import DEFAULT_INPUT


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "lemma_0252_smooth_continuation_checklist.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "lemma_0252_smooth_continuation_checklist.json"

CHECKLIST_ITEM_VERDICTS = (
    "missing_required_input",
    "guardrail_only",
    "dependent_on_new_result",
)
THEOREM_VERDICTS = (
    "criterion_input_missing",
    "extra_assumption_only",
    "deferred_needs_new_result",
)
LOCAL_SOURCE_REFS = (
    "track-a-regularity/reports/lemma_0252_blocker_known_theorem_mapping.md",
    "track-a-regularity/reports/lemma_0252_blocker_known_theorem_mapping.json",
    "track-a-regularity/reports/lemma_0252_proof_obligation_graph.json",
    "docs/LEMMA_0252_PROOF_OBLIGATIONS.md",
    "docs/KNOWN_LOCAL_ENSTROPHY_CRITERIA.md",
    "docs/KNOWN_GEOMETRIC_CRITERIA.md",
    "docs/LEMMA_0252_LOCAL_ENERGY_FORMAL_MAP.md",
    "docs/STEP87_LEMMA_0252_KNOWN_THEOREM_MAPPING.md",
    "docs/STEP88_COMPACTNESS_LIOUVILLE_CHECKLIST.md",
    "docs/STEP89_FINITE_BOUND_SMALLNESS_CHECKLIST.md",
    "track-c-formal/lean/NavierStokesProgram/LocalEnergy.lean",
    "track-c-formal/lean/NavierStokesProgram/ProofObligationGraph.lean",
    "track-c-formal/lean/NavierStokesProgram/SolutionClasses.lean",
)
NON_CLAIMS = (
    "read_only_smooth_continuation_checklist",
    "no_candidate_promotion",
    "no_blocker_discharge",
    "no_bkm_bound",
    "no_serrin_bound",
    "no_high_sobolev_bound",
    "no_terminal_regular_cover",
    "no_weak_to_smooth_upgrade",
    "no_navier_stokes_solution",
)


@dataclass(frozen=True)
class ChecklistItem:
    item_id: str
    required_artifact: str
    exact_required_input: str
    current_project_status: str
    evidence_ref: str
    blocker_effect: str
    verdict: str


@dataclass(frozen=True)
class TheoremBranch:
    theorem_family: str
    required_setting: str
    applies_to_lemma_0252: bool
    mismatch: str
    verdict: str


@dataclass(frozen=True)
class SmoothContinuationChecklist:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    source_blocker_id: str
    branch_verdict: str
    checklist_item_count: int
    theorem_branch_count: int
    dischargeable_now_count: int
    missing_required_input_count: int
    dependent_on_new_result_count: int
    criterion_input_missing_branch_count: int
    extra_assumption_branch_count: int
    mapping_theorem_rows: tuple[str, ...]
    checklist_items: tuple[ChecklistItem, ...]
    theorem_branches: tuple[TheoremBranch, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]


def _checklist_item(
    *,
    item_id: str,
    required_artifact: str,
    exact_required_input: str,
    current_project_status: str,
    evidence_ref: str,
    blocker_effect: str,
    verdict: str,
) -> ChecklistItem:
    if verdict not in CHECKLIST_ITEM_VERDICTS:
        raise ValueError(f"unknown checklist verdict: {verdict}")
    return ChecklistItem(
        item_id=item_id,
        required_artifact=required_artifact,
        exact_required_input=exact_required_input,
        current_project_status=current_project_status,
        evidence_ref=evidence_ref,
        blocker_effect=blocker_effect,
        verdict=verdict,
    )


def _theorem_branch(
    *,
    theorem_family: str,
    required_setting: str,
    applies_to_lemma_0252: bool,
    mismatch: str,
    verdict: str,
) -> TheoremBranch:
    if verdict not in THEOREM_VERDICTS:
        raise ValueError(f"unknown theorem branch verdict: {verdict}")
    return TheoremBranch(
        theorem_family=theorem_family,
        required_setting=required_setting,
        applies_to_lemma_0252=applies_to_lemma_0252,
        mismatch=mismatch,
        verdict=verdict,
    )


def _canonical_checklist_items() -> tuple[ChecklistItem, ...]:
    return (
        _checklist_item(
            item_id="terminal_time_regular_cover",
            required_artifact=(
                "A quantitative cover showing all terminal-time points are regular in a way "
                "uniform enough to extend the classical solution."
            ),
            exact_required_input=(
                "local regularity neighborhoods near time T, uniform radii or bounds, pressure "
                "compatibility, and coverage of the periodic domain."
            ),
            current_project_status=(
                "Step 88 and Step 89 identify possible routes to local regularity, but neither "
                "route is discharged."
            ),
            evidence_ref="docs/STEP88_COMPACTNESS_LIOUVILLE_CHECKLIST.md",
            blocker_effect="Local metadata alone does not yet provide a terminal regular cover.",
            verdict="dependent_on_new_result",
        ),
        _checklist_item(
            item_id="bkm_vorticity_integral_bound",
            required_artifact="A BKM-compatible time-integrated L-infinity vorticity bound.",
            exact_required_input=(
                "proof of integral_0^T ||curl u(t)||_infty dt < infinity or a named equivalent "
                "continuation norm for the smooth periodic solution."
            ),
            current_project_status=(
                "Step 87 maps BKM as a non-direct anchor; finite local L2 enstrophy does not "
                "supply L-infinity vorticity control."
            ),
            evidence_ref="track-a-regularity/reports/lemma_0252_blocker_known_theorem_mapping.md",
            blocker_effect="BKM cannot be invoked without its continuation norm.",
            verdict="missing_required_input",
        ),
        _checklist_item(
            item_id="prodi_serrin_velocity_bound",
            required_artifact="A Prodi-Serrin-compatible global velocity spacetime bound.",
            exact_required_input=(
                "u in L^p_t L^q_x with the chosen critical relation and endpoint convention, "
                "plus proof that the bound persists up to T."
            ),
            current_project_status=(
                "Step 87 maps Prodi-Serrin as non-direct; `lemma_0252` supplies local vorticity "
                "metadata rather than a global velocity class."
            ),
            evidence_ref="docs/LEMMA_0252_PROOF_OBLIGATIONS.md",
            blocker_effect="Serrin continuation cannot be used without the velocity norm.",
            verdict="missing_required_input",
        ),
        _checklist_item(
            item_id="high_sobolev_continuation_bound",
            required_artifact="A high-Sobolev or classical local-wellposedness continuation bound.",
            exact_required_input=(
                "uniform H^s, C^k, or equivalent classical norm near T, with s above the "
                "3D local-wellposedness threshold."
            ),
            current_project_status=(
                "Track C separates smooth and weak vocabulary, but no high-Sobolev estimate is "
                "derived from the Morrey enstrophy envelope."
            ),
            evidence_ref="track-c-formal/lean/NavierStokesProgram/SolutionClasses.lean",
            blocker_effect="Classical continuation requires a strong norm, not only local regularity labels.",
            verdict="missing_required_input",
        ),
        _checklist_item(
            item_id="constantin_fefferman_geometry_input",
            required_artifact="A Constantin-Fefferman-compatible vorticity-direction coherence package.",
            exact_required_input=(
                "direction coherence, magnitude/localization assumptions, and a bridge from "
                "the local enstrophy envelope to that geometric input."
            ),
            current_project_status=(
                "Known geometric criteria are registry-first guardrails; `lemma_0252` has no "
                "vorticity-direction hypothesis."
            ),
            evidence_ref="docs/KNOWN_GEOMETRIC_CRITERIA.md",
            blocker_effect="The geometric criterion is an extra-assumption branch, not a continuation bridge here.",
            verdict="guardrail_only",
        ),
        _checklist_item(
            item_id="suitable_weak_to_classical_guard",
            required_artifact=(
                "A guard preventing suitable-weak local regularity or partial-regularity metadata "
                "from being treated as smooth classical continuation."
            ),
            exact_required_input=(
                "named solution classes, theorem hypotheses, and explicit bridge from local "
                "regularity to a continuation norm."
            ),
            current_project_status=(
                "Solution-class vocabulary exists, but the bridge theorem is not present."
            ),
            evidence_ref="track-c-formal/lean/NavierStokesProgram/SolutionClasses.lean",
            blocker_effect="This prevents a weak-to-smooth upgrade from being assumed silently.",
            verdict="guardrail_only",
        ),
        _checklist_item(
            item_id="local_to_global_terminal_uniformity",
            required_artifact=(
                "A local-to-global terminal-time uniformity argument turning pointwise regularity "
                "into a continuation interval past T."
            ),
            exact_required_input=(
                "compactness of the periodic domain, uniform local estimates, overlapping patch "
                "compatibility, and persistence of the classical solution class."
            ),
            current_project_status=(
                "No terminal cover or uniform patching argument exists in the current reports."
            ),
            evidence_ref="docs/LEMMA_0252_LOCAL_ENERGY_FORMAL_MAP.md",
            blocker_effect="Pointwise or local regularity is not yet a global continuation theorem.",
            verdict="dependent_on_new_result",
        ),
    )


def _canonical_theorem_branches() -> tuple[TheoremBranch, ...]:
    return (
        _theorem_branch(
            theorem_family="BKM continuation criterion",
            required_setting=(
                "smooth solution plus finite time-integrated L-infinity vorticity norm up to T."
            ),
            applies_to_lemma_0252=False,
            mismatch=(
                "lemma_0252 has a finite local L2 vorticity envelope, not the BKM L-infinity "
                "vorticity integral."
            ),
            verdict="criterion_input_missing",
        ),
        _theorem_branch(
            theorem_family="Prodi-Serrin continuation criterion",
            required_setting=(
                "global velocity spacetime norm satisfying the critical Serrin relation and "
                "endpoint conventions."
            ),
            applies_to_lemma_0252=False,
            mismatch=(
                "the current statement does not supply a global velocity class or endpoint "
                "Serrin control."
            ),
            verdict="criterion_input_missing",
        ),
        _theorem_branch(
            theorem_family="High-Sobolev local-wellposedness continuation",
            required_setting=(
                "uniform high-Sobolev or classical norm near terminal time."
            ),
            applies_to_lemma_0252=False,
            mismatch=(
                "finite local enstrophy Morrey metadata is not a high-Sobolev bound."
            ),
            verdict="criterion_input_missing",
        ),
        _theorem_branch(
            theorem_family="Constantin-Fefferman vorticity-direction criterion",
            required_setting=(
                "vorticity-direction coherence plus magnitude/localization hypotheses."
            ),
            applies_to_lemma_0252=False,
            mismatch=(
                "lemma_0252 has no direction-coherence assumption, so this is an extra-assumption "
                "comparison only."
            ),
            verdict="extra_assumption_only",
        ),
        _theorem_branch(
            theorem_family="Terminal local-regularity cover branch",
            required_setting=(
                "uniform local regularity at every terminal point plus patching to a classical "
                "continuation interval."
            ),
            applies_to_lemma_0252=False,
            mismatch=(
                "Steps 88-89 do not discharge the local regularity routes, and no uniform terminal "
                "patching theorem is present."
            ),
            verdict="deferred_needs_new_result",
        ),
    )


def _missing_source_refs() -> tuple[str, ...]:
    return tuple(source for source in LOCAL_SOURCE_REFS if not (ROOT / source).exists())


def build_smooth_continuation_checklist(
    *,
    proof_obligation_json: Path = DEFAULT_INPUT,
) -> SmoothContinuationChecklist:
    mapping = build_known_theorem_mapping(proof_obligation_json=proof_obligation_json)
    continuation_rows = tuple(
        row.candidate_theorem
        for row in mapping.rows
        if row.blocker_id == "smooth_continuation_bridge"
    )
    if len(continuation_rows) < 2:
        raise ValueError("Step 87 smooth_continuation_bridge mapping must have at least two rows")
    if mapping.resolvable_known_count:
        raise ValueError("Step 87 mapping unexpectedly has resolvable_known rows")

    checklist_items = _canonical_checklist_items()
    theorem_branches = _canonical_theorem_branches()
    return SmoothContinuationChecklist(
        schema_version=1,
        lemma_id=mapping.lemma_id,
        candidate_status=mapping.candidate_status,
        active_candidate=mapping.active_candidate,
        source_blocker_id="smooth_continuation_bridge",
        branch_verdict="deferred_needs_new_result",
        checklist_item_count=len(checklist_items),
        theorem_branch_count=len(theorem_branches),
        dischargeable_now_count=0,
        missing_required_input_count=sum(
            1 for item in checklist_items if item.verdict == "missing_required_input"
        ),
        dependent_on_new_result_count=sum(
            1 for item in checklist_items if item.verdict == "dependent_on_new_result"
        ),
        criterion_input_missing_branch_count=sum(
            1 for branch in theorem_branches if branch.verdict == "criterion_input_missing"
        ),
        extra_assumption_branch_count=sum(
            1 for branch in theorem_branches if branch.verdict == "extra_assumption_only"
        ),
        mapping_theorem_rows=continuation_rows,
        checklist_items=checklist_items,
        theorem_branches=theorem_branches,
        source_refs=LOCAL_SOURCE_REFS,
        non_claims=NON_CLAIMS,
    )


def checklist_to_dict(checklist: SmoothContinuationChecklist) -> dict[str, object]:
    return {
        "schema_version": checklist.schema_version,
        "lemma_id": checklist.lemma_id,
        "candidate_status": checklist.candidate_status,
        "active_candidate": checklist.active_candidate,
        "source_blocker_id": checklist.source_blocker_id,
        "branch_verdict": checklist.branch_verdict,
        "checklist_item_count": checklist.checklist_item_count,
        "theorem_branch_count": checklist.theorem_branch_count,
        "dischargeable_now_count": checklist.dischargeable_now_count,
        "missing_required_input_count": checklist.missing_required_input_count,
        "dependent_on_new_result_count": checklist.dependent_on_new_result_count,
        "criterion_input_missing_branch_count": checklist.criterion_input_missing_branch_count,
        "extra_assumption_branch_count": checklist.extra_assumption_branch_count,
        "mapping_theorem_rows": list(checklist.mapping_theorem_rows),
        "checklist_items": [
            {
                "item_id": item.item_id,
                "required_artifact": item.required_artifact,
                "exact_required_input": item.exact_required_input,
                "current_project_status": item.current_project_status,
                "evidence_ref": item.evidence_ref,
                "blocker_effect": item.blocker_effect,
                "verdict": item.verdict,
            }
            for item in checklist.checklist_items
        ],
        "theorem_branches": [
            {
                "theorem_family": branch.theorem_family,
                "required_setting": branch.required_setting,
                "applies_to_lemma_0252": branch.applies_to_lemma_0252,
                "mismatch": branch.mismatch,
                "verdict": branch.verdict,
            }
            for branch in checklist.theorem_branches
        ],
        "source_refs": list(checklist.source_refs),
        "non_claims": list(checklist.non_claims),
    }


def _table_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "/")


def render_markdown(checklist: SmoothContinuationChecklist) -> str:
    item_rows = [
        "| item_id | required_artifact | exact_required_input | current_project_status | evidence_ref | blocker_effect | verdict |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in checklist.checklist_items:
        item_rows.append(
            "| "
            f"`{_table_cell(item.item_id)}` | "
            f"{_table_cell(item.required_artifact)} | "
            f"{_table_cell(item.exact_required_input)} | "
            f"{_table_cell(item.current_project_status)} | "
            f"`{_table_cell(item.evidence_ref)}` | "
            f"{_table_cell(item.blocker_effect)} | "
            f"`{_table_cell(item.verdict)}` |"
        )

    branch_rows = [
        "| theorem_family | required_setting | applies_to_lemma_0252 | mismatch | verdict |",
        "|---|---|---:|---|---|",
    ]
    for branch in checklist.theorem_branches:
        branch_rows.append(
            "| "
            f"{_table_cell(branch.theorem_family)} | "
            f"{_table_cell(branch.required_setting)} | "
            f"`{str(branch.applies_to_lemma_0252).lower()}` | "
            f"{_table_cell(branch.mismatch)} | "
            f"`{_table_cell(branch.verdict)}` |"
        )

    return "\n".join(
        (
            "# Lemma 0252 Smooth-Continuation Bridge Checklist",
            "",
            "Generated by `track-a-regularity/evaluator/lemma_0252_smooth_continuation_checklist.py`.",
            "",
            "This read-only checklist expands the Step 87 `smooth_continuation_bridge` blocker.",
            "It records why local regularity metadata, finite local enstrophy, or epsilon-style",
            "branch scaffolds are not automatically BKM, Prodi-Serrin, high-Sobolev, or",
            "geometric-continuation inputs.",
            "",
            "## Summary",
            "",
            f"- lemma_id: `{checklist.lemma_id}`",
            f"- candidate_status: `{checklist.candidate_status}`",
            f"- active_candidate: `{str(checklist.active_candidate).lower()}`",
            f"- source_blocker_id: `{checklist.source_blocker_id}`",
            f"- branch_verdict: `{checklist.branch_verdict}`",
            f"- checklist_item_count: `{checklist.checklist_item_count}`",
            f"- theorem_branch_count: `{checklist.theorem_branch_count}`",
            f"- dischargeable_now_count: `{checklist.dischargeable_now_count}`",
            f"- missing_required_input_count: `{checklist.missing_required_input_count}`",
            f"- dependent_on_new_result_count: `{checklist.dependent_on_new_result_count}`",
            f"- criterion_input_missing_branch_count: `{checklist.criterion_input_missing_branch_count}`",
            f"- extra_assumption_branch_count: `{checklist.extra_assumption_branch_count}`",
            "",
            "## Step 87 Smooth-Continuation Rows",
            "",
            *(f"- {row}" for row in checklist.mapping_theorem_rows),
            "",
            "## Checklist Items",
            "",
            *item_rows,
            "",
            "## Theorem Branches",
            "",
            *branch_rows,
            "",
            "## Local Source Refs",
            "",
            *(f"- `{source}`" for source in checklist.source_refs),
            "",
            "## Non-Claims",
            "",
            *(f"- `{claim}`" for claim in checklist.non_claims),
            "",
        )
    )


def render_json(checklist: SmoothContinuationChecklist) -> str:
    return json.dumps(checklist_to_dict(checklist), indent=2, sort_keys=True) + "\n"


def render_output(checklist: SmoothContinuationChecklist, output_format: str) -> str:
    if output_format == "markdown":
        return render_markdown(checklist)
    if output_format == "json":
        return render_json(checklist)
    raise ValueError(f"unknown smooth-continuation checklist format: {output_format}")


def write_output(
    output: Path,
    checklist: SmoothContinuationChecklist,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(checklist, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    checklist: SmoothContinuationChecklist,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(checklist, output_format)
    if not output.exists():
        return False, f"missing lemma_0252 smooth-continuation checklist: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale lemma_0252 smooth-continuation checklist: {output}"
    return True, f"fresh lemma_0252 smooth-continuation checklist: {output}"


def check_no_dischargeable(
    checklist: SmoothContinuationChecklist,
) -> tuple[bool, str]:
    if checklist.dischargeable_now_count:
        return False, "smooth-continuation checklist contains dischargeable_now items"
    direct_branches = [
        branch.theorem_family
        for branch in checklist.theorem_branches
        if branch.applies_to_lemma_0252
    ]
    if direct_branches:
        return False, "theorem branches apply directly: " + ", ".join(direct_branches)
    return True, "smooth-continuation branch has no directly dischargeable known route"


def check_continuation_gap(
    checklist: SmoothContinuationChecklist,
) -> tuple[bool, str]:
    required = {
        "terminal_time_regular_cover",
        "bkm_vorticity_integral_bound",
        "prodi_serrin_velocity_bound",
        "high_sobolev_continuation_bound",
        "suitable_weak_to_classical_guard",
        "local_to_global_terminal_uniformity",
    }
    present = {item.item_id for item in checklist.checklist_items}
    missing = sorted(required - present)
    if missing:
        return False, "missing smooth-continuation checklist items: " + ", ".join(missing)
    if checklist.branch_verdict != "deferred_needs_new_result":
        return False, f"unexpected branch_verdict: {checklist.branch_verdict}"
    if checklist.criterion_input_missing_branch_count < 3:
        return False, "expected at least three criterion-input-missing theorem branches"
    return True, "smooth-continuation gap is explicit and branch is deferred"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown smooth-continuation checklist format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render the lemma_0252 smooth-continuation bridge checklist."
    )
    parser.add_argument("--proof-obligation-json", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--check-output",
        action="store_true",
        help="Check that --output already matches the rendered checklist.",
    )
    parser.add_argument(
        "--require-no-dischargeable",
        action="store_true",
        help="Fail if any known branch directly discharges the blocker.",
    )
    parser.add_argument(
        "--require-continuation-gap",
        action="store_true",
        help="Fail if the core smooth-continuation gap is not explicit.",
    )
    parser.add_argument(
        "--require-sources-exist",
        action="store_true",
        help="Fail if local source references are missing.",
    )
    args = parser.parse_args(argv)

    try:
        checklist = build_smooth_continuation_checklist(
            proof_obligation_json=args.proof_obligation_json,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report readable setup failures.
        print(f"failed to build lemma_0252 smooth-continuation checklist: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, checklist, args.format)
        print(message)
        if not ok:
            print("run without --check-output to regenerate the smooth-continuation checklist", file=sys.stderr)
            return 1
    else:
        written = write_output(output, checklist, args.format)
        print(f"wrote {written}")

    if args.require_no_dischargeable:
        ok, message = check_no_dischargeable(checklist)
        print(message)
        if not ok:
            return 1

    if args.require_continuation_gap:
        ok, message = check_continuation_gap(checklist)
        print(message)
        if not ok:
            return 1

    if args.require_sources_exist:
        missing_sources = _missing_source_refs()
        if missing_sources:
            print("missing source refs: " + ", ".join(missing_sources), file=sys.stderr)
            return 1
        print("all smooth-continuation checklist source refs exist")

    print(f"lemma_id: {checklist.lemma_id}")
    print(f"candidate_status: {checklist.candidate_status}")
    print(f"active_candidate: {str(checklist.active_candidate).lower()}")
    print(f"branch_verdict: {checklist.branch_verdict}")
    print(f"checklist_item_count: {checklist.checklist_item_count}")
    print(f"theorem_branch_count: {checklist.theorem_branch_count}")
    print(f"dischargeable_now_count: {checklist.dischargeable_now_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
