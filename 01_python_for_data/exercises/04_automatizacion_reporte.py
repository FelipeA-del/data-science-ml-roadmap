from __future__ import annotations
import pandas as pd 
import matplotlib.pyplot as plt 
import logging 
from pathlib import Path
from datetime import datetime 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calcular_estadisticas(df: pd.DataFrame, col_categorica: str) -> dict:
    """Calcula estadísticas básicas agrupadas por columna categórica.
    
    Args:
        df: DataFrame de entrada.
        col_categorica: Columna para agrupar.
    
    Returns:
        Diccionario con estadísticas por grupo.
    """
    stats = {}
    numeric_cols = df.select_dtypes(include='number').columns
    
    for grupo, datos in df.groupby(col_categorica):
        stats[grupo] = {
            col: {
                "mean": round(datos[col].mean(), 2),
                "min": datos[col].min(),
                "max": datos[col].max()
            }
            for col in numeric_cols
        }
        logger.info(f"Stats calculadas para grupo: {grupo}")
    
    return stats


#with open se cierra independiente lo que pase , si solo se usa open , un error puede dejar abierto el archivo

def generar_reporte(stats: dict, output_path: Path) -> None:
    """Escribe las estadísticas en un archivo .txt.
    
    Args:
        stats: Diccionario con estadísticas por grupo.
        output_path: Ruta donde guardar el reporte.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    with open(output_path, 'w') as f:
        f.write(f"REPORTE GENERADO: {timestamp}\n")
        f.write("=" * 40 + "\n\n")
        
        for grupo, columnas in stats.items():
            f.write(f"GRUPO: {grupo}\n")
            f.write("-" * 20 + "\n")
            for col, valores in columnas.items():
                f.write(f"  {col}:\n")
                f.write(f"    Promedio: {valores['mean']}\n")
                f.write(f"    Mínimo:   {valores['min']}\n")
                f.write(f"    Máximo:   {valores['max']}\n")
            f.write("\n")
    
    logger.info(f"Reporte guardado en: {output_path}")



def generar_grafico(df: pd.DataFrame, col_categorica: str, col_numerica: str, output_path: Path) -> None:
    """Genera un gráfico de barras y lo guarda como PNG.
    
    Args:
        df: DataFrame de entrada.
        col_categorica: Columna para el eje X.
        col_numerica: Columna para el eje Y.
        output_path: Ruta donde guardar el PNG.
    """
    promedios = df.groupby(col_categorica)[col_numerica].mean()
    
    plt.figure(figsize=(8, 5))
    plt.bar(promedios.index, promedios.values, color='steelblue')
    plt.title(f"Promedio de {col_numerica} por {col_categorica}")
    plt.xlabel(col_categorica)
    plt.ylabel(f"Promedio {col_numerica}")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    
    logger.info(f"Gráfico guardado en: {output_path}")    

if __name__ == "__main__":
    # Cargar datos
    df = pd.read_csv("01_python_for_data/data/ventas_enero.csv")
    logger.info("Dataset cargado")
    
    # Calcular estadísticas
    stats = calcular_estadisticas(df, col_categorica="mes")
    
    # Generar reporte txt
    generar_reporte(
        stats,
        output_path=Path("01_python_for_data/exercises/reporte.txt")
    )
    
    # Generar gráfico
    generar_grafico(
        df,
        col_categorica="mes",
        col_numerica="ventas",
        output_path=Path("01_python_for_data/exercises/grafico_ventas.png")
    )
    
    print("✅ Reporte y gráfico generados")