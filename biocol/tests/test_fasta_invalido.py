from pathlib import Path

import pytest

from biocol import InvalidFastaError, validate_fasta_file


def test_invalid_fasta_format() -> None:
    fasta_path = (
        Path(__file__).resolve().parents[2]
        / "tests"
        / "data"
        / "fasta_invalido.faa"
    )

    with pytest.raises(InvalidFastaError):
        validate_fasta_file(fasta_path)
