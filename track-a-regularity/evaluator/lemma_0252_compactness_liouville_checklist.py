from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

from lemma_0252_blocker_known_theorem_mapping import (
    build_known_theorem_mapping,
)
from proof_obligation_blockers import DEFAULT_INPUT


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "lemma_0252_compactness_liouville_checklist.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "lemma_0252_compactness_liouville_checklist.json"

CHECKLIST_ITEM_VERDICTS = (
    "missing_required_input",
    "partial_vocabulary_only",
    "dependent_on_new_result",
)
THEOREM_VERDICTS = (
    "deferred_needs_new_result",
    "outside_setting_only",
)
LOCAL_SOURCE_REFS = (
    "track-a-regularity/reports/lemma_0252_blocker_known_theorem_mapping.md",
    "track-a-regularity/reports/lemma_0252_blocker_known_theorem_mapping.json",
    "track-a-regularity/reports/lemma_0252_proof_obligation_graph.json",
    "docs/LEMMA_0252_PROOF_OBLIGATIONS.md",
    "docs/KNOWN_LOCAL_ENSTROPHY_CRITERIA.md",
    "docs/LEMMA_0252_LOCAL_ENERGY_FORMAL_MAP.md",
    "docs/STEP87_LEMMA_0252_KNOWN_THEOREM_MAPPING.md",
    "track-c-formal/lean/NavierStokesProgram/LocalEnergy.lean",
    "track-c-formal/lean/NavierStokesProgram/ProofObligationGraph.lean",
    "track-c-formal/lean/NavierStokesProgram/SolutionClasses.lean",
)
NON_CLAIMS = (
    "read_only_compactness_liouville_checklist",
    "no_candidate_promotion",
    "no_blocker_discharge",
    "no_ancient_solution_compactness_theorem",
    "no_liouville_theorem",
    "no_backward_uniqueness_application",
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
class CompactnessLiouvilleChecklist:
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
    outside_setting_branch_count: int
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
            item_id="ancient_solution_class",
            required_artifact=(
                "A precise ancient suitable or finite-local-energy solution class produced by "
                "terminal rescaling."
            ),
            exact_required_input=(
                "domain, time interval, pressure convention, local energy inequality, and "
                "solution-class relation to the original smooth periodic solution."
            ),
            current_project_status=(
                "Track C has finite vocabulary for suitable weak metadata, but no compactness "
                "theorem or ancient-limit construction."
            ),
            evidence_ref="track-c-formal/lean/NavierStokesProgram/LocalEnergy.lean",
            blocker_effect="Without this class, no Liouville or backward-uniqueness theorem has a target.",
            verdict="partial_vocabulary_only",
        ),
        _checklist_item(
            item_id="rescaling_compactness",
            required_artifact=(
                "A blow-up sequence extraction theorem preserving the local enstrophy Morrey "
                "bound under parabolic rescaling."
            ),
            exact_required_input=(
                "uniform local energy bounds, pressure compactness, convergence topology, and "
                "scale-invariant vorticity envelope persistence."
            ),
            current_project_status=(
                "The proof-obligation graph names this as a blocker; no compactness statement "
                "exists in docs or Lean artifacts."
            ),
            evidence_ref="docs/LEMMA_0252_PROOF_OBLIGATIONS.md",
            blocker_effect="The compactness/Liouville branch cannot start without a limit object.",
            verdict="missing_required_input",
        ),
        _checklist_item(
            item_id="pressure_local_energy_package",
            required_artifact="A local pressure and local-energy package compatible with the rescaled limit.",
            exact_required_input=(
                "pressure equation, local/nonlocal pressure decomposition, Calderon-Zygmund or "
                "replacement estimates, and cutoff-error handling."
            ),
            current_project_status=(
                "Existing local-energy formal map records metadata only and does not derive the "
                "pressure package from finite local enstrophy."
            ),
            evidence_ref="docs/LEMMA_0252_LOCAL_ENERGY_FORMAL_MAP.md",
            blocker_effect="Known backward-uniqueness or Liouville routes need a well-posed PDE limit.",
            verdict="missing_required_input",
        ),
        _checklist_item(
            item_id="nontriviality_condition",
            required_artifact="A normalized singular blow-up profile that is provably nonzero.",
            exact_required_input=(
                "normalization tied to a terminal singularity, lower-bound persistence, and "
                "compatibility with the chosen convergence topology."
            ),
            current_project_status=(
                "No terminal singularity contradiction setup or lower-bound persistence lemma "
                "has been stated."
            ),
            evidence_ref="docs/LEMMA_0252_PROOF_OBLIGATIONS.md",
            blocker_effect="A zero limit gives no contradiction and cannot be excluded by Liouville theory.",
            verdict="missing_required_input",
        ),
        _checklist_item(
            item_id="liouville_or_backward_uniqueness_theorem",
            required_artifact=(
                "A theorem excluding nonzero ancient profiles with bounded local enstrophy Morrey "
                "envelope in the exact solution class."
            ),
            exact_required_input=(
                "named theorem statement, hypotheses, boundary/domain assumptions, pressure "
                "assumptions, and conclusion strong enough to contradict nontriviality."
            ),
            current_project_status=(
                "Step 87 found ESS/Seregin/KNSS comparison anchors but no directly applicable "
                "known theorem."
            ),
            evidence_ref="track-a-regularity/reports/lemma_0252_blocker_known_theorem_mapping.md",
            blocker_effect="This is the core new-result target if the finite-envelope statement is kept.",
            verdict="dependent_on_new_result",
        ),
        _checklist_item(
            item_id="return_to_smooth_continuation",
            required_artifact=(
                "A bridge from excluded singular profiles or terminal local regularity to smooth "
                "classical continuation past T."
            ),
            exact_required_input=(
                "uniform local regularity near terminal time plus a named BKM, Serrin, or "
                "high-Sobolev continuation criterion."
            ),
            current_project_status=(
                "Step 87 maps BKM/Prodi-Serrin/Constantin-Fefferman as non-direct continuation "
                "anchors only."
            ),
            evidence_ref="track-a-regularity/reports/lemma_0252_blocker_known_theorem_mapping.md",
            blocker_effect="Even a successful Liouville branch still needs a smooth continuation bridge.",
            verdict="dependent_on_new_result",
        ),
    )


def _canonical_theorem_branches() -> tuple[TheoremBranch, ...]:
    return (
        _theorem_branch(
            theorem_family="ESS backward uniqueness branch",
            required_setting=(
                "endpoint critical velocity/backward-uniqueness hypotheses for a compatible "
                "ancient limit."
            ),
            applies_to_lemma_0252=False,
            mismatch=(
                "lemma_0252 provides finite local vorticity-enstrophy metadata, not the endpoint "
                "velocity class or compactness setup required by ESS-style arguments."
            ),
            verdict="deferred_needs_new_result",
        ),
        _theorem_branch(
            theorem_family="Seregin Type-I scale-invariant branch",
            required_setting=(
                "a Type-I or scale-invariant ancient-profile class with exact velocity/pressure "
                "hypotheses and an exclusion theorem."
            ),
            applies_to_lemma_0252=False,
            mismatch=(
                "the finite local enstrophy Morrey envelope is adjacent but not equivalent to a "
                "named Type-I criterion with a known Liouville conclusion."
            ),
            verdict="deferred_needs_new_result",
        ),
        _theorem_branch(
            theorem_family="KNSS axisymmetric Liouville family",
            required_setting="axisymmetric or special-geometry ancient solution setting.",
            applies_to_lemma_0252=False,
            mismatch=(
                "the periodic general 3D statement has no axisymmetry or special geometry, so this "
                "branch remains outside-setting comparison only."
            ),
            verdict="outside_setting_only",
        ),
    )


def _missing_source_refs() -> tuple[str, ...]:
    return tuple(source for source in LOCAL_SOURCE_REFS if not (ROOT / source).exists())


def build_compactness_liouville_checklist(
    *,
    proof_obligation_json: Path = DEFAULT_INPUT,
) -> CompactnessLiouvilleChecklist:
    mapping = build_known_theorem_mapping(proof_obligation_json=proof_obligation_json)
    compactness_rows = tuple(
        row.candidate_theorem
        for row in mapping.rows
        if row.blocker_id == "compactness_liouville"
    )
    if len(compactness_rows) < 2:
        raise ValueError("Step 87 compactness_liouville mapping must have at least two rows")
    if mapping.resolvable_known_count:
        raise ValueError("Step 87 mapping unexpectedly has resolvable_known rows")

    checklist_items = _canonical_checklist_items()
    theorem_branches = _canonical_theorem_branches()
    return CompactnessLiouvilleChecklist(
        schema_version=1,
        lemma_id=mapping.lemma_id,
        candidate_status=mapping.candidate_status,
        active_candidate=mapping.active_candidate,
        source_blocker_id="compactness_liouville",
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
        outside_setting_branch_count=sum(
            1 for branch in theorem_branches if branch.verdict == "outside_setting_only"
        ),
        mapping_theorem_rows=compactness_rows,
        checklist_items=checklist_items,
        theorem_branches=theorem_branches,
        source_refs=LOCAL_SOURCE_REFS,
        non_claims=NON_CLAIMS,
    )


def checklist_to_dict(checklist: CompactnessLiouvilleChecklist) -> dict[str, object]:
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
        "outside_setting_branch_count": checklist.outside_setting_branch_count,
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


def render_markdown(checklist: CompactnessLiouvilleChecklist) -> str:
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
            "# Lemma 0252 Compactness/Liouville Branch Checklist",
            "",
            "Generated by `track-a-regularity/evaluator/lemma_0252_compactness_liouville_checklist.py`.",
            "",
            "This read-only checklist expands the Step 87 `compactness_liouville` blocker into",
            "the exact artifacts that would be required before this branch could discharge a",
            "`lemma_0252` promotion blocker. It does not prove or promote anything.",
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
            f"- outside_setting_branch_count: `{checklist.outside_setting_branch_count}`",
            "",
            "## Step 87 Compactness Rows",
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


def render_json(checklist: CompactnessLiouvilleChecklist) -> str:
    return json.dumps(checklist_to_dict(checklist), indent=2, sort_keys=True) + "\n"


def render_output(checklist: CompactnessLiouvilleChecklist, output_format: str) -> str:
    if output_format == "markdown":
        return render_markdown(checklist)
    if output_format == "json":
        return render_json(checklist)
    raise ValueError(f"unknown compactness/Liouville checklist format: {output_format}")


def write_output(
    output: Path,
    checklist: CompactnessLiouvilleChecklist,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(checklist, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    checklist: CompactnessLiouvilleChecklist,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(checklist, output_format)
    if not output.exists():
        return False, f"missing lemma_0252 compactness/Liouville checklist: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale lemma_0252 compactness/Liouville checklist: {output}"
    return True, f"fresh lemma_0252 compactness/Liouville checklist: {output}"


def check_no_dischargeable(
    checklist: CompactnessLiouvilleChecklist,
) -> tuple[bool, str]:
    if checklist.dischargeable_now_count:
        return False, "compactness/Liouville checklist contains dischargeable_now items"
    direct_branches = [
        branch.theorem_family
        for branch in checklist.theorem_branches
        if branch.applies_to_lemma_0252
    ]
    if direct_branches:
        return False, "theorem branches apply directly: " + ", ".join(direct_branches)
    return True, "compactness/Liouville branch has no directly dischargeable known route"


def check_missing_core(
    checklist: CompactnessLiouvilleChecklist,
) -> tuple[bool, str]:
    required = {
        "rescaling_compactness",
        "pressure_local_energy_package",
        "nontriviality_condition",
        "liouville_or_backward_uniqueness_theorem",
    }
    present = {item.item_id for item in checklist.checklist_items}
    missing = sorted(required - present)
    if missing:
        return False, "missing core checklist items: " + ", ".join(missing)
    if checklist.branch_verdict != "deferred_needs_new_result":
        return False, f"unexpected branch_verdict: {checklist.branch_verdict}"
    return True, "compactness/Liouville core blockers are explicit and branch is deferred"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown compactness/Liouville checklist format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render the lemma_0252 compactness/Liouville branch checklist."
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
        "--require-missing-core",
        action="store_true",
        help="Fail if the core compactness/Liouville blockers are not explicit.",
    )
    parser.add_argument(
        "--require-sources-exist",
        action="store_true",
        help="Fail if local source references are missing.",
    )
    args = parser.parse_args(argv)

    try:
        checklist = build_compactness_liouville_checklist(
            proof_obligation_json=args.proof_obligation_json,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report readable setup failures.
        print(f"failed to build lemma_0252 compactness/Liouville checklist: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, checklist, args.format)
        print(message)
        if not ok:
            print("run without --check-output to regenerate the compactness/Liouville checklist", file=sys.stderr)
            return 1
    else:
        written = write_output(output, checklist, args.format)
        print(f"wrote {written}")

    if args.require_no_dischargeable:
        ok, message = check_no_dischargeable(checklist)
        print(message)
        if not ok:
            return 1

    if args.require_missing_core:
        ok, message = check_missing_core(checklist)
        print(message)
        if not ok:
            return 1

    if args.require_sources_exist:
        missing_sources = _missing_source_refs()
        if missing_sources:
            print("missing source refs: " + ", ".join(missing_sources), file=sys.stderr)
            return 1
        print("all compactness/Liouville checklist source refs exist")

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
