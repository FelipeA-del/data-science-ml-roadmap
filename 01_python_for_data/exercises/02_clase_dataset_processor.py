from __future__ import annotations
import pandas as pd 
import logging 
from pathlib import Path

logger = logging.getLogger(__name__)


#La idea de definir clases es poder ahorrar lineas de codigo al tener que ejecutar las mismas cosas 
# a los mimos tipos de archivos,en este caso con solo definir a los archivos de data como clase 
#puedo aplicarle las funciones creadas para esa misma clase

class DatasetProcessor:
    """Carga, reusmen y limpia datasets de forma encadenable"""

    def __init__(self,filepath):
        """Carga el dataset desde un archivo csv
        
        Args: 
            filepath: Ruta al archivo csv
            """
        self.filepath = Path(filepath)
        self.df = pd.read_csv(self.filepath)
        logger.info(f"Dataset cargado:{self.filepath.name} - {self.df.shape}")

    def summary(self) -> dict:
        """Retorna un resumen estadístico del dataset.
        
        Returns:
            Diccionario con métricas básicas.
        """
        return {
            "n_rows": len(self.df),
            "n_cols": len(self.df.columns),
            "n_nulls": self.df.isnull().sum().sum(),
            "n_duplicates": self.df.duplicated().sum(),
            "dtypes": self.df.dtypes.to_dict()
        }

    def __repr__(self) -> str:
        """Representación del objeto al imprimirlo."""
        return f"DatasetProcessor({self.filepath.name} — {self.df.shape[0]} filas x {self.df.shape[1]} cols)"

    def clean(self,remove_dupes : bool = True, fillna_strategy: str = 'Median'):
        """
        Limpia el dataset en su lugar

        Args:
            remove_dupes : Si True, elimina duplicados.
            fillna_strategy: Estrategia para rellenar nulos

            returns:
                self - permite encadenar metodos
        """
        if remove_dupes:
            before = len(self.df)
            self.df = self.df.drop_duplicates()
            logger.info(f"Duplicados eliminados :{before-len(self.df)}")

        numeric_cols = self.df.select_dtypes(include = 'number').columns
        self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].median())

        logger.info(f"Nulos rellenados con: {fillna_strategy}")
        return self 
    

    def to_parquet(self,output_path: str | Path) -> None:
        """Guarda el dataframe como arrchivo Parquet
        Arg: output_path : Ruta donde guardar el archivo
        """
        output_path = Path(output_path)
        self.df.to_parquet(output_path,index=False)
        logger.info(f"Guardado como parquet:{output_path}")


if __name__ == "__main__":
    p = DatasetProcessor("01_python_for_data/exercises/data_prueba.csv")
    
    print(p)  # usa __repr__
    print("\nResumen:")
    print(p.summary())
    
    p.clean()
    print("\nDespués de limpiar:")
    print(p.df)
    
    p.to_parquet("01_python_for_data/exercises/data_limpia.parquet")
    print("\n✅ Guardado como parquet")
