from __future__ import annotations
import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_pipeline(filepath: Path, required_cols: list | None = None) -> pd.DataFrame | None:
    """Carga un CSV manejando todos los posibles errores.
    
    Args:
        filepath: Ruta al archivo.
        required_cols: Columnas obligatorias que debe tener el archivo.
    
    Returns:
        DataFrame si todo sale bien, None si el archivo no existe.
    
    Raises:
        ValueError: Si el formato no es soportado.
        KeyError: Si faltan columnas obligatorias.
    """
    filepath = Path(filepath)
    
    # Error 1 — archivo no existe
    if not filepath.exists():
        logger.error(f"Archivo no encontrado: {filepath}")
        return None
    
    # Error 2 — formato no soportado
    if filepath.suffix not in [".csv", ".xlsx", ".json"]:
        raise ValueError(f"Formato no soportado: {filepath.suffix}")
    
    # Error 3 — archivo vacío
    try:
        df = pd.read_csv(filepath)
        if df.empty:
            logger.warning(f"Archivo vacío: {filepath}")
            return pd.DataFrame()
    except pd.errors.EmptyDataError:
        logger.warning(f"Archivo sin datos: {filepath}")
        return pd.DataFrame()
    
    # Error 4 — columnas obligatorias faltantes
    # Error 4 — columnas obligatorias faltantes
    if required_cols:
        missing = [col for col in required_cols if col not in df.columns]  # ← esta línea
        if missing:
            raise KeyError(f"Columnas faltantes: {missing}")
    
    logger.info(f"Pipeline exitoso: {filepath.name} — {df.shape}")
    return df




if __name__ == "__main__":
    
    # Caso 1 — archivo válido
    print("--- Caso 1: archivo válido ---")
    df = safe_pipeline("01_python_for_data/data/ventas_enero.csv")
    print(f"Resultado: {type(df)}\n")
    
    # Caso 2 — archivo inexistente
    print("--- Caso 2: archivo inexistente ---")
    df = safe_pipeline("01_python_for_data/data/no_existe.csv")
    print(f"Resultado: {df}\n")
    
    # Caso 3 — formato no soportado
    print("--- Caso 3: formato no soportado ---")
    try:
        df = safe_pipeline("01_python_for_data/data/ventas.db")
    except ValueError as e:
        print(f"ValueError capturado: {e}\n")
    
    # Caso 4 — columnas obligatorias faltantes
    print("--- Caso 4: columnas faltantes ---")
    try:
        df = safe_pipeline(
            "01_python_for_data/data/ventas_enero.csv",
            required_cols=["ventas", "columna_inexistente"]
        )
    except KeyError as e:
        print(f"KeyError capturado: {e}\n")