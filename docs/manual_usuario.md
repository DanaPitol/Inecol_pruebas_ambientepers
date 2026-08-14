# Manual de usuario / User Manual

## 1. Descripción / Description

**ES**

`biocol` es una herramienta de línea de comandos orientada al análisis
y procesamiento de secuencias biológicas mediante BLAST y DIAMOND.

La herramienta permitirá recibir secuencias de interés en formato FASTA
o multiFASTA, contrastarlas con bases de datos de referencia y procesar
los resultados obtenidos para generar una tabla unificada con la
información de anotación requerida.

Para el MVP se consideran las anotaciones asociadas a la secuencia de
interés y a los contrastes con otras especies. Las anotaciones de Pfam,
GO y KEGG no se consideran en esta etapa.

---

**EN**

`biocol` is a command-line tool designed for the analysis and processing
of biological sequences using BLAST and DIAMOND.

The tool will receive sequences of interest in FASTA or multiFASTA
format, compare them against reference databases, and process the
obtained results to generate a unified table containing the required
annotation information.

For the MVP, annotations associated with the sequence of interest and
comparisons with other species are considered. Pfam, GO, and KEGG
annotations are not included at this stage.

## 2. Sintaxis general / General Syntax

**ES**

La sintaxis definitiva de ejecución se encuentra en desarrollo y será
definida mediante la interfaz de línea de comandos (CLI).

Las opciones y argumentos documentados en esta sección se actualizarán
conforme se integren las funciones públicas del backend con la CLI.

---

**EN**

The final execution syntax is currently under development and will be
defined through the command-line interface (CLI).

The options and arguments documented in this section will be updated
as the backend public functions are integrated with the CLI.

## 3. Archivos de entrada / Input Files

### 3.1 FASTA

**ES**

La herramienta utiliza archivos en formato FASTA para representar
secuencias biológicas.

Cada registro FASTA está compuesto por un encabezado y una secuencia.

El encabezado comienza obligatoriamente con el símbolo `>` seguido
del identificador de la secuencia. Después del identificador puede
incluirse un descriptor o descripción con información adicional
sobre la secuencia.

Ejemplo:

    >XP_002862155.2 protochlorophyllide reductase A, chloroplastic [Arabidopsis lyrata subsp. lyrata]
    MACRDFLKAERAAQSAGMPKDSYTVMHLDLASLDSVRQFVDNFRRAEMPLDVLVCNAAVYQPTANQPTFTAEGFELS

La secuencia puede representar nucleótidos o aminoácidos, dependiendo
del análisis que se vaya a realizar.

Las extensiones FASTA aceptadas actualmente por la herramienta son:

- `.fa`
- `.fasta`
- `.fna`
- `.faa`
- `.fas`

La herramienta debe identificar correctamente cada registro FASTA
antes de iniciar el procesamiento.

**EN**

The tool uses FASTA files to represent biological sequences.

Each FASTA record consists of a header and a sequence.

The header must begin with the `>` symbol followed by the sequence
identifier. A descriptor or description containing additional
information about the sequence may appear after the identifier.

Example:

    >XP_002862155.2 protochlorophyllide reductase A, chloroplastic [Arabidopsis lyrata subsp. lyrata]
    MACRDFLKAERAAQSAGMPKDSYTVMHLDLASLDSVRQFVDNFRRAEMPLDVLVCNAAVYQPTANQPTFTAEGFELS

The sequence may represent nucleotides or amino acids depending on
the analysis to be performed.

The FASTA file extensions currently accepted by the tool are:

- `.fa`
- `.fasta`
- `.fna`
- `.faa`
- `.fas`

The tool must correctly identify each FASTA record before processing
begins.

---

### 3.2 multiFASTA

**ES**

Un archivo multiFASTA contiene múltiples registros FASTA dentro
del mismo archivo.

Cada nueva secuencia comienza cuando se encuentra un nuevo encabezado
identificado por el símbolo `>`.

Ejemplo:

    >seq1
    MKTLLVAGTALAGCSTLAA

    >seq2
    MAVKIGINGFGRHPE

Una secuencia no necesariamente debe encontrarse escrita en una
sola línea. Puede estar distribuida en múltiples líneas:

    >seq1
    MKTLLV
    AGTALA
    GCSTLAA

Todas las líneas de secuencia encontradas después de un encabezado
pertenecen al mismo registro hasta que se encuentra un nuevo
encabezado que comienza con `>`.

Por lo tanto, el ejemplo anterior representa la secuencia:

    MKTLLVAGTALAGCSTLAA

y no tres secuencias diferentes.

**EN**

A multiFASTA file contains multiple FASTA records within the same
file.

Each new sequence begins when a new header identified by the `>`
symbol is found.

Example:

    >seq1
    MKTLLVAGTALAGCSTLAA

    >seq2
    MAVKIGINGFGRHPE

A sequence does not necessarily have to be written on a single line.
It may be distributed across multiple lines:

    >seq1
    MKTLLV
    AGTALA
    GCSTLAA

All sequence lines following a header belong to the same record until
a new header beginning with `>` is found.

Therefore, the previous example represents the sequence:

    MKTLLVAGTALAGCSTLAA

and not three different sequences.

---

### 3.3 Base de datos de referencia / Reference Database

> **Estado actual / Current status:** ⏳ En desarrollo / In development
>
> La detección, validación y preparación de la base de datos todavía no
> están implementadas en el backend.
>
> Database detection, validation, and preparation have not yet been
> implemented in the backend.

**ES**

Además del archivo que contiene las secuencias de interés (query),
la herramienta requiere una base de datos de referencia contra la
cual se realizará la comparación.

La base de datos contiene secuencias cuya información puede ser
utilizada para contrastar las secuencias de interés.

Para realizar una búsqueda con BLAST, las secuencias de referencia
deben prepararse como una base de datos compatible con BLAST.

Cuando se utiliza BLAST, este proceso puede realizarse mediante
`makeblastdb`.

La selección del programa BLAST dependerá del tipo de secuencia de
interés y del tipo de secuencias presentes en la base de datos.

**EN**

In addition to the file containing the sequences of interest (query),
the tool requires a reference database against which the comparison
will be performed.

The database contains sequences whose information can be used to
compare the sequences of interest.

To perform a BLAST search, the reference sequences must be prepared
as a BLAST-compatible database.

When BLAST is used, this process can be performed using
`makeblastdb`.

The BLAST program selected will depend on the type of query sequence
and the type of sequences contained in the reference database.

## 4. Ejecución de búsquedas / Search Execution

### 4.1 BLAST

> **Estado actual / Current status:** ⏳ En desarrollo / In development
>
> La selección automática del programa BLAST, la preparación de la base
> de datos y la ejecución de BLAST todavía no están implementadas en el
> backend. Esta sección documenta el flujo previsto para el MVP.
>
> Automatic BLAST program selection, database preparation, and BLAST
> execution have not yet been implemented in the backend. This section
> documents the workflow planned for the MVP.

**ES**

BLAST (Basic Local Alignment Search Tool) permite comparar una
secuencia de interés (query) contra un conjunto de secuencias de
referencia.

La búsqueda permite identificar regiones de similitud entre las
secuencias. El programa BLAST utilizado depende del tipo de secuencia
de la query y del tipo de secuencias almacenadas en la base de datos.

| Query | Base de datos | Programa |
|---|---|---|
| Nucleótidos | Nucleótidos | `blastn` |
| Proteínas | Proteínas | `blastp` |
| Nucleótidos | Proteínas | `blastx` |
| Proteínas | Nucleótidos | `tblastn` |

#### Preparación de la base de datos

Antes de realizar una búsqueda con BLAST, las secuencias de referencia
deben estar disponibles en una base de datos compatible con BLAST.

BLAST proporciona la herramienta `makeblastdb` para realizar este
proceso.

Ejemplo para una base de datos de proteínas:

    makeblastdb -in database.faa -dbtype prot -out database

Donde:

- `-in` indica el archivo de entrada que contiene las secuencias.
- `-dbtype` indica el tipo de secuencia de la base de datos.
- `prot` indica que se trata de secuencias de proteínas.
- `-out` establece el nombre de la base de datos generada.

`makeblastdb` genera archivos adicionales utilizados internamente
por BLAST para realizar las búsquedas.

#### Ejecución de BLAST

Por ejemplo, cuando tanto la query como la base de datos contienen
secuencias de proteínas, se utiliza `blastp`.

Ejemplo:

    blastp \
        -query query.faa \
        -db database \
        -out results.tsv \
        -outfmt 6

Donde:

- `-query` especifica el archivo FASTA/multiFASTA con las secuencias
  de interés.
- `-db` especifica la base de datos contra la cual se realizará
  la búsqueda.
- `-out` especifica el archivo donde se almacenarán los resultados.
- `-outfmt 6` solicita la salida de BLAST en formato tabular.

Para el MVP, los resultados de BLAST que serán procesados por la
herramienta se consideran en formato tabular (`outfmt 6`).

---

**EN**

BLAST (Basic Local Alignment Search Tool) compares a sequence of
interest (query) against a set of reference sequences.

The search identifies regions of similarity between sequences.
The BLAST program used depends on the type of query sequence and
the type of sequences contained in the reference database.

| Query | Database | Program |
|---|---|---|
| Nucleotide | Nucleotide | `blastn` |
| Protein | Protein | `blastp` |
| Nucleotide | Protein | `blastx` |
| Protein | Nucleotide | `tblastn` |

#### Database preparation

Before performing a BLAST search, the reference sequences must be
available as a BLAST-compatible database.

BLAST provides the `makeblastdb` tool for this process.

Example for a protein database:

    makeblastdb -in database.faa -dbtype prot -out database

Where:

- `-in` specifies the input sequence file.
- `-dbtype` specifies the type of sequences in the database.
- `prot` indicates protein sequences.
- `-out` specifies the name of the generated database.

`makeblastdb` generates additional files that BLAST uses internally
to perform searches.

#### Running BLAST

For example, when both the query and database contain protein
sequences, `blastp` is used.

Example:

    blastp \
        -query query.faa \
        -db database \
        -out results.tsv \
        -outfmt 6

Where:

- `-query` specifies the FASTA/multiFASTA file containing the
  sequences of interest.
- `-db` specifies the database used for the search.
- `-out` specifies the output file.
- `-outfmt 6` requests BLAST tabular output.

For the MVP, BLAST results processed by the tool are considered
in tabular format (`outfmt 6`).
### 4.2 DIAMOND

> **Estado actual / Current status:** ⏳ En desarrollo / In development

**ES**

DIAMOND es una herramienta de alineamiento de secuencias que puede
utilizarse como alternativa a BLAST para realizar búsquedas de
secuencias de proteínas.

Su propósito dentro del flujo de trabajo es realizar comparaciones
similares a las de BLAST, utilizando un algoritmo optimizado para
acelerar las búsquedas.

La integración y ejecución de DIAMOND todavía no están implementadas
en el backend. Los comandos y parámetros específicos se documentarán
cuando esta funcionalidad sea incorporada al MVP.

---

**EN**

DIAMOND is a sequence alignment tool that can be used as an alternative
to BLAST for protein sequence searches.

Its purpose within the workflow is to perform comparisons similar to
BLAST using an optimized algorithm to speed up searches.

DIAMOND integration and execution have not yet been implemented in the
backend. Specific commands and parameters will be documented when this
functionality is incorporated into the MVP.

## 5. Parámetros / Parameters

> **Estado actual / Current status:** ⏳ En desarrollo / In development

Los parámetros definitivos de ejecución se establecerán cuando la
ejecución de BLAST y la interfaz de línea de comandos (CLI) se
encuentren integradas.

The final execution parameters will be established when BLAST execution
and the command-line interface (CLI) are integrated.

### 5.1 E-value

**ES**

El E-value (valor de expectancia) es un parámetro utilizado por BLAST
para estimar la probabilidad de que una coincidencia entre secuencias
pueda ocurrir por azar.

Valores de E-value más pequeños representan coincidencias con menor
probabilidad de haberse producido de manera aleatoria.

Este parámetro será configurable por el usuario. La herramienta deberá
proporcionar un valor por defecto, pero el usuario podrá modificarlo
cuando requiera realizar una búsqueda más o menos restrictiva.

El valor por defecto definitivo y la opción correspondiente de la CLI
se documentarán cuando se implemente la ejecución de BLAST.

---

**EN**

The E-value (expectation value) is a parameter used by BLAST to
estimate the probability that a sequence match could occur by chance.

Smaller E-values represent matches with a lower probability of
occurring randomly.

This parameter will be configurable by the user. The tool will provide
a default value, but the user will be able to modify it when a more or
less restrictive search is required.

The final default value and corresponding CLI option will be documented
when BLAST execution is implemented.


### 5.2 Número de núcleos / Threads

**ES**

BLAST permite utilizar varios núcleos de procesamiento para ejecutar
las búsquedas de forma paralela.

La herramienta permitirá configurar el número de núcleos utilizados
durante la ejecución de BLAST.

La cantidad seleccionada deberá considerar los recursos
computacionales disponibles en el sistema donde se ejecute el análisis.

La opción definitiva de la CLI y su valor por defecto se documentarán
cuando la ejecución de BLAST sea implementada.

---

**EN**

BLAST can use multiple processing cores to perform searches in
parallel.

The tool will allow the number of cores used during BLAST execution
to be configured.

The selected number should consider the computational resources
available on the system where the analysis is executed.

The final CLI option and its default value will be documented when
BLAST execution is implemented.


### 5.3 Formato de salida / Output Format

**ES**

BLAST permite generar resultados en diferentes formatos mediante el
parámetro `outfmt`.

Para el MVP, la herramienta procesará resultados de BLAST en formato
tabular (`outfmt 6`), ya que este formato facilita la lectura y el
procesamiento automático de los alineamientos.

Las columnas específicas utilizadas por `biocol` se definirán durante
la implementación del procesamiento de resultados.

---

**EN**

BLAST can generate results in different formats using the `outfmt`
parameter.

For the MVP, the tool will process BLAST results in tabular format
(`outfmt 6`), since this format facilitates automatic reading and
processing of alignments.

The specific columns used by `biocol` will be defined during the
implementation of result processing.


## 6. Procesamiento de resultados / Result Processing

> **Estado actual / Current status:** ⏳ En desarrollo / In development

**ES**

El procesamiento de los resultados generados por BLAST todavía no está
implementado en el backend. Las siguientes secciones documentan el
comportamiento previsto para el MVP.

**EN**

Processing of the results generated by BLAST has not yet been
implemented in the backend. The following sections document the
behavior planned for the MVP.


### 6.1 Salida tabular de BLAST / BLAST Tabular Output

**ES**

Para el MVP, la herramienta procesará resultados de BLAST en formato
tabular (`outfmt 6`).

Este formato presenta cada alineamiento encontrado por BLAST como una
fila y utiliza, por defecto, 12 campos:

| Campo | Nombre | Descripción |
|---|---|---|
| `qseqid` | Query ID | Identificador de la secuencia de interés. |
| `sseqid` | Subject ID | Identificador de la secuencia encontrada en la base de datos. |
| `pident` | % Identity | Porcentaje de posiciones idénticas entre ambas secuencias. |
| `length` | Alignment length | Longitud del alineamiento. |
| `mismatch` | Mismatches | Número de posiciones diferentes en el alineamiento. |
| `gapopen` | Gap openings | Número de aperturas de gaps introducidas durante el alineamiento. |
| `qstart` | Query start | Posición donde comienza el alineamiento en la query. |
| `qend` | Query end | Posición donde termina el alineamiento en la query. |
| `sstart` | Subject start | Posición donde comienza el alineamiento en el subject. |
| `send` | Subject end | Posición donde termina el alineamiento en el subject. |
| `evalue` | E-value | Valor estadístico asociado a la significancia del alineamiento. |
| `bitscore` | Bit score | Puntuación normalizada del alineamiento. |

Ejemplo:

    query_01    protein_125    85.42    307    38    2    1    305    4    308    2.14e-92    279

En este ejemplo:

- `query_01` es la secuencia de interés.
- `protein_125` es la secuencia encontrada en la base de datos.
- La identidad entre ambas secuencias es de `85.42 %`.
- El alineamiento tiene una longitud de `307`.
- El E-value es `2.14e-92`.
- El bit score es `279`.

Un mismo par query-subject puede presentar más de un HSP
(High-scoring Segment Pair), debido a que pueden existir diferentes
regiones de alineamiento entre las mismas secuencias.

Estos registros no deben considerarse automáticamente como datos
duplicados, ya que pueden representar regiones de alineamiento
diferentes.

---

**EN**

For the MVP, the tool will process BLAST results in tabular format
(`outfmt 6`).

This format represents each alignment found by BLAST as a row and,
by default, contains 12 fields:

| Field | Name | Description |
|---|---|---|
| `qseqid` | Query ID | Identifier of the sequence of interest. |
| `sseqid` | Subject ID | Identifier of the sequence found in the database. |
| `pident` | % Identity | Percentage of identical positions between both sequences. |
| `length` | Alignment length | Length of the alignment. |
| `mismatch` | Mismatches | Number of different positions in the alignment. |
| `gapopen` | Gap openings | Number of gap openings introduced during alignment. |
| `qstart` | Query start | Position where the alignment starts in the query. |
| `qend` | Query end | Position where the alignment ends in the query. |
| `sstart` | Subject start | Position where the alignment starts in the subject. |
| `send` | Subject end | Position where the alignment ends in the subject. |
| `evalue` | E-value | Statistical value associated with alignment significance. |
| `bitscore` | Bit score | Normalized alignment score. |

Example:

    query_01    protein_125    85.42    307    38    2    1    305    4    308    2.14e-92    279

In this example:

- `query_01` is the sequence of interest.
- `protein_125` is the sequence found in the database.
- Sequence identity is `85.42 %`.
- The alignment length is `307`.
- The E-value is `2.14e-92`.
- The bit score is `279`.

The same query-subject pair may contain more than one HSP
(High-scoring Segment Pair) because different regions of the same
sequences may align.

These records should not automatically be considered duplicates,
because they may represent different alignment regions.


### 6.2 Selección del mejor HSP / Best HSP Selection

**ES**

Una misma secuencia de interés puede presentar más de un HSP con una
misma secuencia de referencia.

Durante el procesamiento será necesario definir cómo se manejarán
estos múltiples alineamientos.

La regla definitiva para seleccionar, conservar o combinar los HSP
todavía debe definirse antes de su implementación en el backend.

---

**EN**

A query sequence may contain more than one HSP with the same reference
sequence.

During result processing, it will be necessary to define how these
multiple alignments will be handled.

The final rule for selecting, retaining, or combining HSPs must still
be defined before its implementation in the backend.


### 6.3 Descriptores / Descriptors

**ES**

Los identificadores obtenidos en los resultados de alineamiento se
utilizarán para asociar las secuencias encontradas con la información
descriptiva disponible en las bases de datos de referencia.

El objetivo es incorporar esta información al resultado final para
facilitar la interpretación de las posibles funciones asociadas con
cada secuencia de interés.

La estructura y homologación definitiva de los descriptores todavía
se encuentran en desarrollo.

---

**EN**

Identifiers obtained from alignment results will be used to associate
matched sequences with descriptive information available in the
reference databases.

The objective is to incorporate this information into the final result
to facilitate interpretation of the possible functions associated with
each query sequence.

The final structure and standardization of descriptors are still under
development.


## 7. Archivos de salida / Output Files

> **Estado actual / Current status:** ⏳ En desarrollo / In development

### 7.1 Formato tabular / Tabular Format

**ES**

Los resultados obtenidos durante el análisis serán organizados en una
estructura tabular para facilitar su procesamiento, comparación y
posterior exportación.

Cada fila representará información asociada con una secuencia o
resultado procesado y las columnas corresponderán a los campos de
anotación definidos para el MVP.

La estructura definitiva se establecerá durante la implementación del
parseo y procesamiento de resultados.

---

**EN**

Results obtained during the analysis will be organized in a tabular
structure to facilitate processing, comparison, and subsequent export.

Each row will represent information associated with a sequence or
processed result, while the columns will correspond to the annotation
fields defined for the MVP.

The final structure will be established during implementation of result
parsing and processing.


### 7.2 CSV

**ES**

El resultado final del MVP será exportado como un archivo CSV plano.

Este archivo integrará la información procesada de los resultados de
BLAST y las columnas de anotación definidas para esta etapa del
proyecto.

Las anotaciones de Pfam, KEGG y GO no forman parte del CSV final del
MVP actual.

---

**EN**

The final MVP result will be exported as a plain CSV file.

This file will integrate the processed BLAST results and the annotation
columns defined for this stage of the project.

Pfam, KEGG, and GO annotations are not part of the final CSV for the
current MVP.


## 8. Manejo de errores / Error Handling

**ES**

La herramienta debe detectar condiciones que impidan continuar con el
procesamiento y proporcionar mensajes de error comprensibles.

Actualmente, el backend permite detectar casos relacionados con la
lectura y validación de archivos FASTA, entre ellos:

- ruta de archivo inexistente;
- extensión FASTA no soportada;
- archivo FASTA vacío o sin secuencias;
- contenido que no puede interpretarse correctamente como FASTA;
- secuencias vacías;
- caracteres de secuencia no válidos;
- archivos multiFASTA con tipos de secuencia incompatibles.

La validación relacionada con bases de datos, ejecución de BLAST y
procesamiento de resultados se incorporará conforme se implementen
esas funcionalidades.

La presentación definitiva de los errores mediante STDERR y los
códigos de salida se definirá con la integración de la CLI.

---

**EN**

The tool must detect conditions that prevent processing from continuing
and provide understandable error messages.

The backend can currently detect cases related to FASTA reading and
validation, including:

- missing file path;
- unsupported FASTA extension;
- empty FASTA file or file without sequences;
- content that cannot be correctly interpreted as FASTA;
- empty sequences;
- invalid sequence characters;
- multiFASTA files containing incompatible sequence types.

Validation related to databases, BLAST execution, and result processing
will be incorporated as those features are implemented.

The final presentation of errors through STDERR and the corresponding
exit codes will be defined when the CLI is integrated.


## 9. Ayuda / Help

> **Estado actual / Current status:** ⏳ Pendiente de integración con la CLI /
> Pending CLI integration

**ES**

La interfaz de línea de comandos deberá proporcionar una opción de
ayuda para consultar la sintaxis, argumentos y parámetros disponibles.

Se contempla el uso convencional de:

    -h
    --help

La información definitiva mostrada por estas opciones dependerá de la
implementación final de la CLI.

---

**EN**

The command-line interface should provide a help option for consulting
the available syntax, arguments, and parameters.

The conventional options considered are:

    -h
    --help

The final information displayed by these options will depend on the
final CLI implementation.


## 10. Ejemplos / Examples

> **Estado actual / Current status:** ⏳ Pendiente de integración /
> Pending integration

**ES**

Los ejemplos completos de uso de `biocol` se incorporarán cuando la
interfaz de línea de comandos, la ejecución de BLAST y el procesamiento
de resultados se encuentren integrados.

Por el momento, los ejemplos incluidos en las secciones anteriores
documentan el formato de los archivos y el flujo previsto para el MVP.

---

**EN**

Complete `biocol` usage examples will be incorporated when the
command-line interface, BLAST execution, and result processing are
integrated.

For now, the examples included in the previous sections document the
file formats and workflow planned for the MVP.

