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
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "lemma_0252_finite_bound_smallness_checklist.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "lemma_0252_finite_bound_smallness_checklist.json"

CHECKLIST_ITEM_VERDICTS = (
    "missing_required_input",
    "partial_vocabulary_only",
    "dependent_on_new_result",
)
THEOREM_VERDICTS = (
    "smallness_only",
    "deferred_needs_new_result",
    "outside_setting_caution",
)
LOCAL_SOURCE_REFS = (
    "track-a-regularity/reports/lemma_0252_blocker_known_theorem_mapping.md",
    "track-a-regularity/reports/lemma_0252_blocker_known_theorem_mapping.json",
    "track-a-regularity/reports/lemma_0252_proof_obligation_graph.json",
    "docs/LEMMA_0252_PROOF_OBLIGATIONS.md",
    "docs/KNOWN_LOCAL_ENSTROPHY_CRITERIA.md",
    "docs/LEMMA_0252_LOCAL_ENERGY_FORMAL_MAP.md",
    "docs/STEP87_LEMMA_0252_KNOWN_THEOREM_MAPPING.md",
    "docs/STEP88_COMPACTNESS_LIOUVILLE_CHECKLIST.md",
    "docs/paper_notes/1402.0290.md",
    "docs/paper_notes/1709.10033.md",
    "docs/paper_notes/1901.09023.md",
    "track-c-formal/lean/NavierStokesProgram/LocalEnergy.lean",
    "track-c-formal/lean/NavierStokesProgram/ParabolicCylinder.lean",
    "track-c-formal/lean/NavierStokesProgram/ProofObligationGraph.lean",
)
NON_CLAIMS = (
    "read_only_finite_bound_smallness_checklist",
    "no_candidate_promotion",
    "no_blocker_discharge",
    "no_epsilon_regularization",
    "no_finite_bound_to_smallness_theorem",
    "no_pressure_estimate",
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
class FiniteBoundSmallnessChecklist:
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
    smallness_only_branch_count: int
    outside_setting_caution_count: int
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
            item_id="ckn_epsilon_quantity_package",
            required_artifact=(
                "A precise CKN-style epsilon quantity package on backward parabolic cylinders."
            ),
            exact_required_input=(
                "velocity, pressure, local energy or dissipation quantities, cylinder "
                "admissibility, and the exact universal epsilon threshold."
            ),
            current_project_status=(
                "The project has parabolic-cylinder and local-energy vocabulary, but no "
                "formal or analytic CKN package."
            ),
            evidence_ref="docs/KNOWN_LOCAL_ENSTROPHY_CRITERIA.md",
            blocker_effect="Finite local enstrophy cannot be compared to epsilon regularity without the target quantity.",
            verdict="partial_vocabulary_only",
        ),
        _checklist_item(
            item_id="local_vorticity_to_velocity_pressure",
            required_artifact=(
                "A local bridge from vorticity enstrophy to the velocity, pressure, and "
                "dissipation controls used by epsilon regularity."
            ),
            exact_required_input=(
                "cutoff identities, local curl-gradient decomposition, harmonic or boundary "
                "terms, pressure equation, and Calderon-Zygmund/local-nonlocal pressure bounds."
            ),
            current_project_status=(
                "Step 53 names this bridge as missing; Step 87 only maps it to known theorem "
                "families, not a proof."
            ),
            evidence_ref="docs/LEMMA_0252_PROOF_OBLIGATIONS.md",
            blocker_effect="The finite Morrey enstrophy envelope is not yet a CKN epsilon quantity.",
            verdict="missing_required_input",
        ),
        _checklist_item(
            item_id="finite_to_smallness_decay_or_monotonicity",
            required_artifact=(
                "A monotonicity, decay, or concentration theorem converting finite critical "
                "mass into epsilon smallness on some sufficiently small cylinder."
            ),
            exact_required_input=(
                "statement valid for smooth periodic 3D NSE up to terminal time, scale-critical "
                "hypotheses, and a conclusion below the CKN epsilon threshold."
            ),
            current_project_status=(
                "No such theorem is present in local notes, evaluator checks, or Lean vocabulary."
            ),
            evidence_ref="track-a-regularity/reports/lemma_0252_blocker_known_theorem_mapping.md",
            blocker_effect="This is the direct blocker: bounded critical mass can remain non-small at every scale.",
            verdict="dependent_on_new_result",
        ),
        _checklist_item(
            item_id="self_improvement_or_reverse_holder",
            required_artifact=(
                "A self-improvement or reverse-Holder mechanism lowering the effective critical "
                "quantity from finite envelope to subcritical control."
            ),
            exact_required_input=(
                "localized integrability upgrade, pressure compatibility, and proof that the "
                "upgrade persists near hypothetical terminal singular points."
            ),
            current_project_status=(
                "The known-result registry records nearby local Morrey criteria, but they use "
                "smallness, dynamic lower scales, or different velocity quantities."
            ),
            evidence_ref="docs/KNOWN_LOCAL_ENSTROPHY_CRITERIA.md",
            blocker_effect="Without self-improvement, finite boundedness remains materially weaker than smallness.",
            verdict="dependent_on_new_result",
        ),
        _checklist_item(
            item_id="singular_point_lower_bound_or_concentration_alternative",
            required_artifact=(
                "A concentration alternative proving that a singular point forces either "
                "unbounded local Morrey enstrophy or a CKN-small scale."
            ),
            exact_required_input=(
                "localized lower bounds at singular points, compatible pressure/local energy "
                "control, and a contradiction mechanism for bounded non-small profiles."
            ),
            current_project_status=(
                "Step 88 records the compactness/Liouville version of this alternative as "
                "deferred to a new result."
            ),
            evidence_ref="docs/STEP88_COMPACTNESS_LIOUVILLE_CHECKLIST.md",
            blocker_effect="This is the finite-bound branch's non-smallness escape hatch, and it is not available.",
            verdict="dependent_on_new_result",
        ),
        _checklist_item(
            item_id="pressure_and_cutoff_error_control",
            required_artifact=(
                "Quantitative control of pressure and cutoff errors created when localizing "
                "the periodic vorticity envelope to balls."
            ),
            exact_required_input=(
                "pressure decomposition, local/nonlocal estimates, cutoff-gradient error terms, "
                "and constants compatible with the epsilon threshold."
            ),
            current_project_status=(
                "The project records pressure control as vocabulary-only or missing in the "
                "proof-obligation graph."
            ),
            evidence_ref="track-a-regularity/reports/lemma_0252_proof_obligation_graph.json",
            blocker_effect="Even a decay theorem would not reach CKN without pressure and cutoff bookkeeping.",
            verdict="missing_required_input",
        ),
        _checklist_item(
            item_id="return_to_continuation",
            required_artifact=(
                "A bridge from epsilon-small local regularity at terminal cylinders to smooth "
                "classical continuation past T."
            ),
            exact_required_input=(
                "coverage of terminal points, uniform local regularity bounds, and a named "
                "BKM, Serrin, or high-Sobolev continuation criterion."
            ),
            current_project_status=(
                "Step 87 maps continuation criteria as non-direct; no local-to-global "
                "continuation bridge is proved."
            ),
            evidence_ref="track-a-regularity/reports/lemma_0252_blocker_known_theorem_mapping.md",
            blocker_effect="Smallness at selected cylinders is still not the full Clay-style continuation conclusion.",
            verdict="dependent_on_new_result",
        ),
    )


def _canonical_theorem_branches() -> tuple[TheoremBranch, ...]:
    return (
        _theorem_branch(
            theorem_family="CKN epsilon-regularity branch",
            required_setting=(
                "suitable weak solution on a cylinder with epsilon-small velocity, pressure, "
                "and dissipation/local-energy package."
            ),
            applies_to_lemma_0252=False,
            mismatch=(
                "lemma_0252 assumes only finite scale-critical local vorticity enstrophy, not "
                "epsilon smallness of the CKN package."
            ),
            verdict="smallness_only",
        ),
        _theorem_branch(
            theorem_family="Lin streamlined CKN branch",
            required_setting=(
                "the same epsilon-small partial-regularity input as CKN, with a different proof route."
            ),
            applies_to_lemma_0252=False,
            mismatch=(
                "Lin simplifies the proof after smallness is available; it does not turn finite "
                "critical mass into smallness."
            ),
            verdict="smallness_only",
        ),
        _theorem_branch(
            theorem_family="Local Morrey smallness and dynamic-scale branch",
            required_setting=(
                "small local Morrey or spatial-concentration quantities, often with velocity "
                "rather than vorticity and with dynamic lower-scale restrictions."
            ),
            applies_to_lemma_0252=False,
            mismatch=(
                "nearby criteria still require smallness or a different quantity; the finite "
                "enstrophy envelope alone is adjacent but insufficient."
            ),
            verdict="deferred_needs_new_result",
        ),
        _theorem_branch(
            theorem_family="Tao/BV caution branch",
            required_setting=(
                "negative or outside-setting caution about critical-envelope heuristics and "
                "weak-solution pathologies."
            ),
            applies_to_lemma_0252=False,
            mismatch=(
                "not a proof route for exact smooth periodic NSE; it warns that energy-scale "
                "or averaged critical quantities are not automatically regularizing."
            ),
            verdict="outside_setting_caution",
        ),
    )


def _missing_source_refs() -> tuple[str, ...]:
    return tuple(source for source in LOCAL_SOURCE_REFS if not (ROOT / source).exists())


def build_finite_bound_smallness_checklist(
    *,
    proof_obligation_json: Path = DEFAULT_INPUT,
) -> FiniteBoundSmallnessChecklist:
    mapping = build_known_theorem_mapping(proof_obligation_json=proof_obligation_json)
    finite_rows = tuple(
        row.candidate_theorem
        for row in mapping.rows
        if row.blocker_id == "finite_bound_to_smallness"
    )
    if len(finite_rows) < 2:
        raise ValueError("Step 87 finite_bound_to_smallness mapping must have at least two rows")
    if mapping.resolvable_known_count:
        raise ValueError("Step 87 mapping unexpectedly has resolvable_known rows")

    checklist_items = _canonical_checklist_items()
    theorem_branches = _canonical_theorem_branches()
    return FiniteBoundSmallnessChecklist(
        schema_version=1,
        lemma_id=mapping.lemma_id,
        candidate_status=mapping.candidate_status,
        active_candidate=mapping.active_candidate,
        source_blocker_id="finite_bound_to_smallness",
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
        smallness_only_branch_count=sum(
            1 for branch in theorem_branches if branch.verdict == "smallness_only"
        ),
        outside_setting_caution_count=sum(
            1 for branch in theorem_branches if branch.verdict == "outside_setting_caution"
        ),
        mapping_theorem_rows=finite_rows,
        checklist_items=checklist_items,
        theorem_branches=theorem_branches,
        source_refs=LOCAL_SOURCE_REFS,
        non_claims=NON_CLAIMS,
    )


def checklist_to_dict(checklist: FiniteBoundSmallnessChecklist) -> dict[str, object]:
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
        "smallness_only_branch_count": checklist.smallness_only_branch_count,
        "outside_setting_caution_count": checklist.outside_setting_caution_count,
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


def render_markdown(checklist: FiniteBoundSmallnessChecklist) -> str:
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
            "# Lemma 0252 Finite-Bound-to-Smallness Checklist",
            "",
            "Generated by `track-a-regularity/evaluator/lemma_0252_finite_bound_smallness_checklist.py`.",
            "",
            "This read-only checklist expands the Step 87 `finite_bound_to_smallness` blocker.",
            "It makes explicit why finite critical local enstrophy is not the same as CKN-style",
            "epsilon smallness and records the missing artifacts before this branch could",
            "discharge a `lemma_0252` promotion blocker.",
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
            f"- smallness_only_branch_count: `{checklist.smallness_only_branch_count}`",
            f"- outside_setting_caution_count: `{checklist.outside_setting_caution_count}`",
            "",
            "## Step 87 Finite-Bound Rows",
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


def render_json(checklist: FiniteBoundSmallnessChecklist) -> str:
    return json.dumps(checklist_to_dict(checklist), indent=2, sort_keys=True) + "\n"


def render_output(checklist: FiniteBoundSmallnessChecklist, output_format: str) -> str:
    if output_format == "markdown":
        return render_markdown(checklist)
    if output_format == "json":
        return render_json(checklist)
    raise ValueError(f"unknown finite-bound-to-smallness checklist format: {output_format}")


def write_output(
    output: Path,
    checklist: FiniteBoundSmallnessChecklist,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(checklist, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    checklist: FiniteBoundSmallnessChecklist,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(checklist, output_format)
    if not output.exists():
        return False, f"missing lemma_0252 finite-bound-to-smallness checklist: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale lemma_0252 finite-bound-to-smallness checklist: {output}"
    return True, f"fresh lemma_0252 finite-bound-to-smallness checklist: {output}"


def check_no_dischargeable(
    checklist: FiniteBoundSmallnessChecklist,
) -> tuple[bool, str]:
    if checklist.dischargeable_now_count:
        return False, "finite-bound-to-smallness checklist contains dischargeable_now items"
    direct_branches = [
        branch.theorem_family
        for branch in checklist.theorem_branches
        if branch.applies_to_lemma_0252
    ]
    if direct_branches:
        return False, "theorem branches apply directly: " + ", ".join(direct_branches)
    return True, "finite-bound-to-smallness branch has no directly dischargeable known route"


def check_smallness_gap(
    checklist: FiniteBoundSmallnessChecklist,
) -> tuple[bool, str]:
    required = {
        "ckn_epsilon_quantity_package",
        "local_vorticity_to_velocity_pressure",
        "finite_to_smallness_decay_or_monotonicity",
        "self_improvement_or_reverse_holder",
        "singular_point_lower_bound_or_concentration_alternative",
        "pressure_and_cutoff_error_control",
    }
    present = {item.item_id for item in checklist.checklist_items}
    missing = sorted(required - present)
    if missing:
        return False, "missing finite-bound-to-smallness checklist items: " + ", ".join(missing)
    if checklist.branch_verdict != "deferred_needs_new_result":
        return False, f"unexpected branch_verdict: {checklist.branch_verdict}"
    if checklist.smallness_only_branch_count < 2:
        return False, "expected at least two smallness-only theorem branches"
    return True, "finite-bound-to-smallness gap is explicit and branch is deferred"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown finite-bound-to-smallness checklist format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render the lemma_0252 finite-bound-to-smallness branch checklist."
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
        "--require-smallness-gap",
        action="store_true",
        help="Fail if the core finite-bound-to-smallness gap is not explicit.",
    )
    parser.add_argument(
        "--require-sources-exist",
        action="store_true",
        help="Fail if local source references are missing.",
    )
    args = parser.parse_args(argv)

    try:
        checklist = build_finite_bound_smallness_checklist(
            proof_obligation_json=args.proof_obligation_json,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report readable setup failures.
        print(f"failed to build lemma_0252 finite-bound-to-smallness checklist: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, checklist, args.format)
        print(message)
        if not ok:
            print("run without --check-output to regenerate the finite-bound-to-smallness checklist", file=sys.stderr)
            return 1
    else:
        written = write_output(output, checklist, args.format)
        print(f"wrote {written}")

    if args.require_no_dischargeable:
        ok, message = check_no_dischargeable(checklist)
        print(message)
        if not ok:
            return 1

    if args.require_smallness_gap:
        ok, message = check_smallness_gap(checklist)
        print(message)
        if not ok:
            return 1

    if args.require_sources_exist:
        missing_sources = _missing_source_refs()
        if missing_sources:
            print("missing source refs: " + ", ".join(missing_sources), file=sys.stderr)
            return 1
        print("all finite-bound-to-smallness checklist source refs exist")

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
