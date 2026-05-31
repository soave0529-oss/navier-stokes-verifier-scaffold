from __future__ import annotations

import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "track-b-blowup" / "solver"))

from initial_conditions import anti_parallel_vortex_tubes_initial, kida_pelz_initial, self_similar_swirl_initial
from pseudospectral import PseudoSpectralNSE, SolverConfig


def _projected_divergence(n: int, u: np.ndarray) -> float:
    solver = PseudoSpectralNSE(SolverConfig(n=n, t_end=0.0))
    row = solver.diagnostics(0, 0.0, solver.project(solver.fft(u)))
    return row.div_max


def test_kida_pelz_initial_condition_is_projectable() -> None:
    u = kida_pelz_initial(16)
    assert u.shape == (3, 16, 16, 16)
    assert np.isfinite(u).all()
    assert _projected_divergence(16, u) < 1.0e-12


def test_anti_parallel_vortex_tubes_initial_condition_is_projectable() -> None:
    u = anti_parallel_vortex_tubes_initial(16)
    assert u.shape == (3, 16, 16, 16)
    assert np.isfinite(u).all()
    assert _projected_divergence(16, u) < 1.0e-12


def test_self_similar_swirl_initial_condition_is_projectable() -> None:
    u = self_similar_swirl_initial(16, width=0.6)
    assert u.shape == (3, 16, 16, 16)
    assert np.isfinite(u).all()
    assert _projected_divergence(16, u) < 1.0e-12
