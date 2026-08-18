from pathlib import Path

import pandas as pd
import pytest

from biocol import (
    DEFAULT_OUTPUT,
    MetadataError,
    QUERY_COLUMNS,
    build_result_table,
    load_accessions,
    normalize_accession,
    write_results_csv,
)


def _hits() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "qseqid": ["seq1", "seq1", "seq1"],
            "sseqid": ["ref|XP_001.1|", "ref|XP_002.1|", "gb|NO_MATCH.1|"],
            "pident": [99.0, 80.0, 70.0],
            "length": [100, 90, 80],
            "mismatch": [0, 1, 2],
            "gapopen": [0, 0, 0],
            "qstart": [1, 1, 1],
            "qend": [100, 90, 80],
            "sstart": [1, 1, 1],
            "send": [100, 90, 80],
            "evalue": [1e-50, 1e-10, 1e-5],
            "bitscore": [200.0, 150.0, 80.0],
            "database": ["amborella", "vitis", "amborella"],
        }
    )


def test_normalize_accession_strips_ref_prefix() -> None:
    assert normalize_accession("ref|XP_001.1|") == "XP_001.1"
    assert normalize_accession("XP_001") == "XP_001"


def test_load_accessions(fixtures_dir: Path) -> None:
    frame = load_accessions(fixtures_dir / "accessions.txt")
    assert list(frame["accession"]) == ["XP_001", "XP_002", "XP_003"]
    assert "Amborella protein one" in list(frame["description"])


def test_load_accessions_empty_raises(tmp_path: Path) -> None:
    empty = tmp_path / "vacio.txt"
    empty.write_text("", encoding="utf-8")
    with pytest.raises(MetadataError):
        load_accessions(empty)


def test_wide_table_all_hits_and_descriptions(fixtures_dir: Path) -> None:
    table = build_result_table(
        _hits(),
        fixtures_dir / "accessions.txt",
        query_fasta=fixtures_dir / "dna.fa",
    )
    assert list(table.columns[:5]) == QUERY_COLUMNS
    assert "amborella_accession" in table.columns
    assert "vitis_description" in table.columns
    assert len(table) == 2

    best = table.iloc[0]
    assert best["gene_id"] == "seq1"
    assert best["length_nt"] == 28
    assert isinstance(best["cdna_sequence"], str)
    assert pd.isna(best["length_aa"])
    assert pd.isna(best["protein_sequence"])
    assert best["amborella_accession"] == "XP_001.1"
    assert best["amborella_description"] == "Amborella protein one"
    assert best["vitis_accession"] == "XP_002.1"
    assert best["vitis_description"] == "Vitis protein two"

    second = table.iloc[1]
    assert second["amborella_accession"] == "NO_MATCH.1"
    assert second["amborella_description"] == "---"
    assert second["vitis_accession"] == "---"
    assert second["vitis_description"] == "---"


def test_protein_fasta_fills_aa_only(fixtures_dir: Path) -> None:
    hits = _hits()
    hits["qseqid"] = "prot1"
    table = build_result_table(
        hits,
        fixtures_dir / "accessions.txt",
        query_fasta=fixtures_dir / "protein.fa",
    )
    row = table.iloc[0]
    assert row["gene_id"] == "prot1"
    assert pd.isna(row["length_nt"])
    assert row["length_aa"] == 60
    assert isinstance(row["protein_sequence"], str)


def test_camino_2_without_fasta(fixtures_dir: Path) -> None:
    table = build_result_table(
        _hits(),
        fixtures_dir / "accessions.txt",
        query_fasta=None,
    )
    assert table.iloc[0]["gene_id"] == "seq1"
    assert pd.isna(table.iloc[0]["cdna_sequence"])
    assert pd.isna(table.iloc[0]["protein_sequence"])


def test_write_results_csv_default_name(tmp_path: Path, fixtures_dir: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    table = build_result_table(_hits(), fixtures_dir / "accessions.txt")
    path = write_results_csv(table)
    assert path.name == DEFAULT_OUTPUT
    assert path.exists()
    loaded = pd.read_csv(path)
    assert "amborella_evalue" in loaded.columns
    assert "vitis_score" in loaded.columns
