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

## CP-05 - Selección de BLAST según tipo de secuencia / BLAST Selection by Sequence Type

### Estado / Status

✅ Cubierto / Covered

### Funciones evaluadas / Functions Under Test

`detect_query_type()`

`detect_database_type()`

`select_blast_program()`

### Pruebas automatizadas relacionadas / Related Automated Tests

`biocol/tests/test_detect_sequence_type.py`

`biocol/tests/test_blast_selection.py`

### Condición de prueba / Test Condition

**ES:**
La herramienta recibe una query y una base de datos FASTA. Ambas son
clasificadas como `nucleotide` o `protein`.

La combinación de ambos tipos determina qué programa BLAST debe
seleccionarse.

**EN:**
The tool receives a query and a FASTA database. Both are classified as
`nucleotide` or `protein`.

The combination of both types determines which BLAST program must be
selected.

### Resultado esperado / Expected Result

| Query | Base de datos / Database | Opción traducida / Translated | Programa esperado / Expected Program |
|---|---|---|---|
| `nucleotide` | `nucleotide` | `False` | `blastn` |
| `nucleotide` | `nucleotide` | `True` | `tblastx` |
| `nucleotide` | `protein` | se ignora / ignored | `blastx` |
| `protein` | `protein` | se ignora / ignored | `blastp` |
| `protein` | `nucleotide` | se ignora / ignored | `tblastn` |

**ES:**
La selección del programa debe realizarse correctamente sin que el
usuario tenga que indicar manualmente el tipo de BLAST, excepto cuando
quiera utilizar `tblastx` para una comparación nucleótido contra
nucleótido.

**EN:**
The BLAST program must be selected correctly without requiring the
user to manually specify the BLAST type, except when `tblastx` is
explicitly requested for a nucleotide-versus-nucleotide comparison.

------

## CP-06 - Base de datos inexistente / Missing Database

### Estado / Status

🟡 Parcialmente cubierto / Partially covered

### Funciones evaluadas / Functions Under Test

`detect_database_type()`

`list_blast_databases()`

### Prueba automatizada relacionada / Related Automated Test

`biocol/tests/test_blast_selection.py::test_unknown_source_raises`

**ES:**
La validación de la existencia de la base de datos ya está implementada
en el backend. Cuando la ruta proporcionada no corresponde a un archivo
FASTA ni a una carpeta existente con archivos FASTA, el backend genera
una excepción `DatabaseError`.

El manejo de esta excepción desde la interfaz de línea de comandos,
incluyendo la salida mediante STDERR y el código de salida 1, todavía
depende de la implementación del CLI.

**EN:**
Database existence validation is already implemented in the backend.
When the provided path does not correspond to a FASTA file or an
existing directory containing FASTA files, the backend raises a
`DatabaseError`.

Handling this exception from the command-line interface, including
STDERR output and exit code 1, still depends on the CLI implementation.

### Condición de prueba / Test Condition

**ES:**
El usuario proporciona una ruta hacia una base de datos que no existe.

**EN:**
The user provides a path to a database that does not exist.

### Resultado esperado / Expected Result

**ES:**
El backend debe detectar que la base de datos no existe y generar una
excepción `DatabaseError`.

Una vez integrada la interfaz de línea de comandos, el sistema deberá
mostrar el mensaje correspondiente mediante STDERR, finalizar con
código de salida 1 y no iniciar BLAST.

**EN:**
The backend must detect that the database does not exist and raise a
`DatabaseError`.

Once the command-line interface is integrated, the system must display
the corresponding message through STDERR, terminate with exit code 1,
and not start BLAST.
---

## CP-07 - Encabezado FASTA con descriptor / FASTA Header with Descriptor

### Entrada / Input

`biocol/tests/fixtures/protein_with_descriptor.fa`

### Estado / Status

✅ Cubierto / Covered

### Funciones evaluadas / Functions Under Test

`read_fasta()`

### Prueba automatizada relacionada / Related Automated Test

`biocol/tests/test_fasta_descriptor.py::test_fasta_header_with_descriptor`

### Condición de prueba / Test Condition

**ES:**
El archivo FASTA contiene un encabezado formado por un identificador
seguido de un descriptor con información adicional sobre la secuencia.

Ejemplo:

    >XP_002862155.2 protochlorophyllide reductase A, chloroplastic [Arabidopsis lyrata subsp. lyrata]

**EN:**
The FASTA file contains a header consisting of an identifier followed
by a descriptor with additional information about the sequence.

### Resultado esperado / Expected Result

**ES:**
El sistema debe reconocer correctamente el archivo FASTA, interpretar
`XP_002862155.2` como el identificador de la secuencia y conservar el
encabezado completo como descripción.

**EN:**
The system must correctly recognize the FASTA file, interpret
`XP_002862155.2` as the sequence identifier, and preserve the complete
header as the description.

---

## CP-08 - Bases de datos con tipos mezclados / Mixed Database Types

### Estado / Status

✅ Cubierto / Covered

### Funciones evaluadas / Functions Under Test

`detect_database_type()`

`list_blast_databases()`

### Prueba automatizada relacionada / Related Automated Test

`biocol/tests/test_blast_selection.py::test_folder_mixed_types_raises`

### Condición de prueba / Test Condition

**ES:**
La herramienta recibe una carpeta que contiene al menos un archivo
FASTA con secuencias nucleotídicas y otro archivo FASTA con secuencias
proteicas.

**EN:**
The tool receives a directory containing at least one FASTA file with
nucleotide sequences and another FASTA file with protein sequences.

### Resultado esperado / Expected Result

**ES:**
El backend debe detectar que la carpeta contiene bases de datos de tipos
diferentes y generar una excepción `MixedDatabaseTypeError`.

No debe seleccionarse ningún programa BLAST mientras la entrada de bases
de datos no sea homogénea.

**EN:**
The backend must detect that the directory contains databases of
different types and raise a `MixedDatabaseTypeError`.

No BLAST program should be selected while the database input is not
homogeneous.

---

## CP-09 - Carpeta de base de datos vacía / Empty Database Directory

### Estado / Status

✅ Cubierto / Covered

### Funciones evaluadas / Functions Under Test

`detect_database_type()`

`list_blast_databases()`

### Prueba automatizada relacionada / Related Automated Test

`biocol/tests/test_blast_selection.py::test_empty_folder_raises`

### Condición de prueba / Test Condition

**ES:**
La herramienta recibe como base de datos una ruta hacia una carpeta
existente que no contiene archivos FASTA compatibles.

**EN:**
The tool receives an existing directory as the database source, but
the directory does not contain compatible FASTA files.

### Resultado esperado / Expected Result

**ES:**
El backend debe detectar que la carpeta no contiene archivos FASTA
que puedan utilizarse como base de datos y generar una excepción
`DatabaseError`.

No debe seleccionarse ni ejecutarse ningún programa BLAST.

**EN:**
The backend must detect that the directory does not contain FASTA
files that can be used as a database and raise a `DatabaseError`.

No BLAST program should be selected or executed.

---

## CP-10 - Archivo de base de datos no FASTA / Non-FASTA Database File

### Estado / Status

✅ Cubierto / Covered

### Funciones evaluadas / Functions Under Test

`detect_database_type()`

`list_blast_databases()`

### Prueba automatizada relacionada / Related Automated Test

`biocol/tests/test_blast_selection.py::test_non_fasta_file_raises`

### Condición de prueba / Test Condition

**ES:**
La herramienta recibe como base de datos la ruta de un archivo existente
cuya extensión no corresponde a un formato FASTA soportado.

Por ejemplo:

    database.txt

**EN:**
The tool receives the path of an existing file as the database source,
but its extension does not correspond to a supported FASTA format.

For example:

    database.txt

### Resultado esperado / Expected Result

**ES:**
El backend debe detectar que el archivo proporcionado no corresponde a
una base de datos FASTA válida y generar una excepción `DatabaseError`.

No debe seleccionarse ni ejecutarse ningún programa BLAST.

**EN:**
The backend must detect that the provided file does not correspond to a
valid FASTA database and raise a `DatabaseError`.

No BLAST program should be selected or executed.

---

## CP-11 - Parseo de salida BLAST outfmt 6 / BLAST outfmt 6 Parsing

### Estado / Status

✅ Cubierto / Covered

### Funciones evaluadas / Functions Under Test

`parse_blast_results()`

### Prueba automatizada relacionada / Related Automated Test

`biocol/tests/test_blast_parser.py::test_parse_outfmt6`

### Entrada / Input

`biocol/tests/fixtures/blast_outfmt6.txt`

### Condición de prueba / Test Condition

**ES:**
La herramienta recibe un archivo de resultados BLAST generado en formato
tabular `outfmt 6`.

El archivo contiene las 12 columnas estándar de BLAST:

1. `qseqid`
2. `sseqid`
3. `pident`
4. `length`
5. `mismatch`
6. `gapopen`
7. `qstart`
8. `qend`
9. `sstart`
10. `send`
11. `evalue`
12. `bitscore`

**EN:**
The tool receives a BLAST results file generated in tabular
`outfmt 6` format.

The file contains the 12 standard BLAST columns:

1. `qseqid`
2. `sseqid`
3. `pident`
4. `length`
5. `mismatch`
6. `gapopen`
7. `qstart`
8. `qend`
9. `sstart`
10. `send`
11. `evalue`
12. `bitscore`

### Resultado esperado / Expected Result

**ES:**
`parse_blast_results()` debe leer correctamente el archivo y devolver
una tabla con las 12 columnas estándar de `outfmt 6`.

Cada alineamiento debe conservarse como una fila independiente y los
valores deben asociarse con la columna correspondiente.

**EN:**
`parse_blast_results()` must correctly read the file and return a table
containing the 12 standard `outfmt 6` columns.

Each alignment must be preserved as an independent row and its values
must be associated with the corresponding column.

---

## CP-12 - Query sin resultados BLAST / Query Without BLAST Hits

### Estado / Status

✅ Cubierto / Covered

### Funciones evaluadas / Functions Under Test

`parse_blast_results()`

`fill_missing_hits()`

### Prueba automatizada relacionada / Related Automated Test

`biocol/tests/test_blast_parser.py::test_fill_missing_hits_adds_empty_row`

### Condición de prueba / Test Condition

**ES:**
La herramienta procesa resultados BLAST correspondientes a varias
secuencias de consulta. Al menos una de las queries no presenta ningún
hit en la base de datos analizada.

**EN:**
The tool processes BLAST results corresponding to multiple query
sequences. At least one query does not produce any hit in the analyzed
database.

### Resultado esperado / Expected Result

**ES:**
La query sin hit debe conservarse en la tabla de resultados mediante
una fila propia.

El campo `qseqid` debe contener el identificador de la query, mientras
que los campos correspondientes al alineamiento, incluyendo `sseqid`,
deben permanecer vacíos.

La columna `database` debe conservar el identificador de la base de
datos contra la cual se realizó la búsqueda.

**EN:**
The query without a hit must be preserved in the results table as its
own row.

The `qseqid` field must contain the query identifier, while alignment
fields, including `sseqid`, must remain empty.

The `database` column must preserve the identifier of the database
against which the search was performed.

---

## CP-13 - Ejecución BLAST proteína contra proteína / Protein vs Protein BLAST Execution

### Estado / Status

✅ Cubierto / Covered

### Funciones evaluadas / Functions Under Test

`run_blast()`

`select_blast_program()`

### Condición de prueba / Test Condition

**ES:**
La herramienta recibe como query un archivo FASTA de proteínas y utiliza
otro archivo FASTA de proteínas como base de datos.

Para esta combinación, el programa BLAST seleccionado debe ser `blastp`.

**EN:**
The tool receives a protein FASTA file as the query and another protein
FASTA file as the database.

For this combination, the selected BLAST program must be `blastp`.

### Entrada / Input

Query:

`biocol/tests/fixtures/protein.fa`

Base de datos / Database:

`biocol/tests/fixtures/protein.fa`

### Resultado esperado / Expected Result

**ES:**
La ejecución debe completarse correctamente y devolver una tabla con las
12 columnas estándar de BLAST `outfmt 6` más la columna `database`.

La columna `database` debe identificar la base de datos utilizada.

Para el fixture actual se espera al menos un hit de `prot1` contra
`prot1`.

**EN:**
Execution must complete successfully and return a table containing the
12 standard BLAST `outfmt 6` columns plus the `database` column.

The `database` column must identify the database used.

For the current fixture, at least one `prot1` versus `prot1` hit is
expected.

---

## CP-14 - Carpeta con múltiples bases FASTA / Directory with Multiple FASTA Databases

### Estado / Status

✅ Cubierto / Covered

### Funciones evaluadas / Functions Under Test

`run_blast()`

`list_blast_databases()`

### Condición de prueba / Test Condition

**ES:**
La herramienta recibe como base de datos una carpeta que contiene
múltiples archivos FASTA del mismo tipo.

Cada archivo FASTA debe procesarse como una base independiente.

**EN:**
The tool receives a directory containing multiple FASTA files of the
same type as the database source.

Each FASTA file must be processed as an independent database.

### Entrada / Input

Query:

`biocol/tests/fixtures/protein.fa`

Directorio de bases / Database directory:

Una carpeta temporal con:

- `base1.fa`
- `base2.fa`

Ambos archivos contienen secuencias proteicas.

### Resultado esperado / Expected Result

**ES:**
La herramienta debe ejecutar un análisis BLAST independiente por cada
archivo FASTA de la carpeta.

El resultado combinado debe incluir una columna `database` que permita
identificar a qué archivo de base corresponde cada fila.

Para esta prueba deben aparecer las bases:

- `base1`
- `base2`

**EN:**
The tool must execute an independent BLAST analysis for each FASTA file
in the directory.

The combined result must include a `database` column identifying which
database file produced each row.

For this test, the following databases must appear:

- `base1`
- `base2`

---

## CP-15 - Parámetros personalizados de BLAST / Custom BLAST Parameters

### Estado / Status

✅ Cubierto / Covered

### Funciones evaluadas / Functions Under Test

`run_blast()`

`build_blast_command()`

### Condición de prueba / Test Condition

**ES:**
La herramienta ejecuta BLAST utilizando valores personalizados para
los parámetros `evalue` y `max_target_seqs`.

Para esta prueba se utilizan:

- `evalue = 1e-20`
- `max_target_seqs = 10`

**EN:**
The tool executes BLAST using custom values for the `evalue` and
`max_target_seqs` parameters.

For this test, the following values are used:

- `evalue = 1e-20`
- `max_target_seqs = 10`

### Resultado esperado / Expected Result

**ES:**
La ejecución debe completarse correctamente y los valores proporcionados
deben incluirse en el comando enviado a BLAST.

El comando debe contener:

    -evalue 1e-20
    -max_target_seqs 10

El valor de la columna `evalue` en los resultados corresponde al valor
estadístico calculado para cada hit y no necesariamente coincide con el
umbral proporcionado por el usuario.

**EN:**
Execution must complete successfully and the provided values must be
included in the command sent to BLAST.

The command must contain:

    -evalue 1e-20
    -max_target_seqs 10

The value stored in the result `evalue` column corresponds to the
statistical value calculated for each hit and does not necessarily match
the threshold provided by the user.

---

## CP-16 - Ejecutable BLAST no disponible / BLAST Executable Not Available

### Estado / Status

✅ Cubierto / Covered

### Funciones evaluadas / Functions Under Test

`run_blast()`

`_run_command()`

### Prueba automatizada relacionada / Related Automated Test

`biocol/tests/test_blast_runner.py::test_run_blast_requires_executable`

### Condición de prueba / Test Condition

**ES:**
La herramienta intenta ejecutar un análisis BLAST, pero el ejecutable
requerido no se encuentra disponible en el `PATH` del sistema.

**EN:**
The tool attempts to execute a BLAST analysis, but the required
executable is not available in the system `PATH`.

### Resultado esperado / Expected Result

**ES:**
El backend debe detectar que el ejecutable requerido no está disponible
y generar una excepción `BlastExecutionError`.

El análisis BLAST no debe continuar ni producir resultados parciales.

**EN:**
The backend must detect that the required executable is not available
and raise a `BlastExecutionError`.

The BLAST analysis must not continue or produce partial results.
