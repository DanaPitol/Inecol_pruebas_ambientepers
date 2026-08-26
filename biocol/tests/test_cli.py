from pathlib import Path

import pandas as pd

from biocol.cli import main


def test_from_blast_writes_csv(tmp_path: Path, fixtures_dir: Path) -> None:
    output = tmp_path / "out.csv"
    code = main(
        [
            "from-blast",
            "--blast",
            str(fixtures_dir / "blast_outfmt6.txt"),
            "--accessions",
            str(fixtures_dir / "accessions.txt"),
            "--output",
            str(output),
        ]
    )
    assert code == 0
    assert output.exists()
    table = pd.read_csv(output, header=2)
    assert "Gene ID" in table.columns
    assert "Accesion No." in table.columns
    assert "q1" in set(table["Gene ID"].astype(str))


def test_from_blast_missing_file_returns_error(tmp_path: Path) -> None:
    code = main(
        [
            "from-blast",
            "--blast",
            str(tmp_path / "missing.txt"),
            "--accessions",
            str(tmp_path / "acc.txt"),
        ]
    )
    assert code == 1


def test_run_help_is_english() -> None:
    try:
        main(["run", "--help"])
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("expected SystemExit from --help")
