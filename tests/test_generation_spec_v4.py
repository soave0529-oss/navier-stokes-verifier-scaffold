from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "track-a-regularity" / "evaluator"))

from generation_spec_v4 import assess_candidate
from needs_review_blocker_sources import build_source_index, write_output
from preflight_v4 import main as preflight_main
from proof_obligation_blockers import load_blocker_summary, write_summary
from proof_obligation_report import lemma_0252_graph_report, report_to_dict
from schema import LemmaCandidate, load_candidate


def write_zero_blocker_report(tmp_path: Path, candidate_id: str) -> tuple[Path, Path]:
    report_path = tmp_path / f"{candidate_id}_proof_obligations.json"
    summary_path = tmp_path / f"{candidate_id}_proof_obligation_summary.json"
    data = report_to_dict(lemma_0252_graph_report())
    data["lemma_id"] = candidate_id
    data["candidate_status"] = "candidate"
    data["active_candidate"] = True
    data["promotion_blockers"] = []
    report_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_summary(summary_path, load_blocker_summary(report_path), "json")
    return report_path, summary_path


def write_source_index(tmp_path: Path) -> tuple[Path, Path]:
    markdown_path = tmp_path / "needs_review_blocker_sources.md"
    json_path = tmp_path / "needs_review_blocker_sources.json"
    index = build_source_index()
    write_output(markdown_path, index, "markdown")
    write_output(json_path, index, "json")
    return markdown_path, json_path


def v4_markers() -> list[str]:
    return [
        "V4:ExactQuantityDefinitions",
        "V4:ExactFunctionSpaces",
        "V4:KnownResultSeparation",
        "V4:ProofRoute",
        "V4:SolutionClassBridge",
        "V4:ZeroProofObligationBlockers",
        "V4:FreshBlockerSourceIndex",
    ]


def test_v4_preflight_rejects_duhamel_placeholder_family() -> None:
    candidate = load_candidate(ROOT / "track-a-regularity/candidates/lemma_0209.yaml")
    assessment = assess_candidate(candidate)
    assert not assessment.emit_ready
    assert any("critical space-time norm" in reason for reason in assessment.reasons)


def test_v4_preflight_rejects_review_candidate_without_markers() -> None:
    candidate = load_candidate(ROOT / "track-a-regularity/candidates/lemma_0252.yaml")
    assessment = assess_candidate(candidate)
    assert not assessment.emit_ready
    assert any("expected_evaluator.status" in reason for reason in assessment.reasons)
    assert any("missing v4 metadata markers" in reason for reason in assessment.reasons)


def test_v4_preflight_blocks_candidate_without_proof_obligation_gate() -> None:
    candidate = LemmaCandidate(
        id="lemma_v4_synthetic_exact_shape",
        generated_by="pytest",
        date="2026-05-20",
        statement_en=(
            "Let u be a smooth divergence-free mean-zero solution of the 3D incompressible "
            "Navier-Stokes equations on T^3 with viscosity nu > 0 and zero force on [0,T). "
            "Define X(u) as the explicitly indexed L^4_t Besov B^{1/2}_{2,1} norm on [0,T) x T^3. "
            "If X(u) is finite and the documented proof route derives a named BKM continuation "
            "criterion without changing solution class, then u extends smoothly past time T."
        ),
        statement_lean_skel="def lemma_v4_synthetic_exact_shape : Prop := True",
        type="hypothesis_complete_v4_exact",
        related_known=tuple(v4_markers()),
        evaluator={},
        expected_evaluator={"status": "candidate"},
        status="pending",
        why_interesting="Synthetic gate-negative fixture for v4 preflight.",
    )
    assessment = assess_candidate(candidate)
    assert not assessment.emit_ready
    assert any(
        "missing expected_evaluator.proof_obligation_report_json" in reason
        for reason in assessment.reasons
    )
    assert any(
        "missing expected_evaluator.proof_obligation_summary_json" in reason
        for reason in assessment.reasons
    )
    assert any(
        "missing expected_evaluator.blocker_source_index_markdown" in reason
        for reason in assessment.reasons
    )
    assert any(
        "missing expected_evaluator.blocker_source_index_json" in reason
        for reason in assessment.reasons
    )


def test_v4_preflight_blocks_candidate_with_nonzero_proof_obligation_blockers(tmp_path) -> None:
    report_path = tmp_path / "blocked_report.json"
    summary_path = tmp_path / "blocked_summary.json"
    data = report_to_dict(lemma_0252_graph_report())
    data["lemma_id"] = "lemma_v4_blocked"
    data["candidate_status"] = "candidate"
    data["active_candidate"] = True
    report_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_summary(summary_path, load_blocker_summary(report_path), "json")
    source_index_markdown, source_index_json = write_source_index(tmp_path)

    candidate = LemmaCandidate(
        id="lemma_v4_blocked",
        generated_by="pytest",
        date="2026-05-20",
        statement_en=(
            "Let u be a smooth divergence-free mean-zero solution of the 3D incompressible "
            "Navier-Stokes equations on T^3 with viscosity nu > 0 and zero force on [0,T). "
            "Define X(u) as an indexed norm with all function spaces explicit. If X(u) is finite "
            "and the documented proof route derives smooth continuation without changing solution "
            "class, then u extends smoothly past time T."
        ),
        statement_lean_skel="def lemma_v4_blocked : Prop := True",
        type="hypothesis_complete_v4_exact",
        related_known=tuple(v4_markers()),
        evaluator={},
        expected_evaluator={
            "status": "candidate",
            "proof_obligation_report_json": str(report_path),
            "proof_obligation_summary_json": str(summary_path),
            "blocker_source_index_markdown": str(source_index_markdown),
            "blocker_source_index_json": str(source_index_json),
        },
        status="pending",
        why_interesting="Synthetic blocked proof-obligation fixture.",
    )
    assessment = assess_candidate(candidate)
    assert not assessment.emit_ready
    assert any("still has promotion blockers" in reason for reason in assessment.reasons)


def test_v4_preflight_allows_exact_audited_candidate_shape(tmp_path) -> None:
    report_path, summary_path = write_zero_blocker_report(
        tmp_path, "lemma_v4_synthetic_exact_shape"
    )
    source_index_markdown, source_index_json = write_source_index(tmp_path)
    candidate = LemmaCandidate(
        id="lemma_v4_synthetic_exact_shape",
        generated_by="pytest",
        date="2026-05-20",
        statement_en=(
            "Let u be a smooth divergence-free mean-zero solution of the 3D incompressible "
            "Navier-Stokes equations on T^3 with viscosity nu > 0 and zero force on [0,T). "
            "Define X(u) as the explicitly indexed L^4_t Besov B^{1/2}_{2,1} norm on [0,T) x T^3. "
            "If X(u) is finite and the documented proof route derives a named BKM continuation "
            "criterion without changing solution class, then u extends smoothly past time T."
        ),
        statement_lean_skel="def lemma_v4_synthetic_exact_shape : Prop := True",
        type="hypothesis_complete_v4_exact",
        related_known=tuple(v4_markers()),
        evaluator={},
        expected_evaluator={
            "status": "candidate",
            "proof_obligation_report_json": str(report_path),
            "proof_obligation_summary_json": str(summary_path),
            "blocker_source_index_markdown": str(source_index_markdown),
            "blocker_source_index_json": str(source_index_json),
        },
        status="pending",
        why_interesting="Synthetic positive-control shape for the v4 generation preflight.",
    )
    assessment = assess_candidate(candidate)
    assert assessment.emit_ready
    assert assessment.reasons == ()


def test_v4_preflight_blocks_stale_source_index(tmp_path) -> None:
    report_path, summary_path = write_zero_blocker_report(
        tmp_path, "lemma_v4_stale_source_index"
    )
    source_index_markdown, source_index_json = write_source_index(tmp_path)
    source_index_json.write_text("stale\n", encoding="utf-8")
    candidate = LemmaCandidate(
        id="lemma_v4_stale_source_index",
        generated_by="pytest",
        date="2026-05-20",
        statement_en=(
            "Let u be a smooth divergence-free mean-zero solution of the 3D incompressible "
            "Navier-Stokes equations on T^3 with viscosity nu > 0 and zero force on [0,T). "
            "Define X(u) as the explicitly indexed L^4_t Besov B^{1/2}_{2,1} norm. If X(u) "
            "is finite and the documented proof route derives a named continuation criterion "
            "without changing solution class, then u extends smoothly past time T."
        ),
        statement_lean_skel="def lemma_v4_stale_source_index : Prop := True",
        type="hypothesis_complete_v4_exact",
        related_known=tuple(v4_markers()),
        evaluator={},
        expected_evaluator={
            "status": "candidate",
            "proof_obligation_report_json": str(report_path),
            "proof_obligation_summary_json": str(summary_path),
            "blocker_source_index_markdown": str(source_index_markdown),
            "blocker_source_index_json": str(source_index_json),
        },
        status="pending",
        why_interesting="Synthetic stale source-index fixture.",
    )
    assessment = assess_candidate(candidate)
    assert not assessment.emit_ready
    assert any("stale needs-review blocker source index" in reason for reason in assessment.reasons)


def test_v4_preflight_cli_skips_existing_non_candidate_pool(capsys) -> None:
    exit_code = preflight_main([str(ROOT / "track-a-regularity/candidates")])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "summary: checked=0 skipped=252 blocked=0" in output


def test_v4_preflight_cli_blocks_bad_candidate_yaml(tmp_path, capsys) -> None:
    path = tmp_path / "lemma_9999.yaml"
    path.write_text(
        """
id: lemma_9999
generated_by: pytest
date: 2026-05-20
statement_en: A candidate with a critical space-time norm and no exact gate metadata.
statement_lean_skel: "def lemma_9999 : Prop := True"
type: bad_v4_candidate_shape
related_known: []
evaluator: {}
expected_evaluator:
  status: candidate
status: pending
""".lstrip()
    )

    exit_code = preflight_main([str(path)])
    output = capsys.readouterr().out
    assert exit_code == 1
    assert "lemma_9999: blocked" in output
    assert "missing v4 metadata markers" in output


def test_v4_preflight_cli_allows_good_candidate_yaml(tmp_path, capsys) -> None:
    path = tmp_path / "lemma_9998.yaml"
    report_path, summary_path = write_zero_blocker_report(tmp_path, "lemma_9998")
    source_index_markdown, source_index_json = write_source_index(tmp_path)
    path.write_text(
        f"""
id: lemma_9998
generated_by: pytest
date: 2026-05-20
statement_en: >
  Let u be a smooth classical solution on [0,T) x T^3. Define X(u) as the
  indexed L^4_t Besov B^{{1/2}}_{{2,1}} norm on that cylinder. If X(u) is finite
  and the documented proof route derives BKM continuation without changing
  solution class, then u extends smoothly past T.
statement_lean_skel: "def lemma_9998 : Prop := True"
type: good_v4_candidate_shape
related_known:
  - V4:ExactQuantityDefinitions
  - V4:ExactFunctionSpaces
  - V4:KnownResultSeparation
  - V4:ProofRoute
  - V4:SolutionClassBridge
  - V4:ZeroProofObligationBlockers
  - V4:FreshBlockerSourceIndex
evaluator: {{}}
expected_evaluator:
  status: candidate
  proof_obligation_report_json: "{report_path}"
  proof_obligation_summary_json: "{summary_path}"
  blocker_source_index_markdown: "{source_index_markdown}"
  blocker_source_index_json: "{source_index_json}"
status: pending
why_interesting: Synthetic CLI fixture for the v4 emission gate.
""".lstrip()
    )

    exit_code = preflight_main([str(path)])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "lemma_9998: ready" in output
