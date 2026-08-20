"""Argument parser for the biocol CLI. No backend logic here."""

from __future__ import annotations

import argparse
import sys

from biocol import DEFAULT_MAX_TARGET_SEQS, DEFAULT_OUTPUT

from biocol.cli.style import BOLD, CYAN, DIM, MAGENTA, YELLOW, paint, use_color


class _HelpFormatter(argparse.RawDescriptionHelpFormatter):
    """Wider help with colored section titles when the terminal allows it."""

    def __init__(self, prog: str, **kwargs) -> None:
        kwargs.setdefault("max_help_position", 36)
        kwargs.setdefault("width", 100)
        super().__init__(prog, **kwargs)

    def start_section(self, heading: str | None) -> None:
        if heading:
            heading = paint(heading, BOLD, CYAN, stream=sys.stderr)
        super().start_section(heading)

    def _format_action_invocation(self, action: argparse.Action) -> str:
        text = super()._format_action_invocation(action)
        if action.option_strings:
            return paint(text, YELLOW, stream=sys.stderr)
        return paint(text, MAGENTA, BOLD, stream=sys.stderr)

    def _format_usage(self, usage, actions, groups, prefix) -> str:
        if prefix is None:
            prefix = paint("Usage: ", BOLD, CYAN, stream=sys.stderr)
        return super()._format_usage(usage, actions, groups, prefix)


EPILOG = """
Commands
  run          Path 1 — FASTA query + local FASTA databases → BLAST+ → CSV
  from-blast   Path 2 — existing BLAST tabular (outfmt 6) + accessions → CSV
               (no BLAST+ run; query sequence columns stay empty)

Typical use cases
  1) Protein query vs one proteome (blastp)
       biocol run --query query.faa --db species.faa --accessions species.txt \\
                  --output results.csv

  2) Same, with gene-model columns (cDNA + protein of the QUERY)
       biocol run --query query.faa --protein query.faa --cdna query_cds.fna \\
                  --db species.faa --accessions species.txt --output results.csv
       --cdna must be CDS/transcripts, not a whole-genome *.fna
       --accessions must list SUBJECT ids (the --db proteins), not the query

  3) Several species at once (folder of FASTA files, same molecule type)
       biocol run --query query.faa --db databases/ --accessions all_species.txt \\
                  --output results.csv

  4) Nucleotide vs nucleotide (blastn). Use --tblastx for six-frame protein search
       biocol run --query query.fna --db other.fna --accessions other.txt
       biocol run --query query.fna --db other.fna --accessions other.txt --tblastx

  5) Rebuild the CSV from a BLAST file you already have
       biocol from-blast --blast hits.txt --accessions species.txt --output results.csv

Defaults
  e-value 10 · max-target-seqs {max_targets} · threads 1 · output {output}

Colors
  Enabled on an interactive terminal. Disable with --no-color or NO_COLOR=1.
""".format(max_targets=DEFAULT_MAX_TARGET_SEQS, output=DEFAULT_OUTPUT)


def build_parser() -> argparse.ArgumentParser:
    color_note = paint(" (colors on TTY)", DIM) if use_color() else ""
    parser = argparse.ArgumentParser(
        prog="biocol",
        formatter_class=_HelpFormatter,
        description=(
            "biocol builds a BLAST annotation CSV (Dataset S2-style header) "
            "from a FASTA query and local FASTA databases, or from an existing "
            f"BLAST tabular file.{color_note}"
        ),
        epilog=EPILOG,
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
        title="commands",
    )

    run = subparsers.add_parser(
        "run",
        formatter_class=_HelpFormatter,
        help="FASTA + databases → BLAST+ → CSV",
        description=(
            "Path 1. Run BLAST+ on a FASTA query against one FASTA file or a "
            "folder of FASTA files (subfolders included). Join descriptors from "
            "--accessions and write a CSV with a 3-row header."
        ),
        epilog="""
Required
  --query, --db, --accessions

Optional gene models (query organism)
  --protein   fills Length(aa) and protein sequence columns
  --cdna      fills Length (nt) and cDNA columns (CDS FASTA, not genomic)

BLAST program is chosen from sequence types:
  protein vs protein → blastp · nucleotide vs nucleotide → blastn
  (use --tblastx for tblastx) · mixed types → blastx or tblastn
""",
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
        "--protein",
        default=None,
        dest="protein_fasta",
        metavar="FASTA",
        help="Optional query protein FASTA: Length(aa) and protein columns",
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
        formatter_class=_HelpFormatter,
        help="Existing BLAST tabular + accessions → CSV (no BLAST+)",
        description=(
            "Path 2. Parse a BLAST outfmt 6 text file, join accession descriptors, "
            "and write the same CSV as path 1. Sequence columns are left empty. "
            "The species/database block name is taken from the accessions filename "
            "(e.g. Benincasa_hispida_gd.txt → Benincasa_hispida_gd)."
        ),
        epilog="""
Does not run BLAST+. Use this when you already have outfmt 6 hits.
Does not take --query / --cdna / --protein (those columns stay empty).
""",
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
