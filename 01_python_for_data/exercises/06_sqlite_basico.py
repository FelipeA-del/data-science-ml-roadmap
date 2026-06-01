import sqlite3
import pandas as pd 
import random
from pathlib import Path


def crear_base_datos(db_path: Path) -> sqlite3.Connection:
    """Crea la base de datos con 2 tablas relacionadas.
    
    Args:
        db_path: Ruta donde guardar el archivo .db
    
    Returns:
        Conexión a la base de datos.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            ciudad TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY,
            cliente_id INTEGER,
            producto TEXT NOT NULL,
            monto REAL NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    """)
    
    conn.commit()
    print("✅ Tablas creadas")
    return conn


def insertar_datos(conn: sqlite3.Connection) -> None:
    """Inserta 50 registros sintéticos en las tablas.
    
    Args:
        conn: Conexión a la base de datos.
    """
    cursor = conn.cursor()
    
    nombres = ["Ana", "Luis", "Pedro", "María", "Carlos",
               "Sofia", "Diego", "Valentina", "Matías", "Camila"]
    ciudades = ["Santiago", "Valparaíso", "Concepción", "Temuco", "Antofagasta"]
    productos = ["Laptop", "Mouse", "Teclado", "Monitor", "Auriculares"]
    
    # Insertar 10 clientes
    for i in range(1, 11):
        cursor.execute(
            "INSERT OR IGNORE INTO clientes VALUES (?, ?, ?)",
            (i, nombres[i-1], random.choice(ciudades))
        )
    
    # Insertar 50 ventas
    for i in range(1, 51):
        cursor.execute(
            "INSERT OR IGNORE INTO ventas VALUES (?, ?, ?, ?)",
            (i, random.randint(1, 10), random.choice(productos), round(random.uniform(100, 2000), 2))
        )
    
    conn.commit()
    print("✅ 50 registros insertados")


def consultar_datos(conn: sqlite3.Connection) -> None:
    """Lee datos y compara JOIN en SQL vs pandas.
    
    Args:
        conn: Conexión a la base de datos.
    """
    # Leer tablas con pandas
    clientes_df = pd.read_sql_query("SELECT * FROM clientes", conn)
    ventas_df = pd.read_sql_query("SELECT * FROM ventas", conn)
    
    print("Clientes:")
    print(clientes_df.head())
    print("\nVentas:")
    print(ventas_df.head())
    
    # JOIN en SQL
    print("\n--- JOIN en SQL ---")
    query = """
        SELECT c.nombre, c.ciudad, v.producto, v.monto
        FROM ventas v
        JOIN clientes c ON v.cliente_id = c.id
        ORDER BY v.monto DESC
        LIMIT 5
    """
    resultado_sql = pd.read_sql_query(query, conn)
    print(resultado_sql)
    
    # JOIN equivalente en pandas
    print("\n--- JOIN en pandas ---")
    resultado_pandas = (
        ventas_df
        .merge(clientes_df, left_on="cliente_id", right_on="id")
        [["nombre", "ciudad", "producto", "monto"]]
        .sort_values("monto", ascending=False)
        .head(5)
    )
    print(resultado_pandas)



if __name__ == "__main__":
    db_path = Path("01_python_for_data/data/ventas.db")
    
    conn = crear_base_datos(db_path)
    insertar_datos(conn)
    consultar_datos(conn)
    conn.close()
    
    print(f"\n✅ Base de datos guardada en: {db_path}")
