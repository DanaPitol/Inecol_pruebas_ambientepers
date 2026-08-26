from __future__ import annotations

import logging
import re
from pathlib import Path

import pandas as pd

from biocol.blast.parser import OUTFMT6_COLUMNS
from biocol.metadata.accessions import load_accessions, normalize_accession
from biocol.sequence.classifier import detect_query_type
from biocol.sequence.reader import read_fasta

logger = logging.getLogger(__name__)

QUERY_COLUMNS = [
    "gene_id",
    "length_nt",
    "cdna_sequence",
    "length_aa",
    "protein_sequence",
]

HIT_FIELDS = [
    ("accession", "sseqid"),
    ("description", "description"),
    ("identity_pct", "pident"),
    ("alignment_length", "length"),
    ("evalue", "evalue"),
    ("score", "bitscore"),
]


def _safe_name(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_")
    return cleaned or "db"


def _empty_query_row(query_id: str) -> dict:
    return {
        "gene_id": query_id,
        "length_nt": pd.NA,
        "cdna_sequence": pd.NA,
        "length_aa": pd.NA,
        "protein_sequence": pd.NA,
    }


def _strip_version(accession: str) -> str:
    if "." in accession:
        head, tail = accession.rsplit(".", 1)
        if tail.isdigit():
            return head
    return accession


_PROTEIN_ID_TAG = re.compile(r"\[protein_id=([^\]]+)\]", re.IGNORECASE)
_CDS_ACCESSION = re.compile(r"_cds_([A-Z]{1,3}_?\d+(?:\.\d+)?)", re.IGNORECASE)


def _record_lookup_keys(record) -> list[str]:
    """IDs con los que se puede cruzar un FASTA NCBI CDS con un .faa."""
    keys = [record.id, normalize_accession(record.id)]
    description = record.description or ""
    tagged = _PROTEIN_ID_TAG.search(description)
    if tagged:
        keys.append(tagged.group(1).strip())
    cds = _CDS_ACCESSION.search(record.id)
    if cds:
        keys.append(cds.group(1))
    expanded: list[str] = []
    for key in keys:
        if not key:
            continue
        expanded.append(key)
        stripped = _strip_version(key)
        if stripped != key:
            expanded.append(stripped)
    return list(dict.fromkeys(expanded))


def _apply_fasta_to_rows(
    rows: dict[str, dict],
    fasta_path: str | Path,
    *,
    force_type: str | None = None,
) -> None:
    records = read_fasta(fasta_path)
    seq_type = force_type or detect_query_type(records)
    by_key: dict[str, str] = {}
    for record in records:
        sequence = str(record.seq)
        for key in _record_lookup_keys(record):
            by_key.setdefault(key, sequence)
    for query_id, row in rows.items():
        sequence = by_key.get(query_id) or by_key.get(_strip_version(query_id), "")
        if not sequence:
            continue
        if seq_type == "nucleotide":
            row["length_nt"] = len(sequence)
            row["cdna_sequence"] = sequence
        else:
            row["length_aa"] = len(sequence)
            row["protein_sequence"] = sequence


def _query_metadata(
    query_ids: list[str],
    query_fasta: str | Path | None = None,
    cdna_fasta: str | Path | None = None,
    protein_fasta: str | Path | None = None,
) -> pd.DataFrame:
    if not query_ids:
        return pd.DataFrame(columns=QUERY_COLUMNS)
    rows = {query_id: _empty_query_row(query_id) for query_id in query_ids}
    if query_fasta is not None:
        _apply_fasta_to_rows(rows, query_fasta)
    if cdna_fasta is not None:
        _apply_fasta_to_rows(rows, cdna_fasta, force_type="nucleotide")
    if protein_fasta is not None:
        _apply_fasta_to_rows(rows, protein_fasta, force_type="protein")
    return pd.DataFrame(list(rows.values()))


def _lookup_description(accession: object, accessions: pd.DataFrame) -> str:
    if accession is None or (isinstance(accession, float) and pd.isna(accession)):
        return "---"
    raw = str(accession).strip()
    candidates = [raw, normalize_accession(raw)]
    candidates.append(_strip_version(candidates[-1]))
    for key in dict.fromkeys(candidates):
        exact = accessions.loc[accessions["accession"] == key, "description"]
        if not exact.empty:
            return exact.iloc[0] or "---"
        by_norm = accessions.loc[accessions["accession_norm"] == key, "description"]
        if not by_norm.empty:
            return by_norm.iloc[0] or "---"
    return "---"


def build_result_table(
    blast_hits: pd.DataFrame,
    accessions_path: str | Path,
    query_fasta: str | Path | None = None,
    cdna_fasta: str | Path | None = None,
    protein_fasta: str | Path | None = None,
) -> pd.DataFrame:
    """Tabla ancha estilo Dataset S2 (sin Pfam/KEGG/GO).

    Una fila por query y rango de hit. Cada FASTA de base aporta un bloque
    de columnas. Se conservan todos los hits.
    """
    accessions = load_accessions(accessions_path)
    hits = blast_hits.copy()
    if hits.empty:
        hits = pd.DataFrame(columns=[*OUTFMT6_COLUMNS, "database"])

    if "database" not in hits.columns:
        hits["database"] = "hit"

    hits["qseqid"] = hits["qseqid"].astype(str)
    query_ids = list(dict.fromkeys(hits["qseqid"].tolist()))
    if query_fasta is not None:
        fasta_ids = [record.id for record in read_fasta(query_fasta)]
        query_ids = list(dict.fromkeys([*fasta_ids, *query_ids]))
    if protein_fasta is not None:
        fasta_ids = [record.id for record in read_fasta(protein_fasta)]
        query_ids = list(dict.fromkeys([*fasta_ids, *query_ids]))

    hits["description"] = hits["sseqid"].map(
        lambda value: _lookup_description(value, accessions)
    )
    hits["_evalue_sort"] = pd.to_numeric(hits["evalue"], errors="coerce")
    hits["_score_sort"] = pd.to_numeric(hits["bitscore"], errors="coerce")
    hits = hits.sort_values(
        ["qseqid", "database", "_evalue_sort", "_score_sort"],
        ascending=[True, True, True, False],
        na_position="last",
    )
    hits["hit_rank"] = hits.groupby(["qseqid", "database"], dropna=False).cumcount() + 1
    empty_mask = hits["sseqid"].isna() | (hits["sseqid"].astype(str) == "")
    hits.loc[empty_mask, "hit_rank"] = 1

    databases = list(dict.fromkeys(hits["database"].astype(str).tolist()))
    query_meta = _query_metadata(
        query_ids,
        query_fasta=query_fasta,
        cdna_fasta=cdna_fasta,
        protein_fasta=protein_fasta,
    )

    max_rank_by_query = (
        hits.groupby("qseqid")["hit_rank"].max().to_dict() if not hits.empty else {}
    )
    table_rows: list[dict] = []
    for query_id in query_ids:
        max_rank = int(max_rank_by_query.get(query_id, 1) or 1)
        base = query_meta.loc[query_meta["gene_id"] == query_id]
        query_row = base.iloc[0].to_dict() if not base.empty else {
            "gene_id": query_id,
            "length_nt": pd.NA,
            "cdna_sequence": pd.NA,
            "length_aa": pd.NA,
            "protein_sequence": pd.NA,
        }
        for rank in range(1, max_rank + 1):
            row = {column: query_row[column] for column in QUERY_COLUMNS}
            for database in databases:
                prefix = _safe_name(str(database))
                match = hits[
                    (hits["qseqid"] == query_id)
                    & (hits["database"].astype(str) == str(database))
                    & (hits["hit_rank"] == rank)
                ]
                for field, source in HIT_FIELDS:
                    column = f"{prefix}_{field}"
                    if match.empty:
                        row[column] = "---" if field in {"accession", "description"} else pd.NA
                    else:
                        value = match.iloc[0][source]
                        if field == "accession":
                            if pd.isna(value) or str(value) == "":
                                row[column] = "---"
                            else:
                                row[column] = normalize_accession(value) or str(value)
                        elif field == "description":
                            row[column] = value if value else "---"
                        else:
                            row[column] = value
            table_rows.append(row)

    table = pd.DataFrame(table_rows)
    logger.info("build_result_table: %s filas, %s columnas", len(table), table.shape[1])
    return table
