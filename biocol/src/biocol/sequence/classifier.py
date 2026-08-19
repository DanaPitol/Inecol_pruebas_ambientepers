from __future__ import annotations

import logging
from collections.abc import Iterable

from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from biocol.exceptions import MixedSequenceTypeError
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

    Usa ``Bio.Data.IUPACData``. El ARN (U) cuenta como nucleótido.

    Las letras solo proteicas (E, F, I, L, P, Q, ...) marcan proteína.
    Los códigos de ambigüedad nucleotídica (K, R, Y, ...) también son
    aminoácidos: sin al menos una base inequívoca (A, C, G, T o U) la
    secuencia se trata como proteína (p. ej. poli-lisina ``KKK…``).
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
    """Tipo de query de un FASTA completo.

    Todas las secuencias deben ser del mismo tipo; si no, se lanza error.
    """
    records_list = list(records)
    types = [detect_sequence_type(record) for record in records_list]
    unique = set(types) #guarda los tipos de secuencias en un conjunto
    if len(unique) > 1:
        logger.info(
            "detect_query_type: FASTA mixto tipos=%s ids=%s",
            types,
            [_sequence_id(record) for record in records_list],
        )
        raise MixedSequenceTypeError(
            "FASTA mixes nucleotide and protein sequences"
        )
    query_type = types[0]
    logger.info(
        "detect_query_type: FASTA clasificado como %s (%s secuencias)",
        query_type,
        len(types),
    )
    return query_type
