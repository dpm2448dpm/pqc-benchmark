# Algorithms Covered

## Post-Quantum Algorithms (NIST Standards)

### ML-KEM — Module-Lattice Key Encapsulation Mechanism (FIPS 203)

Standardized by NIST in August 2024. Based on the CRYSTALS-Kyber submission; uses Module Learning With Errors (MLWE) hardness assumption.

| Variant | NIST Level | Public Key | Secret Key | Ciphertext |
|---|---|---|---|---|
| ML-KEM-512 | 1 (≈AES-128) | 800 B | 1,632 B | 768 B |
| ML-KEM-768 | 3 (≈AES-192) | 1,184 B | 2,400 B | 1,088 B |
| ML-KEM-1024 | 5 (≈AES-256) | 1,568 B | 3,168 B | 1,568 B |

Operations benchmarked: `keygen`, `encaps`, `decaps`.

### ML-DSA — Module-Lattice Digital Signature Algorithm (FIPS 204)

Standardized by NIST in August 2024. Based on CRYSTALS-Dilithium; uses MLWE and Module Short Integer Solution (MSIS).

| Variant | NIST Level | Public Key | Secret Key | Signature |
|---|---|---|---|---|
| ML-DSA-44 | 2 (≈AES-128) | 1,312 B | 2,528 B | 2,420 B |
| ML-DSA-65 | 3 (≈AES-192) | 1,952 B | 4,000 B | 3,309 B |
| ML-DSA-87 | 5 (≈AES-256) | 2,592 B | 4,864 B | 4,627 B |

Operations benchmarked: `keygen`, `sign`, `verify`.

---

## Classical Algorithms (Baselines)

### RSA

| Variant | Key Size | Public Key | Signature |
|---|---|---|---|
| RSA-2048 | 2048 bits | 294 B | 256 B |
| RSA-3072 | 3072 bits | 422 B | 384 B |
| RSA-4096 | 4096 bits | 550 B | 512 B |

Operations benchmarked: `sign`, `verify`, `encrypt`, `decrypt`.

### ECDSA

| Variant | Curve | Public Key | Signature |
|---|---|---|---|
| ECDSA P-256 | NIST P-256 | 64 B | 64 B |
| ECDSA P-384 | NIST P-384 | 96 B | 96 B |
| ECDSA P-521 | NIST P-521 | 132 B | 132 B |

Operations benchmarked: `sign`, `verify`.

### EdDSA

| Variant | Curve | Public Key | Signature |
|---|---|---|---|
| Ed25519 | Curve25519 | 32 B | 64 B |
| Ed448 | Curve448 | 57 B | 114 B |

Operations benchmarked: `sign`, `verify`.

---

## NIST Security Level Mapping

| Level | Classical equivalent | PQC algorithms | Classical baselines |
|---|---|---|---|
| 1 | AES-128 | ML-KEM-512, ML-DSA-44 | ECDSA P-256, Ed25519, RSA-2048 |
| 3 | AES-192 | ML-KEM-768, ML-DSA-65 | ECDSA P-384, Ed448, RSA-3072 |
| 5 | AES-256 | ML-KEM-1024, ML-DSA-87 | ECDSA P-521, RSA-4096 |

---

## TLS Handshake Algorithms

The TLS benchmark suite covers 25 algorithm configurations per platform, including:

- Classical: ECDH (P-256, P-384, P-521), X25519, FFDHE groups.
- Pure PQC: BIKE Level 1/3/5, ML-KEM hybrids.
- Hybrid: X25519+ML-KEM-768, P-256+ML-KEM-512, Brainpool+ML-KEM variants.

Hybrids combine a classical ECDH key exchange with a PQC KEM for dual protection — required during the migration period by most security frameworks.
