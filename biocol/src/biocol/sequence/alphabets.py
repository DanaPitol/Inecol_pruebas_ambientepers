"""Alfabetos IUPAC tomados de Biopython."""

from Bio.Data.IUPACData import (
    ambiguous_dna_letters,
    ambiguous_rna_letters,
    extended_protein_letters,
)

NUCLEOTIDE_LETTERS = set((ambiguous_dna_letters + ambiguous_rna_letters).upper())
PROTEIN_LETTERS = set(extended_protein_letters.upper())
GAP_LETTERS = {"-", "."}
VALID_RESIDUES = NUCLEOTIDE_LETTERS | PROTEIN_LETTERS | GAP_LETTERS | {"*"}
PROTEIN_ONLY_LETTERS = (PROTEIN_LETTERS - NUCLEOTIDE_LETTERS) | {"*"}
