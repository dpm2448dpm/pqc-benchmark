# Measurement Methodology

## Benchmark Design

All benchmarks measure steady-state throughput: each algorithm is exercised repeatedly over a fixed time window, and the number of completed operations is divided by elapsed time to obtain **operations per second (ops/s)**. Latency in **ms/op** is derived as the arithmetic inverse.

### PQC algorithms (ML-KEM, ML-DSA)

- Implementation: [liboqs](https://github.com/open-quantum-safe/liboqs) via OpenSSL's `openssl speed` integration (post-3.x with OQS provider) and direct liboqs Python bindings.
- Operations measured: `keygen`, `encaps`, `decaps` (KEM); `keygen`, `sign`, `verify` (signatures).
- Each operation was repeated in **3 independent runs**, each consisting of the number of iterations OpenSSL speed determines for a 3-second window.
- Raw per-run results are stored as individual CSV files; aggregation is done at analysis time.

### Classical algorithms (RSA, ECDSA, EdDSA)

- Implementation: OpenSSL 3.x (`openssl speed`).
- Algorithms: RSA-2048/3072/4096, ECDSA P-256/384/521, Ed25519, Ed448.
- Operations measured: `sign`, `verify`, `encrypt`, `decrypt` (where applicable).
- Same 3-run repetition scheme.

### TLS handshake benchmarks

- Tool: custom Python/OpenSSL scripts performing full TLS 1.3 handshakes between a local server and client.
- 100 iterations per algorithm per platform.
- Measured metric: wall-clock handshake time in seconds.
- Algorithms include classical (ECDH, FFDHE), PQC (ML-KEM hybrids via OQS), and hybrid combinations.

## Timer and Precision

- High-resolution timer: `CLOCK_MONOTONIC` via OpenSSL's internal timer (`perf_counter_ns` for Python scripts).
- System idle at benchmark time; no other CPU-intensive processes running.
- CPU frequency scaling disabled on x86_64 platforms (performance governor).

## Hardware Detection

Platform metadata (CPU model, core count, clock speed, OS, kernel version) is logged at benchmark start to the `meta_*.txt` files stored alongside raw CSVs.

## Controlled Variables

| Variable | Control method |
|---|---|
| CPU frequency | Performance governor (x86_64) / fixed clock (RPi) |
| Memory | Results fit in L3 cache for all algorithms |
| Compiler | Distribution default (GCC 12+ / Clang 14+) |
| OpenSSL version | 3.x with OQS provider (same binary per platform) |
| OS | Fresh install, no background services |

## Statistical Analysis

For each (algorithm, operation, platform) triple:

- **Mean** and **standard deviation** computed across all repeats.
- **Relative standard deviation (RSD)** used to flag unstable measurements (>5% flagged).
- Bar charts display mean ± 1 std deviation.

Full aggregated statistics are available in [`results/processed/`](../results/processed/).
