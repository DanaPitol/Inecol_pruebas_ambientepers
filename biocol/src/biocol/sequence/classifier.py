from __future__ import annotations

import logging
from collections.abc import Iterable

from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from biocol.exceptions import MixedSequenceTypeError
from biocol.sequence.alphabets import GAP_LETTERS, NUCLEOTIDE_LETTERS, PROTEIN_ONLY_LETTERS

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
    return "<sin id>"


def detect_sequence_type(sequence: SequenceLike) -> SequenceType:
    """Clasifica una secuencia como ``nucleotide`` o ``protein``.

    Usa los alfabetos IUPAC de ``Bio.Data.IUPACData``. El ARN (U) se trata
    como nucleótido. Letras solo proteicas (E, F, L, P, Q, ...) marcan proteína.
    """
    residues = _residues(sequence)
    if not residues:
        raise ValueError("La secuencia no contiene residuos clasificables")

    if any(char in PROTEIN_ONLY_LETTERS for char in residues):
        sequence_type = "protein"
    elif all(char in NUCLEOTIDE_LETTERS for char in residues):
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
            "El FASTA mezcla secuencias nucleotídicas y proteicas"
        )
    query_type = types[0]
    logger.info(
        "detect_query_type: FASTA clasificado como %s (%s secuencias)",
        query_type,
        len(types),
    )
    return query_type
