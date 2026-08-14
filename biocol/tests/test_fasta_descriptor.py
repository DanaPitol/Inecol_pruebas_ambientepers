from pathlib import Path

from biocol.sequence.reader import read_fasta


def test_fasta_header_with_descriptor(fixtures_dir: Path) -> None:
    records = read_fasta(fixtures_dir / "protein_with_descriptor.fa")

    assert len(records) == 1

    record = records[0]

    assert record.id == "XP_002862155.2"
    assert record.description == (
        "XP_002862155.2 protochlorophyllide reductase A, chloroplastic "
        "[Arabidopsis lyrata subsp. lyrata]"
    )
