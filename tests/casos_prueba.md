# Casos de prueba HU-01 / HU-01 Test Cases

Este documento contiene los casos de prueba definidos para validar el
comportamiento de la herramienta desarrollada durante HU-01.

Los casos incluyen pruebas unitarias, pruebas de integración y pruebas
manuales de la interfaz de línea de comandos (CLI).

This document contains the test cases defined to validate the behavior
of the tool developed during HU-01.

The test cases include unit tests, integration tests, and manual tests
of the command-line interface (CLI).

---

## CP-01 - FASTA válido / Valid FASTA

### Estado / Status

✅ Cubierto / Covered

### Función evaluada / Function Under Test

`validate_fasta_file()`

### Condición de prueba / Test Condition

**ES:**
La herramienta recibe un archivo que cumple correctamente con el
formato FASTA.

**EN:**
The tool receives a file that correctly follows the FASTA format.

### Resultado esperado / Expected Result

**ES:**
El archivo debe ser reconocido como un FASTA válido y el procesamiento
debe continuar normalmente.

**EN:**
The file must be recognized as a valid FASTA file and processing must
continue normally.

---

## CP-02 - multiFASTA con secuencia multilínea / Multi-line multiFASTA

### Estado / Status

✅ Cubierto / Covered

### Función evaluada / Function Under Test

`read_fasta()`

### Condición de prueba / Test Condition

**ES:**
La herramienta recibe un archivo multiFASTA que contiene varias
secuencias y al menos una de ellas está dividida en múltiples líneas.

**EN:**
The tool receives a multiFASTA file containing multiple sequences,
with at least one sequence split across multiple lines.

### Resultado esperado / Expected Result

**ES:**
Cada registro debe identificarse correctamente y las líneas que
pertenecen a una misma secuencia deben concatenarse.

**EN:**
Each record must be correctly identified and lines belonging to the
same sequence must be concatenated.

---

## CP-03 - Archivo FASTA vacío / Empty FASTA File

### Estado / Status

✅ Cubierto / Covered

### Función evaluada / Function Under Test

`validate_fasta_file()`

### Condición de prueba / Test Condition

**ES:**
La herramienta recibe un archivo FASTA vacío.

**EN:**
The tool receives an empty FASTA file.

### Resultado esperado / Expected Result

**ES:**
El archivo debe rechazarse y el procesamiento no debe continuar.

**EN:**
The file must be rejected and processing must not continue.

---

## CP-04 - Formato FASTA incorrecto / Invalid FASTA Format

### Estado / Status

✅ Cubierto / Covered

### Funciones evaluadas / Functions Under Test

`validate_fasta_file()`

`read_fasta()`

### Condición de prueba / Test Condition

**ES:**
La herramienta recibe un archivo que no cumple con la estructura
esperada de un FASTA válido.

**EN:**
The tool receives a file that does not follow the expected structure
of a valid FASTA file.

### Resultado esperado / Expected Result

**ES:**
El sistema debe detectar el formato incorrecto, rechazar el archivo y
evitar que el procesamiento continúe.

**EN:**
The system must detect the invalid format, reject the file, and prevent
further processing.

---

## CP-05 - Encabezado FASTA con descriptor / FASTA Header with Descriptor

### Estado / Status

✅ Cubierto / Covered

### Función evaluada / Function Under Test

`read_fasta()`

### Condición de prueba / Test Condition

**ES:**
El encabezado de una secuencia FASTA contiene un identificador seguido
de información descriptiva adicional.

**EN:**
A FASTA sequence header contains an identifier followed by additional
descriptive information.

### Resultado esperado / Expected Result

**ES:**
La herramienta debe reconocer correctamente el identificador de la
secuencia sin que la presencia del descriptor invalide el registro.

**EN:**
The tool must correctly recognize the sequence identifier without the
descriptor invalidating the record.

---

## CP-06 - Detección del tipo de secuencia / Sequence Type Detection

### Estado / Status

✅ Cubierto / Covered

### Funciones evaluadas / Functions Under Test

`detect_query_type()`

`detect_database_type()`

### Condición de prueba / Test Condition

**ES:**
La herramienta recibe secuencias nucleotídicas o proteicas tanto en la
query como en las bases de datos.

**EN:**
The tool receives nucleotide or protein sequences in both the query and
the databases.

### Resultado esperado / Expected Result

**ES:**
La herramienta debe clasificar correctamente las secuencias como
`nucleotide` o `protein`.

**EN:**
The tool must correctly classify sequences as `nucleotide` or
`protein`.

---

## CP-07 - Selección automática del programa BLAST / Automatic BLAST Program Selection

### Estado / Status

✅ Cubierto / Covered

### Función evaluada / Function Under Test

`select_blast_program()`

### Condición de prueba / Test Condition

**ES:**
Una vez identificado el tipo de la query y de la base de datos, la
herramienta debe determinar automáticamente qué programa BLAST utilizar.

**EN:**
Once the query and database types have been identified, the tool must
automatically determine which BLAST program to use.

### Resultado esperado / Expected Result

| Query | Base / Database | Programa / Program |
|---|---|---|
| nucleotide | nucleotide | `blastn` |
| nucleotide | nucleotide con `--tblastx` | `tblastx` |
| nucleotide | protein | `blastx` |
| protein | protein | `blastp` |
| protein | nucleotide | `tblastn` |

**ES:**
El usuario no debe tener que seleccionar manualmente el programa BLAST,
excepto para solicitar explícitamente `tblastx` en una comparación
nucleótido contra nucleótido.

**EN:**
The user must not need to manually select the BLAST program, except
when explicitly requesting `tblastx` for a nucleotide-versus-nucleotide
comparison.

---

## CP-08 - Base de datos inexistente o inválida / Missing or Invalid Database

### Estado / Status

✅ Cubierto / Covered

### Funciones evaluadas / Functions Under Test

`detect_database_type()`

`list_blast_databases()`

`biocol run`

### Condición de prueba / Test Condition

**ES:**
La ruta proporcionada como base de datos no existe o corresponde a un
archivo que no puede utilizarse como FASTA.

**EN:**
The path provided as the database does not exist or corresponds to a
file that cannot be used as a FASTA database.

### Resultado esperado / Expected Result

**ES:**
El backend debe rechazar la base de datos y la CLI debe informar el
error sin iniciar BLAST.

Cuando el error ocurre mediante la CLI, la ejecución debe finalizar con
un código de salida distinto de `0`.

**EN:**
The backend must reject the database and the CLI must report the error
without starting BLAST.

When the error occurs through the CLI, execution must terminate with a
non-zero exit code.

---

## CP-09 - Carpeta de bases FASTA vacía / Empty FASTA Database Directory

### Estado / Status

✅ Cubierto / Covered

### Funciones evaluadas / Functions Under Test

`detect_database_type()`

`list_blast_databases()`

### Condición de prueba / Test Condition

**ES:**
La herramienta recibe una carpeta existente que no contiene archivos
FASTA compatibles.

**EN:**
The tool receives an existing directory that contains no compatible
FASTA files.

### Resultado esperado / Expected Result

**ES:**
La herramienta debe rechazar la carpeta y no debe seleccionar ni
ejecutar ningún programa BLAST.

**EN:**
The tool must reject the directory and must not select or execute any
BLAST program.

---

## CP-10 - Bases de datos con tipos mezclados / Mixed Database Types

### Estado / Status

✅ Cubierto / Covered

### Funciones evaluadas / Functions Under Test

`detect_database_type()`

`list_blast_databases()`

### Condición de prueba / Test Condition

**ES:**
Una carpeta de bases contiene archivos FASTA nucleotídicos y proteicos
al mismo tiempo.

**EN:**
A database directory contains both nucleotide and protein FASTA files.

### Resultado esperado / Expected Result

**ES:**
La herramienta debe detectar que las bases no son homogéneas y rechazar
la entrada.

No debe ejecutarse BLAST.

**EN:**
The tool must detect that the databases are not homogeneous and reject
the input.

BLAST must not be executed.

---

## CP-11 - Parseo de salida BLAST outfmt 6 / BLAST outfmt 6 Parsing

### Estado / Status

✅ Cubierto / Covered

### Función evaluada / Function Under Test

`parse_blast_results()`

### Condición de prueba / Test Condition

**ES:**
La herramienta recibe resultados BLAST en formato tabular estándar
`outfmt 6`.

**EN:**
The tool receives BLAST results in standard tabular `outfmt 6` format.

### Resultado esperado / Expected Result

La tabla debe contener correctamente:

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

**ES:**
Cada alineamiento debe conservarse como una fila independiente.

**EN:**
Each alignment must be preserved as an independent row.

---

## CP-12 - Query sin resultados BLAST / Query Without BLAST Hits

### Estado / Status

✅ Cubierto / Covered

### Funciones evaluadas / Functions Under Test

`parse_blast_results()`

`fill_missing_hits()`

### Condición de prueba / Test Condition

**ES:**
Una de las secuencias de la query no obtiene ningún hit en una base de
datos.

**EN:**
One of the query sequences produces no hit in a database.

### Resultado esperado / Expected Result

**ES:**
La query debe conservarse en los resultados mediante una fila propia.

El identificador debe permanecer disponible y los campos del
alineamiento deben quedar vacíos.

**EN:**
The query must remain in the results as its own row.

Its identifier must remain available and alignment fields must be empty.

---

## CP-13 - Ejecución local de BLAST / Local BLAST Execution

### Estado / Status

✅ Cubierto / Covered

### Funciones evaluadas / Functions Under Test

`run_blast()`

`build_blast_command()`

### Condición de prueba / Test Condition

**ES:**
La herramienta recibe una query FASTA y una base FASTA compatibles y
ejecuta BLAST+ instalado localmente.

**EN:**
The tool receives compatible query and database FASTA files and runs
the locally installed BLAST+ program.

### Resultado esperado / Expected Result

**ES:**
Debe construirse y ejecutarse correctamente el comando BLAST
correspondiente.

Los resultados deben obtenerse en formato `outfmt 6` y procesarse sin
errores.

**EN:**
The corresponding BLAST command must be correctly built and executed.

Results must be obtained in `outfmt 6` format and processed without
errors.

---

## CP-14 - Carpeta con múltiples bases FASTA / Directory with Multiple FASTA Databases

### Estado / Status

✅ Cubierto / Covered

### Funciones evaluadas / Functions Under Test

`run_blast()`

`list_blast_databases()`

### Condición de prueba / Test Condition

**ES:**
La ruta de bases corresponde a una carpeta que contiene múltiples
archivos FASTA compatibles del mismo tipo.

**EN:**
The database path corresponds to a directory containing multiple
compatible FASTA files of the same type.

### Resultado esperado / Expected Result

**ES:**
Cada archivo FASTA debe procesarse como una base independiente.

Los resultados combinados deben conservar una etiqueta que permita
identificar qué especie o base produjo cada hit.

Cuando los encabezados FASTA contienen información de organismo en
formato NCBI, por ejemplo:

`[Cucumis melo]`

la herramienta debe utilizar el organismo detectado como etiqueta de
la base.

Si no puede inferirse un organismo a partir de los encabezados, debe
utilizarse como respaldo el nombre del archivo FASTA sin extensión.

Ejemplo:

`amborella.faa` → `amborella`

**EN:**
Each FASTA file must be processed as an independent database.

Combined results must preserve a label identifying which species or
database produced each hit.

When FASTA headers contain NCBI organism information, for example:

`[Cucumis melo]`

the detected organism must be used as the database label.

If an organism cannot be inferred from the headers, the FASTA filename
without its extension must be used as a fallback.

Example:

`amborella.faa` → `amborella`

---

## CP-15 - Parámetros personalizados de BLAST / Custom BLAST Parameters

### Estado / Status

✅ Cubierto / Covered

### Función evaluada / Function Under Test

`build_blast_command()`

### Condición de prueba / Test Condition

**ES:**
El usuario proporciona valores personalizados para los parámetros de
ejecución de BLAST.

Entre los parámetros disponibles se encuentran:

- `evalue`
- `max_target_seqs`
- `threads`

**EN:**
The user provides custom values for BLAST execution parameters.

Available parameters include:

- `evalue`
- `max_target_seqs`
- `threads`

### Resultado esperado / Expected Result

**ES:**
Los valores proporcionados deben incorporarse correctamente al comando
BLAST ejecutado.

**EN:**
The provided values must be correctly incorporated into the executed
BLAST command.

---

## CP-16 - Error durante la ejecución de BLAST / BLAST Execution Error

### Estado / Status

✅ Cubierto / Covered

### Funciones evaluadas / Functions Under Test

`run_blast()`

`_run_command()`

### Condición de prueba / Test Condition

**ES:**
BLAST+ no puede ejecutarse correctamente, ya sea porque el ejecutable
requerido no está disponible o porque BLAST rechaza los parámetros
proporcionados.

También se comprobaron manualmente valores inválidos como:

- `--max-target-seqs 0`
- `--threads 0`
- `--evalue 0`

**EN:**
BLAST+ cannot execute correctly, either because the required executable
is unavailable or because BLAST rejects the provided parameters.

Invalid values were also manually checked, including:

- `--max-target-seqs 0`
- `--threads 0`
- `--evalue 0`

### Resultado esperado / Expected Result

**ES:**
La herramienta debe detectar el fallo de BLAST, informar el error y no
continuar como si la ejecución hubiera sido exitosa.

Desde la CLI, el proceso debe finalizar con código de salida `1`.

**EN:**
The tool must detect the BLAST failure, report the error, and must not
continue as if execution had succeeded.

From the CLI, the process must terminate with exit code `1`.

---

## CP-17 - Normalización de accesiones / Accession Normalization

### Estado / Status

✅ Cubierto / Covered

### Función evaluada / Function Under Test

`normalize_accession()`

### Condición de prueba / Test Condition

**ES:**
La herramienta recibe identificadores de accesión con diferentes
formatos y prefijos.

Ejemplos:

- `ref|XP_001.1|`
- `XP_001`
- `sp|P12345|`

**EN:**
The tool receives accession identifiers using different formats and
prefixes.

### Resultado esperado / Expected Result

- `ref|XP_001.1|` → `XP_001.1`
- `XP_001` → `XP_001`
- `sp|P12345|` → `P12345`

**ES:**
La versión de la accesión debe conservarse cuando exista.

**EN:**
The accession version must be preserved when present.

---

## CP-18 - Carga de accesiones y descriptores / Accession and Descriptor Loading

### Estado / Status

✅ Cubierto / Covered

### Función evaluada / Function Under Test

`load_accessions()`

### Condición de prueba / Test Condition

**ES:**
La herramienta recibe un archivo tabulado con la estructura:

`accession<TAB>description`

**EN:**
The tool receives a tab-separated file with the structure:

`accession<TAB>description`

### Resultado esperado / Expected Result

**ES:**
La información debe cargarse correctamente y debe poder relacionarse
con las accesiones encontradas en los resultados BLAST.

La ausencia de una descripción asociada a un hit es válida y puede
representarse mediante `---`.

**EN:**
The information must be loaded correctly and must be available for
matching against accessions found in BLAST results.

The absence of a description associated with a hit is valid and may be
represented by `---`.

---

## CP-19 - Archivo de accesiones vacío o inexistente / Empty or Missing Accessions File

### Estado / Status

✅ Cubierto / Covered

### Funciones evaluadas / Functions Under Test

`load_accessions()`

`biocol run`

`biocol from-blast`

### Condición de prueba / Test Condition

**ES:**
El archivo de accesiones está vacío o la ruta proporcionada no existe.

**EN:**
The accessions file is empty or the provided path does not exist.

### Resultado esperado / Expected Result

**ES:**
Un archivo vacío debe ser rechazado por el backend.

Una ruta inexistente utilizada mediante la CLI debe generar un mensaje
de error y finalizar con código de salida `1`.

**EN:**
An empty file must be rejected by the backend.

A missing path used through the CLI must produce an error message and
terminate with exit code `1`.

---

## CP-20 - Construcción de tabla final / Final Results Table Construction

### Estado / Status

✅ Cubierto / Covered

### Función evaluada / Function Under Test

`build_result_table()`

### Condición de prueba / Test Condition

**ES:**
La herramienta recibe resultados BLAST y debe transformarlos en la tabla
final utilizada por el usuario.

**EN:**
The tool receives BLAST results and must transform them into the final
table used by the user.

### Resultado esperado / Expected Result

**ES:**
La tabla debe conservar la información de la query e incorporar un
bloque de resultados por cada base procesada.

Cada bloque debe incluir:

- accession
- description
- identity percentage
- alignment length
- evalue
- score

Cuando un valor no esté disponible, debe permanecer vacío o utilizar
`---` según corresponda.

**EN:**
The table must preserve query information and include one result block
for each processed database.

Each block must include:

- accession
- description
- identity percentage
- alignment length
- evalue
- score

When a value is unavailable, it must remain empty or use `---` as
appropriate.

---

## CP-21 - Metadatos de secuencia en la tabla final / Sequence Metadata in Final Table

### Estado / Status

✅ Cubierto / Covered

### Función evaluada / Function Under Test

`build_result_table()`

### Condición de prueba / Test Condition

**ES:**
La tabla final se construye utilizando el archivo FASTA original de la
query.

**EN:**
The final table is built using the original query FASTA file.
### Resultado esperado / Expected Result

**ES:**
Si únicamente se proporciona el FASTA utilizado como query, la herramienta
debe completar los campos correspondientes al tipo de secuencia disponible.

Para una query nucleotídica se completan:

- `gene_id`
- `length_nt`
- `cdna_sequence`

Para una query proteica se completan:

- `gene_id`
- `length_aa`
- `protein_sequence`

Cuando el usuario proporciona además archivos separados mediante
`--cdna` y `--protein`, la herramienta debe utilizar ambos para completar
la información nucleotídica y proteica del mismo modelo génico.

La asociación entre CDS y proteína debe poder realizarse utilizando los
identificadores presentes en encabezados NCBI, incluyendo etiquetas como
`[protein_id=...]`.

**EN:**
If only the FASTA used as the query is provided, the tool must populate
the fields corresponding to the available sequence type.

For a nucleotide query:

- `gene_id`
- `length_nt`
- `cdna_sequence`

For a protein query:

- `gene_id`
- `length_aa`
- `protein_sequence`

When separate files are additionally provided through `--cdna` and
`--protein`, the tool must use both to populate nucleotide and protein
information for the same gene model.

CDS and protein records must be matchable using identifiers present in
NCBI headers, including tags such as `[protein_id=...]`.

---

## CP-22 - Escritura del CSV final / Final CSV Writing

### Estado / Status

✅ Cubierto / Covered

### Función evaluada / Function Under Test

`write_results_csv()`

### Condición de prueba / Test Condition

**ES:**
La tabla final debe almacenarse como un archivo CSV.

**EN:**
The final results table must be stored as a CSV file.
### Resultado esperado / Expected Result

**ES:**
El archivo debe escribirse en formato CSV siguiendo la estructura tipo
Dataset S2.

El CSV debe contener tres filas de cabecera:

1. sección de anotación;
2. especie o base de datos;
3. nombre de cada columna.

Cada bloque BLAST debe incluir la sección:

`Annotation based on top-BLAST-hit method`

y los campos:

- `Accesion No.`
- `Description`
- `Identity %`
- `Alignment length`
- `e-value`
- `Score`

Las columnas de información de query que estén completamente vacías no
deben escribirse en el CSV.

Por ejemplo, si solamente existe una query proteica, no deben aparecer
`Length (nt)` ni `cDNA Sequences (nt)`.

Cuando no se proporcione una ruta de salida debe utilizarse
`results.csv` como nombre predeterminado.

**EN:**
The file must be written as CSV using the Dataset S2-style structure.

The CSV must contain three header rows:

1. annotation section;
2. species or database;
3. column names.

Each BLAST block must include the section:

`Annotation based on top-BLAST-hit method`

and the fields:

- `Accesion No.`
- `Description`
- `Identity %`
- `Alignment length`
- `e-value`
- `Score`

Query information columns that contain no values must not be written
to the CSV.

For example, when only a protein query is available, `Length (nt)` and
`cDNA Sequences (nt)` must not appear.

When no output path is provided, `results.csv` must be used as the
default filename.

---

## CP-23 - Flujo completo biocol run / Complete biocol run Workflow

### Estado / Status

✅ Cubierto / Covered

### Tipo de prueba / Test Type

Integración / Integration

### Funciones evaluadas / Functions Under Test

`biocol run`

`run_blast()`

`build_result_table()`

`write_results_csv()`

### Condición de prueba / Test Condition

**ES:**
El usuario proporciona:

- una query FASTA;
- una base FASTA o carpeta de bases;
- un archivo de accesiones;
- opcionalmente una ruta de salida.

La herramienta debe ejecutar todo el flujo automáticamente.

También se realizó una prueba manual con datos biológicos reales de
*Benincasa hispida* y *Cucumis melo*.

El comando también puede recibir opcionalmente:

- `--cdna`: FASTA de secuencias cDNA;
- `--protein`: FASTA de secuencias proteicas.

Cuando ambos están disponibles, la herramienta debe utilizarlos para
completar las columnas nucleotídicas y proteicas del bloque de query.

**EN:**
The user provides:

- a FASTA query;
- a FASTA database or database directory;
- an accessions file;
- optionally an output path.

The tool must automatically execute the complete workflow.

A manual test was also performed using real biological data from
*Benincasa hispida* and *Cucumis melo*.

The command may also optionally receive:

- `--cdna`: cDNA FASTA;
- `--protein`: protein FASTA.

When both are available, the tool must use them to populate both
nucleotide and protein query columns.

### Resultado esperado / Expected Result

**ES:**
La ejecución debe completar correctamente:

1. lectura y validación de la query;
2. detección del tipo de secuencia;
3. detección de las bases;
4. selección del programa BLAST;
5. ejecución de BLAST+;
6. parseo de resultados;
7. asociación de accesiones/descriptores;
8. construcción de la tabla;
9. escritura del CSV.

La prueba con datos reales generó correctamente un archivo CSV de
resultados.

**EN:**
Execution must correctly complete:

1. query reading and validation;
2. sequence type detection;
3. database detection;
4. BLAST program selection;
5. BLAST+ execution;
6. result parsing;
7. accession/descriptor matching;
8. table construction;
9. CSV writing.

The test using real biological data successfully generated a results
CSV file.

---

## CP-24 - Flujo completo biocol from-blast / Complete biocol from-blast Workflow

### Estado / Status

✅ Cubierto / Covered

### Tipo de prueba / Test Type

Integración / Integration

### Funciones evaluadas / Functions Under Test

`biocol from-blast`

`parse_blast_results()`

`build_result_table()`

`write_results_csv()`

### Condición de prueba / Test Condition

**ES:**
El usuario ya dispone de un archivo BLAST tabular `outfmt 6` y un
archivo de accesiones.

No se proporciona el FASTA original de la query y BLAST+ no debe
ejecutarse nuevamente.

**EN:**
The user already has a tabular BLAST `outfmt 6` file and an accessions
file.

The original query FASTA is not provided and BLAST+ must not be executed
again.

### Resultado esperado / Expected Result

**ES:**
El comando debe procesar directamente el resultado BLAST y generar el
CSV final.

`gene_id` debe obtenerse de `qseqid`.

Debido a que no existe FASTA de query, deben permanecer vacíos:

- `length_nt`
- `cdna_sequence`
- `length_aa`
- `protein_sequence`

Los datos correspondientes a los hits BLAST deben conservarse.

**EN:**
The command must directly process the BLAST results and generate the
final CSV.

`gene_id` must be obtained from `qseqid`.

Because no query FASTA is available, the following fields must remain
empty:

- `length_nt`
- `cdna_sequence`
- `length_aa`
- `protein_sequence`

BLAST hit information must be preserved.

---

## CP-25 - Validación y manejo de errores de la CLI / CLI Validation and Error Handling

### Estado / Status

✅ Cubierto / Covered

### Tipo de prueba / Test Type

Integración manual / Manual Integration

### Funciones evaluadas / Functions Under Test

`biocol run`

`biocol from-blast`

### Condiciones probadas / Tested Conditions

**ES:**
Se verificó el comportamiento de la CLI ante entradas incorrectas,
incluyendo:

- query inexistente en `biocol run`;
- base de datos inexistente en `biocol run`;
- archivo de accesiones inexistente;
- archivo BLAST inexistente en `biocol from-blast`;
- argumentos obligatorios faltantes.

**EN:**
CLI behavior was verified with invalid inputs, including:

- missing query in `biocol run`;
- missing database in `biocol run`;
- missing accessions file;
- missing BLAST file in `biocol from-blast`;
- missing required arguments.

### Resultado esperado / Expected Result

**ES:**
La herramienta debe mostrar un mensaje de error comprensible y evitar
que el procesamiento continúe.

Los errores detectados durante el procesamiento deben finalizar con un
código de salida distinto de `0`.

Cuando `argparse` detecta argumentos obligatorios faltantes, la
ejecución finaliza con código `2`.

Los errores de archivos inexistentes o fallos controlados durante el
procesamiento finalizan con código `1`.

**EN:**
The tool must display an understandable error message and prevent
processing from continuing.

Errors detected during processing must terminate with a non-zero exit
code.

When `argparse` detects missing required arguments, execution terminates
with exit code `2`.

Missing files and controlled processing failures terminate with exit
code `1`.

---

# Resumen de cobertura / Coverage Summary

Los casos de prueba documentados cubren los principales componentes
desarrollados durante HU-01:

- lectura y validación de archivos FASTA;
- archivos FASTA y multiFASTA;
- identificación de secuencias nucleotídicas y proteicas;
- detección y validación de bases de datos;
- selección automática de `blastn`, `blastp`, `blastx`, `tblastn` y
  `tblastx`;
- ejecución local de BLAST+;
- procesamiento de una o múltiples bases FASTA;
- parseo de resultados BLAST `outfmt 6`;
- conservación de queries sin hits;
- parámetros configurables de BLAST;
- manejo de errores de ejecución de BLAST;
- normalización y carga de accesiones;
- asociación opcional de descriptores;
- construcción de la tabla final;
- incorporación de información de la secuencia query;
- generación del archivo CSV;
- flujo completo mediante `biocol run`;
- flujo alternativo mediante `biocol from-blast`;
- manejo de errores desde la interfaz de línea de comandos.

La suite automatizada actual se ejecutó correctamente con:

`57 passed`

Además de las pruebas automatizadas, se realizaron pruebas manuales de
integración mediante la CLI y una ejecución con archivos biológicos
reales.

---

The documented test cases cover the main components developed during
HU-01:

- FASTA reading and validation;
- FASTA and multiFASTA files;
- nucleotide and protein sequence identification;
- database detection and validation;
- automatic selection of `blastn`, `blastp`, `blastx`, `tblastn`, and
  `tblastx`;
- local BLAST+ execution;
- processing of one or multiple FASTA databases;
- BLAST `outfmt 6` result parsing;
- preservation of queries without hits;
- configurable BLAST parameters;
- BLAST execution error handling;
- accession normalization and loading;
- optional descriptor association;
- final results table construction;
- query sequence metadata integration;
- CSV generation;
- complete workflow through `biocol run`;
- alternative workflow through `biocol from-blast`;
- command-line error handling.

The current automated test suite completed successfully with:

`57 passed`

In addition to automated tests, manual CLI integration tests and an
execution using real biological files were performed.
