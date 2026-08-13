# Casos de prueba HU-01 / HU-01 Test Cases

Este documento contiene los casos de prueba definidos para validar
el comportamiento de la herramienta durante el desarrollo de HU-01.

This document contains the test cases defined to validate the behavior
of the tool during the development of HU-01.

---

## CP-01 - FASTA válido / Valid FASTA

### Entrada / Input

`tests/data/fasta_valido.faa`

### Función evaluada / Function Under Test

`validate_fasta_file()`

### Prueba automatizada / Automated Test

`biocol/tests/test_fasta_validator.py::test_existing_valid_fasta`

### Estado / Status

✅ Aprobado / Passed

### Resultado esperado / Expected Result

**ES:**  
El sistema debe reconocer un registro FASTA válido y continuar
con el procesamiento.

**EN:**  
The system must recognize a valid FASTA record and continue
processing.

---

## CP-02 - multiFASTA con secuencia multilínea / Multi-line multiFASTA

### Entrada / Input

`tests/data/multifasta_multilinea.faa`

### Función evaluada / Function Under Test

`read_fasta()`

### Prueba automatizada / Automated Test

`biocol/tests/test_multifasta_multilinea.py::test_read_multiline_multifasta`

### Estado / Status

✅ Aprobado / Passed

### Resultado esperado / Expected Result

**ES:**  
El sistema debe reconocer dos secuencias. La secuencia de `seq1`
debe interpretarse como una sola secuencia aunque esté dividida
en varias líneas.

**EN:**  
The system must recognize two sequences. The `seq1` sequence
must be interpreted as a single sequence even when it is split
across multiple lines.

---

## CP-03 - Archivo FASTA vacío / Empty FASTA File

### Entrada / Input

`tests/data/fasta_vacio.faa`

### Función evaluada / Function Under Test

`validate_fasta_file()`

### Prueba automatizada / Automated Test

`biocol/tests/test_fasta_validator.py::test_empty_fasta`

### Estado / Status

✅ Aprobado / Passed

### Resultado esperado / Expected Result

**ES:**  
El sistema debe rechazar el archivo vacío, mostrar un mensaje
de error mediante STDERR y finalizar con código de salida 1.

**EN:**  
The system must reject the empty file, display an error message
through STDERR, and terminate with exit code 1.

---

## CP-04 - Formato FASTA incorrecto / Invalid FASTA Format

### Entrada / Input

`tests/data/fasta_invalido.faa`

### Función evaluada / Function Under Test

`validate_fasta_file()`

### Prueba automatizada / Automated Test

`biocol/tests/test_fasta_invalido.py::test_invalid_fasta_format`

### Estado / Status

✅ Aprobado / Passed

### Condición de prueba / Test Condition

**ES:**  
El archivo contiene una secuencia, pero el identificador no comienza
con el símbolo `>` requerido por el formato FASTA.

**EN:**  
The file contains a sequence, but the identifier does not begin
with the `>` symbol required by the FASTA format.

### Resultado esperado / Expected Result

**ES:**  
El sistema debe detectar que el archivo no cumple con el formato
FASTA esperado, mostrar un mensaje de error mediante STDERR y
finalizar con código de salida 1. El procesamiento de BLAST no
debe comenzar.

**EN:**  
The system must detect that the file does not comply with the
expected FASTA format, display an error message through STDERR,
and terminate with exit code 1. BLAST processing must not start.

---

## CP-05 - Tipo FASTA incorrecto / Invalid FASTA Type

### Entrada / Input

`tests/data/fasta_type.fna`

### Estado / Status

⏳ Pendiente / Pending

**ES:**  
La detección del tipo de secuencia ya está implementada, pero la
validación de compatibilidad entre la query y el tipo de análisis BLAST
todavía no está implementada.

**EN:**  
Sequence type detection is already implemented, but validation of
compatibility between the query and the BLAST analysis type has not
been implemented yet.

### Condición de prueba / Test Condition

**ES:**
El archivo contiene una secuencia nucleotídica, pero se requiere
una secuencia de aminoácidos.

**EN:**
File contains a nucleotidic sequence, but it is required to be aminoacidic.

### Resultado esperado / Expected Result

**ES:**
El sistema debe detectar que el archivo tiene un formato FAST pero
que no contiene el tipo de información requerida para el proceso, mostrar
un mensaje de error mediante STDERR y finalizar con código de salida 1. 
El procesamiento de BLAST no debe comenzar.

**EN:**
System must detect that file is in FASTA format, but does not cointain
the information type required for the process, and terminate with exit 
code 1. BLAST processing must not start.

---

## CP-06 - Base de datos inexistente / Missing Database

### Estado / Status

⏳ Pendiente / Pending

**ES:**  
La validación y manejo de la base de datos todavía no están
implementados en el backend.

**EN:**  
Database validation and handling have not yet been implemented
in the backend.

### Condición de prueba / Test Condition

**ES:**  
El usuario proporciona una ruta hacia una base de datos que no existe.

**EN:**  
The user provides a path to a database that does not exist.

### Resultado esperado / Expected Result

**ES:**  
El sistema debe detectar que la base de datos no existe, mostrar
un mensaje de error mediante STDERR y finalizar con código de salida 1.
BLAST no debe comenzar.

**EN:**  
The system must detect that the database does not exist, display
an error message through STDERR, and terminate with exit code 1.
BLAST must not start.

