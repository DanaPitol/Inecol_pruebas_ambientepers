from pathlib import Path

from biocol import read_fasta


def test_read_multiline_multifasta() -> None:
    fasta_path = (
        Path(__file__).resolve().parents[2]
        / "tests"
        / "data"
        / "multifasta_multilinea.faa"
    )

    records = read_fasta(fasta_path)

    assert len(records) == 2
    assert [record.id for record in records] == ["seq1", "seq2"]
    assert str(records[0].seq) == "MKTLLVAGTALAGCSTLAA"
    assert str(records[1].seq) == "MAVKIGINGFGRHPE"
