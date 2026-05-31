"""Tao 2014 averaged-NSE cascade proxy.

This is not a solver for the true Navier-Stokes equations and not Tao's full
averaged Euler bilinear operator. It reproduces the finite-time cascade mechanism
from the exogenously truncated dyadic model discussed around Tao 1402.0290,
Proposition 5.1, as a bounded Track B falsifier harness.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class TaoCascadeConfig:
    lambda_base: float = 2.0
    alpha: float = 0.4
    delta: float = 0.05
    n0: int = 40
    transfers: int = 24
    dtau: float = 0.002
    tau_max: float = 100.0
    blowup_weight_delta: float = 0.15


@dataclass(frozen=True)
class TaoCascadeRow:
    k: int
    mode_n: int
    epsilon: float
    tau_duration: float
    physical_dt: float
    physical_t: float
    source_end: float
    receiver_end: float
    receiver_target: float
    weighted_receiver: float
    reached_target: bool
    rk_steps: int


def _rk4_pair(x: float, y: float, dtau: float, epsilon: float, lambda_base: float, alpha: float) -> tuple[float, float]:
    damping_ratio = lambda_base ** (2.0 * alpha)

    def rhs(a: float, b: float) -> tuple[float, float]:
        return (-epsilon * a - a * b, -damping_ratio * epsilon * b + a * a)

    k1x, k1y = rhs(x, y)
    k2x, k2y = rhs(x + 0.5 * dtau * k1x, y + 0.5 * dtau * k1y)
    k3x, k3y = rhs(x + 0.5 * dtau * k2x, y + 0.5 * dtau * k2y)
    k4x, k4y = rhs(x + dtau * k3x, y + dtau * k3y)
    next_x = x + dtau * (k1x + 2.0 * k2x + 2.0 * k3x + k4x) / 6.0
    next_y = y + dtau * (k1y + 2.0 * k2y + 2.0 * k3y + k4y) / 6.0
    return max(next_x, 0.0), max(next_y, 0.0)


def simulate(config: TaoCascadeConfig) -> list[TaoCascadeRow]:
    if not (0.0 < config.alpha < 0.5):
        raise ValueError("Tao truncated cascade proxy expects supercritical alpha in (0, 1/2)")
    if not (0.0 < config.delta < 1.0 - 2.0 * config.alpha):
        raise ValueError("delta must satisfy 0 < delta < 1 - 2*alpha")
    if config.blowup_weight_delta <= config.delta:
        raise ValueError("blowup_weight_delta should be greater than delta to show the blow-up proxy")

    rows: list[TaoCascadeRow] = []
    physical_t = 0.0
    target_scaled = config.lambda_base ** (-config.delta)

    for k in range(config.transfers):
        mode_n = config.n0 + k
        epsilon = config.lambda_base ** ((2.0 * config.alpha - 1.0) * mode_n + config.delta * k)
        x = 1.0
        y = 0.0
        tau = 0.0
        steps = 0
        max_steps = int(math.ceil(config.tau_max / config.dtau))

        while y < target_scaled and steps < max_steps:
            x, y = _rk4_pair(x, y, config.dtau, epsilon, config.lambda_base, config.alpha)
            tau += config.dtau
            steps += 1
            if not math.isfinite(x) or not math.isfinite(y):
                raise FloatingPointError(f"non-finite cascade state at k={k}: x={x}, y={y}")

        source_end = (config.lambda_base ** (-config.delta * k)) * x
        receiver_end = (config.lambda_base ** (-config.delta * k)) * y
        receiver_target = config.lambda_base ** (-config.delta * (k + 1))
        physical_dt = (config.lambda_base ** (-mode_n + config.delta * k)) * tau
        physical_t += physical_dt
        weighted_receiver = (config.lambda_base ** (config.blowup_weight_delta * mode_n)) * receiver_end
        rows.append(
            TaoCascadeRow(
                k=k,
                mode_n=mode_n,
                epsilon=epsilon,
                tau_duration=tau,
                physical_dt=physical_dt,
                physical_t=physical_t,
                source_end=source_end,
                receiver_end=receiver_end,
                receiver_target=receiver_target,
                weighted_receiver=weighted_receiver,
                reached_target=bool(y >= target_scaled),
                rk_steps=steps,
            )
        )
        if y < target_scaled:
            break

    return rows


def write_csv(path: Path, rows: list[TaoCascadeRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(asdict(rows[0]).keys()) if rows else list(TaoCascadeRow.__dataclass_fields__.keys())
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def summarize(config: TaoCascadeConfig, rows: list[TaoCascadeRow], elapsed_seconds: float) -> dict[str, object]:
    if not rows:
        raise ValueError("no rows produced")
    weighted = np.asarray([row.weighted_receiver for row in rows], dtype=float)
    physical_t = np.asarray([row.physical_t for row in rows], dtype=float)
    physical_dt = np.asarray([row.physical_dt for row in rows], dtype=float)
    reached_all = all(row.reached_target for row in rows) and len(rows) == config.transfers
    return {
        "model": "exogenously_truncated_dyadic_cascade_proxy",
        "not_true_nse": True,
        "not_full_tao_averaged_operator": True,
        "lambda_base": config.lambda_base,
        "alpha": config.alpha,
        "delta": config.delta,
        "n0": config.n0,
        "transfers_requested": config.transfers,
        "transfers_completed": len(rows),
        "dtau": config.dtau,
        "tau_max": config.tau_max,
        "blowup_weight_delta": config.blowup_weight_delta,
        "reached_all_targets": reached_all,
        "physical_time_end": float(physical_t[-1]),
        "physical_dt_first": float(physical_dt[0]),
        "physical_dt_last": float(physical_dt[-1]),
        "physical_dt_ratio_last_first": float(physical_dt[-1] / physical_dt[0]),
        "weighted_receiver_start": float(weighted[0]),
        "weighted_receiver_end": float(weighted[-1]),
        "weighted_receiver_growth": float(weighted[-1] / weighted[0]),
        "max_rk_steps": int(max(row.rk_steps for row in rows)),
        "elapsed_seconds": elapsed_seconds,
    }


def write_plots(out_dir: Path, rows: list[TaoCascadeRow]) -> list[Path]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plots = out_dir / "plots"
    plots.mkdir(parents=True, exist_ok=True)
    k = np.asarray([row.k for row in rows], dtype=float)
    weighted = np.asarray([row.weighted_receiver for row in rows], dtype=float)
    physical_dt = np.asarray([row.physical_dt for row in rows], dtype=float)
    receiver = np.asarray([row.receiver_end for row in rows], dtype=float)
    target = np.asarray([row.receiver_target for row in rows], dtype=float)

    made: list[Path] = []

    plt.figure(figsize=(8, 5))
    plt.plot(k, weighted, marker="o")
    plt.yscale("log")
    plt.xlabel("cascade transfer k")
    plt.ylabel("lambda^(delta' n) |X_n|")
    plt.grid(True, alpha=0.25)
    plt.tight_layout()
    path = plots / "weighted_receiver.png"
    plt.savefig(path, dpi=160)
    plt.close()
    made.append(path)

    plt.figure(figsize=(8, 5))
    plt.plot(k, physical_dt, marker="o")
    plt.yscale("log")
    plt.xlabel("cascade transfer k")
    plt.ylabel("physical dt")
    plt.grid(True, alpha=0.25)
    plt.tight_layout()
    path = plots / "physical_dt.png"
    plt.savefig(path, dpi=160)
    plt.close()
    made.append(path)

    plt.figure(figsize=(8, 5))
    plt.plot(k, receiver, marker="o", label="receiver_end")
    plt.plot(k, target, linestyle="--", label="target")
    plt.yscale("log")
    plt.xlabel("cascade transfer k")
    plt.ylabel("mode amplitude")
    plt.legend()
    plt.grid(True, alpha=0.25)
    plt.tight_layout()
    path = plots / "receiver_target.png"
    plt.savefig(path, dpi=160)
    plt.close()
    made.append(path)

    return made


def write_readme(out_dir: Path, config: TaoCascadeConfig, summary: dict[str, object], plots: list[Path]) -> None:
    rel_plots = [path.relative_to(ROOT) for path in plots]
    lines = [
        "# Tao Averaged-NSE Cascade Proxy",
        "",
        "This run reproduces the exogenously truncated dyadic cascade mechanism used as",
        "a simple proxy for Tao 1402.0290. It is not a simulation of the true",
        "Navier-Stokes equations and not Tao's full averaged bilinear operator.",
        "",
        "## Config",
        "",
        f"- lambda: `{config.lambda_base}`",
        f"- alpha: `{config.alpha}`",
        f"- delta: `{config.delta}`",
        f"- n0: `{config.n0}`",
        f"- transfers: `{config.transfers}`",
        f"- blowup weight delta': `{config.blowup_weight_delta}`",
        "",
        "## Summary",
        "",
        f"- completed transfers: `{summary['transfers_completed']}` / `{summary['transfers_requested']}`",
        f"- reached all targets: `{summary['reached_all_targets']}`",
        f"- physical time end: `{summary['physical_time_end']:.10e}`",
        f"- first physical dt: `{summary['physical_dt_first']:.10e}`",
        f"- last physical dt: `{summary['physical_dt_last']:.10e}`",
        f"- weighted receiver growth: `{summary['weighted_receiver_growth']:.6g}`",
        "",
        "## Outputs",
        "",
        "- `config.json`",
        "- `timeseries.csv`",
        "- `summary.json`",
        *[f"- `{path}`" for path in rel_plots],
        "",
        "## Interpretation",
        "",
        "The decreasing physical time increments and increasing weighted high-mode",
        "amplitude reproduce the qualitative cascade/blow-up proxy. This is Track B",
        "barrier evidence for evaluator design only, not evidence for Clay NSE blow-up.",
        "",
    ]
    (out_dir / "README.md").write_text("\n".join(lines))


def run(config: TaoCascadeConfig, out_dir: Path) -> dict[str, object]:
    out_dir = out_dir.resolve()
    start = time.perf_counter()
    rows = simulate(config)
    elapsed = time.perf_counter() - start
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "config.json").write_text(json.dumps(asdict(config), indent=2, sort_keys=True) + "\n")
    write_csv(out_dir / "timeseries.csv", rows)
    summary = summarize(config, rows, elapsed)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    plots = write_plots(out_dir, rows)
    write_readme(out_dir, config, summary, plots)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lambda-base", type=float, default=2.0)
    parser.add_argument("--alpha", type=float, default=0.4)
    parser.add_argument("--delta", type=float, default=0.05)
    parser.add_argument("--n0", type=int, default=40)
    parser.add_argument("--transfers", type=int, default=24)
    parser.add_argument("--dtau", type=float, default=0.002)
    parser.add_argument("--tau-max", type=float, default=100.0)
    parser.add_argument("--blowup-weight-delta", type=float, default=0.15)
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "track-b-blowup/runs/tao_truncated_cascade",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = TaoCascadeConfig(
        lambda_base=args.lambda_base,
        alpha=args.alpha,
        delta=args.delta,
        n0=args.n0,
        transfers=args.transfers,
        dtau=args.dtau,
        tau_max=args.tau_max,
        blowup_weight_delta=args.blowup_weight_delta,
    )
    summary = run(config, args.out_dir)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
