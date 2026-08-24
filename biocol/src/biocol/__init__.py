"""Backend para lectura de FASTA, BLAST y construcción de la tabla de resultados."""

from biocol.blast import (
    DEFAULT_MAX_TARGET_SEQS,
    DEFAULT_NUM_THREADS,
    detect_database_type,
    list_blast_databases,
    parse_blast_results,
    run_blast,
    select_blast_program,
)
from biocol.exceptions import (
    BlastError,
    BlastExecutionError,
    DatabaseError,
    EmptyFastaError,
    FastaError,
    InvalidFastaError,
    MetadataError,
    MixedDatabaseTypeError,
    MixedSequenceTypeError,
)
from biocol.metadata import load_accessions, normalize_accession
from biocol.output import DEFAULT_OUTPUT, write_results_csv
from biocol.processing import QUERY_COLUMNS, build_result_table
from biocol.sequence import (
    detect_query_type,
    detect_sequence_type,
    read_fasta,
    validate_fasta_file,
)

__all__ = [
    "BlastError",
    "BlastExecutionError",
    "DEFAULT_MAX_TARGET_SEQS",
    "DEFAULT_NUM_THREADS",
    "DEFAULT_OUTPUT",
    "DatabaseError",
    "EmptyFastaError",
    "FastaError",
    "InvalidFastaError",
    "MetadataError",
    "MixedDatabaseTypeError",
    "MixedSequenceTypeError",
    "QUERY_COLUMNS",
    "build_result_table",
    "detect_database_type",
    "detect_query_type",
    "detect_sequence_type",
    "list_blast_databases",
    "load_accessions",
    "normalize_accession",
    "parse_blast_results",
    "read_fasta",
    "run_blast",
    "select_blast_program",
    "validate_fasta_file",
    "write_results_csv",
]
