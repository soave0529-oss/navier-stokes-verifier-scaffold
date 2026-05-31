from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "track-b-blowup" / "solver"))

from pseudospectral import PseudoSpectralNSE, SolverConfig, taylor_green_initial


def test_taylor_green_initial_is_divergence_free() -> None:
    solver = PseudoSpectralNSE(SolverConfig(n=16, t_end=0.0))
    u_hat = solver.project(solver.fft(taylor_green_initial(16)))
    row = solver.diagnostics(0, 0.0, u_hat)
    assert row.div_max < 1e-12


def test_short_taylor_green_run_preserves_projection_and_decays_energy() -> None:
    solver = PseudoSpectralNSE(SolverConfig(n=16, nu=1.0e-2, dt=1.0e-3, t_end=1.0e-2))
    _, rows = solver.run(taylor_green_initial(16), sample_every=1)
    assert max(row.div_max for row in rows) < 1e-10
    assert rows[-1].energy <= rows[0].energy
    assert np.isfinite(rows[-1].enstrophy)


def test_ifrk4_short_taylor_green_run_preserves_projection_and_decays_energy() -> None:
    solver = PseudoSpectralNSE(SolverConfig(n=16, nu=1.0e-2, dt=1.0e-3, t_end=1.0e-2, integrator="ifrk4"))
    _, rows = solver.run(taylor_green_initial(16), sample_every=1)
    assert max(row.div_max for row in rows) < 1e-10
    assert rows[-1].energy <= rows[0].energy
    assert np.isfinite(rows[-1].enstrophy)
