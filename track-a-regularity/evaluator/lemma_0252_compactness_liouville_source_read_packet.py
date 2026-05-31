from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from lemma_0252_theorem_artifact_review_queue import (
    DEFAULT_JSON_OUTPUT as DEFAULT_QUEUE_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_QUEUE_MARKDOWN,
)
from lemma_0252_theorem_artifact_review_queue_operator_dependency import (
    DEFAULT_JSON_OUTPUT as DEFAULT_QUEUE_OPERATOR_DEPENDENCY_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_QUEUE_OPERATOR_DEPENDENCY_MARKDOWN,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = (
    DEFAULT_REPORT_DIR / "lemma_0252_compactness_liouville_source_read_packet.md"
)
DEFAULT_JSON_OUTPUT = (
    DEFAULT_REPORT_DIR / "lemma_0252_compactness_liouville_source_read_packet.json"
)
DEFAULT_PAPERS_INDEX = ROOT / "papers/blockers/index.md"

GAP_ID = "gap_003"
SOURCE_BRANCH = "compactness_liouville"
QUEUE_STATUS = "blocked_waiting_for_real_theorem_artifact"
PACKET_STATUS = "blocked_source_read_only"
BRANCH_VERDICT = "blocked_needs_new_result"
REVIEW_PHASE = "non_promotional_source_read_packet"
REQUIRED_ARTIFACT_TYPE = "compactness_liouville_discharge_bundle"

NON_CLAIMS = (
    "read_only_compactness_liouville_source_read_packet",
    "non_promotional_gap_003_review_only",
    "no_candidate_promotion",
    "no_candidate_emission",
    "no_blocker_discharge",
    "no_process_gate_opened",
    "no_file_copy",
    "no_compactness_theorem",
    "no_liouville_theorem",
    "no_backward_uniqueness_application",
    "no_weak_to_smooth_upgrade",
    "no_navier_stokes_solution",
)


@dataclass(frozen=True)
class CompactnessLiouvilleSourceRead:
    source_id: str
    title: str
    blocker_family: str
    relative_path: str
    source_type: str
    priority: str
    direct_branch_support: bool
    read_basis: tuple[str, ...]
    theorem_hypotheses: tuple[str, ...]
    conclusion_shape: str
    mismatch_fields: tuple[str, ...]
    source_verdict: str
    source_exists: bool
    exact_discharge_artifact_present: bool
    actionable_now: bool
    may_discharge_gap: bool


@dataclass(frozen=True)
class CompactnessLiouvillePacketCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class Lemma0252CompactnessLiouvilleSourceReadPacket:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    gap_id: str
    source_branch: str
    packet_status: str
    branch_verdict: str
    review_phase: str
    theorem_artifact_review_queue_markdown: str
    theorem_artifact_review_queue_json: str
    theorem_artifact_review_queue_operator_dependency_markdown: str
    theorem_artifact_review_queue_operator_dependency_json: str
    papers_blockers_index: str
    missing_artifact: str
    required_artifact_type: str
    minimum_acceptance_checks: tuple[str, ...]
    required_review_evidence: tuple[str, ...]
    source_ref_count: int
    source_read_count: int
    direct_branch_source_read_count: int
    cross_cutting_source_read_count: int
    source_with_hypothesis_count: int
    source_with_conclusion_count: int
    mismatch_field_count: int
    blocked_source_read_count: int
    actionable_source_read_count: int
    may_discharge_source_read_count: int
    exact_discharge_artifact_count: int
    direct_theorem_artifact_count: int
    queue_literature_source_count: int
    queue_direct_branch_source_count: int
    queue_cross_cutting_source_count: int
    queue_status: str
    queue_actionable_now: bool
    queue_may_discharge_blocker: bool
    queue_direct_theorem_artifact_present: bool
    theorem_artifact_review_queue_operator_dependency_consistent: bool
    failed_theorem_artifact_review_queue_operator_dependency_check_count: int
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    packet_check_count: int
    passed_packet_check_count: int
    failed_packet_check_count: int
    packet_consistent: bool
    issues: tuple[str, ...]
    source_reads: tuple[CompactnessLiouvilleSourceRead, ...]
    checks: tuple[CompactnessLiouvillePacketCheck, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]
    theorem_artifact_review_queue_snapshot: dict[str, object]
    theorem_artifact_review_queue_operator_dependency_snapshot: dict[str, object]


def _load_json(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"expected object JSON report: {path}")
    return data


def _check(
    *,
    key: str,
    expected: object,
    observed: object,
    source_artifacts: tuple[str, ...],
) -> CompactnessLiouvillePacketCheck:
    return CompactnessLiouvillePacketCheck(
        key=key,
        expected=str(expected),
        observed=str(observed),
        passed=expected == observed,
        source_artifacts=source_artifacts,
    )


def _missing_sources(source_refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(source for source in source_refs if not (ROOT / source).exists())


def _direct_sources() -> tuple[str, ...]:
    return (
        "track-a-regularity/reports/lemma_0252_theorem_artifact_review_queue.md",
        "track-a-regularity/reports/lemma_0252_theorem_artifact_review_queue.json",
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_operator_dependency.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_operator_dependency.json"
        ),
        "papers/blockers/index.md",
    )


def _source_reads() -> tuple[CompactnessLiouvilleSourceRead, ...]:
    rows = (
        CompactnessLiouvilleSourceRead(
            source_id="knss_0709_3599",
            title="Koch-Nadirashvili-Seregin-Sverak ancient Liouville source",
            blocker_family="compactness_liouville",
            relative_path=(
                "papers/blockers/compactness_liouville/"
                "0709.3599_KNSS2009_liouville_acta_math.pdf"
            ),
            source_type="pdf",
            priority="high",
            direct_branch_support=True,
            read_basis=(
                "abstract and introduction",
                "ancient solution and Liouville theorem setup",
                "axisymmetric restriction and boundedness assumptions",
            ),
            theorem_hypotheses=(
                "ancient Navier-Stokes solution with strong boundedness hypotheses",
                "axisymmetric or otherwise structurally restricted setting",
                "regularity/backward-uniqueness framework inputs already available",
            ),
            conclusion_shape=(
                "Liouville rigidity or triviality for ancient solutions in the restricted "
                "setting"
            ),
            mismatch_fields=(
                "imports axisymmetric or special structural hypotheses not present in general T3",
                "does not construct the ancient suitable limit from lemma_0252 terminal rescaling",
                "does not show finite parabolic Morrey enstrophy gives the boundedness package",
            ),
            source_verdict="outside_setting_axisymmetric_not_discharge",
            source_exists=True,
            exact_discharge_artifact_present=False,
            actionable_now=False,
            may_discharge_gap=False,
        ),
        CompactnessLiouvilleSourceRead(
            source_id="axisymmetric_1011_5066",
            title="Axisymmetric Liouville follow-up",
            blocker_family="compactness_liouville",
            relative_path=(
                "papers/blockers/compactness_liouville/"
                "1011.5066_axisymmetric_liouville_2010.pdf"
            ),
            source_type="pdf",
            priority="normal",
            direct_branch_support=True,
            read_basis=(
                "abstract and introduction",
                "axisymmetric ancient-solution hypotheses",
                "Liouville conclusion and comparison with KNSS",
            ),
            theorem_hypotheses=(
                "axisymmetric ancient Navier-Stokes solution",
                "boundedness or scale-invariant control tailored to the axisymmetric class",
                "regularity class sufficient to apply the Liouville argument",
            ),
            conclusion_shape=(
                "axisymmetric Liouville-type rigidity under the paper's structural assumptions"
            ),
            mismatch_fields=(
                "axisymmetry is not part of lemma_0252",
                "the result is not a general periodic suitable-weak compactness theorem",
                "does not supply nontriviality or pressure compactness for a terminal blow-up limit",
            ),
            source_verdict="outside_setting_axisymmetric_not_discharge",
            source_exists=True,
            exact_discharge_artifact_present=False,
            actionable_now=False,
            may_discharge_gap=False,
        ),
        CompactnessLiouvilleSourceRead(
            source_id="backward_uniqueness_1509_04940",
            title="Backward uniqueness remarks",
            blocker_family="compactness_liouville",
            relative_path=(
                "papers/blockers/compactness_liouville/"
                "1509.04940_backward_uniqueness_remarks.pdf"
            ),
            source_type="pdf",
            priority="normal",
            direct_branch_support=True,
            read_basis=(
                "abstract and introduction",
                "backward uniqueness or unique-continuation inputs",
                "Navier-Stokes regularity application context",
            ),
            theorem_hypotheses=(
                "solution class with enough regularity for backward uniqueness",
                "decay, boundedness, or continuation hypotheses tied to the unique-continuation tool",
                "a PDE limit already known to solve the required system",
            ),
            conclusion_shape=(
                "a backward-uniqueness or unique-continuation implication usable only after "
                "the correct ancient limit exists"
            ),
            mismatch_fields=(
                "tool-level backward uniqueness is not the missing compactness construction",
                "requires inputs not derived from finite parabolic Morrey enstrophy",
                "does not provide a Liouville contradiction for the current general T3 setting",
            ),
            source_verdict="partial_backward_uniqueness_tool_only",
            source_exists=True,
            exact_discharge_artifact_present=False,
            actionable_now=False,
            may_discharge_gap=False,
        ),
        CompactnessLiouvilleSourceRead(
            source_id="lorentz_1407_5129",
            title="Lorentz-space Navier-Stokes regularity comparison",
            blocker_family="compactness_liouville",
            relative_path=(
                "papers/blockers/compactness_liouville/"
                "1407.5129_lorentz_navier_stokes.pdf"
            ),
            source_type="pdf",
            priority="normal",
            direct_branch_support=True,
            read_basis=(
                "abstract and introduction",
                "critical Lorentz-space regularity assumptions",
                "comparison to ESS endpoint routes",
            ),
            theorem_hypotheses=(
                "critical velocity integrability in Lorentz-type spaces",
                "suitable weak or mild solution framework matching that input",
                "known endpoint or near-endpoint regularity hypotheses",
            ),
            conclusion_shape=(
                "regularity under critical Lorentz-space assumptions rather than a Morrey "
                "enstrophy Liouville theorem"
            ),
            mismatch_fields=(
                "hypothesis is a different critical velocity-space input",
                "does not build an ancient suitable limit from the lemma_0252 envelope",
                "does not remove the compactness and nontriviality blockers",
            ),
            source_verdict="partial_different_critical_space",
            source_exists=True,
            exact_discharge_artifact_present=False,
            actionable_now=False,
            may_discharge_gap=False,
        ),
        CompactnessLiouvilleSourceRead(
            source_id="seregin_axisym_math0702720",
            title="Seregin axisymmetric sufficient local regularity",
            blocker_family="compactness_liouville",
            relative_path=(
                "papers/blockers/compactness_liouville/"
                "math0702720_seregin_axisym_sufficient_2007.pdf"
            ),
            source_type="pdf",
            priority="normal",
            direct_branch_support=True,
            read_basis=(
                "abstract and introduction",
                "axisymmetric local regularity criterion",
                "L3 or scale-invariant local assumptions",
            ),
            theorem_hypotheses=(
                "axisymmetric Navier-Stokes setting",
                "local L3-type or related scale-invariant assumptions",
                "special-structure hypotheses excluding the general periodic case",
            ),
            conclusion_shape=(
                "local regularity for axisymmetric solutions under sufficient local criteria"
            ),
            mismatch_fields=(
                "axisymmetric structure is outside lemma_0252",
                "local sufficient criterion is not an ancient compactness/Liouville discharge",
                "does not provide a general suitable-limit theorem for periodic terminal rescaling",
            ),
            source_verdict="partial_axisymmetric_local_criterion",
            source_exists=True,
            exact_discharge_artifact_present=False,
            actionable_now=False,
            may_discharge_gap=False,
        ),
        CompactnessLiouvilleSourceRead(
            source_id="tao_localisation_1108_1165",
            title="Localisation and compactness for Navier-Stokes",
            blocker_family="cross_cutting",
            relative_path=(
                "papers/blockers/cross_cutting/"
                "1108.1165_tao2013_localisation_compactness.pdf"
            ),
            source_type="pdf",
            priority="top",
            direct_branch_support=False,
            read_basis=(
                "abstract and introduction",
                "localised energy and enstrophy estimate framework",
                "compactness/localisation implications between Navier-Stokes formulations",
            ),
            theorem_hypotheses=(
                "smooth finite-energy or periodic Navier-Stokes formulation",
                "localised energy/enstrophy estimates in a large-data framework",
                "compactness-oriented comparison of global regularity formulations",
            ),
            conclusion_shape=(
                "framework-level localisation/compactness control, not a Liouville discharge "
                "for lemma_0252"
            ),
            mismatch_fields=(
                "helps organize the localised quantities but does not prove the required ancient limit",
                "does not supply a Liouville or backward-uniqueness theorem for the gap_003 setting",
                "does not turn finite parabolic Morrey enstrophy into the needed bounded ancient profile",
            ),
            source_verdict="framework_anchor_not_discharge",
            source_exists=True,
            exact_discharge_artifact_present=False,
            actionable_now=False,
            may_discharge_gap=False,
        ),
    )
    return tuple(
        row.__class__(
            **{
                **asdict(row),
                "source_exists": (ROOT / row.relative_path).exists(),
            }
        )
        for row in rows
    )


def _queue_item_for_gap(queue: dict[str, object], gap_id: str) -> dict[str, object]:
    items = queue.get("queue_items", ())
    if not isinstance(items, list):
        raise ValueError("expected list field `queue_items`")
    for item in items:
        if isinstance(item, dict) and item.get("gap_id") == gap_id:
            return item
    raise ValueError(f"missing queue item for {gap_id}")


def build_compactness_liouville_source_read_packet(
    *,
    theorem_artifact_review_queue_json: Path = DEFAULT_QUEUE_JSON,
    theorem_artifact_review_queue_operator_dependency_json: Path = (
        DEFAULT_QUEUE_OPERATOR_DEPENDENCY_JSON
    ),
    papers_blockers_index: Path = DEFAULT_PAPERS_INDEX,
) -> Lemma0252CompactnessLiouvilleSourceReadPacket:
    queue = _load_json(theorem_artifact_review_queue_json)
    operator_dependency = _load_json(theorem_artifact_review_queue_operator_dependency_json)
    queue_item = _queue_item_for_gap(queue, GAP_ID)
    source_reads = _source_reads()

    source_ids = tuple(row.source_id for row in source_reads)
    source_paths = tuple(row.relative_path for row in source_reads)
    queue_source_ids = tuple(str(item) for item in queue_item.get("source_ids", ()))
    queue_source_paths = tuple(str(item) for item in queue_item.get("source_paths", ()))

    source_refs = tuple(
        dict.fromkeys(
            _direct_sources()
            + source_paths
            + tuple(str(item) for item in queue.get("source_refs", ()))
            + tuple(str(item) for item in operator_dependency.get("source_refs", ()))
        )
    )
    missing_sources = _missing_sources(source_refs)

    direct_branch_count = sum(1 for row in source_reads if row.direct_branch_support)
    exact_discharge_artifact_count = sum(
        1 for row in source_reads if row.exact_discharge_artifact_present
    )
    actionable_source_read_count = sum(1 for row in source_reads if row.actionable_now)
    may_discharge_source_read_count = sum(1 for row in source_reads if row.may_discharge_gap)
    mismatch_field_count = sum(len(row.mismatch_fields) for row in source_reads)
    source_with_hypothesis_count = sum(1 for row in source_reads if row.theorem_hypotheses)
    source_with_conclusion_count = sum(1 for row in source_reads if row.conclusion_shape)

    queue_source = (
        "track-a-regularity/reports/lemma_0252_theorem_artifact_review_queue.md",
        "track-a-regularity/reports/lemma_0252_theorem_artifact_review_queue.json",
    )
    operator_dependency_source = (
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_operator_dependency.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_operator_dependency.json"
        ),
    )

    checks = (
        _check(
            key="queue.lemma_id.expected_lemma_0252",
            expected="lemma_0252",
            observed=queue.get("lemma_id"),
            source_artifacts=queue_source,
        ),
        _check(
            key="queue.candidate_status.remains_needs_review",
            expected="needs_review",
            observed=queue.get("candidate_status"),
            source_artifacts=queue_source,
        ),
        _check(
            key="queue.active_candidate.remains_false",
            expected=False,
            observed=queue.get("active_candidate"),
            source_artifacts=queue_source,
        ),
        _check(
            key="gap.id.expected_gap_003",
            expected=GAP_ID,
            observed=queue_item.get("gap_id"),
            source_artifacts=queue_source,
        ),
        _check(
            key="gap.source_branch.expected_compactness_liouville",
            expected=SOURCE_BRANCH,
            observed=queue_item.get("source_branch"),
            source_artifacts=queue_source,
        ),
        _check(
            key="gap.required_artifact_type.expected",
            expected=REQUIRED_ARTIFACT_TYPE,
            observed=queue_item.get("required_artifact_type"),
            source_artifacts=queue_source,
        ),
        _check(
            key="gap.queue_status.remains_blocked",
            expected=QUEUE_STATUS,
            observed=queue_item.get("queue_status"),
            source_artifacts=queue_source,
        ),
        _check(
            key="source_read_count.matches_queue_gap_003",
            expected=queue_item.get("literature_source_count"),
            observed=len(source_reads),
            source_artifacts=queue_source + source_paths,
        ),
        _check(
            key="direct_branch_source_read_count.matches_queue_gap_003",
            expected=queue_item.get("direct_branch_source_count"),
            observed=direct_branch_count,
            source_artifacts=queue_source + source_paths,
        ),
        _check(
            key="cross_cutting_source_read_count.matches_queue_gap_003",
            expected=queue_item.get("cross_cutting_source_count"),
            observed=len(source_reads) - direct_branch_count,
            source_artifacts=queue_source + source_paths,
        ),
        _check(
            key="source_ids.match_queue_gap_003",
            expected=queue_source_ids,
            observed=source_ids,
            source_artifacts=queue_source,
        ),
        _check(
            key="source_paths.match_queue_gap_003",
            expected=queue_source_paths,
            observed=source_paths,
            source_artifacts=queue_source,
        ),
        _check(
            key="all_source_reads.exist",
            expected=len(source_reads),
            observed=sum(1 for row in source_reads if row.source_exists),
            source_artifacts=source_paths,
        ),
        _check(
            key="all_source_reads.have_hypothesis_fields",
            expected=len(source_reads),
            observed=source_with_hypothesis_count,
            source_artifacts=source_paths,
        ),
        _check(
            key="all_source_reads.have_conclusion_shape",
            expected=len(source_reads),
            observed=source_with_conclusion_count,
            source_artifacts=source_paths,
        ),
        _check(
            key="mismatch_field_count.expected_eighteen",
            expected=18,
            observed=mismatch_field_count,
            source_artifacts=source_paths,
        ),
        _check(
            key="exact_discharge_artifact_count.remains_zero",
            expected=0,
            observed=exact_discharge_artifact_count,
            source_artifacts=source_paths,
        ),
        _check(
            key="actionable_source_read_count.remains_zero",
            expected=0,
            observed=actionable_source_read_count,
            source_artifacts=source_paths,
        ),
        _check(
            key="may_discharge_source_read_count.remains_zero",
            expected=0,
            observed=may_discharge_source_read_count,
            source_artifacts=source_paths,
        ),
        _check(
            key="queue.direct_theorem_artifact_present.false",
            expected=False,
            observed=queue_item.get("direct_theorem_artifact_present"),
            source_artifacts=queue_source,
        ),
        _check(
            key="queue.actionable_now.false",
            expected=False,
            observed=queue_item.get("actionable_now"),
            source_artifacts=queue_source,
        ),
        _check(
            key="queue.may_discharge_blocker.false",
            expected=False,
            observed=queue_item.get("may_discharge_blocker"),
            source_artifacts=queue_source,
        ),
        _check(
            key="operator_dependency.consistent.true",
            expected=True,
            observed=operator_dependency.get(
                "theorem_artifact_review_queue_operator_dependency_consistent"
            ),
            source_artifacts=operator_dependency_source,
        ),
        _check(
            key="operator_dependency.failed_checks.remain_zero",
            expected=0,
            observed=operator_dependency.get(
                "failed_theorem_artifact_review_queue_operator_dependency_check_count"
            ),
            source_artifacts=operator_dependency_source,
        ),
        _check(
            key="operator_dependency.direct_theorem_artifact_count.remains_zero",
            expected=0,
            observed=operator_dependency.get("direct_theorem_artifact_count"),
            source_artifacts=operator_dependency_source,
        ),
        _check(
            key="all.process_gate_open_authorized.false",
            expected=(False, False),
            observed=(
                queue.get("process_gate_open_authorized"),
                operator_dependency.get("process_gate_open_authorized"),
            ),
            source_artifacts=queue_source + operator_dependency_source,
        ),
        _check(
            key="all.blocker_state_changed.false",
            expected=(False, False),
            observed=(
                queue.get("blocker_state_changed"),
                operator_dependency.get("blocker_state_changed"),
            ),
            source_artifacts=queue_source + operator_dependency_source,
        ),
        _check(
            key="all.candidate_emission_authorized.false",
            expected=(False, False),
            observed=(
                queue.get("candidate_emission_authorized"),
                operator_dependency.get("candidate_emission_authorized"),
            ),
            source_artifacts=queue_source + operator_dependency_source,
        ),
        _check(
            key="source_refs.missing_count.remains_zero",
            expected=0,
            observed=len(missing_sources),
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.include_papers_blockers_index",
            expected=True,
            observed="papers/blockers/index.md" in source_refs and papers_blockers_index.exists(),
            source_artifacts=("papers/blockers/index.md",),
        ),
        _check(
            key="source_refs.include_knss_0709_3599",
            expected=True,
            observed=(
                "papers/blockers/compactness_liouville/"
                "0709.3599_KNSS2009_liouville_acta_math.pdf"
            )
            in source_refs,
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.include_tao_localisation",
            expected=True,
            observed=(
                "papers/blockers/cross_cutting/"
                "1108.1165_tao2013_localisation_compactness.pdf"
            )
            in source_refs,
            source_artifacts=source_refs,
        ),
        _check(
            key="packet_status.remains_blocked_source_read_only",
            expected=PACKET_STATUS,
            observed=PACKET_STATUS,
            source_artifacts=_direct_sources(),
        ),
        _check(
            key="branch_verdict.remains_blocked_needs_new_result",
            expected=BRANCH_VERDICT,
            observed=BRANCH_VERDICT,
            source_artifacts=_direct_sources(),
        ),
    )

    issues = tuple(check.key for check in checks if not check.passed)
    process_gate_open_authorized = bool(
        queue.get("process_gate_open_authorized")
    ) or bool(operator_dependency.get("process_gate_open_authorized"))
    blocker_state_changed = bool(queue.get("blocker_state_changed")) or bool(
        operator_dependency.get("blocker_state_changed")
    )
    candidate_emission_authorized = bool(
        queue.get("candidate_emission_authorized")
    ) or bool(operator_dependency.get("candidate_emission_authorized"))

    return Lemma0252CompactnessLiouvilleSourceReadPacket(
        schema_version=1,
        lemma_id=str(queue.get("lemma_id")),
        candidate_status=str(queue.get("candidate_status")),
        active_candidate=bool(queue.get("active_candidate")),
        gap_id=GAP_ID,
        source_branch=SOURCE_BRANCH,
        packet_status=PACKET_STATUS,
        branch_verdict=BRANCH_VERDICT,
        review_phase=REVIEW_PHASE,
        theorem_artifact_review_queue_markdown=str(DEFAULT_QUEUE_MARKDOWN),
        theorem_artifact_review_queue_json=str(DEFAULT_QUEUE_JSON),
        theorem_artifact_review_queue_operator_dependency_markdown=str(
            DEFAULT_QUEUE_OPERATOR_DEPENDENCY_MARKDOWN
        ),
        theorem_artifact_review_queue_operator_dependency_json=str(
            DEFAULT_QUEUE_OPERATOR_DEPENDENCY_JSON
        ),
        papers_blockers_index=str(DEFAULT_PAPERS_INDEX),
        missing_artifact=str(queue_item.get("missing_artifact")),
        required_artifact_type=str(queue_item.get("required_artifact_type")),
        minimum_acceptance_checks=tuple(
            str(item) for item in queue_item.get("minimum_acceptance_checks", ())
        ),
        required_review_evidence=tuple(
            str(item) for item in queue_item.get("required_review_evidence", ())
        ),
        source_ref_count=len(source_refs),
        source_read_count=len(source_reads),
        direct_branch_source_read_count=direct_branch_count,
        cross_cutting_source_read_count=len(source_reads) - direct_branch_count,
        source_with_hypothesis_count=source_with_hypothesis_count,
        source_with_conclusion_count=source_with_conclusion_count,
        mismatch_field_count=mismatch_field_count,
        blocked_source_read_count=len(source_reads),
        actionable_source_read_count=actionable_source_read_count,
        may_discharge_source_read_count=may_discharge_source_read_count,
        exact_discharge_artifact_count=exact_discharge_artifact_count,
        direct_theorem_artifact_count=exact_discharge_artifact_count,
        queue_literature_source_count=int(queue_item.get("literature_source_count", 0)),
        queue_direct_branch_source_count=int(queue_item.get("direct_branch_source_count", 0)),
        queue_cross_cutting_source_count=int(queue_item.get("cross_cutting_source_count", 0)),
        queue_status=str(queue_item.get("queue_status")),
        queue_actionable_now=bool(queue_item.get("actionable_now")),
        queue_may_discharge_blocker=bool(queue_item.get("may_discharge_blocker")),
        queue_direct_theorem_artifact_present=bool(
            queue_item.get("direct_theorem_artifact_present")
        ),
        theorem_artifact_review_queue_operator_dependency_consistent=bool(
            operator_dependency.get(
                "theorem_artifact_review_queue_operator_dependency_consistent"
            )
        ),
        failed_theorem_artifact_review_queue_operator_dependency_check_count=int(
            operator_dependency.get(
                "failed_theorem_artifact_review_queue_operator_dependency_check_count",
                0,
            )
        ),
        process_gate_open_authorized=process_gate_open_authorized,
        blocker_state_changed=blocker_state_changed,
        candidate_emission_authorized=candidate_emission_authorized,
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        packet_check_count=len(checks),
        passed_packet_check_count=sum(1 for check in checks if check.passed),
        failed_packet_check_count=len(issues),
        packet_consistent=len(issues) == 0,
        issues=issues,
        source_reads=source_reads,
        checks=checks,
        source_refs=source_refs,
        non_claims=NON_CLAIMS,
        theorem_artifact_review_queue_snapshot=queue,
        theorem_artifact_review_queue_operator_dependency_snapshot=operator_dependency,
    )


def render_markdown(report: Lemma0252CompactnessLiouvilleSourceReadPacket) -> str:
    lines = [
        "# Lemma 0252 Compactness Liouville Source Read Packet",
        "",
        "## Summary",
        "",
        f"- lemma_id: `{report.lemma_id}`",
        f"- candidate_status: `{report.candidate_status}`",
        f"- active_candidate: `{str(report.active_candidate).lower()}`",
        f"- gap_id: `{report.gap_id}`",
        f"- source_branch: `{report.source_branch}`",
        f"- packet_status: `{report.packet_status}`",
        f"- branch_verdict: `{report.branch_verdict}`",
        f"- source_read_count: `{report.source_read_count}`",
        f"- source_ref_count: `{report.source_ref_count}`",
        f"- direct_branch_source_read_count: `{report.direct_branch_source_read_count}`",
        f"- cross_cutting_source_read_count: `{report.cross_cutting_source_read_count}`",
        f"- mismatch_field_count: `{report.mismatch_field_count}`",
        f"- exact_discharge_artifact_count: `{report.exact_discharge_artifact_count}`",
        f"- actionable_source_read_count: `{report.actionable_source_read_count}`",
        f"- may_discharge_source_read_count: `{report.may_discharge_source_read_count}`",
        f"- packet_check_count: `{report.packet_check_count}`",
        f"- failed_packet_check_count: `{report.failed_packet_check_count}`",
        f"- packet_consistent: `{str(report.packet_consistent).lower()}`",
        f"- missing_source_count: `{report.missing_source_count}`",
        f"- process_gate_open_authorized: `{str(report.process_gate_open_authorized).lower()}`",
        f"- blocker_state_changed: `{str(report.blocker_state_changed).lower()}`",
        f"- candidate_emission_authorized: `{str(report.candidate_emission_authorized).lower()}`",
        "",
        "## Missing Artifact",
        "",
        report.missing_artifact,
        "",
        "## Source Reads",
        "",
        "| source_id | priority | direct | verdict | hypotheses | conclusion | mismatches |",
        "|---|---|---:|---|---|---|---|",
    ]
    for row in report.source_reads:
        hypotheses = "; ".join(row.theorem_hypotheses)
        mismatches = "; ".join(row.mismatch_fields)
        lines.append(
            "| "
            f"`{row.source_id}` | `{row.priority}` | "
            f"{str(row.direct_branch_support).lower()} | `{row.source_verdict}` | "
            f"{hypotheses} | {row.conclusion_shape} | {mismatches} |"
        )

    lines.extend(
        [
            "",
            "## Checks",
            "",
            "| key | expected | observed | passed |",
            "|---|---|---|---:|",
        ]
    )
    for check in report.checks:
        lines.append(
            f"| `{check.key}` | `{check.expected}` | `{check.observed}` | "
            f"{str(check.passed).lower()} |"
        )

    lines.extend(["", "## Source Refs", ""])
    lines.extend(f"- `{source}`" for source in report.source_refs)
    lines.extend(["", "## Non-Claims", ""])
    lines.extend(f"- `{claim}`" for claim in report.non_claims)
    lines.append("")
    return "\n".join(lines)


def render_json(report: Lemma0252CompactnessLiouvilleSourceReadPacket) -> str:
    return json.dumps(asdict(report), indent=2, sort_keys=True) + "\n"


def check_sources(report: Lemma0252CompactnessLiouvilleSourceReadPacket) -> tuple[bool, str]:
    if report.missing_source_count:
        return False, "missing source refs: " + ", ".join(report.missing_sources)
    return True, "all compactness/Liouville source-read packet sources exist"


def check_consistent(
    report: Lemma0252CompactnessLiouvilleSourceReadPacket,
) -> tuple[bool, str]:
    if not report.packet_consistent:
        return False, "inconsistent compactness/Liouville source-read packet: " + ", ".join(
            report.issues
        )
    return True, "compactness/Liouville source-read packet is consistent"


def check_blocked(report: Lemma0252CompactnessLiouvilleSourceReadPacket) -> tuple[bool, str]:
    if (
        report.packet_status != PACKET_STATUS
        or report.branch_verdict != BRANCH_VERDICT
        or report.actionable_source_read_count != 0
        or report.may_discharge_source_read_count != 0
        or report.exact_discharge_artifact_count != 0
        or report.process_gate_open_authorized
        or report.blocker_state_changed
        or report.candidate_emission_authorized
    ):
        return False, "compactness/Liouville source-read packet is not blocked"
    return True, "compactness/Liouville source-read packet remains blocked"


def check_output(
    output: Path,
    report: Lemma0252CompactnessLiouvilleSourceReadPacket,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_json(report) if output_format == "json" else render_markdown(report)
    if not output.exists():
        return False, f"missing compactness/Liouville source-read packet output: {output}"
    observed = output.read_text(encoding="utf-8")
    if observed != expected:
        return False, f"stale compactness/Liouville source-read packet output: {output}"
    return True, f"fresh compactness/Liouville source-read packet output: {output}"


def _write_output(
    *,
    output: Path,
    report: Lemma0252CompactnessLiouvilleSourceReadPacket,
    output_format: str,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    text = render_json(report) if output_format == "json" else render_markdown(report)
    output.write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a read-only source-read packet for lemma_0252 gap_003."
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    parser.add_argument("--require-consistent", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    args = parser.parse_args(argv)

    report = build_compactness_liouville_source_read_packet()
    output = args.output
    if output is None:
        output = DEFAULT_JSON_OUTPUT if args.format == "json" else DEFAULT_MARKDOWN_OUTPUT

    if not args.check_output:
        _write_output(output=output, report=report, output_format=args.format)

    failures: list[str] = []
    if args.check_output:
        ok, message = check_output(output, report, args.format)
        print(message)
        if not ok:
            failures.append(message)
    if args.require_sources_exist:
        ok, message = check_sources(report)
        print(message)
        if not ok:
            failures.append(message)
    if args.require_consistent:
        ok, message = check_consistent(report)
        print(message)
        if not ok:
            failures.append(message)
    if args.require_blocked:
        ok, message = check_blocked(report)
        print(message)
        if not ok:
            failures.append(message)

    print(f"source_read_count: {report.source_read_count}")
    print(f"packet_check_count: {report.packet_check_count}")
    print(f"failed_packet_check_count: {report.failed_packet_check_count}")
    print(f"exact_discharge_artifact_count: {report.exact_discharge_artifact_count}")
    print(f"candidate_emission_authorized: {str(report.candidate_emission_authorized).lower()}")

    if failures:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
