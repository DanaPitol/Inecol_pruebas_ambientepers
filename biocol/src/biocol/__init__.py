"""Backend for FASTA reading, BLAST, and result table construction."""

from biocol.blast import (
    DEFAULT_BLAST_DIR,
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
    HmmError,
    HmmExecutionError,
    InvalidFastaError,
    MetadataError,
    MixedDatabaseTypeError,
    MixedSequenceTypeError,
)
from biocol.hmm import DEFAULT_HMM_DIR, parse_hmmscan_tblout, run_hmmscan
from biocol.metadata import load_accessions, normalize_accession
from biocol.output import DEFAULT_OUTPUT, write_results_csv
from biocol.processing import PFAM_COLUMNS, QUERY_COLUMNS, build_result_table, filter_hits_by_pident
from biocol.sequence import (
    detect_query_type,
    detect_sequence_type,
    read_fasta,
    validate_fasta_file,
)

__all__ = [
    "BlastError",
    "BlastExecutionError",
    "DEFAULT_BLAST_DIR",
    "DEFAULT_HMM_DIR",
    "DEFAULT_MAX_TARGET_SEQS",
    "DEFAULT_NUM_THREADS",
    "DEFAULT_OUTPUT",
    "DatabaseError",
    "EmptyFastaError",
    "FastaError",
    "HmmError",
    "HmmExecutionError",
    "InvalidFastaError",
    "MetadataError",
    "MixedDatabaseTypeError",
    "MixedSequenceTypeError",
    "PFAM_COLUMNS",
    "QUERY_COLUMNS",
    "build_result_table",
    "detect_database_type",
    "detect_query_type",
    "detect_sequence_type",
    "filter_hits_by_pident",
    "list_blast_databases",
    "load_accessions",
    "normalize_accession",
    "parse_blast_results",
    "parse_hmmscan_tblout",
    "read_fasta",
    "run_blast",
    "run_hmmscan",
    "select_blast_program",
    "validate_fasta_file",
    "write_results_csv",
]
