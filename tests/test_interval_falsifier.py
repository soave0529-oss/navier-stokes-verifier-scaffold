from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "track-b-blowup" / "solver" / "interval"))

from falsify import evaluate_default_inequalities


def test_default_interval_inequalities_include_expected_passes_and_fails() -> None:
    results = {result.id: result for result in evaluate_default_inequalities(ROOT)}
    assert results["ineq_0001_tg_divergence_small"].status == "pass"
    assert results["ineq_0002_bad_tg_tail_le_005"].status == "fail"
    assert results["ineq_0003_tao_proxy_weighted_growth"].status == "pass"
    assert results["ineq_0004_bad_kida_enstrophy_nonincreasing"].status == "fail"
    assert results["ineq_0005_houluo_energy_nonincreasing"].status == "pass"
