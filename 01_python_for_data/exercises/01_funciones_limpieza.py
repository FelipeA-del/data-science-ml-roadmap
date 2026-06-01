import pandas as pd
import logging
#libreria para registrar mensajes en produccion 
#ayuda a registrar los eventos que suceden (info , warning , error)

logger = logging.getLogger(__name__)   #crea un logger con el nombre de este archivo

def remove_duplicates(df: pd.DataFrame, subset=None) -> pd.DataFrame:
    """Elimina filas duplicadas y registra cuántas se eliminaron.
    
    Args:
        df: DataFrame de entrada.
        subset: Lista de columnas a considerar. None = todas.
    
    Returns:
        DataFrame sin duplicados.
    """
    before = len(df)
    df_clean = df.drop_duplicates(subset=subset)
    removed = before - len(df_clean)
    logger.info(f"Duplicados eliminados: {removed}")
    return df_clean





def fill_missing(df: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
    """Rellena valores nulos según una estrategia.
    
    Args:
        df: DataFrame de entrada.
        strategy: 'mean', 'median', 'mode' o 'zero'.
    
    Returns:
        DataFrame sin nulos.
    """
    df_clean = df.copy()
    numeric_cols = df_clean.select_dtypes(include='number').columns
    
    if strategy == 'mean':
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())
    elif strategy == 'median':
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
    elif strategy == 'mode':
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mode().iloc[0])
    elif strategy == 'zero':
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(0)
    else:
        raise ValueError(f"Estrategia no válida: {strategy}. Usa 'mean', 'median', 'mode' o 'zero'")
    
    logger.info(f"Nulos rellenados con estrategia: {strategy}")
    return df_clean

def clip_outliers_iqr(df: pd.DataFrame, column: str, k: float = 1.5) -> pd.DataFrame:
    """Recorta outliers usando el método IQR.
    
    Args:
        df: DataFrame de entrada.
        column: Columna a limpiar.
        k: Factor de sensibilidad. Default 1.5.
    
    Returns:
        DataFrame con outliers recortados.
    """
    df_clean = df.copy()
    Q1 = df_clean[column].quantile(0.25)
    Q3 = df_clean[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - k * IQR
    upper = Q3 + k * IQR
    df_clean[column] = df_clean[column].clip(lower, upper)
    logger.info(f"Outliers recortados en '{column}': rango [{lower:.2f}, {upper:.2f}]")
    return df_clean





#ayuda a definir el tipo de datos por columna , para eso debo collar en nombre columa : tipo de dato
def convert_dtypes(df: pd.DataFrame, dtype_map: dict) -> pd.DataFrame:
    """Convierte columnas a los tipos de datos especificados.
    
    Args:
        df: DataFrame de entrada.
        dtype_map: Diccionario {columna: tipo}. Ej: {'edad': int, 'precio': float}
    
    Returns:
        DataFrame con tipos convertidos.
    """
    df_clean = df.copy()
    for column, dtype in dtype_map.items():
        try:
            df_clean[column] = df_clean[column].astype(dtype)
            logger.info(f"Columna '{column}' convertida a {dtype}")
        except (ValueError, KeyError) as e:
            logger.error(f"No se pudo convertir '{column}': {e}")
    return df_clean


#esta funcion valida que no exista valores nulos y no los manda a entrenamiento ya que se detiene si encuentra nulos
def validate_no_nulls(df: pd.DataFrame, required_cols: list) -> None:
    """Valida que las columnas requeridas no tengan valores nulos.
    
    Args:
        df: DataFrame de entrada.
        required_cols: Lista de columnas que no pueden tener nulos.
    
    Raises:
        ValueError: Si alguna columna requerida tiene nulos.
    """
    for col in required_cols:
        if col not in df.columns:
            raise KeyError(f"La columna '{col}' no existe en el DataFrame")
        nulls = df[col].isnull().sum()
        if nulls > 0:
            raise ValueError(f"La columna '{col}' tiene {nulls} valores nulos")
    logger.info(f"Validación OK — sin nulos en: {required_cols}")



if __name__ == "__main__":
    # Dataset sucio de prueba
    data = {
        'nombre':  ['Ana', 'Luis', 'Pedro', 'Ana', None],
        'edad':    [25, 30, 28, 25, 22],
        'sueldo':  [1500.0, None, 1800.0, 1500.0, 50000.0],
        'depto':   ['ventas', 'tech', 'tech', 'ventas', 'tech']
    }
    df = pd.DataFrame(data)
    print("DataFrame original:")
    print(df)
    print()

    # Probar las 5 funciones
    df = remove_duplicates(df)
    df = fill_missing(df, strategy='mean')
    df = clip_outliers_iqr(df, column='sueldo')
    df = convert_dtypes(df, {'edad': int})
    df['nombre'] = df['nombre'].fillna('Desconocido')  # ← agrega esta línea
    validate_no_nulls(df, ['nombre', 'edad', 'sueldo'])

    print("DataFrame limpio:")
    print(df)