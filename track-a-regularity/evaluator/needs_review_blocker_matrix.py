from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from candidate_obligation_template import TEMPLATE_OBLIGATIONS
from needs_review_obligation_registry import (
    DEFAULT_CANDIDATE_DIR,
    DEFAULT_REPORT_DIR,
    NeedsReviewEntry,
    NeedsReviewRegistry,
    build_registry,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "needs_review_blocker_matrix.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "needs_review_blocker_matrix.json"
TEMPLATE_KEYS = tuple(obligation.key for obligation in TEMPLATE_OBLIGATIONS)
TEMPLATE_LABELS = {obligation.key: obligation.label for obligation in TEMPLATE_OBLIGATIONS}
NON_CLAIMS = (
    "matrix_only",
    "no_new_active_candidate",
    "no_navier_stokes_solution",
    "no_epsilon_regularity_theorem",
    "no_weak_to_smooth_upgrade",
)


class BlockerMatrixError(ValueError):
    pass


@dataclass(frozen=True)
class FamilyBlockerDetail:
    obligation_key: str
    obligation_label: str
    family_blocker: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class FamilyBlockerMatrix:
    blocker_family: str
    candidate_count: int
    core_blocker: str
    details: tuple[FamilyBlockerDetail, ...]


@dataclass(frozen=True)
class BlockerMatrixEntry:
    candidate_id: str
    blocker_family: str
    matrix_family: str
    scaffold_status: str
    promotion_blocker_count: int | None
    scaffold_report: str
    scaffold_summary: str
    scaffold_obligation_keys: tuple[str, ...]
    matrix_obligation_keys: tuple[str, ...]
    scaffold_matrix_consistent: bool
    scaffold_matrix_issues: tuple[str, ...]


@dataclass(frozen=True)
class NeedsReviewBlockerMatrix:
    schema_version: int
    needs_review_count: int
    blocker_family_counts: dict[str, int]
    families: tuple[FamilyBlockerMatrix, ...]
    entries: tuple[BlockerMatrixEntry, ...]
    non_claims: tuple[str, ...]


FAMILY_CORE_BLOCKERS: dict[str, str] = {
    "critical_duhamel_bilinear_formal_only": (
        "Formal Duhamel boundedness is not yet a named continuation criterion for the "
        "actual Leray-projected NSE nonlinearity."
    ),
    "dyadic_flux_exact": (
        "The current positive low-pass flux budget has sign/coercivity risk and does "
        "not yet control a smooth continuation criterion."
    ),
    "parabolic_morrey_enstrophy_exact": (
        "A finite parabolic Morrey enstrophy bound has no identified finite-bound-to-"
        "smallness or compactness/Liouville promotion route."
    ),
}


FAMILY_BLOCKER_DETAILS: dict[str, dict[str, str]] = {
    "critical_duhamel_bilinear_formal_only": {
        "exact_quantity_definitions": (
            "Duhamel bilinear term must define heat semigroup, Leray projection, "
            "product convention, and integration domain."
        ),
        "exact_function_spaces": (
            "Critical space-time norm must name q, p, s or Besov/Morrey indices, "
            "endpoint convention, and domain."
        ),
        "known_result_separation": (
            "Must separate from Kato, Koch-Tataru, Besov-Morrey mild-solution "
            "criteria, Prodi-Serrin, and BKM continuations."
        ),
        "proof_route": (
            "Need a route from bilinear bound to a named continuation criterion; "
            "formal boundedness alone is not enough."
        ),
        "solution_class_bridge": (
            "Must keep smooth mild/classical solution, Leray-Hopf, suitable weak, "
            "and continuation classes separate."
        ),
        "analytic_promotion_blockers": (
            "Must prove the bilinear estimate with the actual NSE Leray-projected "
            "nonlinearity and time integral."
        ),
    },
    "dyadic_flux_exact": {
        "exact_quantity_definitions": (
            "Flux sign, projector normalization, dyadic shell set, and positive or "
            "forward-flux convention must be fixed."
        ),
        "exact_function_spaces": (
            "Flux budget norm and time summability must specify dyadic weights, "
            "endpoints, viscosity, and domain conventions."
        ),
        "known_result_separation": (
            "Must separate from Onsager, LES, energy equality, flux-locality, and "
            "automatic-finiteness results."
        ),
        "proof_route": (
            "Need a coercive route from positive flux envelope to a continuation "
            "criterion; current audit found sign/coercivity risk."
        ),
        "solution_class_bridge": (
            "Must specify whether the flux identity is for smooth solutions only or "
            "weak/LES limits and how it returns to smooth continuation."
        ),
        "analytic_promotion_blockers": (
            "Must repair the low-pass balance Pi_N^LES = dE_N/dt + nu D_N sign "
            "issue and prove coercive forward-cascade control."
        ),
    },
    "parabolic_morrey_enstrophy_exact": {
        "exact_quantity_definitions": (
            "Cylinder geometry, periodic lift, radius/time ranges, vorticity "
            "convention, and beta=1 normalization must remain exact."
        ),
        "exact_function_spaces": (
            "Local energy, pressure, vorticity, and Morrey envelope spaces must "
            "name scale, integrability, and endpoint conventions."
        ),
        "known_result_separation": (
            "Must separate from CKN, ESS, local-energy epsilon-regularity, and "
            "local enstrophy criteria."
        ),
        "proof_route": (
            "Need finite-bound-to-smallness, compactness/Liouville contradiction, "
            "or epsilon-pressure route; none is currently identified."
        ),
        "solution_class_bridge": (
            "Must state the bridge among smooth classical, suitable weak/local "
            "energy, ancient blow-up limit, and smooth continuation."
        ),
        "analytic_promotion_blockers": (
            "Must discharge pressure estimates, smallness extraction, compactness/"
            "Liouville, and smooth-continuation bridge."
        ),
    },
}


FAMILY_BLOCKER_SOURCE_REFS: dict[str, dict[str, tuple[str, ...]]] = {
    "critical_duhamel_bilinear_formal_only": {
        "exact_quantity_definitions": (
            "docs/FINAL_CANDIDATE_TRIAGE.md",
            "logs/step55_duhamel_formal_only_evaluator_20260519.md",
            "track-c-formal/lean/NavierStokesProgram/DuhamelBilinear.lean",
        ),
        "exact_function_spaces": (
            "docs/FINAL_CANDIDATE_TRIAGE.md",
            "docs/KNOWN_CRITICAL_SPACE_CRITERIA.md",
            "docs/definitions/round3_selected_definitions.md",
        ),
        "known_result_separation": (
            "docs/KNOWN_CRITICAL_SPACE_CRITERIA.md",
            "docs/FINAL_CANDIDATE_TRIAGE.md",
            "track-a-regularity/evaluator/checks/duhamel_formal_only.py",
        ),
        "proof_route": (
            "docs/FINAL_CANDIDATE_TRIAGE.md",
            "logs/step55_duhamel_formal_only_evaluator_20260519.md",
            "track-a-regularity/evaluator/checks/duhamel_formal_only.py",
        ),
        "solution_class_bridge": (
            "docs/CANDIDATE_GENERATION_SPEC_V4.md",
            "docs/FINAL_CANDIDATE_TRIAGE.md",
        ),
        "analytic_promotion_blockers": (
            "docs/FINAL_CANDIDATE_TRIAGE.md",
            "logs/step55_duhamel_formal_only_evaluator_20260519.md",
            "track-c-formal/lean/NavierStokesProgram/DuhamelBilinear.lean",
        ),
    },
    "dyadic_flux_exact": {
        "exact_quantity_definitions": (
            "docs/definitions/round3_selected_definitions.md",
            "docs/KNOWN_ENERGY_FLUX_CRITERIA.md",
            "track-c-formal/lean/NavierStokesProgram/ShellProjector.lean",
        ),
        "exact_function_spaces": (
            "docs/definitions/round3_selected_definitions.md",
            "docs/KNOWN_ENERGY_FLUX_CRITERIA.md",
            "track-c-formal/lean/NavierStokesProgram/ShellProjector.lean",
        ),
        "known_result_separation": (
            "docs/KNOWN_ENERGY_FLUX_CRITERIA.md",
            "logs/step50_energy_flux_registry_20260519.md",
        ),
        "proof_route": (
            "docs/LEMMA_0251_FLUX_BALANCE_AUDIT.md",
            "logs/step52_flux_balance_risk_evaluator_20260519.md",
            "track-a-regularity/evaluator/checks/flux_balance_risk.py",
        ),
        "solution_class_bridge": (
            "docs/CANDIDATE_GENERATION_SPEC_V4.md",
            "docs/FINAL_CANDIDATE_TRIAGE.md",
        ),
        "analytic_promotion_blockers": (
            "docs/LEMMA_0251_FLUX_BALANCE_AUDIT.md",
            "logs/step51_flux_balance_audit_20260519.md",
            "logs/step52_flux_balance_risk_evaluator_20260519.md",
            "track-a-regularity/evaluator/checks/flux_balance_risk.py",
        ),
    },
    "parabolic_morrey_enstrophy_exact": {
        "exact_quantity_definitions": (
            "docs/KNOWN_LOCAL_ENSTROPHY_CRITERIA.md",
            "docs/LEMMA_0252_PROOF_OBLIGATIONS.md",
            "track-c-formal/lean/NavierStokesProgram/ParabolicCylinder.lean",
        ),
        "exact_function_spaces": (
            "docs/KNOWN_LOCAL_ENSTROPHY_CRITERIA.md",
            "docs/LEMMA_0252_PROOF_OBLIGATIONS.md",
            "track-c-formal/lean/NavierStokesProgram/LocalEnergy.lean",
        ),
        "known_result_separation": (
            "docs/KNOWN_LOCAL_ENSTROPHY_CRITERIA.md",
            "logs/step49_local_enstrophy_registry_20260519.md",
        ),
        "proof_route": (
            "docs/LEMMA_0252_PROOF_OBLIGATIONS.md",
            "docs/LEMMA_0252_LOCAL_ENERGY_FORMAL_MAP.md",
            "track-c-formal/lean/NavierStokesProgram/ProofObligationGraph.lean",
        ),
        "solution_class_bridge": (
            "docs/CANDIDATE_GENERATION_SPEC_V4.md",
            "docs/LEMMA_0252_LOCAL_ENERGY_FORMAL_MAP.md",
            "track-c-formal/lean/NavierStokesProgram/LocalEnergy.lean",
        ),
        "analytic_promotion_blockers": (
            "docs/LEMMA_0252_PROOF_OBLIGATIONS.md",
            "logs/step53_parabolic_morrey_obligations_20260519.md",
            "logs/step54_parabolic_morrey_evaluator_20260519.md",
            "track-a-regularity/evaluator/checks/parabolic_morrey_obligation.py",
        ),
    },
}


def _ordered_families(family_counts: dict[str, int]) -> tuple[str, ...]:
    canonical = tuple(
        family for family in FAMILY_CORE_BLOCKERS if family in family_counts
    )
    extras = tuple(sorted(set(family_counts) - set(canonical)))
    return canonical + extras


def validate_family_matrix_definitions() -> None:
    expected = set(TEMPLATE_KEYS)
    missing_core = sorted(set(FAMILY_BLOCKER_DETAILS) - set(FAMILY_CORE_BLOCKERS))
    if missing_core:
        raise BlockerMatrixError(
            "families missing core blocker: " + ", ".join(missing_core)
        )
    for family, details in FAMILY_BLOCKER_DETAILS.items():
        actual = set(details)
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        if missing or extra:
            raise BlockerMatrixError(
                f"incomplete matrix for {family}: "
                f"missing={','.join(missing) or 'none'} "
                f"extra={','.join(extra) or 'none'}"
            )
    missing_sources = sorted(
        set(FAMILY_BLOCKER_DETAILS) - set(FAMILY_BLOCKER_SOURCE_REFS)
    )
    extra_sources = sorted(
        set(FAMILY_BLOCKER_SOURCE_REFS) - set(FAMILY_BLOCKER_DETAILS)
    )
    if missing_sources or extra_sources:
        raise BlockerMatrixError(
            "source reference family mismatch: "
            f"missing={','.join(missing_sources) or 'none'} "
            f"extra={','.join(extra_sources) or 'none'}"
        )
    for family, source_refs in FAMILY_BLOCKER_SOURCE_REFS.items():
        actual = set(source_refs)
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        if missing or extra:
            raise BlockerMatrixError(
                f"incomplete source references for {family}: "
                f"missing={','.join(missing) or 'none'} "
                f"extra={','.join(extra) or 'none'}"
            )
        empty = sorted(key for key, refs in source_refs.items() if not refs)
        if empty:
            raise BlockerMatrixError(
                f"empty source references for {family}: " + ",".join(empty)
            )


def _source_refs_for(family: str, obligation_key: str) -> tuple[str, ...]:
    return FAMILY_BLOCKER_SOURCE_REFS[family][obligation_key]


def _family_matrix(family: str, count: int) -> FamilyBlockerMatrix:
    if family not in FAMILY_BLOCKER_DETAILS or family not in FAMILY_CORE_BLOCKERS:
        raise BlockerMatrixError(f"unknown needs_review blocker family: {family}")
    details = tuple(
        FamilyBlockerDetail(
            obligation_key=key,
            obligation_label=TEMPLATE_LABELS[key],
            family_blocker=FAMILY_BLOCKER_DETAILS[family][key],
            source_refs=_source_refs_for(family, key),
        )
        for key in TEMPLATE_KEYS
    )
    return FamilyBlockerMatrix(
        blocker_family=family,
        candidate_count=count,
        core_blocker=FAMILY_CORE_BLOCKERS[family],
        details=details,
    )


def _resolve_report_path(path: str) -> Path:
    report_path = Path(path)
    if report_path.is_absolute():
        return report_path
    return ROOT / report_path


def _string_key_list(items: object, label: str) -> tuple[str, ...]:
    if not isinstance(items, list):
        raise BlockerMatrixError(f"{label} must be a list")
    keys: list[str] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise BlockerMatrixError(f"{label}[{index}] must be an object")
        key = item.get("key")
        if not isinstance(key, str):
            raise BlockerMatrixError(f"{label}[{index}].key must be a string")
        keys.append(key)
    return tuple(keys)


def inspect_scaffold_matrix_consistency(
    *,
    candidate_id: str,
    scaffold_report: str,
    scaffold_status: str,
    matrix_family: str,
) -> tuple[tuple[str, ...], tuple[str, ...], bool, tuple[str, ...]]:
    matrix_keys = tuple(FAMILY_BLOCKER_DETAILS.get(matrix_family, {}))
    issues: list[str] = []
    if matrix_keys != TEMPLATE_KEYS:
        issues.append("matrix_keys_not_template_order")
    if scaffold_status != "present_blocked":
        issues.append(f"scaffold_status={scaffold_status}")
        return (), matrix_keys, False, tuple(issues)

    try:
        report = json.loads(_resolve_report_path(scaffold_report).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return (), matrix_keys, False, ("missing_scaffold_report",)
    except json.JSONDecodeError:
        return (), matrix_keys, False, ("invalid_scaffold_report_json",)

    if not isinstance(report, dict):
        return (), matrix_keys, False, ("scaffold_report_not_object",)

    if report.get("lemma_id") != candidate_id:
        issues.append("lemma_id_mismatch")
    if report.get("candidate_status") != "needs_review":
        issues.append("candidate_status_not_needs_review")
    if report.get("active_candidate") is not False:
        issues.append("active_candidate_not_false")

    try:
        node_keys = _string_key_list(report.get("nodes"), "nodes")
        blocker_keys = _string_key_list(
            report.get("promotion_blockers"),
            "promotion_blockers",
        )
    except BlockerMatrixError as exc:
        return (), matrix_keys, False, (str(exc),)

    if node_keys != TEMPLATE_KEYS:
        issues.append("node_keys_do_not_match_template")
    if blocker_keys != TEMPLATE_KEYS:
        issues.append("promotion_blocker_keys_do_not_match_template")
    if blocker_keys != matrix_keys:
        issues.append("promotion_blocker_keys_do_not_match_matrix")

    return blocker_keys, matrix_keys, not issues, tuple(issues)


def _entry_from_registry_entry(entry: NeedsReviewEntry) -> BlockerMatrixEntry:
    candidate_id = entry.candidate_id
    blocker_family = entry.blocker_family
    scaffold_report = entry.scaffold_report
    scaffold_status = entry.scaffold_status
    matrix_family = (
        blocker_family
        if blocker_family in FAMILY_BLOCKER_DETAILS
        else "missing_matrix_family"
    )
    consistency = inspect_scaffold_matrix_consistency(
        candidate_id=candidate_id,
        scaffold_report=scaffold_report,
        scaffold_status=scaffold_status,
        matrix_family=matrix_family,
    )
    return BlockerMatrixEntry(
        candidate_id=candidate_id,
        blocker_family=blocker_family,
        matrix_family=matrix_family,
        scaffold_status=scaffold_status,
        promotion_blocker_count=entry.promotion_blocker_count,
        scaffold_report=scaffold_report,
        scaffold_summary=entry.scaffold_summary,
        scaffold_obligation_keys=consistency[0],
        matrix_obligation_keys=consistency[1],
        scaffold_matrix_consistent=consistency[2],
        scaffold_matrix_issues=consistency[3],
    )


def build_blocker_matrix(
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
    report_dir: Path = DEFAULT_REPORT_DIR,
) -> NeedsReviewBlockerMatrix:
    validate_family_matrix_definitions()
    registry: NeedsReviewRegistry = build_registry(
        candidate_dir=candidate_dir,
        report_dir=report_dir,
    )
    families = tuple(
        _family_matrix(family, registry.blocker_family_counts[family])
        for family in _ordered_families(registry.blocker_family_counts)
    )
    entries = tuple(_entry_from_registry_entry(entry) for entry in registry.entries)
    unknown = sorted(
        {entry.blocker_family for entry in entries}
        - set(FAMILY_BLOCKER_DETAILS)
    )
    if unknown:
        raise BlockerMatrixError(
            "needs_review entries missing matrix family: " + ", ".join(unknown)
        )
    return NeedsReviewBlockerMatrix(
        schema_version=1,
        needs_review_count=registry.needs_review_count,
        blocker_family_counts=registry.blocker_family_counts,
        families=families,
        entries=entries,
        non_claims=NON_CLAIMS,
    )


def matrix_to_dict(matrix: NeedsReviewBlockerMatrix) -> dict[str, object]:
    return {
        "schema_version": matrix.schema_version,
        "needs_review_count": matrix.needs_review_count,
        "blocker_family_counts": matrix.blocker_family_counts,
        "families": [asdict(family) for family in matrix.families],
        "entries": [asdict(entry) for entry in matrix.entries],
        "non_claims": list(matrix.non_claims),
        "docs": {
            "template_doc": "docs/STEP72_CANDIDATE_OBLIGATION_TEMPLATE.md",
            "registry_doc": "docs/STEP73_NEEDS_REVIEW_OBLIGATION_REGISTRY.md",
            "scaffold_doc": "docs/STEP74_NEEDS_REVIEW_SCAFFOLD_MATERIALIZATION.md",
        },
    }


def render_markdown(matrix: NeedsReviewBlockerMatrix) -> str:
    family_rows = [
        "| blocker family | candidates | core blocker |",
        "|---|---:|---|",
    ]
    for family in matrix.families:
        family_rows.append(
            "| "
            f"`{family.blocker_family}` | "
            f"{family.candidate_count} | "
            f"{family.core_blocker} |"
        )

    detail_rows = [
        "| blocker family | template obligation | family-specific blocker | source refs |",
        "|---|---|---|---|",
    ]
    for family in matrix.families:
        for detail in family.details:
            source_refs = ", ".join(f"`{source}`" for source in detail.source_refs)
            detail_rows.append(
                "| "
                f"`{family.blocker_family}` | "
                f"`{detail.obligation_key}` ({detail.obligation_label}) | "
                f"{detail.family_blocker} | "
                f"{source_refs} |"
            )

    entry_rows = [
        "| candidate | blocker family | scaffold status | blockers | matrix family | matrix consistent | issues |",
        "|---|---|---|---:|---|---|---|",
    ]
    for entry in matrix.entries:
        blockers = (
            "n/a"
            if entry.promotion_blocker_count is None
            else str(entry.promotion_blocker_count)
        )
        consistent = str(entry.scaffold_matrix_consistent).lower()
        issues = ", ".join(entry.scaffold_matrix_issues)
        entry_rows.append(
            "| "
            f"`{entry.candidate_id}` | "
            f"`{entry.blocker_family}` | "
            f"`{entry.scaffold_status}` | "
            f"{blockers} | "
            f"`{entry.matrix_family}` | "
            f"`{consistent}` | "
            f"{issues} |"
        )

    non_claim_rows = [f"- `{item}`" for item in matrix.non_claims]
    return "\n".join(
        (
            "# Needs-Review Family-Specific Blocker Matrix",
            "",
            "Generated by `track-a-regularity/evaluator/needs_review_blocker_matrix.py`.",
            "",
            "This report maps generic Step 72 template obligations to the actual blocker",
            "families for existing `needs_review` records. It does not emit a candidate,",
            "discharge analytic blockers, prove epsilon regularity, or prove Navier-Stokes",
            "regularity.",
            "",
            "## Summary",
            "",
            f"- needs_review_count: `{matrix.needs_review_count}`",
            "",
            *family_rows,
            "",
            "## Matrix",
            "",
            *detail_rows,
            "",
            "## Entries",
            "",
            *entry_rows,
            "",
            "## Non-Claims",
            "",
            *non_claim_rows,
            "",
        )
    )


def render_json(matrix: NeedsReviewBlockerMatrix) -> str:
    return json.dumps(matrix_to_dict(matrix), indent=2, sort_keys=True) + "\n"


def render_output(matrix: NeedsReviewBlockerMatrix, output_format: str) -> str:
    if output_format == "markdown":
        return render_markdown(matrix)
    if output_format == "json":
        return render_json(matrix)
    raise ValueError(f"unknown blocker matrix format: {output_format}")


def write_output(
    output: Path,
    matrix: NeedsReviewBlockerMatrix,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(matrix, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    matrix: NeedsReviewBlockerMatrix,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(matrix, output_format)
    if not output.exists():
        return False, f"missing needs-review blocker matrix: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale needs-review blocker matrix: {output}"
    return True, f"fresh needs-review blocker matrix: {output}"


def check_required_scaffold_status(
    matrix: NeedsReviewBlockerMatrix,
    required_status: str,
) -> tuple[bool, str]:
    mismatches = [
        f"{entry.candidate_id}:{entry.scaffold_status}"
        for entry in matrix.entries
        if entry.scaffold_status != required_status
    ]
    if mismatches:
        return (
            False,
            "needs-review blocker matrix scaffold status mismatch: expected "
            f"{required_status}; " + ", ".join(mismatches),
        )
    return True, f"all matrix entries have scaffold status {required_status}"


def check_matrix_completeness(matrix: NeedsReviewBlockerMatrix) -> tuple[bool, str]:
    expected = set(TEMPLATE_KEYS)
    family_errors: list[str] = []
    for family in matrix.families:
        actual = {detail.obligation_key for detail in family.details}
        if actual != expected:
            missing = sorted(expected - actual)
            extra = sorted(actual - expected)
            family_errors.append(
                f"{family.blocker_family}:missing={missing}:extra={extra}"
            )
    if family_errors:
        return False, "incomplete blocker matrix: " + "; ".join(family_errors)
    return True, "blocker matrix covers every template obligation for every family"


def check_scaffold_matrix_consistency(
    matrix: NeedsReviewBlockerMatrix,
) -> tuple[bool, str]:
    mismatches = [
        f"{entry.candidate_id}:{','.join(entry.scaffold_matrix_issues)}"
        for entry in matrix.entries
        if not entry.scaffold_matrix_consistent
    ]
    if mismatches:
        return False, "scaffold/matrix consistency mismatch: " + "; ".join(mismatches)
    return True, "all scaffold obligation keys match their matrix family"


def check_source_refs(matrix: NeedsReviewBlockerMatrix) -> tuple[bool, str]:
    missing: list[str] = []
    empty: list[str] = []
    for family in matrix.families:
        for detail in family.details:
            label = f"{family.blocker_family}:{detail.obligation_key}"
            if not detail.source_refs:
                empty.append(label)
            for source_ref in detail.source_refs:
                if not (ROOT / source_ref).exists():
                    missing.append(f"{label}:{source_ref}")
    problems: list[str] = []
    if empty:
        problems.append("empty=" + ",".join(empty))
    if missing:
        problems.append("missing=" + ",".join(missing))
    if problems:
        return False, "blocker matrix source reference mismatch: " + "; ".join(problems)
    return True, "all blocker matrix source references exist"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown blocker matrix format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Render family-specific blocker details for existing needs_review "
            "proof-obligation scaffolds."
        )
    )
    parser.add_argument("--candidate-dir", type=Path, default=DEFAULT_CANDIDATE_DIR)
    parser.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT_DIR)
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Blocker matrix output format.",
    )
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--check-output",
        action="store_true",
        help="Check that --output already matches the rendered blocker matrix.",
    )
    parser.add_argument(
        "--require-scaffold-status",
        default=None,
        help="Fail unless every matrix entry has this scaffold status.",
    )
    parser.add_argument(
        "--require-scaffold-matrix-consistency",
        action="store_true",
        help=(
            "Fail unless every scaffold has template-order blocker keys matching "
            "its family-specific matrix."
        ),
    )
    parser.add_argument(
        "--require-source-refs",
        action="store_true",
        help="Fail unless every family-specific blocker row has existing source refs.",
    )
    parser.add_argument(
        "--require-count",
        type=int,
        default=7,
        help="Fail unless this many needs_review records are present. Use -1 to disable.",
    )
    args = parser.parse_args(argv)

    try:
        matrix = build_blocker_matrix(
            candidate_dir=args.candidate_dir,
            report_dir=args.report_dir,
        )
    except BlockerMatrixError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.require_count >= 0 and matrix.needs_review_count != args.require_count:
        print(
            f"needs_review_count mismatch: expected {args.require_count}, "
            f"found {matrix.needs_review_count}",
            file=sys.stderr,
        )
        return 1

    ok, message = check_matrix_completeness(matrix)
    print(message)
    if not ok:
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, matrix, args.format)
        print(message)
        if not ok:
            print("run without --check-output to regenerate the matrix", file=sys.stderr)
            return 1
    else:
        written = write_output(output, matrix, args.format)
        print(f"wrote {written}")

    if args.require_scaffold_status is not None:
        ok, message = check_required_scaffold_status(
            matrix,
            args.require_scaffold_status,
        )
        print(message)
        if not ok:
            return 1

    if args.require_scaffold_matrix_consistency:
        ok, message = check_scaffold_matrix_consistency(matrix)
        print(message)
        if not ok:
            return 1

    if args.require_source_refs:
        ok, message = check_source_refs(matrix)
        print(message)
        if not ok:
            return 1

    print(f"needs_review_count: {matrix.needs_review_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
