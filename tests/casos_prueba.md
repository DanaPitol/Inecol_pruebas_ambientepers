# Casos de prueba HU-01

## CP-01 - FASTA válido

Entrada:
tests/data/fasta_valido.faa

Resultado esperado:
El sistema reconoce un registro FASTA válido y continúa el procesamiento.

---

## CP-02 - multiFASTA con secuencia multilínea

Entrada:
tests/data/multifasta_multilinea.faa

Resultado esperado:
El sistema reconoce dos secuencias.
La secuencia de seq1 debe interpretarse como una sola secuencia aunque esté dividida en varias líneas.

---

## CP-03 - Archivo FASTA vacío

Entrada:
tests/data/fasta_vacio.faa

Resultado esperado:
El sistema debe rechazar el archivo,
mostrar un mensaje de error por STDERR
y finalizar con código de salida 1.
