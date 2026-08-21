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


def test_top_help_lists_commands_and_use_cases(capsys) -> None:
    try:
        main(["--no-color", "--help"])
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("expected SystemExit from --help")
    text = capsys.readouterr().out
    assert "BIOCOL" in text
    assert "WORKFLOWS" in text
    assert "QUICK START" in text
    assert "run" in text
    assert "from-blast" in text
    assert "biocol run" in text
    assert "--no-color" in text
    assert "\033[" not in text
    assert "SUBJECT" in text


def test_run_help_documents_gene_models(capsys) -> None:
    try:
        main(["--no-color", "run", "--help"])
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("expected SystemExit from --help")
    text = capsys.readouterr().out
    assert "PROGRAM SELECTION" in text
    assert "--cdna" in text
    assert "--protein" not in text
    assert "blastp" in text
    assert "SUBJECT" in text
    assert "BIOCOL" in text


def test_from_blast_help_documents_outfmt6(capsys) -> None:
    try:
        main(["--no-color", "from-blast", "--help"])
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("expected SystemExit from --help")
    text = capsys.readouterr().out
    assert "from-blast" in text
    assert "--blast" in text
    assert "outfmt 6" in text
