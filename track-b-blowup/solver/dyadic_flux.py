"""Dyadic LES-style energy-flux diagnostics for pseudo-spectral fields.

This module is diagnostic-only. It does not provide a proof ingredient for
Navier-Stokes regularity.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from pseudospectral import Array, PseudoSpectralNSE


@dataclass(frozen=True)
class DyadicFluxRow:
    step: int
    t: float
    cutoff: int
    pi_les: float
    positive_flux: float
    normalized_positive_flux: float


def low_pass_mask(solver: PseudoSpectralNSE, cutoff: int) -> Array:
    """Return the radial Fourier mask `|k| <= cutoff`."""
    if cutoff <= 0:
        raise ValueError("cutoff must be positive")
    return np.sqrt(solver.k2) <= float(cutoff)


def low_pass_velocity(solver: PseudoSpectralNSE, u_hat: Array, cutoff: int) -> Array:
    mask = low_pass_mask(solver, cutoff)
    out = np.zeros_like(u_hat)
    out[:, mask] = u_hat[:, mask]
    return out


def low_pass_scalar(solver: PseudoSpectralNSE, scalar: Array, cutoff: int) -> Array:
    mask = low_pass_mask(solver, cutoff)
    scalar_hat = np.fft.fftn(scalar, axes=(0, 1, 2))
    filtered = np.zeros_like(scalar_hat)
    filtered[mask] = scalar_hat[mask]
    return np.fft.ifftn(filtered, axes=(0, 1, 2)).real


def gradient_tensor(solver: PseudoSpectralNSE, u_hat: Array) -> Array:
    """Return `grad[i,j] = partial_j u_i` in physical space."""
    grad = np.empty((3, 3, solver.n, solver.n, solver.n), dtype=float)
    for comp in range(3):
        for direction in range(3):
            grad[comp, direction] = solver.ifft((1j * solver.k[direction] * u_hat[comp])[None, ...])[0]
    return grad


def les_stress(solver: PseudoSpectralNSE, u_hat: Array, cutoff: int) -> Array:
    """Return `P_{<=N}(u_i u_j) - u_{<=N,i} u_{<=N,j}` in physical space."""
    u = solver.ifft(u_hat)
    u_low_hat = low_pass_velocity(solver, u_hat, cutoff)
    u_low = solver.ifft(u_low_hat)
    tau = np.empty((3, 3, solver.n, solver.n, solver.n), dtype=float)
    for i in range(3):
        for j in range(3):
            tau[i, j] = low_pass_scalar(solver, u[i] * u[j], cutoff) - u_low[i] * u_low[j]
    return tau


def pi_les_mean(solver: PseudoSpectralNSE, u_hat: Array, cutoff: int) -> float:
    """Mean-normalized LES flux `grad u_{<=N} : tau_N(u,u)`.

    The project candidate statement uses an integral over `T^3`; the solver diagnostics use
    spatial means, so this returns the corresponding mean-normalized quantity.
    """
    u_low_hat = low_pass_velocity(solver, u_hat, cutoff)
    grad_low = gradient_tensor(solver, u_low_hat)
    tau = les_stress(solver, u_hat, cutoff)
    return float(np.mean(np.sum(grad_low * tau, axis=(0, 1))))


def flux_row(solver: PseudoSpectralNSE, step: int, t: float, u_hat: Array, cutoff: int, alpha: float) -> DyadicFluxRow:
    pi = pi_les_mean(solver, solver.project(u_hat), cutoff)
    positive = max(pi, 0.0)
    normalized = (float(cutoff) ** (-alpha)) * positive
    return DyadicFluxRow(
        step=step,
        t=t,
        cutoff=cutoff,
        pi_les=pi,
        positive_flux=positive,
        normalized_positive_flux=normalized,
    )
