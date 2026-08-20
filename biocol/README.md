# biocol

Backend de la herramienta BLAST de INECOL. Toma una query FASTA (o un BLAST tabular ya existente), la compara contra bases FASTA locales y escribe un **CSV plano** de anotación.


## Requisitos

- Python 3.10+
- BLAST+ en el PATH (`conda activate inecol` en Ubuntu/WSL)
- Dependencias: Biopython y pandas

```bash
cd biocol
pip install -e ".[dev]"
```

`-e` instala el paquete en modo editable: los cambios del backend se ven sin reinstalar.

## Entradas

| Entrada | Formato |
|---------|---------|
| Query | FASTA / multifasta: `.fa`, `.fasta`, `.fna`, `.faa`, `.fas`. Todo el archivo debe ser del mismo tipo (ADN, ARN o proteína). `U` cuenta como nucleótido. |
| Bases | Un FASTA o una **carpeta** (incluye subcarpetas). Mismas extensiones. Todas las bases del mismo tipo. Un BLAST por archivo FASTA. |
| Accesiones | Texto `accession<TAB>descriptor`, sin encabezado. |
| BLAST tabular (camino 2) | `outfmt 6` estándar (12 columnas NCBI). |

Parámetros de BLAST (modificables): `evalue` default **10**, `max_target_seqs` default **3**.

## Cómo se elige el programa BLAST

`run_blast` detecta el tipo de la query y de las bases y llama a `select_blast_program`. Si **ambos** son nucleótido, el default es **blastn**. `translated=True` (flag CLI `--tblastx`) elige **tblastx**. En las demás combinaciones `translated` se ignora.

| Query | Base de datos | `translated` | Programa | Qué compara |
|-------|---------------|--------------|----------|-------------|
| Nucleótido | Nucleótido | no se pasa / `False` (default) | `blastn` | Nucleótido contra nucleótido |
| Nucleótido | Nucleótido | `True` (explícito) | `tblastx` | Query y base traducidas en seis marcos (proteína) |
| Nucleótido | Proteína | se ignora | `blastx` | Query nucleotídica traducida contra proteínas |
| Proteína | Proteína | se ignora | `blastp` | Proteína contra proteína |
| Proteína | Nucleótido | se ignora | `tblastn` | Proteína contra traducciones de la base nucleotídica |

## Uso

Hay dos caminos al mismo CSV.

### Camino 1 — FASTA + bases

```python
from biocol import run_blast, build_result_table, write_results_csv

hits = run_blast(
    "query.fa",
    "bases/",                 # un FASTA o carpeta
    translated=False,         # True → tblastx si query y base son nucleótido
    evalue=10,
    max_target_seqs=3,
)
table = build_result_table(hits, "accessions.txt", query_fasta="query.fa")
write_results_csv(table, "results.csv")  # si se omite, usa results.csv
```

`run_blast` crea bases temporales con `makeblastdb`, lanza un BLAST por FASTA y parsea `outfmt 6`. Si una query no tiene hit en una base, queda una fila vacía.

### Camino 2 — BLAST tabular ya existente

Sin FASTA de query: se rellenan `qseqid` + hits + descriptores; las columnas de secuencia quedan vacías.

```python
from biocol import parse_blast_results, build_result_table, write_results_csv

hits = parse_blast_results("blast_outfmt6.txt")
table = build_result_table(hits, "accessions.txt", query_fasta=None)
write_results_csv(table)
```

Si el tabular no trae columna `database`, se usa el nombre `hit`.

### CLI

After `pip install -e ".[dev]"`:

```bash
biocol --help
biocol run --help
biocol from-blast --help

biocol run --query query.fa --db bases/ --accessions accessions.txt
biocol run --query query.fa --db bases/ --accessions accessions.txt --tblastx --evalue 1e-5 --max-target-seqs 50 --threads 4 --output my_results.csv
biocol run --query genes.faa --db bases/ --accessions accessions.txt --cdna genes.fna --protein genes.faa

biocol from-blast --blast hits.txt --accessions Benincasa_hispida_gd.txt
biocol from-blast --blast hits.txt --accessions Benincasa_hispida_gd.txt --output my_results.csv
```

`--output` is optional (default: `results.csv`). Help, errors, and status lines are in English. Colors are on in an interactive terminal; disable with `--no-color` or `NO_COLOR=1`.

`from-blast` does not take a query FASTA. The species name in the CSV header is the accessions file stem (`Benincasa_hispida_gd.txt` → `Benincasa hispida gd`). `--accessions` describes **subject** IDs from `--db`, not the query.

## CSV de salida

CSV con **tres filas de cabecera**, como Dataset S2 (sin Pfam, KEGG ni GO). No hay celdas combinadas: el nombre de sección y el de la especie se repiten o quedan en la primera columna de cada bloque.

1. Sección: vacío en query; `Annotation based on top-BLAST-hit method` en cada bloque BLAST.
2. Especie: `stem` del FASTA de base (p. ej. `protein`, `amborella`).
3. Nombres de columna: `Gene ID`, `Length (nt)`, `cDNA Sequences (nt)`, `Length(aa)`, `Protein Sequences (aa)`, y por especie `Accesion No.`, `Description`, `Identity %`, `Alignment length`, `e-value`, `Score`.

No se incluyen Length (aa) ni secuencia del hit. Sin hit o sin descriptor: `---`.

Las columnas de query que vayan vacías **no se escriben** (query proteína → sin cDNA; query nucleótido → sin proteína). Si hay modelos de gen, se pueden pasar ambos FASTA (`--cdna` y `--protein`) y el primer bloque queda completo.

Una fila por query y rango de hit (se conservan todos los hits). En Excel, importar el CSV y opcionalmente combinar celdas de las dos primeras filas.

## API pública

```python
from biocol import (
    # FASTA
    validate_fasta_file,
    read_fasta,
    detect_sequence_type,
    detect_query_type,
    # BLAST
    detect_database_type,
    list_blast_databases,
    select_blast_program,
    run_blast,
    parse_blast_results,
    # Resultados
    load_accessions,
    build_result_table,
    write_results_csv,
    QUERY_COLUMNS,
    DEFAULT_OUTPUT,
)
```

`detect_sequence_type()` acepta `str`, `Bio.Seq.Seq` o `SeqRecord`. `detect_query_type()` clasifica un FASTA completo (error si está mixto).

Errores: `FastaError`, `EmptyFastaError`, `InvalidFastaError`, `MixedSequenceTypeError`, `BlastError`, `DatabaseError`, `MixedDatabaseTypeError`, `BlastExecutionError`, `MetadataError`.

## Pruebas (Dana)

```bash
pytest -q
pytest tests/test_detect_sequence_type.py -q
```

Al correr Pytest se muestran logs INFO. Fixtures en `tests/fixtures/` (FASTA, BLAST `outfmt 6`, accesiones). Importar solo desde `biocol`.

`run_blast` contra BLAST+ real solo en el entorno `conda` `inecol`.

| Entrada | Resultado esperado |
|---------|--------------------|
| FASTA de ADN | `nucleotide` |
| FASTA de ARN | `nucleotide` |
| FASTA de proteína | `protein` |
| Multifasta del mismo tipo | tipo único |
| Multifasta mixto ADN + proteína | `MixedSequenceTypeError` |
| Ruta inexistente | `FileNotFoundError` |
| Extensión no FASTA (p. ej. `.txt`) | `InvalidFastaError` |
| Archivo vacío / sin secuencias | `EmptyFastaError` |
| Contenido que no es FASTA | `InvalidFastaError` |
| Secuencia vacía o caracteres inválidos | `InvalidFastaError` |

## Equipo y estructura

| Persona  | Rol    | Trabaja sobre |
|----------|--------|----------------|
| Alondra  | lógica | `src/biocol/`  |
| Emiliano | CLI    | `src/biocol/cli/` (solo API pública de `biocol`) |
| Dana     | pruebas | `tests/` |

```
src/biocol/           backend
  sequence/           lectura, validación y tipo de query
  blast/              tipo de base, selección, ejecución y parseo tabular
  metadata/           accesiones y descriptores
  processing/         tabla ancha de resultados
  output/             escritura del CSV
  cli/                CLI (argparse + comandos run / from-blast)
tests/                pruebas (pytest)
tests/fixtures/       FASTA, BLAST outfmt 6 y accesiones de ejemplo
```

La lectura de FASTA usa `Bio.SeqIO`. Los alfabetos nucleótido/proteína salen de `Bio.Data.IUPACData`.
