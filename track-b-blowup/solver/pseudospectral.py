"""Pseudo-spectral solver for incompressible 3D Navier-Stokes on [0, 2pi)^3.

This module is a falsification/diagnostic tool, not proof infrastructure.
It evolves divergence-free velocity fields with a 2/3-dealiased Fourier
method, Leray projection, and RK4 time stepping.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np


Array = np.ndarray


@dataclass(frozen=True)
class SolverConfig:
    n: int = 32
    nu: float = 1.0e-3
    dt: float = 2.5e-3
    t_end: float = 0.1
    dealias: bool = True
    integrator: str = "rk4"


@dataclass(frozen=True)
class DiagnosticRow:
    step: int
    t: float
    energy: float
    enstrophy: float
    omega_inf: float
    div_max: float
    spectrum_tail: float


class PseudoSpectralNSE:
    """3D incompressible NSE solver on a periodic cube of side length 2pi."""

    def __init__(self, config: SolverConfig):
        if config.n % 2 != 0:
            raise ValueError("n must be even for the 2/3 dealiasing mask")
        if config.integrator not in {"rk4", "ifrk4"}:
            raise ValueError(f"unsupported integrator: {config.integrator}")
        self.config = config
        self.n = config.n
        self.nu = config.nu
        self.dt = config.dt
        self._linear_factor_cache: dict[float, Array] = {}
        self._build_grid()

    def _build_grid(self) -> None:
        n = self.n
        x1 = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
        self.x, self.y, self.z = np.meshgrid(x1, x1, x1, indexing="ij")

        k1 = np.fft.fftfreq(n, d=1.0 / n)
        self.kx, self.ky, self.kz = np.meshgrid(k1, k1, k1, indexing="ij")
        self.k = np.stack([self.kx, self.ky, self.kz])
        self.k2 = self.kx**2 + self.ky**2 + self.kz**2
        self.nonzero = self.k2 > 0

        cutoff = n // 3
        self.dealias_mask = (
            (np.abs(self.kx) <= cutoff)
            & (np.abs(self.ky) <= cutoff)
            & (np.abs(self.kz) <= cutoff)
        )

    def fft(self, u: Array) -> Array:
        return np.fft.fftn(u, axes=(1, 2, 3))

    def ifft(self, u_hat: Array) -> Array:
        return np.fft.ifftn(u_hat, axes=(1, 2, 3)).real

    def apply_dealias(self, u_hat: Array) -> Array:
        if not self.config.dealias:
            return u_hat
        out = u_hat.copy()
        out[:, ~self.dealias_mask] = 0.0
        return out

    def project(self, u_hat: Array) -> Array:
        """Apply the Fourier Leray projection to make k dot u_hat = 0."""
        out = u_hat.copy()
        k_dot_u = np.sum(self.k * out, axis=0)
        for i in range(3):
            correction = np.zeros_like(k_dot_u)
            correction[self.nonzero] = (
                self.k[i][self.nonzero] * k_dot_u[self.nonzero] / self.k2[self.nonzero]
            )
            out[i] -= correction
        out[:, 0, 0, 0] = 0.0
        return self.apply_dealias(out)

    def gradient(self, scalar_hat: Array) -> Array:
        return np.stack([self.ifft(1j * self.k[i] * scalar_hat[None, ...])[0] for i in range(3)])

    def curl_hat(self, u_hat: Array) -> Array:
        ux, uy, uz = u_hat
        return np.stack(
            [
                1j * (self.ky * uz - self.kz * uy),
                1j * (self.kz * ux - self.kx * uz),
                1j * (self.kx * uy - self.ky * ux),
            ]
        )

    def nonlinear_rhs(self, u_hat: Array) -> Array:
        u_hat = self.project(u_hat)
        u = self.ifft(u_hat)

        grad_u = np.empty((3, 3, self.n, self.n, self.n), dtype=float)
        for comp in range(3):
            for direction in range(3):
                grad_u[comp, direction] = self.ifft((1j * self.k[direction] * u_hat[comp])[None, ...])[0]

        nonlinear = np.zeros_like(u)
        for comp in range(3):
            nonlinear[comp] = (
                u[0] * grad_u[comp, 0]
                + u[1] * grad_u[comp, 1]
                + u[2] * grad_u[comp, 2]
            )

        nonlinear_hat = self.apply_dealias(self.fft(nonlinear))
        projected_nonlinear = self.project(nonlinear_hat)
        return -projected_nonlinear

    def rhs(self, u_hat: Array) -> Array:
        u_hat = self.project(u_hat)
        projected_nonlinear = -self.nonlinear_rhs(u_hat)
        diffusion = -self.nu * self.k2[None, ...] * u_hat
        return -projected_nonlinear + diffusion

    def step_rk4(self, u_hat: Array) -> Array:
        dt = self.dt
        k1 = self.rhs(u_hat)
        k2 = self.rhs(u_hat + 0.5 * dt * k1)
        k3 = self.rhs(u_hat + 0.5 * dt * k2)
        k4 = self.rhs(u_hat + dt * k3)
        return self.project(u_hat + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4))

    def linear_evolve(self, u_hat: Array, fraction: float) -> Array:
        factor = self._linear_factor_cache.get(fraction)
        if factor is None:
            factor = np.exp(-self.nu * self.k2 * self.dt * fraction)
            self._linear_factor_cache[fraction] = factor
        return u_hat * factor[None, ...]

    def step_ifrk4(self, u_hat: Array) -> Array:
        """Integrating-factor RK4 with exact linear diffusion substeps."""
        dt = self.dt

        k1 = self.nonlinear_rhs(u_hat)
        stage2 = self.linear_evolve(u_hat + 0.5 * dt * k1, 0.5)
        k2 = self.linear_evolve(self.nonlinear_rhs(stage2), -0.5)
        stage3 = self.linear_evolve(u_hat + 0.5 * dt * k2, 0.5)
        k3 = self.linear_evolve(self.nonlinear_rhs(stage3), -0.5)
        stage4 = self.linear_evolve(u_hat + dt * k3, 1.0)
        k4 = self.linear_evolve(self.nonlinear_rhs(stage4), -1.0)

        w_next = u_hat + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        return self.project(self.linear_evolve(w_next, 1.0))

    def step(self, u_hat: Array) -> Array:
        if self.config.integrator == "rk4":
            return self.step_rk4(u_hat)
        if self.config.integrator == "ifrk4":
            return self.step_ifrk4(u_hat)
        raise AssertionError(f"unreachable integrator: {self.config.integrator}")

    def diagnostics(self, step: int, t: float, u_hat: Array) -> DiagnosticRow:
        u_hat = self.project(u_hat)
        u = self.ifft(u_hat)
        omega = self.ifft(self.curl_hat(u_hat))
        div = self.ifft((1j * np.sum(self.k * u_hat, axis=0))[None, ...])[0]

        energy = 0.5 * float(np.mean(np.sum(u * u, axis=0)))
        enstrophy = 0.5 * float(np.mean(np.sum(omega * omega, axis=0)))
        omega_inf = float(np.max(np.sqrt(np.sum(omega * omega, axis=0))))
        div_max = float(np.max(np.abs(div)))
        spectrum_tail = self.spectrum_tail(u_hat)
        return DiagnosticRow(step, t, energy, enstrophy, omega_inf, div_max, spectrum_tail)

    def spectrum_tail(self, u_hat: Array) -> float:
        radius = np.sqrt(self.k2)
        high = radius >= (self.n / 3) * 0.8
        total = float(np.sum(np.abs(u_hat) ** 2))
        if total == 0.0:
            return 0.0
        return float(np.sum(np.abs(u_hat[:, high]) ** 2) / total)

    def run(self, u0: Array, sample_every: int = 1) -> tuple[Array, list[DiagnosticRow]]:
        u_hat = self.project(self.fft(u0))
        rows: list[DiagnosticRow] = []
        steps = int(round(self.config.t_end / self.dt))
        for step in range(steps + 1):
            t = step * self.dt
            if step % sample_every == 0 or step == steps:
                rows.append(self.diagnostics(step, t, u_hat))
            if step < steps:
                u_hat = self.step(u_hat)
        return u_hat, rows


def taylor_green_initial(n: int, amplitude: float = 1.0) -> Array:
    x1 = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
    x, y, z = np.meshgrid(x1, x1, x1, indexing="ij")
    u = np.zeros((3, n, n, n), dtype=float)
    u[0] = amplitude * np.sin(x) * np.cos(y) * np.cos(z)
    u[1] = -amplitude * np.cos(x) * np.sin(y) * np.cos(z)
    u[2] = 0.0
    return u


def write_csv(path: Path, rows: Iterable[DiagnosticRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "step",
                "t",
                "energy",
                "enstrophy",
                "omega_inf",
                "div_max",
                "spectrum_tail",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=32)
    parser.add_argument("--nu", type=float, default=1.0e-3)
    parser.add_argument("--dt", type=float, default=2.5e-3)
    parser.add_argument("--t-end", type=float, default=0.1)
    parser.add_argument("--sample-every", type=int, default=10)
    parser.add_argument("--integrator", choices=["rk4", "ifrk4"], default="rk4")
    parser.add_argument("--out", type=Path, default=Path("track-b-blowup/runs/taylor_green_smoke/timeseries.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = SolverConfig(n=args.n, nu=args.nu, dt=args.dt, t_end=args.t_end, integrator=args.integrator)
    solver = PseudoSpectralNSE(cfg)
    u0 = taylor_green_initial(args.n)
    _, rows = solver.run(u0, sample_every=args.sample_every)
    write_csv(args.out, rows)
    last = rows[-1]
    print(
        "Taylor-Green run complete: "
        f"n={args.n} integrator={args.integrator} t={last.t:.6g} E={last.energy:.8g} "
        f"Omega={last.enstrophy:.8g} div_max={last.div_max:.3e}"
    )


if __name__ == "__main__":
    main()
