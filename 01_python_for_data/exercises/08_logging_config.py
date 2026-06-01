from __future__ import annotations
import logging
from pathlib import Path


def setup_logger(name: str, log_file: str | Path, level: int = logging.INFO) -> logging.Logger:
    """Crea un logger que escribe en consola Y en archivo.
    
    Args:
        name: Nombre del logger.
        log_file: Ruta al archivo de log.
        level: Nivel mínimo de mensajes. Default INFO.
    
    Returns:
        Logger configurado.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    formato = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Handler 1 — escribe en consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formato)
    
    # Handler 2 — escribe en archivo
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formato)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


if __name__ == "__main__":
    logger = setup_logger(
        name="mi_pipeline",
        log_file="01_python_for_data/logs/pipeline.log"
    )
    
    logger.info("Pipeline iniciado")
    logger.warning("Dataset tiene valores nulos")
    logger.error("No se pudo conectar a la base de datos")
    logger.info("Pipeline finalizado")
    
    print("\n✅ Revisa el archivo: 01_python_for_data/logs/pipeline.log")