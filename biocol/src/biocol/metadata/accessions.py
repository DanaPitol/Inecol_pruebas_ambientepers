from __future__ import annotations

import logging
import re
from pathlib import Path

import pandas as pd

from biocol.exceptions import MetadataError

logger = logging.getLogger(__name__)

_DB_PREFIXES = {
    "ref",
    "gb",
    "emb",
    "dbj",
    "sp",
    "pdb",
    "tpg",
    "tpe",
    "tpd",
    "lcl",
    "gi",
}


def normalize_accession(value: object) -> str:
    """Quita prefijos tipo ``ref|XP_123.1|`` y deja el accession."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    text = str(value).strip()
    if not text:
        return ""
    if "|" not in text:
        return text.split()[0]
    tokens = [token for token in text.split("|") if token]
    for token in reversed(tokens):
        lowered = token.lower()
        if lowered in _DB_PREFIXES:
            continue
        if re.fullmatch(r"\d+", token):
            continue
        return token.split()[0]
    return tokens[-1]


def load_accessions(path: str | Path) -> pd.DataFrame:
    """Lee ``accession<TAB>descriptor`` (sin encabezado)."""
    acc_path = Path(path)
    if not acc_path.exists():
        raise FileNotFoundError(f"No existe el archivo de accesiones: {acc_path}")
    try:
        frame = pd.read_csv(
            acc_path,
            sep="\t",
            header=None,
            names=["accession", "description"],
            dtype=str,
            comment="#",
        )
    except Exception as exc:
        raise MetadataError(f"No se pudo leer accesiones: {acc_path}") from exc

    frame = frame.dropna(how="all")
    if frame.empty:
        raise MetadataError(f"El archivo de accesiones no tiene filas: {acc_path}")
    if frame["accession"].isna().any() or (frame["accession"].str.strip() == "").any():
        raise MetadataError("Hay filas sin accession en el archivo de metadatos")

    frame["accession"] = frame["accession"].str.strip()
    frame["description"] = frame["description"].fillna("").str.strip()
    frame["accession_norm"] = frame["accession"].map(normalize_accession)
    logger.info("load_accessions: %s filas en %s", len(frame), acc_path)
    return frame
