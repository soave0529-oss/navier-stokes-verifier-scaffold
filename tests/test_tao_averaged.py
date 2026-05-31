from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "track-b-blowup" / "solver"))

from tao_averaged import TaoCascadeConfig, simulate, summarize


def test_truncated_cascade_reaches_targets_and_accelerates() -> None:
    config = TaoCascadeConfig(n0=40, transfers=8, dtau=0.004)
    rows = simulate(config)
    summary = summarize(config, rows, elapsed_seconds=0.0)
    assert len(rows) == config.transfers
    assert all(row.reached_target for row in rows)
    assert summary["physical_dt_last"] < summary["physical_dt_first"]
    assert summary["weighted_receiver_growth"] > 1.0


def test_truncated_cascade_rejects_subcritical_alpha() -> None:
    config = TaoCascadeConfig(alpha=0.5)
    try:
        simulate(config)
    except ValueError as exc:
        assert "supercritical alpha" in str(exc)
    else:
        raise AssertionError("expected ValueError for critical alpha")
