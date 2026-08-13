from __future__ import annotations

from collections.abc import Iterable

from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from biocol.exceptions import MixedSequenceTypeError
from biocol.sequence.alphabets import GAP_LETTERS, NUCLEOTIDE_LETTERS, PROTEIN_ONLY_LETTERS

SequenceType = str
SequenceLike = str | Seq | SeqRecord


def _residues(sequence: SequenceLike) -> str:
    if isinstance(sequence, SeqRecord):
        text = str(sequence.seq)
    else:
        text = str(sequence)
    return "".join(char for char in text.upper() if char not in GAP_LETTERS)


def detect_sequence_type(sequence: SequenceLike) -> SequenceType:
    """Clasifica una secuencia como ``nucleotide`` o ``protein``.

    Usa los alfabetos IUPAC de ``Bio.Data.IUPACData``. El ARN (U) se trata
    como nucleótido. Letras solo proteicas (E, F, L, P, Q, ...) marcan proteína.
    """
    residues = _residues(sequence)
    if not residues:
        raise ValueError("La secuencia no contiene residuos clasificables")

    if any(char in PROTEIN_ONLY_LETTERS for char in residues):
        return "protein"
    if all(char in NUCLEOTIDE_LETTERS for char in residues):
        return "nucleotide"
    return "protein"


def detect_query_type(records: Iterable[SequenceLike]) -> SequenceType:
    """Tipo de query de un FASTA completo.

    Todas las secuencias deben ser del mismo tipo; si no, se lanza error.
    """
    types = [detect_sequence_type(record) for record in records]
    unique = set(types)
    if len(unique) > 1:
        raise MixedSequenceTypeError(
            "El FASTA mezcla secuencias nucleotídicas y proteicas"
        )
    return types[0]
