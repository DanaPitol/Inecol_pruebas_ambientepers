from __future__ import annotations

import logging
from pathlib import Path

from biocol.exceptions import DatabaseError, MixedDatabaseTypeError
from biocol.sequence.classifier import detect_query_type
from biocol.sequence.reader import read_fasta
from biocol.sequence.validator import FASTA_EXTENSIONS

logger = logging.getLogger(__name__)

SequenceType = str


def _is_fasta_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in FASTA_EXTENSIONS


def _type_from_fasta(path: Path) -> SequenceType:
    records = read_fasta(path)
    return detect_query_type(records)


def _iter_fasta_in_directory(directory: Path) -> list[Path]:
    files = [
        path
        for path in directory.rglob("*")
        if _is_fasta_file(path)
    ]
    return sorted(files)


def list_blast_databases(source: str | Path) -> list[tuple[Path, SequenceType]]:
    """Resuelve un FASTA o una carpeta (incluye subcarpetas).

    Devuelve pares ``(ruta, tipo)``.
    """
    raw = Path(source)

    if raw.is_dir():
        fasta_files = _iter_fasta_in_directory(raw)
        if not fasta_files:
            raise DatabaseError(
                f"La carpeta no contiene archivos FASTA ({', '.join(sorted(FASTA_EXTENSIONS))}): {raw}"
            )
        return [(path, _type_from_fasta(path)) for path in fasta_files]

    if _is_fasta_file(raw):
        return [(raw, _type_from_fasta(raw))]

    if raw.is_file():
        raise DatabaseError(
            f"La base debe ser FASTA ({', '.join(sorted(FASTA_EXTENSIONS))}), no {raw.suffix}: {raw}"
        )

    raise DatabaseError(
        f"No se reconoció la base de datos: {source}. "
        "Pase un archivo FASTA o una carpeta con archivos FASTA."
    )


def detect_database_type(source: str | Path) -> SequenceType:
    """Tipo de una base FASTA: ``nucleotide`` o ``protein``.

    Acepta un archivo FASTA o una carpeta (y subcarpetas) con FASTA
    del mismo tipo.
    """
    entries = list_blast_databases(source)
    types = [db_type for _, db_type in entries]
    unique = set(types)
    if len(unique) > 1:
        logger.info(
            "detect_database_type: bases mixtas %s",
            [(str(path), db_type) for path, db_type in entries],
        )
        raise MixedDatabaseTypeError(
            "La entrada mezcla bases nucleotídicas y proteicas"
        )
    database_type = types[0]
    logger.info(
        "detect_database_type: source=%s tipo=%s bases=%s",
        source,
        database_type,
        len(entries),
    )
    return database_type
