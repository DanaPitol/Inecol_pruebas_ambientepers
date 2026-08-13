"""Backend para lectura de FASTA, BLAST y construcción de la tabla de resultados."""

from biocol.exceptions import (
    EmptyFastaError,
    FastaError,
    InvalidFastaError,
    MixedSequenceTypeError,
)
from biocol.sequence import (
    detect_query_type,
    detect_sequence_type,
    read_fasta,
    validate_fasta_file,
)

__all__ = [
    "EmptyFastaError",
    "FastaError",
    "InvalidFastaError",
    "MixedSequenceTypeError",
    "detect_query_type",
    "detect_sequence_type",
    "read_fasta",
    "validate_fasta_file",
]
