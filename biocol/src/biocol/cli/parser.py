"""Argument parser for the biocol CLI. No backend logic here."""

from __future__ import annotations

import argparse

from biocol import DEFAULT_MAX_TARGET_SEQS, DEFAULT_NUM_THREADS, DEFAULT_OUTPUT


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="biocol",
        description=(
            "Build a BLAST annotation CSV from a FASTA query and databases, "
            "or from an existing BLAST tabular file."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser(
        "run",
        help="Path 1: FASTA + databases → BLAST+ → CSV",
        description=(
            "Run BLAST+ on a FASTA query against one FASTA file or a folder "
            "of FASTA files, join accession descriptors, and write the CSV."
        ),
    )
    run.add_argument("--query", required=True, help="Query FASTA / multifasta used for BLAST")
    run.add_argument(
        "--cdna",
        default=None,
        help="Optional cDNA FASTA (gene models): fills Length (nt) and cDNA columns",
    )
    run.add_argument(
        "--protein",
        default=None,
        dest="protein_fasta",
        help="Optional protein FASTA (gene models): fills Length(aa) and protein columns",
    )
    run.add_argument(
        "--db",
        required=True,
        help="Subject FASTA file or folder of FASTA files (subfolders included)",
    )
    run.add_argument(
        "--accessions",
        required=True,
        help="Tab-separated file: accession<TAB>descriptor (no header)",
    )
    run.add_argument(
        "--output",
        default=None,
        help=f"Output CSV path (default: {DEFAULT_OUTPUT})",
    )
    run.add_argument(
        "--tblastx",
        action="store_true",
        help="When query and database are both nucleotide, use tblastx instead of blastn",
    )
    run.add_argument(
        "--evalue",
        type=float,
        default=10,
        help="BLAST E-value threshold (default: 10)",
    )
    run.add_argument(
        "--max-target-seqs",
        type=int,
        default=DEFAULT_MAX_TARGET_SEQS,
        dest="max_target_seqs",
        help=f"Maximum aligned sequences to keep (default: {DEFAULT_MAX_TARGET_SEQS})",
    )
    run.add_argument(
        "--threads",
        type=int,
        default=DEFAULT_NUM_THREADS,
        help=f"BLAST+ CPU threads (default: {DEFAULT_NUM_THREADS})",
    )

    from_blast = subparsers.add_parser(
        "from-blast",
        help="Path 2: existing BLAST tabular + accessions → CSV",
        description=(
            "Parse a BLAST outfmt 6 text file, join accession descriptors, "
            "and write the same CSV as path 1. Sequence columns are left empty. "
            "The species/database block name is taken from the accessions filename "
            "(e.g. Benincasa_hispida_gd.txt → Benincasa_hispida_gd)."
        ),
    )
    from_blast.add_argument(
        "--blast",
        required=True,
        help="BLAST tabular file (outfmt 6, .txt)",
    )
    from_blast.add_argument(
        "--accessions",
        required=True,
        help="Tab-separated file: accession<TAB>descriptor (no header)",
    )
    from_blast.add_argument(
        "--output",
        default=None,
        help=f"Output CSV path (default: {DEFAULT_OUTPUT})",
    )
    return parser
