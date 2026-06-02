# Módulo 01 — Python profesional para datos

## Qué hice
- 10 ejercicios de Python para datos
- Funciones de limpieza con type hints y docstrings
- Clase DatasetProcessor encadenable
- Lectura de múltiples archivos con pathlib
- Reporte automático con matplotlib
- Manejo de formatos CSV, JSON, Excel, Parquet
- Base de datos SQLite con 50 registros sintéticos
- Manejo de errores profesional con try/except
- Sistema de logging con FileHandler
- Tests con pytest (8 tests pasando)
- Mini proyecto integrador con merge, métricas y gráficos

## Qué aprendí
- La diferencia entre print y logging
- Por qué los entornos virtuales son necesarios
- Cómo funciona Git internamente (no es solo guardar en la nube)
- El patrón Split-Apply-Combine con groupby
- Cuándo usar return None vs raise en manejo de errores
- Por qué los tests son diferenciales en entrevistas

## Qué me costó
- La indentación en Python (espacios vs tabs)
- Entender if __name__ == "__main__"
- La autenticación de GitHub con tokens
- La diferencia entre Jupyter y scripts .py

## Cómo correr los ejercicios
git clone https://github.com/FelipeA-del/data-science-ml-roadmap.git
cd data-science-ml-roadmap
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 01_python_for_data/exercises/01_funciones_limpieza.py