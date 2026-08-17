from __future__ import annotations

from pathlib import Path

import pandas as pd

DEFAULT_OUTPUT = "results.csv"


def write_results_csv(
    table: pd.DataFrame,
    output: str | Path | None = None,
) -> Path:
    """Escribe el CSV plano final. Por defecto ``results.csv``."""
    path = Path(output) if output else Path(DEFAULT_OUTPUT)
    table.to_csv(path, index=False)
    return path
