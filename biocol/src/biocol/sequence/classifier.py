from __future__ import annotations

import logging
from collections import Counter
from collections.abc import Iterable

from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from biocol.sequence.alphabets import (
    GAP_LETTERS,
    NUCLEOTIDE_LETTERS,
    PROTEIN_ONLY_LETTERS,
    UNAMBIGUOUS_NUCLEOTIDE_LETTERS,
)

logger = logging.getLogger(__name__)

SequenceType = str
SequenceLike = str | Seq | SeqRecord


def _residues(sequence: SequenceLike) -> str:
    if isinstance(sequence, SeqRecord):
        text = str(sequence.seq)
    else:
        text = str(sequence)
    return "".join(char for char in text.upper() if char not in GAP_LETTERS)


def _sequence_id(sequence: SequenceLike) -> str:
    if isinstance(sequence, SeqRecord) and sequence.id:
        return sequence.id
    return "<no id>"


def detect_sequence_type(sequence: SequenceLike) -> SequenceType:
    """Clasifica una secuencia como ``nucleotide`` o ``protein``.
    Usa ``Bio.Data.IUPACData``.
    """
    residues = _residues(sequence)
    if not residues:
        raise ValueError("Sequence has no classifiable residues")

    if any(char in PROTEIN_ONLY_LETTERS for char in residues):
        sequence_type = "protein"
    elif all(char in NUCLEOTIDE_LETTERS for char in residues) and any(
        char in UNAMBIGUOUS_NUCLEOTIDE_LETTERS for char in residues
    ):
        sequence_type = "nucleotide"
    else:
        sequence_type = "protein"

    logger.info(
        "detect_sequence_type: id=%s longitud=%s tipo=%s",
        _sequence_id(sequence),
        len(residues),
        sequence_type,
    )
    return sequence_type


def detect_query_type(records: Iterable[SequenceLike]) -> SequenceType:
    """Tipo de un FASTA completo: el tipo mayoritario.

    Si hay secuencias clasificadas distinto (p. ej. péptidos cortos que
    parecen ADN), no se aborta: se usa proteína en empate.
    """
    records_list = list(records)
    types = [detect_sequence_type(record) for record in records_list]
    counts = Counter(types)
    protein_n = counts.get("protein", 0)
    nucleotide_n = counts.get("nucleotide", 0)
    query_type = "protein" if protein_n >= nucleotide_n else "nucleotide"
    if len(counts) > 1:
        minority_ids = [
            _sequence_id(record)
            for record, seq_type in zip(records_list, types, strict=True)
            if seq_type != query_type
        ]
        logger.debug(
            "detect_query_type: FASTA mixto; se usa %s (protein=%s nucleotide=%s) ids minoría=%s",
            query_type,
            protein_n,
            nucleotide_n,
            minority_ids[:20],
        )
    logger.info(
        "detect_query_type: FASTA clasificado como %s (%s secuencias)",
        query_type,
        len(types),
    )
    return query_type
