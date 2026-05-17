"""Cross-algorithm comparison figures grouped by NIST security level."""

from __future__ import annotations

import glob
import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")
sns.set_context("paper", font_scale=1.5)

# NIST security level groupings
NIST_LEVELS: dict[int, dict[str, list[str]]] = {
    1: {
        "pqc":      ["ML-KEM-512", "ML-DSA-44"],
        "classical": ["ecdsap256", "ed25519", "rsa2048"],
    },
    3: {
        "pqc":      ["ML-KEM-768", "ML-DSA-65"],
        "classical": ["ecdsap384", "ed448", "rsa3072"],
    },
    5: {
        "pqc":      ["ML-KEM-1024", "ML-DSA-87"],
        "classical": ["ecdsap521", "rsa4096"],
    },
}

# Classical key/signature sizes (bytes) — not present in OpenSSL speed CSV output
CLASSICAL_SIZES: dict[str, dict[str, int]] = {
    "ecdsap256": {"pk": 64,  "sk": 32,  "sig": 64},
    "ecdsap384": {"pk": 96,  "sk": 48,  "sig": 96},
    "ecdsap521": {"pk": 132, "sk": 66,  "sig": 132},
    "ed25519":   {"pk": 32,  "sk": 32,  "sig": 64},
    "ed448":     {"pk": 57,  "sk": 57,  "sig": 114},
    "rsa2048":   {"pk": 294, "sk": 1190, "sig": 256},
    "rsa3072":   {"pk": 422, "sk": 1700, "sig": 384},
    "rsa4096":   {"pk": 550, "sk": 2400, "sig": 512},
}


def _parse_bytes(value: str) -> pd.Series:
    out: dict[str, float] = {}
    if pd.isna(value):
        return pd.Series(out)
    for part in str(value).split("|"):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = pd.to_numeric(v, errors="coerce")
    return pd.Series(out)


def load_classical(folder: str | Path, platform: str) -> pd.DataFrame:
    """Load classical CSV results from *folder* and tag with *platform*."""
    files = glob.glob(os.path.join(str(folder), "*.csv"))
    if not files:
        return pd.DataFrame()

    frames = []
    for f in files:
        df = pd.read_csv(f)
        df = df[df["algo"] != "algo"]
        df["family"] = "classical"
        df["platform"] = platform
        if "ops_per_sec" in df.columns:
            df["ops_per_sec"] = pd.to_numeric(df["ops_per_sec"], errors="coerce")
            df["ms_per_op"] = 1000.0 / df["ops_per_sec"]
        frames.append(df)

    return pd.concat(frames, ignore_index=True)


def load_pqc(folder: str | Path, platform: str) -> pd.DataFrame:
    """Load PQC CSV results from *folder* and tag with *platform*."""
    files = glob.glob(os.path.join(str(folder), "*.csv"))
    if not files:
        return pd.DataFrame()

    frames = []
    for f in files:
        df = pd.read_csv(f)
        if "bytes" in df.columns:
            sizes = df["bytes"].apply(_parse_bytes)
            df = pd.concat([df, sizes], axis=1)
        df["family"] = "pqc"
        df["platform"] = platform
        if "ops_per_sec" in df.columns:
            df["ms_per_op"] = 1000.0 / pd.to_numeric(df["ops_per_sec"], errors="coerce")
        frames.append(df)

    return pd.concat(frames, ignore_index=True)


def _algo_level_map() -> dict[str, int]:
    mapping = {}
    for level, groups in NIST_LEVELS.items():
        for algo in groups["pqc"] + groups["classical"]:
            mapping[algo] = level
    return mapping


def _barplot(df: pd.DataFrame, metric: str, title: str, outfile: str | Path) -> None:
    plt.figure(figsize=(16, 9))
    sns.barplot(data=df, x="algo", y=metric, hue="platform", errorbar=None)
    plt.xticks(rotation=25, ha="right")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outfile, dpi=300)
    plt.close()


def generate_figures(
    platform_dirs: dict[str, tuple[str | Path, str | Path]],
    output_dir: str | Path,
) -> None:
    """Generate PQC-vs-classical comparison figures grouped by NIST security level.

    Args:
        platform_dirs: mapping of ``{platform: (classical_folder, pqc_folder)}``.
        output_dir: root destination; sub-folders ``level_1/``, ``level_3/``, ``level_5/``
            are created automatically.
    """
    output_dir = Path(output_dir)
    all_frames = []

    for platform, (classic_dir, pqc_dir) in platform_dirs.items():
        df_classic = load_classical(classic_dir, platform)
        df_pqc = load_pqc(pqc_dir, platform)
        all_frames.extend([df_classic, df_pqc])

    df = pd.concat(all_frames, ignore_index=True)
    level_map = _algo_level_map()
    df["nist_level"] = df["algo"].map(level_map)

    for level in [1, 3, 5]:
        level_dir = output_dir / f"level_{level}"
        os.makedirs(level_dir, exist_ok=True)
        algos = NIST_LEVELS[level]["pqc"] + NIST_LEVELS[level]["classical"]
        df_n = df[df["algo"].isin(algos)].copy()

        if "ops_per_sec" in df_n.columns:
            _barplot(df_n, "ops_per_sec",
                     f"NIST Level {level} — Throughput (ops/s)",
                     level_dir / "ops_per_sec.png")

        if "ms_per_op" in df_n.columns:
            _barplot(df_n, "ms_per_op",
                     f"NIST Level {level} — Latency (ms/op)",
                     level_dir / "ms_per_op.png")

        size_cols = [c for c in ["pk", "sk", "sig", "ct", "ss"] if c in df_n.columns]
        if size_cols:
            df_sizes = df_n[size_cols + ["algo", "platform"]].dropna(how="all")
            if not df_sizes.empty:
                df_agg = df_sizes.groupby(["algo", "platform"]).max().reset_index()
                _barplot(df_agg, "pk",
                         f"NIST Level {level} — Public key size (bytes)",
                         level_dir / "pk_sizes.png")
