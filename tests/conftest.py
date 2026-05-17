"""Shared fixtures for the test suite."""

import pandas as pd
import pytest


@pytest.fixture
def sample_pqc_df() -> pd.DataFrame:
    """Minimal ML-KEM DataFrame mimicking the real CSV format after parsing."""
    return pd.DataFrame({
        "algo": ["ML-KEM-768", "ML-KEM-768", "ML-KEM-512", "ML-KEM-512"],
        "repeat": [1, 1, 1, 1],
        "op": ["encaps", "decaps", "encaps", "decaps"],
        "ops_per_sec": [92000.0, 76000.0, 120000.0, 100000.0],
        "pk": [1184, 1184, 800, 800],
        "sk": [2400, 2400, 1632, 1632],
        "ct": [1088, 1088, 768, 768],
        "ss": [32, 32, 32, 32],
        "sig": [pd.NA, pd.NA, pd.NA, pd.NA],
        "notes": ["speed_table"] * 4,
    })


@pytest.fixture
def sample_classical_df() -> pd.DataFrame:
    """Minimal classical benchmark DataFrame."""
    return pd.DataFrame({
        "algo": ["ecdsap256", "ecdsap256", "rsa2048", "rsa2048"],
        "repeat": [1, 1, 1, 1],
        "op": ["sign", "verify", "sign", "verify"],
        "ops_per_sec": [66700.0, 21900.0, 2270.0, 78860.0],
        "bytes": ["NA", "NA", "NA", "NA"],
        "notes": ["openssl_speed"] * 4,
    })


@pytest.fixture
def sample_tls_df() -> pd.DataFrame:
    """Minimal TLS benchmark DataFrame."""
    return pd.DataFrame({
        "iteration": [1, 2, 3, 1, 2, 3],
        "algorithm": ["X25519", "X25519", "X25519", "MLKEM768", "MLKEM768", "MLKEM768"],
        "time_s": [0.045, 0.047, 0.046, 0.052, 0.051, 0.053],
        "platform": ["ryzen"] * 6,
    })
