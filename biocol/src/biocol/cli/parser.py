"""Argument parser for the biocol CLI. No backend logic here."""

from __future__ import annotations

import argparse
import sys

from biocol import DEFAULT_MAX_TARGET_SEQS, DEFAULT_OUTPUT

from biocol.cli.helptext import render_from_blast_help, render_run_help, render_top_help
from biocol.cli.style import BOLD, RED, paint


class _HelpParser(argparse.ArgumentParser):
    """argparse parser that prints the custom BIOCOL help screens."""

    def __init__(self, *args, help_renderer=None, **kwargs) -> None:
        self._help_renderer = help_renderer
        super().__init__(*args, **kwargs)

    def format_help(self) -> str:
        if self._help_renderer is not None:
            return self._help_renderer()
        return super().format_help()

    def error(self, message: str) -> None:
        # Show the custom screen instead of argparse's short usage blurb.
        sys.stderr.write(self.format_help())
        sys.stderr.write(paint(f"\nerror: {message}\n", BOLD, RED, stream=sys.stderr))
        self.exit(2)


def build_parser() -> argparse.ArgumentParser:
    parser = _HelpParser(
        prog="biocol",
        add_help=True,
        help_renderer=render_top_help,
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI colors in help, errors, and status lines",
    )
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        metavar="COMMAND",
        parser_class=_HelpParser,
    )

    run = subparsers.add_parser(
        "run",
        help="FASTA + databases → BLAST+ → CSV",
        help_renderer=render_run_help,
    )
    run.add_argument(
        "--query",
        required=True,
        metavar="FASTA",
        help="Query FASTA / multifasta used for BLAST (all records same type)",
    )
    run.add_argument(
        "--cdna",
        default=None,
        metavar="FASTA",
        help="Optional query CDS FASTA: Length (nt) and cDNA columns",
    )
    run.add_argument(
        "--db",
        required=True,
        metavar="PATH",
        help="Subject FASTA file, or folder of FASTA files (same type; subfolders included)",
    )
    run.add_argument(
        "--accessions",
        required=True,
        metavar="FILE",
        help="TSV of SUBJECT hits: accession<TAB>descriptor (no header). Missing ids → ---",
    )
    run.add_argument(
        "--output",
        default=None,
        metavar="CSV",
        help=f"Output CSV path (default: {DEFAULT_OUTPUT})",
    )
    run.add_argument(
        "--tblastx",
        action="store_true",
        help="If query and database are both nucleotide, use tblastx instead of blastn",
    )
    run.add_argument(
        "--evalue",
        type=float,
        default=10,
        metavar="N",
        help="BLAST E-value threshold (default: 10)",
    )
    run.add_argument(
        "--max-target-seqs",
        type=int,
        default=DEFAULT_MAX_TARGET_SEQS,
        dest="max_target_seqs",
        metavar="N",
        help=f"Maximum aligned sequences to keep per query (default: {DEFAULT_MAX_TARGET_SEQS})",
    )
    run.add_argument(
        "--threads",
        type=int,
        default=1,
        metavar="N",
        help="BLAST+ CPU threads (default: 1)",
    )

    from_blast = subparsers.add_parser(
        "from-blast",
        help="Existing BLAST tabular + accessions → CSV (no BLAST+)",
        help_renderer=render_from_blast_help,
    )
    from_blast.add_argument(
        "--blast",
        required=True,
        metavar="FILE",
        help="BLAST tabular file (outfmt 6, typically .txt)",
    )
    from_blast.add_argument(
        "--accessions",
        required=True,
        metavar="FILE",
        help="TSV of SUBJECT hits: accession<TAB>descriptor (no header)",
    )
    from_blast.add_argument(
        "--output",
        default=None,
        metavar="CSV",
        help=f"Output CSV path (default: {DEFAULT_OUTPUT})",
    )
    return parser
