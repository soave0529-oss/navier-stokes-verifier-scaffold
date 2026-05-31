# Step 15 Interval Falsifier Results

All values are wrapped in narrow intervals before comparison. `unknown` means
interval overlap, not mathematical truth.

| id | relation | status | lhs interval | rhs interval | description |
|---|---|---|---|---|---|
| `ineq_0001_tg_divergence_small` | `<=` | `pass` | `(4.1698409662588214e-16, 4.1898409662588217e-16)` | `(9.999999900000001e-11, 1.00000001e-10)` | Taylor-Green diagnostic divergence stays below 1e-10. |
| `ineq_0002_bad_tg_tail_le_005` | `<=` | `fail` | `(0.19670154804864506, 0.19670154804903847)` | `(0.04999999999995, 0.050000000000050004)` | False control: Taylor-Green spectrum tail remains <= 0.05. |
| `ineq_0003_tao_proxy_weighted_growth` | `>` | `pass` | `(4.924455658811889, 4.924455658821737)` | `(0.999999999999, 1.000000000001)` | Tao cascade proxy weighted high-mode amplitude grows by more than 1. |
| `ineq_0004_bad_kida_enstrophy_nonincreasing` | `<=` | `fail` | `(4.287139658357426, 4.287139658366001)` | `(4.124999999995875, 4.125000000004125)` | False control: Kida scenario enstrophy is nonincreasing over the cheap run. |
| `ineq_0005_houluo_energy_nonincreasing` | `<=` | `pass` | `(0.0005103257171428703, 0.000510325717143891)` | `(0.0005121844578204077, 0.0005121844578214321)` | Hou-Luo-inspired scenario energy is nonincreasing over the cheap run. |
