from __future__ import annotations
import pandas as pd 
import logging 

logger = logging.getLogger(__name__)

def remove_duplicates(df: pd.DataFrame, subset=None) -> pd.DataFrame:
    before = len(df)
    df_clean = df.drop_duplicates(subset=subset)
    removed = before - len(df_clean)
    logger.info(f"Duplicados eliminados: {removed}")
    return df_clean


def fill_missing(df: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
    df_clean = df.copy()
    numeric_cols = df_clean.select_dtypes(include='number').columns
    if strategy == 'mean':
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())
    elif strategy == 'median':
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
    elif strategy == 'zero':
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(0)
    else:
        raise ValueError(f"Estrategia no válida: {strategy}")
    return df_clean


def validate_no_nulls(df: pd.DataFrame, required_cols: list) -> None:
    for col in required_cols:
        if col not in df.columns:
            raise KeyError(f"La columna '{col}' no existe")
        nulls = df[col].isnull().sum()
        if nulls > 0:
            raise ValueError(f"La columna '{col}' tiene {nulls} valores nulos")
