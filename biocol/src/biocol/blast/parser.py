"""Columnas y lectura de BLAST tabular ``outfmt 6``."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

OUTFMT6_COLUMNS = [
    "qseqid",
    "sseqid",
    "pident",
    "length",
    "mismatch",
    "gapopen",
    "qstart",
    "qend",
    "sstart",
    "send",
    "evalue",
    "bitscore",
]


def parse_blast_results(path: str | Path) -> pd.DataFrame:
    """Lee un archivo BLAST tabular (outfmt 6) a DataFrame.

    Un archivo vacío (sin hits) devuelve un DataFrame sin filas, con las
    12 columnas estándar.
    """
    blast_path = Path(path)
    if not blast_path.exists():
        raise FileNotFoundError(f"BLAST file not found: {blast_path}")
    if blast_path.stat().st_size == 0:
        return pd.DataFrame(columns=OUTFMT6_COLUMNS)

    frame = pd.read_csv(
        blast_path,
        sep="\t",
        header=None,
        names=OUTFMT6_COLUMNS,
        comment="#",
    )
    return frame


def fill_missing_hits(
    results: pd.DataFrame,
    query_ids: list[str],
    database_name: str,
) -> pd.DataFrame:
    """Asegura una fila por query; si no hubo hit, los campos BLAST van vacíos."""
    frame = results.copy()
    if "database" not in frame.columns:
        frame["database"] = database_name
    present = set(frame["qseqid"].astype(str)) if not frame.empty else set()
    missing = [query_id for query_id in query_ids if query_id not in present]
    if not missing:
        return frame
    empty = pd.DataFrame(
        {
            "qseqid": missing,
            "database": database_name,
        }
    )
    for column in OUTFMT6_COLUMNS:
        if column != "qseqid" and column not in empty.columns:
            empty[column] = pd.NA
    return pd.concat([frame, empty], ignore_index=True)
