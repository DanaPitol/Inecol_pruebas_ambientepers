"""Alfabetos IUPAC tomados de Biopython (``Bio.Data.IUPACData``)."""

from Bio.Data.IUPACData import (
    ambiguous_dna_letters,
    ambiguous_rna_letters,
    extended_protein_letters,
    unambiguous_dna_letters,
    unambiguous_rna_letters,
)

# ADN/ARN con códigos de ambigüedad (K, R, Y, ...). Se solapan con aminoácidos.
NUCLEOTIDE_LETTERS = set((ambiguous_dna_letters + ambiguous_rna_letters).upper())
# Bases inequívocas: no se confunden con lisina (K), arginina (R), etc.
UNAMBIGUOUS_NUCLEOTIDE_LETTERS = set(
    (unambiguous_dna_letters + unambiguous_rna_letters).upper()
)
PROTEIN_LETTERS = set(extended_protein_letters.upper())
GAP_LETTERS = {"-", "."}
VALID_RESIDUES = NUCLEOTIDE_LETTERS | PROTEIN_LETTERS | GAP_LETTERS | {"*"}
# E, F, I, L, P, Q, X, O, Z, J, *
PROTEIN_ONLY_LETTERS = (PROTEIN_LETTERS - NUCLEOTIDE_LETTERS) | {"*"}
