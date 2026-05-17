# Results

Pre-computed benchmark results from the thesis experiments. All data can be regenerated from the raw CSVs using:

```bash
python benchmarks/regenerate_all_figures.py
```

## Structure

```
results/
├── raw/                  # Per-run CSV measurements (source of truth)
│   ├── pqc/              # ML-KEM and ML-DSA results
│   │   ├── celeron/      # Intel Celeron N4020 (x86_64, low-power)
│   │   ├── ryzen/        # AMD Ryzen 5 (x86_64, high-performance)
│   │   └── raspberry/    # Raspberry Pi 5 (ARM64)
│   ├── classical/        # RSA, ECDSA, EdDSA results (same platform split)
│   └── tls/              # TLS handshake measurements
├── processed/            # Aggregated summary statistics (CSV)
└── figures/              # Pre-generated PNG figures
```

## CSV Format

**PQC results** (`results/raw/pqc/`):

| Column | Description |
|---|---|
| `algo` | Algorithm name (e.g., `ML-KEM-768`) |
| `repeat` | Run index (1–3) |
| `op` | Operation (`encaps`, `decaps`, `sign`, `verify`, `keygen`) |
| `ops_per_sec` | Throughput in operations per second |
| `bytes` | Key/ciphertext/signature sizes as `pk=N\|sk=N\|ct=N` |
| `notes` | Source tool identifier |

**Classical results** (`results/raw/classical/`): same columns; `bytes` field is `NA` (sizes are constant and documented in [`docs/algorithms.md`](../docs/algorithms.md)).

**TLS results** (`results/raw/tls/`):

| Column | Description |
|---|---|
| `Iteration` | Run index |
| `Algorithm` | TLS group/algorithm name |
| `Time(s)` | Wall-clock handshake duration in seconds |

## Figures Index

| File | Description |
|---|---|
| `pqc_vs_classical_level1_ops.png` | Throughput comparison at NIST Level 1 |
| `pqc_vs_classical_level3_ops.png` | Throughput comparison at NIST Level 3 |
| `pqc_vs_classical_level5_ops.png` | Throughput comparison at NIST Level 5 |
| `pqc_vs_classical_level3_latency.png` | Latency comparison at NIST Level 3 |
| `pqc_vs_classical_level3_key_sizes.png` | Public key size comparison at NIST Level 3 |
| `mlkem_ops_per_sec_ryzen.png` | ML-KEM throughput on AMD Ryzen |
| `mlkem_latency_ryzen.png` | ML-KEM latency on AMD Ryzen |
| `mlkem_key_sizes.png` | ML-KEM key and ciphertext sizes |
| `mldsa_ops_per_sec_ryzen.png` | ML-DSA throughput on AMD Ryzen |
| `mldsa_key_sizes.png` | ML-DSA key and signature sizes |
| `classical_sign_ryzen.png` | Classical signing throughput on AMD Ryzen |
| `classical_verify_ryzen.png` | Classical verification throughput on AMD Ryzen |
| `classical_all_ops_logscale_ryzen.png` | All classical operations (log scale) |
| `tls_handshake_ryzen.png` | TLS handshake latency — AMD Ryzen |
| `tls_handshake_celeron.png` | TLS handshake latency — Intel Celeron |
| `tls_handshake_raspberry.png` | TLS handshake latency — Raspberry Pi 5 |
