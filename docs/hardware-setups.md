# Hardware Setups

Benchmarks were executed on three physically distinct machines representing different deployment environments: a high-performance x86_64 desktop, a low-power x86_64 embedded platform, and an ARM64 single-board computer.

## Platform Summary

| ID | Architecture | CPU | Cores | RAM | OS | Kernel |
|----|---|---|---|---|---|---|
| `ryzen` | x86_64 | AMD Ryzen 5 | 6C/12T | 16 GB | Ubuntu 24.04 LTS | 6.8 |
| `celeron` | x86_64 | Intel Celeron N4020 | 2C/2T | 4 GB | Ubuntu 22.04 LTS | 5.15 |
| `raspberry` | ARM64 | Broadcom BCM2712 (RPi 5) | 4C | 8 GB | Raspberry Pi OS (Debian 12) | 6.6 |

## Platform Details

### `ryzen` — AMD Ryzen 5 (x86_64)

Represents a **developer workstation / server node** environment. This is the highest-performance platform in the suite and is used as the reference baseline in cross-platform comparisons.

- AVX2 and AES-NI instructions available — benefits algorithms with optimised x86 implementations.
- CPU frequency governor set to `performance` during benchmarks.

### `celeron` — Intel Celeron N4020 (x86_64)

Represents a **low-power embedded or IoT** x86_64 device. The Celeron N4020 is a Gemini Lake Refresh SoC with significantly lower single-threaded performance than the Ryzen.

- SSE4.2 and AES-NI available; no AVX2.
- TDP: ~6 W — representative of edge gateway devices.
- CPU frequency governor set to `performance` during benchmarks.

### `raspberry` — Raspberry Pi 5 (ARM64)

Represents an **ARM64 embedded / IoT** deployment. The RPi 5 uses the Cortex-A76 core which has hardware AES and SHA extensions but no x86-specific SIMD.

- AES and SHA extensions available via ARMv8 Crypto Extensions.
- No AVX2 equivalent — lattice-based algorithms rely on generic C implementations from liboqs.
- Fixed CPU clock at 2.4 GHz during benchmarks (performance mode via `cpufreq-set`).

## Software Environment

| Component | Version |
|---|---|
| OpenSSL | 3.3.x |
| OQS Provider | 0.6.x |
| liboqs | 0.10.x |
| Python | 3.11 |
| GCC | 12+ (Ubuntu) / 12 (Debian) |

Full environment metadata is logged alongside raw results in `meta_*.txt` files under `results/raw/pqc/`.
