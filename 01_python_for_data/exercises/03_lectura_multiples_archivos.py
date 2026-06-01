from __future__ import annotations
import pandas as pd
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


def read_multiple_csvs(folder: Path) -> tuple[pd.DataFrame, dict]:
    """Lee todos los CSVs de una carpeta y los concatena.
    
    Args:
        folder: Carpeta donde buscar archivos CSV.
    
    Returns:
        Tupla con (DataFrame concatenado, stats por archivo).
    """
    folder = Path(folder)
    csv_files = list(folder.glob("*.csv"))
    
    if not csv_files:
        raise FileNotFoundError(f"No hay CSVs en: {folder}")
    
    dfs = []
    stats = {}
    
    for file in csv_files:
        df = pd.read_csv(file)
        df["source_file"] = file.name
        dfs.append(df)
        stats[file.name] = {
            "filas": len(df),
            "columnas": len(df.columns),
            "modificado": datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        }
        logger.info(f"Leído: {file.name} — {df.shape}")
    
    result = pd.concat(dfs, ignore_index=True)
    logger.info(f"Total concatenado: {result.shape}")
    return result, stats




if __name__ == "__main__":
    df, stats = read_multiple_csvs("01_python_for_data/data/")
    
    print("DataFrame concatenado:")
    print(df)
    print("\nStats por archivo:")
    for archivo, info in stats.items():
        print(f"  {archivo}: {info}")