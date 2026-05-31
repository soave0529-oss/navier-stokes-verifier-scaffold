"""Initial conditions for bounded Track B scenario runs."""

from __future__ import annotations

import numpy as np


Array = np.ndarray


def grid(n: int) -> tuple[Array, Array, Array]:
    x1 = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
    return np.meshgrid(x1, x1, x1, indexing="ij")


def kida_pelz_initial(n: int, amplitude: float = 1.0) -> Array:
    """Kida-Pelz high-symmetry vortex initial condition on the periodic cube."""
    x, y, z = grid(n)
    u = np.zeros((3, n, n, n), dtype=float)
    u[0] = np.sin(x) * (np.cos(3.0 * y) * np.cos(z) - np.cos(y) * np.cos(3.0 * z))
    u[1] = np.sin(y) * (np.cos(3.0 * z) * np.cos(x) - np.cos(z) * np.cos(3.0 * x))
    u[2] = np.sin(z) * (np.cos(3.0 * x) * np.cos(y) - np.cos(x) * np.cos(3.0 * y))
    return amplitude * u


def _periodic_delta(coord: Array, center: float) -> Array:
    return np.angle(np.exp(1j * (coord - center)))


def anti_parallel_vortex_tubes_initial(
    n: int,
    amplitude: float = 1.0,
    radius: float = 0.35,
    separation: float = 0.9,
) -> Array:
    """Hou-Luo-inspired anti-parallel vortex tube velocity.

    The vorticity proxy is two opposite-sign z-vorticity tubes. We recover a
    divergence-free velocity by the periodic Fourier Biot-Savart relation.
    This is a diagnostic initial condition, not a faithful Hou-Luo geometry.
    """
    x, y, _z = grid(n)
    c1 = (np.pi - separation * 0.5, np.pi)
    c2 = (np.pi + separation * 0.5, np.pi)
    r1_sq = _periodic_delta(x, c1[0]) ** 2 + _periodic_delta(y, c1[1]) ** 2
    r2_sq = _periodic_delta(x, c2[0]) ** 2 + _periodic_delta(y, c2[1]) ** 2
    omega = np.zeros((3, n, n, n), dtype=float)
    omega[2] = amplitude * (np.exp(-r1_sq / radius**2) - np.exp(-r2_sq / radius**2))
    omega[2] -= float(np.mean(omega[2]))

    omega_hat = np.fft.fftn(omega, axes=(1, 2, 3))
    k1 = np.fft.fftfreq(n, d=1.0 / n)
    kx, ky, kz = np.meshgrid(k1, k1, k1, indexing="ij")
    k2 = kx**2 + ky**2 + kz**2
    cross = np.stack(
        [
            ky * omega_hat[2] - kz * omega_hat[1],
            kz * omega_hat[0] - kx * omega_hat[2],
            kx * omega_hat[1] - ky * omega_hat[0],
        ]
    )
    u_hat = np.zeros_like(omega_hat)
    nonzero = k2 > 0
    u_hat[:, nonzero] = 1j * cross[:, nonzero] / k2[nonzero]
    u_hat[:, 0, 0, 0] = 0.0
    return np.fft.ifftn(u_hat, axes=(1, 2, 3)).real


def self_similar_swirl_initial(
    n: int,
    amplitude: float = 1.0,
    width: float = 0.55,
    axial_stretch: float = 1.0,
    center: tuple[float, float, float] = (np.pi, np.pi, np.pi),
) -> Array:
    """Localized swirl profile for cheap self-similar diagnostics.

    The profile is generated from a Gaussian streamfunction
    `A = (0, 0, psi)`, so `u = curl A = (d_y psi, -d_x psi, 0)` is a
    compact, divergence-free swirl up to the periodic-grid projection used by
    the solver. Width/amplitude sweeps mimic concentration diagnostics only;
    this is not an exact self-similar NSE ansatz.
    """
    if width <= 0.0:
        raise ValueError("width must be positive")
    if axial_stretch <= 0.0:
        raise ValueError("axial_stretch must be positive")

    x, y, z = grid(n)
    dx = _periodic_delta(x, center[0])
    dy = _periodic_delta(y, center[1])
    dz = _periodic_delta(z, center[2])
    radius_sq = dx**2 + dy**2 + axial_stretch * dz**2
    psi = np.exp(-radius_sq / width**2)

    u = np.zeros((3, n, n, n), dtype=float)
    u[0] = amplitude * (-2.0 * dy / width**2) * psi
    u[1] = amplitude * (2.0 * dx / width**2) * psi
    u[2] = 0.0
    u -= np.mean(u, axis=(1, 2, 3), keepdims=True)
    return u
