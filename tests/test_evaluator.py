from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "track-a-regularity" / "evaluator"))

from run_all import evaluate
from schema import LemmaCandidate, load_candidate


def test_seed_controls_match_expected_results() -> None:
    expected_first_failures = {
        "lemma_0001": None,
        "lemma_0002": None,
        "lemma_0003": "galilean_check",
        "lemma_0004": "scaling_check",
        "lemma_0005": "taylor_green_test",
    }
    for ident in expected_first_failures:
        path = ROOT / "track-a-regularity/candidates" / f"{ident}.yaml"
        candidate = load_candidate(path)
        report = evaluate(candidate)
        assert report.matches_expected, candidate.id
        first_failure = report.first_failure.name if report.first_failure else None
        assert first_failure == expected_first_failures[candidate.id]


def test_known_controls_are_labeled_separately_from_new_candidates() -> None:
    candidate = load_candidate(ROOT / "track-a-regularity/candidates/lemma_0001.yaml")
    report = evaluate(candidate)
    assert report.final_status == "known_control"
    novelty = [result for result in report.results if result.name == "novelty_check"]
    assert novelty
    assert novelty[0].status == "known_control"


def test_ambiguous_unknown_candidate_fails_hypothesis_completeness() -> None:
    candidate = LemmaCandidate(
        id="lemma_test_missing_hypotheses",
        generated_by="pytest",
        date="2026-05-19",
        statement_en="If a solution has bounded diagnostic quantity, then it extends smoothly.",
        statement_lean_skel="def placeholder : Prop := True",
        type="blow_up_criterion",
        related_known=(),
        evaluator={},
        expected_evaluator={"status": "fail", "first_expected_failure": "hypothesis_completeness_check"},
        status="pending",
    )
    report = evaluate(candidate)
    assert report.first_failure is not None
    assert report.first_failure.name == "hypothesis_completeness_check"


def test_prodi_endpoint_candidate_is_rejected_for_separate_endpoint_treatment() -> None:
    candidate = LemmaCandidate(
        id="lemma_test_endpoint",
        generated_by="pytest",
        date="2026-05-19",
        statement_en=(
            "Let u be a smooth divergence-free solution of the Navier-Stokes equations "
            "on T^3 with viscosity nu > 0 on [0,T). If u belongs to L^infty_t L^3_x, "
            "then u extends smoothly past time T."
        ),
        statement_lean_skel="def placeholder : Prop := True",
        type="blow_up_criterion",
        related_known=("Prodi1959", "Serrin1962"),
        evaluator={},
        expected_evaluator={"status": "fail", "first_expected_failure": "endpoint_check"},
        status="pending",
    )
    report = evaluate(candidate)
    assert report.first_failure is not None
    assert report.first_failure.name == "endpoint_check"


def test_convex_integration_guard_rejects_broad_weak_energy_claim() -> None:
    candidate = LemmaCandidate(
        id="lemma_test_bv_guard",
        generated_by="pytest",
        date="2026-05-19",
        statement_en=(
            "Let u be a weak solution of the 3D incompressible Navier-Stokes equations "
            "on T^3 with viscosity nu > 0 and zero force on [0,T). Every weak solution "
            "conserves kinetic energy."
        ),
        statement_lean_skel="def placeholder : Prop := True",
        type="weak_solution_claim",
        related_known=("BuckmasterVicolNonuniqueness",),
        evaluator={},
        expected_evaluator={"status": "fail", "first_expected_failure": "convex_integration_check"},
        status="pending",
    )
    report = evaluate(candidate)
    assert report.first_failure is not None
    assert report.first_failure.name == "convex_integration_check"


def test_taylor_green_negative_control_uses_existing_diagnostics() -> None:
    candidate = load_candidate(ROOT / "track-a-regularity/candidates/lemma_0005.yaml")
    report = evaluate(candidate)
    failure = report.first_failure
    assert failure is not None
    assert failure.name == "taylor_green_test"
    assert failure.evidence["spectrum_tail_max"] > failure.evidence["claimed_bound"]


def test_bkm_with_extra_assumption_is_not_counted_as_new_candidate() -> None:
    candidate = load_candidate(ROOT / "track-a-regularity/candidates/lemma_0192.yaml")
    report = evaluate(candidate)
    assert report.first_failure is None
    assert report.final_status == "known_control_with_extra_assumption"
    extension = [result for result in report.results if result.name == "known_control_extension_check"]
    assert extension
    assert extension[0].status == "known_control_with_extra_assumption"


def test_undefined_pressure_proxy_is_rejected() -> None:
    candidate = load_candidate(ROOT / "track-a-regularity/candidates/lemma_0195.yaml")
    report = evaluate(candidate)
    failure = report.first_failure
    assert failure is not None
    assert failure.name == "pressure_proxy_check"


def test_duplicate_family_detector_marks_repeated_survivor_template() -> None:
    candidate = load_candidate(ROOT / "track-a-regularity/candidates/lemma_0197.yaml")
    report = evaluate(candidate)
    duplicate = [result for result in report.results if result.name == "duplicate_family_check"]
    assert duplicate
    assert duplicate[0].status == "review"
    assert duplicate[0].evidence["primary"] == "lemma_0192"


def test_selected_round3_family_requires_definition_tightening() -> None:
    candidate = load_candidate(ROOT / "track-a-regularity/candidates/lemma_0204.yaml")
    report = evaluate(candidate)
    failure = report.first_failure
    assert failure is not None
    assert failure.name == "definition_rule_check"
    assert failure.evidence["family"] == "dyadic_flux"


def test_geometric_known_result_check_preempts_definition_rule() -> None:
    expected_families = {
        "lemma_0202": "localized_vortex_stretching",
        "lemma_0203": "strain_eigenvalue",
        "lemma_0207": "vorticity_direction",
        "lemma_0208": "depleted_vortex_stretching",
        "lemma_0210": "strain_vorticity_alignment",
    }
    for ident, family in expected_families.items():
        candidate = load_candidate(ROOT / "track-a-regularity/candidates" / f"{ident}.yaml")
        report = evaluate(candidate)
        failure = report.first_failure
        assert failure is not None
        assert failure.name == "geometric_known_result_check"
        assert failure.evidence["family"] == family


def test_critical_space_known_result_check_filters_broad_besov_morrey() -> None:
    expected_families = {
        "lemma_0201": "critical_besov",
        "lemma_0206": "critical_morrey",
    }
    for ident, family in expected_families.items():
        candidate = load_candidate(ROOT / "track-a-regularity/candidates" / f"{ident}.yaml")
        report = evaluate(candidate)
        failure = report.first_failure
        assert failure is not None
        assert failure.name == "critical_space_known_result_check"
        assert failure.evidence["family"] == family


def test_definition_tightened_dyadic_flux_candidate_needs_rewrite_review() -> None:
    candidate = load_candidate(ROOT / "track-a-regularity/candidates/lemma_0251.yaml")
    report = evaluate(candidate)
    assert report.matches_expected
    assert report.first_failure is None
    assert report.final_status == "needs_review"
    definition = [result for result in report.results if result.name == "definition_rule_check"]
    assert definition
    assert definition[0].status == "pass"
    flux_review = [result for result in report.results if result.name == "flux_balance_risk_check"]
    assert flux_review
    assert flux_review[0].status == "review"
    assert flux_review[0].evidence["family"] == "dyadic_flux_exact"


def test_definition_tightened_parabolic_morrey_candidate_needs_obligation_review() -> None:
    candidate = load_candidate(ROOT / "track-a-regularity/candidates/lemma_0252.yaml")
    report = evaluate(candidate)
    assert report.matches_expected
    assert report.first_failure is None
    assert report.final_status == "needs_review"
    definition = [result for result in report.results if result.name == "definition_rule_check"]
    assert definition
    assert definition[0].status == "pass"
    morrey_review = [result for result in report.results if result.name == "parabolic_morrey_obligation_check"]
    assert morrey_review
    assert morrey_review[0].status == "review"
    assert morrey_review[0].evidence["family"] == "parabolic_morrey_enstrophy_exact"


def test_critical_duhamel_family_is_formal_only_review() -> None:
    for ident in ("lemma_0209", "lemma_0219", "lemma_0229", "lemma_0239", "lemma_0249"):
        candidate = load_candidate(ROOT / "track-a-regularity/candidates" / f"{ident}.yaml")
        report = evaluate(candidate)
        assert report.matches_expected
        assert report.first_failure is None
        assert report.final_status == "needs_review"
        review = [result for result in report.results if result.name == "duhamel_formal_only_check"]
        assert review
        assert review[0].status == "review"
        assert review[0].evidence["family"] == "critical_duhamel_bilinear_formal_only"
