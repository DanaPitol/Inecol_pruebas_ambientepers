# biocol

Backend para el análisis y procesamiento de BLAST. El resultado final será un CSV plano con las columnas de anotación BLAST de la tabla de referencia (sin Pfam, KEGG ni GO).

## Equipo

| Persona   | Rol      | Trabaja sobre |
|-----------|----------|----------------|
| Backend   | lógica   | `src/biocol/`  |
| Emiliano  | CLI      | llama la API pública de `biocol` |
| Dana      | pruebas  | `tests/` e importaciones desde `biocol` |

El CLI y las pruebas deben importar **solo** desde `biocol`, no desde módulos internos (`biocol.sequence.reader`, etc.).

## Estado actual

Listo:

- leer FASTA / multifasta (`.fa`, `.fasta`, `.fna`, `.faa`, `.fas`)
- validar archivo y secuencias
- detectar si la query es nucleótido o proteína (`U` cuenta como nucleótido)
- detectar tipo de base de datos (un FASTA o una carpeta con FASTA, incluidas subcarpetas)
- elegir el programa BLAST (`select_blast_program`)
- ejecutar BLAST+ (`run_blast`: `makeblastdb` temporal, un run por FASTA, `outfmt 6`)
- parsear tabular (`parse_blast_results`); queries sin hit → fila vacía

Aún no:

- accesiones / descriptores
- CSV final

## Instalación

Python 3.10+ y el entorno del proyecto (`conda activate inecol` o el venv local).

```bash
cd biocol
pip install -e ".[dev]"
```

`-e` instala el paquete en modo editable: los cambios del backend se ven sin reinstalar.

## Cómo probar (Dana)

Correr la suite:

```bash
pytest -q
```

Una prueba concreta:

```bash
pytest tests/test_detect_sequence_type.py -q
```

Al correr Pytest se muestran logs INFO de la clasificación, por ejemplo
`detect_sequence_type: id=seq1 longitud=28 tipo=nucleotide`.

Hay FASTA de ejemplo en `tests/fixtures/` (ADN, ARN, proteína, multifasta, casos inválidos).

### API pública para nuevas pruebas

```python
from biocol import (
    read_fasta,
    validate_fasta_file,
    detect_sequence_type,
    detect_query_type,
    EmptyFastaError,
    InvalidFastaError,
    MixedSequenceTypeError,
)

validate_fasta_file("query.fa")
records = read_fasta("query.fa")          # list[Bio.SeqRecord.SeqRecord]
print(records[0].id)
print(str(records[0].seq))

detect_sequence_type(records[0])          # "nucleotide" | "protein"
detect_query_type(records)                # mismo valor si todo el FASTA es homogéneo
```

`detect_sequence_type()` acepta `str`, `Bio.Seq.Seq` o `SeqRecord`.

### Casos que conviene cubrir

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

Las pruebas nuevas pueden ir en `tests/` usando fixtures propios o archivos reales (por ejemplo un `.fna` / `.faa` de NCBI).

## Cómo usarlo desde el CLI (Emiliano)

Todavía no hay punto de entrada de consola. El CLI debe llamar las mismas funciones:

```python
from biocol import run_blast, parse_blast_results

hits = run_blast(
    args.fasta,
    args.db,
    translated=args.tblastx,  # False por defecto
    evalue=args.evalue,       # default 10
    max_target_seqs=args.max_target_seqs,  # default 500
)
# Camino 2 (BLAST tabular ya existente):
# hits = parse_blast_results(args.blast_txt)
```

`run_blast` crea bases temporales con `makeblastdb`, lanza un BLAST por FASTA de la carpeta y parsea `outfmt 6`. El `.txt` no se conserva; el CSV final (con accesiones) vendrá después. Queries sin hit quedan como fila vacía.

### Reglas para el tipo de BLAST

`select_blast_program` combina **tipo de query + tipo de base**. Si ambos son nucleótido, el default es **blastn**. `translated=True` (opción explícita, desactivada por defecto) elige **tblastx**. En las demás combinaciones `translated` se ignora.

| Query | Base de datos | `translated` | Programa | Qué compara |
|-------|---------------|--------------|----------|-------------|
| Nucleótido | Nucleótido | no se pasa / `False` (default) | `blastn` | Nucleótido contra nucleótido |
| Nucleótido | Nucleótido | `True` (explícito) | `tblastx` | Query y base traducidas en seis marcos (proteína) |
| Nucleótido | Proteína | se ignora | `blastx` | Query nucleotídica traducida contra proteínas |
| Proteína | Proteína | se ignora | `blastp` | Proteína contra proteína |
| Proteína | Nucleótido | se ignora | `tblastn` | Proteína contra traducciones de la base nucleotídica |

`detect_database_type` acepta un archivo FASTA (mismas extensiones que la query: `.fa`, `.fasta`, `.fna`, `.faa`, `.fas`) o una carpeta con varios FASTA, **incluyendo subcarpetas**. Todos deben ser del mismo tipo.

## Estructura

```
src/biocol/           backend
  sequence/           lectura, validación y tipo de query
  blast/              tipo de base, selección, ejecución y parseo tabular
tests/                pruebas (pytest)
tests/fixtures/       FASTA y BLAST outfmt 6 de ejemplo
```

La lectura de FASTA usa `Bio.SeqIO`. Los alfabetos nucleótido/proteína salen de `Bio.Data.IUPACData`.
