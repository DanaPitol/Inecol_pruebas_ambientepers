"""CLI commands. Calls only the public biocol API."""

from __future__ import annotations

from argparse import Namespace
from pathlib import Path

from biocol import (
    DEFAULT_BLAST_DIR,
    DEFAULT_HMM_DIR,
    DEFAULT_OUTPUT,
    HmmError,
    build_result_table,
    filter_hits_by_pident,
    parse_blast_results,
    run_blast,
    run_hmmscan,
    write_results_csv,
)


def _dir_next_to_output(output: str | None, explicit: str | None, default_name: str) -> Path:
    if explicit:
        return Path(explicit)
    parent = Path(output).parent if output else Path(DEFAULT_OUTPUT).parent
    return parent / default_name


def _maybe_hmmscan(args: Namespace, protein_fasta: str | None):
    if not args.hmm_db:
        return None
    if not protein_fasta:
        raise HmmError("hmmscan requires a protein sequence")
    return run_hmmscan(
        protein_fasta,
        args.hmm_db,
        hmm_dir=_dir_next_to_output(args.output, args.hmm_dir, DEFAULT_HMM_DIR),
        num_threads=getattr(args, "threads", 1),
    )


def run_from_fasta(args: Namespace) -> Path:
    hits = run_blast(
        args.query,
        args.db,
        translated=args.tblastx,
        evalue=args.evalue,
        max_target_seqs=args.max_target_seqs,
        num_threads=args.threads,
        blast_dir=_dir_next_to_output(args.output, args.blast_dir, DEFAULT_BLAST_DIR),
        min_identity=args.min_identity,
    )
    hmm_hits = _maybe_hmmscan(args, args.query)
    table = build_result_table(
        hits,
        args.accessions,
        query_fasta=args.query,
        cdna_fasta=args.cdna,
        protein_fasta=args.protein_fasta,
        hmm_hits=hmm_hits,
    )
    return write_results_csv(table, args.output)


def run_from_blast(args: Namespace) -> Path:
    hits = parse_blast_results(args.blast)
    if "database" not in hits.columns:
        hits["database"] = Path(args.accessions).stem
    hits = filter_hits_by_pident(hits, args.min_identity)
    hmm_hits = _maybe_hmmscan(args, args.protein_fasta)
    table = build_result_table(
        hits,
        args.accessions,
        query_fasta=None,
        protein_fasta=args.protein_fasta,
        hmm_hits=hmm_hits,
    )
    return write_results_csv(table, args.output)
