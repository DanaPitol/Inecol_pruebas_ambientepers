from __future__ import annotations

import logging
import shutil
import subprocess
import tempfile
from pathlib import Path

import pandas as pd

from biocol.blast.databases import detect_database_type, infer_database_label, list_blast_databases
from biocol.blast.parser import fill_missing_hits, parse_blast_results
from biocol.blast.selection import select_blast_program
from biocol.exceptions import BlastExecutionError
from biocol.sequence.classifier import detect_query_type
from biocol.sequence.reader import read_fasta

logger = logging.getLogger(__name__)

_DBTYPE = {"nucleotide": "nucl", "protein": "prot"}
DEFAULT_MAX_TARGET_SEQS = 3


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
    num_threads: int = 1,
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
    logger.info("ejecutar: %s", " ".join(command))
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
    num_threads: int = 1,
) -> pd.DataFrame:
    """Ejecuta BLAST+ (un run por FASTA de base) y parsea outfmt 6.

    Las bases BLAST se crean en un directorio temporal y se borran al terminar.
    Si una query no tiene hit en una base, se incluye una fila vacía.
    """
    query_path = Path(query)
    records = read_fasta(query_path)
    query_ids = [record.id for record in records]
    query_type = detect_query_type(records)
    database_type = detect_database_type(database)
    program = select_blast_program(
        query_type, database_type, translated=translated
    )
    dbtype = _DBTYPE[database_type]
    db_entries = list_blast_databases(database)

    frames: list[pd.DataFrame] = []
    with tempfile.TemporaryDirectory(prefix="biocol_blast_") as tmp:
        tmp_path = Path(tmp)
        for fasta_path, _db_type in db_entries:
            file_stem = fasta_path.stem
            db_label = infer_database_label(fasta_path)
            prefix = tmp_path / file_stem
            out_file = tmp_path / f"{file_stem}.txt"
            _run_command(build_makeblastdb_command(fasta_path, prefix, dbtype))
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
                "run_blast: db=%s archivo=%s hits=%s filas=%s",
                db_label,
                file_stem,
                0 if parsed.empty else len(parsed),
                len(filled),
            )

    combined = pd.concat(frames, ignore_index=True)
    logger.info("run_blast: programa=%s filas_totales=%s", program, len(combined))
    return combined
