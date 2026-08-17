from pathlib import Path

import pandas as pd

from biocol.blast.parser import OUTFMT6_COLUMNS, fill_missing_hits, parse_blast_results


def test_parse_outfmt6(fixtures_dir: Path) -> None:
    frame = parse_blast_results(fixtures_dir / "blast_outfmt6.txt")
    assert list(frame.columns) == OUTFMT6_COLUMNS
    assert len(frame) == 3
    assert set(frame["qseqid"]) == {"q1", "q2"}
    assert frame.loc[frame["qseqid"] == "q2", "pident"].iloc[0] == 88.0


def test_parse_empty_file(tmp_path: Path) -> None:
    empty = tmp_path / "sin_hits.txt"
    empty.write_text("", encoding="utf-8")
    frame = parse_blast_results(empty)
    assert list(frame.columns) == OUTFMT6_COLUMNS
    assert frame.empty


def test_fill_missing_hits_adds_empty_row(fixtures_dir: Path) -> None:
    parsed = parse_blast_results(fixtures_dir / "blast_outfmt6.txt")
    filled = fill_missing_hits(parsed, ["q1", "q2", "q3"], "amborella")
    assert set(filled["qseqid"]) == {"q1", "q2", "q3"}
    empty_row = filled[filled["qseqid"] == "q3"].iloc[0]
    assert pd.isna(empty_row["sseqid"])
    assert empty_row["database"] == "amborella"
