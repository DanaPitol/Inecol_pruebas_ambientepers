from pathlib import Path

import pytest

from biocol.blast.runner import build_blast_command, build_makeblastdb_command, run_blast
from biocol.exceptions import BlastExecutionError


def test_makeblastdb_command(tmp_path: Path) -> None:
    fasta = tmp_path / "db.faa"
    prefix = tmp_path / "db"
    command = build_makeblastdb_command(fasta, prefix, "prot")
    assert command[0] == "makeblastdb"
    assert "-dbtype" in command
    assert "prot" in command


def test_blast_command_outfmt6(tmp_path: Path) -> None:
    command = build_blast_command(
        "blastp",
        tmp_path / "q.faa",
        tmp_path / "db",
        tmp_path / "out.txt",
        evalue=1e-5,
        max_target_seqs=1,
        num_threads=2,
    )
    assert command[0] == "blastp"
    assert command[command.index("-outfmt") + 1] == "6"
    assert command[command.index("-evalue") + 1] == "1e-05"
    assert command[command.index("-max_target_seqs") + 1] == "1"


def test_run_blast_requires_executable(fixtures_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("biocol.blast.runner.shutil.which", lambda _name: None)
    with pytest.raises(BlastExecutionError, match="was not found"):
        run_blast(fixtures_dir / "protein.fa", fixtures_dir / "protein.fa")
