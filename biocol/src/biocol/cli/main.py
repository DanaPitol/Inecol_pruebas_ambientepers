"""Entry point: parse arguments, dispatch, report errors."""

from __future__ import annotations

import sys

from biocol import BlastError, FastaError, MetadataError

from biocol.cli.commands import run_from_blast, run_from_fasta
from biocol.cli.parser import build_parser
from biocol.cli.style import (
    BOLD,
    GREEN,
    RED,
    disable_color,
    enable_windows_vt,
    paint,
    reset_color,
)

_COMMANDS = {
    "run": run_from_fasta,
    "from-blast": run_from_blast,
}


def main(argv: list[str] | None = None) -> int:
    argv_list = list(sys.argv[1:] if argv is None else argv)
    reset_color()
    if "--no-color" in argv_list:
        disable_color()
    enable_windows_vt()

    parser = build_parser()
    stripped = [item for item in argv_list if item != "--no-color"]
    if not stripped:
        parser.print_help()
        print("error: a command is required (run or from-blast)", file=sys.stderr)
        return 2
    args = parser.parse_args(argv_list)
    try:
        output = _COMMANDS[args.command](args)
    except (FileNotFoundError, FastaError, BlastError, MetadataError, OSError) as exc:
        print(paint(f"error: {exc}", BOLD, RED, stream=sys.stderr), file=sys.stderr)
        return 1
    print(paint(str(output), GREEN, stream=sys.stdout))
    return 0


def console() -> None:
    raise SystemExit(main())
