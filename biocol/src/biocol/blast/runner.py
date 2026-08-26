from __future__ import annotations

import logging
import shutil
import subprocess
import tempfile
from pathlib import Path

import pandas as pd

+from biocol.blast.databases import infer_database_label, list_blast_databases
from biocol.blast.parser import fill_missing_hits, parse_blast_results
from biocol.blast.selection import select_blast_program
from biocol.exceptions import BlastExecutionError, MixedDatabaseTypeError
from biocol.sequence.classifier import detect_query_type
from biocol.sequence.reader import read_fasta

logger = logging.getLogger(__name__)

_DBTYPE = {"nucleotide": "nucl", "protein": "prot"}
DEFAULT_MAX_TARGET_SEQS = 3
DEFAULT_NUM_THREADS = 1


def build_makeblastdb_command(
    fasta: Path,
    out_prefix: Path,
    dbtype: str,
) -> list[str]:
    return [
        "makeblastdb",
        "-in",
        str(fasta),
        "-dbtype",
        dbtype,
        "-out",
        str(out_prefix),
        "-parse_seqids",
    ]


def build_blast_command(
    program: str,
    query: Path,
    db_prefix: Path,
    out_file: Path,
    *,
    evalue: float = 10,
    max_target_seqs: int = DEFAULT_MAX_TARGET_SEQS,
    num_threads: int = DEFAULT_NUM_THREADS,
) -> list[str]:
    return [
        program,
        "-query",
        str(query),
        "-db",
        str(db_prefix),
        "-out",
        str(out_file),
        "-outfmt",
        "6",
        "-evalue",
        str(evalue),
        "-max_target_seqs",
        str(max_target_seqs),
        "-num_threads",
        str(num_threads),
    ]


def _run_command(command: list[str]) -> None:
    executable = command[0]
    if shutil.which(executable) is None:
        raise BlastExecutionError(
            f"'{executable}' was not found in PATH. Activate the conda environment inecol."
        )
    logger.debug("BLAST+ command: %s", " ".join(command))
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise BlastExecutionError(
            f"{executable} failed (exit code {completed.returncode}): {completed.stderr.strip()}"
        )


def run_blast(
    query: str | Path,
    database: str | Path,
    *,
    translated: bool = False,
    evalue: float = 10,
    max_target_seqs: int = DEFAULT_MAX_TARGET_SEQS,
    num_threads: int = DEFAULT_NUM_THREADS,
) -> pd.DataFrame:
    """Run BLAST+ (one run per database FASTA) and parse outfmt 6.

    BLAST databases are built in a temporary directory and removed afterwards.
    If a query has no hit in a database, an empty row is included.
    """
    query_path = Path(query)
    logger.info("Reading query FASTA: %s", query_path)
    records = read_fasta(query_path)
    query_ids = [record.id for record in records]
    logger.info("Query has %s sequence(s)", len(query_ids))
    query_type = detect_query_type(records)
    db_entries = list_blast_databases(database)
    db_types = {db_type for _, db_type in db_entries}
    if len(db_types) > 1:
        raise MixedDatabaseTypeError(
            "Input mixes nucleotide and protein databases"
        )
    database_type = next(iter(db_types))
    logger.info(
        "Database type: %s (%s FASTA file(s))",
        database_type,
        len(db_entries),
    )
    program = select_blast_program(
        query_type, database_type, translated=translated
    )
    logger.info(
        "Selected %s (query=%s, database=%s, evalue=%s, max_target_seqs=%s, threads=%s)",
        program,
        query_type,
        database_type,
        evalue,
        max_target_seqs,
        num_threads,
    )
    dbtype = _DBTYPE[database_type]

    frames: list[pd.DataFrame] = []
    with tempfile.TemporaryDirectory(prefix="biocol_blast_") as tmp:
        tmp_path = Path(tmp)
        total = len(db_entries)
        for index, (fasta_path, _db_type) in enumerate(db_entries, start=1):
            file_stem = fasta_path.stem
            db_label = infer_database_label(fasta_path)
            prefix = tmp_path / file_stem
            out_file = tmp_path / f"{file_stem}.txt"
            logger.info(
                "[%s/%s] Building BLAST database for %s (%s)",
                index,
                total,
                db_label,
                fasta_path.name,
            )
            _run_command(build_makeblastdb_command(fasta_path, prefix, dbtype))
            logger.info("[%s/%s] Running %s against %s", index, total, program, db_label)
            _run_command(
                build_blast_command(
                    program,
                    query_path,
                    prefix,
                    out_file,
                    evalue=evalue,
                    max_target_seqs=max_target_seqs,
                    num_threads=num_threads,
                )
            )
            parsed = parse_blast_results(out_file)
            parsed["database"] = db_label
            filled = fill_missing_hits(parsed, query_ids, db_label)
            frames.append(filled)
            logger.info(
                "[%s/%s] %s: %s BLAST hit(s)",
                index,
                total,
                db_label,
                0 if parsed.empty else len(parsed),
            )

    combined = pd.concat(frames, ignore_index=True)
    logger.info("BLAST finished (%s row(s) including empty hits)", len(combined))
    return combined
