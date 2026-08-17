from __future__ import annotations

import logging

from biocol.exceptions import BlastError

logger = logging.getLogger(__name__)

_DIRECT_PROGRAMS = {
    ("nucleotide", "protein"): "blastx",
    ("protein", "protein"): "blastp",
    ("protein", "nucleotide"): "tblastn",
}


def select_blast_program(
    query_type: str,
    database_type: str,
    *,
    translated: bool = False,
) -> str:
    """Elige blastn, blastp, blastx, tblastn o tblastx.

    Si query y base son nucleótido, el valor por defecto es blastn.
    ``translated=True`` (opción explícita, desactivada por defecto) elige tblastx.
    En las demás combinaciones ``translated`` se ignora.
    """
    if query_type not in {"nucleotide", "protein"}:
        raise BlastError(f"Tipo de query no soportado: {query_type}")
    if database_type not in {"nucleotide", "protein"}:
        raise BlastError(f"Tipo de base no soportado: {database_type}")

    both_nucleotide = query_type == "nucleotide" and database_type == "nucleotide"
    if both_nucleotide:
        program = "tblastx" if translated else "blastn"
    else:
        program = _DIRECT_PROGRAMS[(query_type, database_type)]

    logger.info(
        "select_blast_program: query=%s db=%s translated=%s → %s",
        query_type,
        database_type,
        translated,
        program,
    )
    return program
