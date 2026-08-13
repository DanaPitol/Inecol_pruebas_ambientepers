class FastaError(ValueError):
    """Error base relacionado con archivos FASTA."""


class EmptyFastaError(FastaError):
    """El archivo existe pero no contiene secuencias."""


class InvalidFastaError(FastaError):
    """El archivo no es un FASTA válido o las secuencias no son aceptables."""


class MixedSequenceTypeError(FastaError):
    """Un multifasta mezcla nucleótidos y proteínas."""
