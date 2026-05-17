"""Tests for the pqc_benchmark.reporting modules."""

import pandas as pd
import pytest

from pqc_benchmark.reporting.plots_pqc import parse_bytes_field, load_pqc_folder
from pqc_benchmark.reporting.plots_classical import compute_stats
from pqc_benchmark.reporting.plots_tls import compute_tls_stats
from pqc_benchmark.reporting.plots_comparison import NIST_LEVELS, _algo_level_map


class TestParseBytesField:
    def test_kem_format(self):
        result = parse_bytes_field("pk=1184|sk=2400|ct=1088|ss=32")
        assert result["pk"] == 1184
        assert result["sk"] == 2400
        assert result["ct"] == 1088
        assert result["ss"] == 32

    def test_sig_format(self):
        result = parse_bytes_field("pk=1952|sk=4000|sig=3309")
        assert result["pk"] == 1952
        assert result["sig"] == 3309

    def test_na_value(self):
        result = parse_bytes_field("NA")
        assert len(result) == 0

    def test_empty_string(self):
        result = parse_bytes_field("")
        assert len(result) == 0


class TestLoadPqcFolder:
    def test_raises_on_missing_folder(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_pqc_folder(tmp_path / "nonexistent")

    def test_raises_on_empty_folder(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_pqc_folder(tmp_path)

    def test_loads_real_data(self):
        real_folder = "results/raw/pqc/ryzen"
        try:
            df = load_pqc_folder(real_folder)
            assert not df.empty
            assert "algo" in df.columns
            assert "ops_per_sec" in df.columns
            assert "ms_per_op" in df.columns
        except FileNotFoundError:
            pytest.skip("Real data not available in this environment")


class TestComputeStats:
    def test_output_columns(self, sample_classical_df):
        stats = compute_stats(sample_classical_df)
        assert "mean_ops" in stats.columns
        assert "std_ops" in stats.columns
        assert "algo" in stats.columns
        assert "op" in stats.columns

    def test_aggregation(self, sample_classical_df):
        stats = compute_stats(sample_classical_df)
        ecdsa_sign = stats[(stats["algo"] == "ecdsap256") & (stats["op"] == "sign")]
        assert len(ecdsa_sign) == 1
        assert ecdsa_sign["mean_ops"].iloc[0] == pytest.approx(66700.0)


class TestComputeTlsStats:
    def test_output_columns(self, sample_tls_df):
        stats = compute_tls_stats(sample_tls_df)
        for col in ["platform", "algorithm", "mean", "std", "median"]:
            assert col in stats.columns

    def test_mean_value(self, sample_tls_df):
        stats = compute_tls_stats(sample_tls_df)
        x25519 = stats[(stats["algorithm"] == "X25519") & (stats["platform"] == "ryzen")]
        assert x25519["mean"].iloc[0] == pytest.approx(0.046, rel=0.01)


class TestNistLevels:
    def test_all_levels_present(self):
        assert set(NIST_LEVELS.keys()) == {1, 3, 5}

    def test_ml_kem_in_levels(self):
        assert "ML-KEM-512" in NIST_LEVELS[1]["pqc"]
        assert "ML-KEM-768" in NIST_LEVELS[3]["pqc"]
        assert "ML-KEM-1024" in NIST_LEVELS[5]["pqc"]

    def test_algo_level_map_complete(self):
        mapping = _algo_level_map()
        assert mapping["ML-KEM-768"] == 3
        assert mapping["ecdsap256"] == 1
        assert mapping["rsa4096"] == 5
