"""Entry point: parse arguments, dispatch, report errors."""

from __future__ import annotations

import sys

from biocol import BlastError, FastaError, MetadataError

from biocol.cli.commands import run_from_blast, run_from_fasta
from biocol.cli.parser import build_parser

_COMMANDS = {
    "run": run_from_fasta,
    "from-blast": run_from_blast,
}


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        output = _COMMANDS[args.command](args)
    except (FileNotFoundError, FastaError, BlastError, MetadataError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(output)
    return 0


def console() -> None:
    raise SystemExit(main())
