"""CLI commands. Calls only the public biocol API."""

from __future__ import annotations

from argparse import Namespace
from pathlib import Path

from biocol import (
    build_result_table,
    parse_blast_results,
    run_blast,
    write_results_csv,
)


def run_from_fasta(args: Namespace) -> Path:
    hits = run_blast(
        args.query,
        args.db,
        translated=args.tblastx,
        evalue=args.evalue,
        max_target_seqs=args.max_target_seqs,
        num_threads=args.threads,
    )
    table = build_result_table(
        hits,
        args.accessions,
        query_fasta=args.query,
        cdna_fasta=args.cdna,
        protein_fasta=args.protein_fasta,
    )
    return write_results_csv(table, args.output)


def run_from_blast(args: Namespace) -> Path:
    hits = parse_blast_results(args.blast)
    if "database" not in hits.columns:
        hits["database"] = Path(args.accessions).stem
    table = build_result_table(
        hits,
        args.accessions,
        query_fasta=None,
    )
    return write_results_csv(table, args.output)
